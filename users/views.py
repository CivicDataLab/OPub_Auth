from logging import exception
from operator import contains
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import Http404
import keycloak
from keycloak import KeycloakOpenID
import requests
import json
from django.views.decorators.csrf import csrf_exempt
import ast
from configparser import ConfigParser
from .models import *

config = ConfigParser()
config.read("config.ini")


# configure keycloak client
keycloak_openid = KeycloakOpenID(
    server_url=config.get("keycloak", "server_url"),
    client_id=config.get("keycloak", "client_id"),
    realm_name=config.get("keycloak", "realm_name"),
    client_secret_key=config.get("keycloak", "client_secret_key"),
)
config_well_known = keycloak_openid.well_known()


# graphql config
password = config.get("graphql", "password")
auth_url = config.get("graphql", "base_url")


# util functions
@csrf_exempt
def get_user(access_token):

    try:
        userinfo = keycloak_openid.userinfo(access_token)
        userinfo["success"] = True
    except Exception as error:
        print(error)
        userinfo = {
            "success": False,
            "error": "invalid_token",
            "error_description": "Token verification failed",
        }

    return userinfo


@csrf_exempt
def has_access(username, access_org_id, access_data_id, access_req):

    # access_dict = {"PMU":['CREATE', 'UPDATE', 'DELETE', 'APPROVE', 'APPROVE PUB', 'VIEW'],
    #                "PRA":['CREATE', 'UPDATE', 'DELETE', 'APPROVE', 'VIEW'],
    #                "PR": ['CREATE', 'VIEW'],
    #                "CR": ['VIEW']}

    userroleobj = UserRole.objects.filter(
        username__username=username, org_id=access_org_id
    ).values("org_id", "role__role_name")
    if len(userroleobj) == 0:

        userroleobj = UserRole.objects.filter(username__username=username).values(
            "org_id", "role__role_name"
        )
        if len(userroleobj) != 0 and "PMU" in [
            each["role__role_name"] for each in userroleobj
        ]:
            context = {"Success": True, "access_allowed": True}
            return JsonResponse(context, safe=False)

        context = {
            "Success": False,
            "error": "No Matching user found",
            "error_description": "No Matching user found",
        }
        return JsonResponse(context, safe=False)

    userrole = userroleobj[0]["role__role_name"]
    userorg = userroleobj[0]["org_id"]

    if userrole == "PMU":
        context = {"Success": True, "access_allowed": True, "role": "PMU"}
        return JsonResponse(context, safe=False)

    if userrole == "DPA" and userorg != None:
        context = {"Success": True, "access_allowed": True, "role": "DPA"}
        return JsonResponse(context, safe=False)

    if (
        userrole == "DP"
        and userorg != None
        and "create" in access_req
        and access_req not in ["create_dam"]
    ):
        context = {"Success": True, "access_allowed": True, "role": "DP"}
        return JsonResponse(context, safe=False)

    if (
        userrole == "DP"
        and userorg != None
        and ("update" in access_req or "patch" in access_req)
        and access_data_id != None
    ):
        datasetobj = DatasetOwner.objects.filter(
            username__username=username, dataset_id=access_data_id
        ).values("is_owner")
        if len(datasetobj) != 0 and datasetobj[0]["is_owner"] == True:
            context = {"Success": True, "access_allowed": True, "role": "DP"}
            return JsonResponse(context, safe=False)

    context = {"Success": True, "access_allowed": False}
    return JsonResponse(context, safe=False)

    # role_access = "Available" if access_req in access_dict.get(role) else "Denied"

    # if role_access == "Denied":
    #     context = {"success": False, "username":username, "access_org_id":access_org_id, "role": role, "access_req":access_req, "access":role_access}
    # else:
    #     context = {"success": True, "username":username, "access_org_id":access_org_id, "role": role, "access_req":access_req, "access":role_access}
    # return context


# api functions
@csrf_exempt
def verify_user_token(request):

    print("-----------------", request.body)
    post_data = json.loads(request.body.decode("utf-8"))
    access_token = post_data.get("access_token", None)
    userinfo = get_user(access_token)

    return JsonResponse(userinfo, safe=False)


@csrf_exempt
def check_user(request):
    post_data = json.loads(request.body.decode("utf-8"))
    access_token = post_data.get("access_token", None)
    userinfo = get_user(access_token)

    if userinfo["success"] == False:
        context = {
            "Success": False,
            "error": userinfo["error"],
            "error_description": userinfo["error_description"],
        }
        return JsonResponse(context, safe=False)

    username = userinfo["preferred_username"]
    try:
        email = userinfo["email"]
    except Exception as e:
        context = {
            "Success": False,
            "error": "user doesn't have a email set",
            "error_description": "please set a valid email",
        }
        return JsonResponse(context, safe=False)

    # check if username is in auth db
    num_users = CustomUser.objects.filter(username=username).count()

    if num_users == 0:

        try:

            query = f"""
                    mutation {{
                        register(
                        email: "{email}",
                        username: "{username}",
                        password1: "{password}",
                        password2: "{password}",
                    ) {{
                        success,
                        errors,
                        token,
                        refresh_token
                    }}
            }}"""

            headers = {}
            response = requests.post(auth_url, json={"query": query}, headers=headers)
            response_json = json.loads(response.text)
            print(response_json)

            if response_json["data"]["register"]["success"] == True:
                context = {
                    "Success": True,
                    "username": username,
                    "email": email,
                    "access_token": access_token,
                    "Comment": "User Registration successful",
                }
            else:
                context = {
                    "Success": False,
                    "errors": response_json["data"]["register"]["errors"],
                }

            return JsonResponse(context, safe=False)

        except Exception as e:
            print(e)
            context = {
                "Success": False,
                "errors": response_json["data"]["register"]["errors"],
            }
            return JsonResponse(context, safe=False)
    else:
        user_roles = UserRole.objects.filter(username__username=username).values(
            "org_id", "org_title", "role__role_name"
        )
        user_roles_res = []
        for role in user_roles:
            user_roles_res.append(
                {
                    "org_id": role["org_id"],
                    "org_title": role["org_title"],
                    "role": role["role__role_name"],
                }
            )
        context = {
            "Success": True,
            "username": username,
            "email": email,
            "access_token": access_token,
            "access": user_roles_res,
            "comment": "User already exists",
        }
        return JsonResponse(context, safe=False)


@csrf_exempt
def check_user_access(request):

    print("-----------------", request.body)
    post_data = json.loads(request.body.decode("utf-8"))
    access_token = post_data.get("access_token", None)
    access_org_id = post_data.get("access_org_id", None)
    access_data_id = post_data.get("access_data_id", None)
    access_req = post_data.get("access_req", None)
    userinfo = get_user(access_token)

    if userinfo["success"] == False:
        context = {
            "Success": False,
            "error": userinfo["error"],
            "error_description": userinfo["error_description"],
        }
        return JsonResponse(context, safe=False)

    username = userinfo["preferred_username"]

    has_access_res = has_access(username, access_org_id, access_data_id, access_req)

    return has_access_res  # JsonResponse(has_access_res, safe=False)


@csrf_exempt
def create_user_role(request):

    print("-----------------", request.body)
    post_data = json.loads(request.body.decode("utf-8"))
    access_token = post_data.get("access_token", None)
    org_id = post_data.get("org_id", None)
    org_title = post_data.get("org_title", None)
    role_name = "DPA"

    userinfo = get_user(access_token)

    if userinfo["success"] == False:
        context = {
            "Success": False,
            "error": userinfo["error"],
            "error_description": userinfo["error_description"],
        }
        return JsonResponse(context, safe=False)

    if org_id == None:
        context = {
            "Success": False,
            "error": "wrong org_id",
            "error_description": "org_id is blank",
        }
        return JsonResponse(context, safe=False)

    username = userinfo["preferred_username"]

    try:
        role = Role.objects.get(role_name=role_name)
        user = CustomUser.objects.get(username=username)
        newUserRole = UserRole(
            username=user, org_id=org_id, org_title=org_title, role=role
        )

        newUserRole.save()
        context = {"Success": True, "comment": "User Role Added Successfully"}
        return JsonResponse(context, safe=False)
    except Exception as e:
        context = {"Success": False, "error": e, "error_description": e}
        return JsonResponse(context, safe=False)


@csrf_exempt
def get_users(request):

    print("-----------------", request.body)
    post_data = json.loads(request.body.decode("utf-8"))
    access_token = post_data.get("access_token", None)
    org_id = post_data.get("org_id", None)

    userinfo = get_user(access_token)
    if userinfo["success"] == False:
        context = {
            "Success": False,
            "error": userinfo["error"],
            "error_description": userinfo["error_description"],
        }
        return JsonResponse(context, safe=False)
    username = userinfo["preferred_username"]

    ispmu = False
    ispra = False
    userroleobj = UserRole.objects.filter(
        username__username=username, org_id=org_id
    ).values("org_id", "role__role_name")
    if len(userroleobj) == 0:
        userroleobj = UserRole.objects.filter(username__username=username).values(
            "org_id", "role__role_name"
        )
        if len(userroleobj) != 0 and userroleobj[0]["role__role_name"] == "PMU":
            ispmu = True
    else:
        if userroleobj[0]["role__role_name"] == "DPA":
            ispra = True

    if ispmu == False and ispra == False:
        context = {
            "Success": False,
            "error": "No access for the org for this user",
            "error_description": "No access for the org for this user",
        }
        return JsonResponse(context, safe=False)

    userrole = userroleobj[0]["role__role_name"]
    userorg = userroleobj[0]["org_id"]

    if userrole == "PMU":
        users = CustomUser.objects.exclude(username=username).values(
            "username", "email"
        )
        users_list = []
        for user in users:
            user_roles = UserRole.objects.filter(
                username__username=user["username"]
            ).values("org_id", "org_title", "role__role_name")
            user_roles_res = []
            for role in user_roles:
                user_roles_res.append(
                    {
                        "org_id": role["org_id"],
                        "org_title": role["org_title"],
                        "role": role["role__role_name"],
                    }
                )
            users_list.append(
                {
                    "username": user["username"],
                    "email": user["email"],
                    "access": user_roles_res,
                }
            )

        context = {"Success": True, "users": users_list}
        return JsonResponse(context, safe=False)

    if userrole == "DPA" and userorg != None:
        user_roles = (
            UserRole.objects.filter(org_id=userorg)
            .exclude(role__role_name__in=["PMU", "DPA"])
            .exclude(username__username=username)
            .values(
                "username__username",
                "username__email",
                "org_id",
                "org_title",
                "role__role_name",
            )
        )
        user_roles_res = {}
        for role in user_roles:
            if role["username__username"] in user_roles_res:
                user_roles_res[role["username__username"]]["access"].append(
                    {
                        "org_id": role["org_id"],
                        "org_title": role["org_title"],
                        "role": role["role__role_name"],
                    }
                )
            else:
                user_roles_res[role["username__username"]] = {
                    "email": role["username__email"],
                    "access": [
                        {
                            "org_id": role["org_id"],
                            "org_title": role["org_title"],
                            "role": role["role__role_name"],
                        }
                    ],
                }

        users_list = []
        for key, value in user_roles_res.items():
            users_list.append(
                {"username": key, "email": value["email"], "access": value["access"]}
            )
        context = {"Success": True, "users": users_list}
        return JsonResponse(context, safe=False)

    context = {
        "Success": False,
        "error": "No Matching org and user found",
        "error_description": ("org is " + userorg + " and role is " + userrole),
    }
    return JsonResponse(context, safe=False)


@csrf_exempt
def update_user_role(request):

    print("-----------------", request.body)
    post_data = json.loads(request.body.decode("utf-8"))
    access_token = post_data.get("access_token", None)
    org_id = post_data.get("org_id", None)
    org_title = post_data.get("org_title", None)
    role_name = post_data.get("role_name", None)
    tgt_user_name = post_data.get("tgt_user_name", None)
    action = post_data.get("action", None)

    userinfo = get_user(access_token)

    if userinfo["success"] == False:
        context = {
            "Success": False,
            "error": userinfo["error"],
            "error_description": userinfo["error_description"],
        }
        return JsonResponse(context, safe=False)

    if org_id == None:
        context = {
            "Success": False,
            "error": "wrong org_id",
            "error_description": "org_id is blank",
        }
        return JsonResponse(context, safe=False)

    if (
        role_name == None
        or role_name not in ["DPA", "DP", "PMU"]
        and action != "delete"
    ):
        context = {
            "Success": False,
            "error": "wrong role",
            "error_description": "role is not valid",
        }
        return JsonResponse(context, safe=False)

    username = userinfo["preferred_username"]
    # check for username access

    ispmu = False
    ispra = False
    userroleobj = UserRole.objects.filter(
        username__username=username, org_id=org_id
    ).values("org_id", "role__role_name")
    if len(userroleobj) == 0:
        userroleobj = UserRole.objects.filter(username__username=username).values(
            "org_id", "role__role_name"
        )
        if len(userroleobj) != 0 and userroleobj[0]["role__role_name"] == "PMU":
            ispmu = True
    else:
        if userroleobj[0]["role__role_name"] == "DPA":
            ispra = True

    if ispmu == False and ispra == False:
        context = {
            "Success": False,
            "error": "Access Denied",
            "error_description": "User is not Authorized",
        }
        return JsonResponse(context, safe=False)

    if action == "update":
        try:
            role = Role.objects.get(role_name=role_name)
            user = CustomUser.objects.get(username=tgt_user_name)

            UserRoleObjs = UserRole.objects.filter(username=user, org_id=org_id)
            UserRoleObjCount = UserRoleObjs.count()
            if UserRoleObjCount == 0:
                newUserRole = UserRole(
                    username=user, org_id=org_id, org_title=org_title, role=role
                )
                newUserRole.save()
            else:
                UserRoleObjs.update(role=role)
            context = {"Success": True, "comment": "User Role Added Successfully"}
            return JsonResponse(context, safe=False)
        except Exception as e:
            context = {"Success": False, "error": str(e), "error_description": str(e)}
            return JsonResponse(context, safe=False)

    if action == "delete":
        try:
            role = Role.objects.get(role_name=role_name)
            user = CustomUser.objects.get(username=tgt_user_name)
            UserRoleObj = UserRole.objects.get(username=user, org_id=org_id, role=role)
            UserRoleObj.delete()
            context = {"Success": True, "comment": "User Role Deleted Successfully"}
            return JsonResponse(context, safe=False)
        except Exception as e:
            context = {"Success": False, "error": str(e), "error_description": str(e)}
            return JsonResponse(context, safe=False)


@csrf_exempt
def update_dataset_owner(request):

    print("-----------------", request.body)
    post_data = json.loads(request.body.decode("utf-8"))
    access_token = post_data.get("access_token", None)
    dataset_id = post_data.get("dataset_id", None)
    org_id = post_data.get("org_id", None)
    tgt_user_name = post_data.get("tgt_user_name", None)
    action = post_data.get("action", None)
    userinfo = get_user(access_token)

    if userinfo["success"] == False:
        context = {
            "Success": False,
            "error": userinfo["error"],
            "error_description": userinfo["error_description"],
        }
        return JsonResponse(context, safe=False)

    if dataset_id == None:
        context = {
            "Success": False,
            "error": "wrong dataset_id",
            "error_description": "dataset_id is blank",
        }
        return JsonResponse(context, safe=False)

    username = userinfo["preferred_username"]
    if action == "create":

        user = CustomUser.objects.get(username=username)
        newDatasetOwner = DatasetOwner(
            username=user, dataset_id=dataset_id, is_owner=True
        )
        newDatasetOwner.save()
        context = {"Success": True, "comment": "Dataset owner created Successfully"}
        return JsonResponse(context, safe=False)

    ispmu = False
    ispra = False
    userroleobj = UserRole.objects.filter(
        username__username=username, org_id=org_id
    ).values("org_id", "role__role_name")
    if len(userroleobj) == 0:
        userroleobj = UserRole.objects.filter(username__username=username).values(
            "org_id", "role__role_name"
        )
        if len(userroleobj) != 0 and userroleobj[0]["role__role_name"] == "PMU":
            ispmu = True
    else:
        if userroleobj[0]["role__role_name"] == "DPA":
            ispra = True

    if ispmu == False and ispra == False:
        context = {
            "Success": False,
            "error": "access denied",
            "error_description": "access denied",
        }
        return JsonResponse(context, safe=False)

    if (ispmu or ispra) and action == "update" or action == "delete":
        try:
            user = CustomUser.objects.get(username=tgt_user_name)
            DatasetOwnerObjs = DatasetOwner.objects.filter(
                username=user, dataset_id=dataset_id
            )
            DOObjCount = DatasetOwnerObjs.count()
            if DOObjCount == 0:
                context = {
                    "Success": False,
                    "error": "user and dataset doesn't exist",
                    "error_description": "user and dataset doesn't exist",
                }
                return JsonResponse(context, safe=False)
            else:
                if action == "update":
                    DatasetOwnerObjs.update(is_owner=False)
                    context = {
                        "Success": True,
                        "comment": "Dataset owner updated Successfully",
                    }
                    return JsonResponse(context, safe=False)

                if action == "delete":
                    DatasetOwnerObjs.delete()
                    context = {
                        "Success": True,
                        "comment": "Dataset owner deleted Successfully",
                    }
                    return JsonResponse(context, safe=False)

        except Exception as e:
            context = {"Success": False, "error": str(e), "error_description": str(e)}
            return JsonResponse(context, safe=False)

    context = {
        "Success": False,
        "error": "Invalid action",
        "error_description": "Invalid action",
    }
    return JsonResponse(context, safe=False)


@csrf_exempt
def get_user_count(request):

    users = CustomUser.objects.all().values("username")
    user_count = len(users)
    context = {"Success": True, "user_count": user_count}
    return JsonResponse(context, safe=False)


@csrf_exempt
def get_access_datasets(request):

    print("-----------------", request.body)
    post_data = json.loads(request.body.decode("utf-8"))
    access_token = post_data.get("access_token", None)
    org_id = post_data.get("org_id", None)

    userinfo = get_user(access_token)
    if userinfo["success"] == False:
        context = {
            "Success": False,
            "error": userinfo["error"],
            "error_description": userinfo["error_description"],
        }
        return JsonResponse(context, safe=False)
    username = userinfo["preferred_username"]

    ispmu = False
    ispra = False
    userroleobj = UserRole.objects.filter(
        username__username=username, org_id=org_id
    ).values("org_id", "role__role_name")
    if len(userroleobj) == 0:
        userroleobj = UserRole.objects.filter(username__username=username).values(
            "org_id", "role__role_name"
        )
        if len(userroleobj) != 0 and userroleobj[0]["role__role_name"] == "PMU":
            ispmu = True
    else:
        if userroleobj[0]["role__role_name"] == "DPA":
            ispra = True

    if ispmu == False and ispra == False:
        context = {
            "Success": False,
            "error": "No access for the org for this user",
            "error_description": "No access for the org for this user",
        }
        return JsonResponse(context, safe=False)

    userrole = userroleobj[0]["role__role_name"]
    userorg = userroleobj[0]["org_id"]

    if userrole == "PMU":
        users = CustomUser.objects.all().values("username")
        users_list = []
        for user in users:
            user_roles = UserRole.objects.filter(
                username__username=user["username"]
            ).values("org_id", "role__role_name")
            user_roles_res = []
            for role in user_roles:
                user_roles_res.append(
                    {"org_id": role["org_id"], "role": role["role__role_name"]}
                )
            users_list.append({"username": user["username"], "access": user_roles_res})

        context = {"Success": True, "users": users_list}
        return JsonResponse(context, safe=False)

    if userrole == "DPA" and userorg != None:
        user_roles = UserRole.objects.filter(org_id=userorg).values(
            "username__username", "org_id", "org_title", "role__role_name"
        )
        user_roles_res = {}
        for role in user_roles:
            if role["username__username"] in user_roles_res:
                user_roles_res[role["username__username"]].append(
                    {
                        "org_id": role["org_id"],
                        "org_title": role["org_title"],
                        "role": role["role__role_name"],
                    }
                )
            else:
                user_roles_res[role["username__username"]] = [
                    {
                        "org_id": role["org_id"],
                        "org_title": role["org_title"],
                        "role": role["role__role_name"],
                    }
                ]

        users_list = []
        for key, value in user_roles_res.items():
            users_list.append({"username": key, "access": value})
        context = {"Success": True, "users": users_list}
        return JsonResponse(context, safe=False)

    context = {
        "Success": False,
        "error": "No Matching org and user found",
        "error_description": ("org is " + userorg + " and role is " + userrole),
    }
    return JsonResponse(context, safe=False)


@csrf_exempt
def login(request):

    post_data = json.loads(request.body.decode("utf-8"))
    token = post_data.get("token", None)

    userinfo = get_user(token)
    user_name = userinfo["preferred_username"]

    try:

        query = f"""
                mutation {{
                    token_auth(username: {user_name}, password: {password}) {{
                        success,
                        errors,
                        unarchiving,
                        token,
                        refresh_token,
                        unarchiving,
                        user {{
                        id,
                        username,
                        }}
                    }}
    }}"""

        headers = {}
        response = requests.post(auth_url, json={"query": query}, headers=headers)

        response_json = json.loads(response.text)
        print(response_json)

        return JsonResponse(response_json, safe=False)
    except Exception as e:
        raise Http404("login failed")
