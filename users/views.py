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
import os

config = ConfigParser()
config.read("config.ini")


# configure keycloak client
keycloak_openid = KeycloakOpenID(
    server_url=os.environ.get('KEYCLOAK_URL', config.get("keycloak", "server_url")),
    client_id=os.environ.get('KEYCLOAK_CLIENT_ID', config.get("keycloak", "client_id")),
    realm_name=os.environ.get('KEYCLOAK_REALM_NAME', config.get("keycloak", "realm_name")),
    client_secret_key=os.environ.get('KEYCLOAK_SECRET', config.get("keycloak", "client_secret_key")),
)
config_well_known = keycloak_openid.well_known()



# graphql config
password = os.environ.get('USER_PASS', config.get("graphql", "password"))
auth_url = os.environ.get('AUTH_GRAPHQL_URL', config.get("graphql", "base_url"))

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

    ispmu = False
    iscr = False

    userroleobj = UserRole.objects.filter(
        username__username=username, org_id=access_org_id
    ).values("org_id", "role__role_name")
    
    if "PMU" in [each["role__role_name"] for each in userroleobj]:
        ispmu = True    

    if len(userroleobj) == 0:

        userroles = UserRole.objects.filter(username__username=username).values(
            "org_id", "role__role_name"
        )
        if len(userroles) != 0:
            if "PMU" in [each["role__role_name"] for each in userroles]:
                ispmu = True
            if "CR" in [each["role__role_name"] for each in userroles]:
                iscr = True
        if len(userroles) == 0:
            if access_req == "query":
                context = {"Success": True, "access_allowed": True, "role": ""}
                return JsonResponse(context, safe=False)
            context = {
                "Success": False,
                "error": "No Matching user role found",
                "error_description": "No Matching user role found",
            }
            return JsonResponse(context, safe=False)

    userrole = (
        "PMU"
        if ispmu == True
        else "CR"
        if iscr == True
        else userroleobj[0]["role__role_name"]
        if len(userroleobj) != 0
        else userroles[0]["role__role_name"]
    )
    userorg = (
        ""
        if (userrole in ["PMU", "CR"] or len(userroleobj) == 0)
        else userroleobj[0]["org_id"]
    )

    if access_req == "query":
        context = {"Success": True, "access_allowed": True, "role": userrole}
        return JsonResponse(context, safe=False)

    if ispmu == True:
        context = {"Success": True, "access_allowed": True, "role": "PMU"}
        return JsonResponse(context, safe=False)

    # request_dataset_mod
    if (
        userrole == "DPA"
        and userorg != ""
        and access_req
        not in ["approve_organization", "publish_dataset", "approve_license"]
    ):
        context = {"Success": True, "access_allowed": True, "role": "DPA"}
        return JsonResponse(context, safe=False)

    if (
        userrole == "DP"
        and userorg != ""
        and (("create" in access_req) or (access_req in ["list_review_request"]))
        and access_req not in ["create_dam"]
    ):
        context = {"Success": True, "access_allowed": True, "role": "DP"}
        return JsonResponse(context, safe=False)

    if (
        userrole == "DP"
        and userorg != ""
        and (
            "update" in access_req
            or "delete" in access_req
            or "patch" in access_req
            or "get_draft_datasets" in access_req
            or "request_dataset_review" in access_req
        )
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


# api functions
@csrf_exempt
def verify_user_token(request):

    print("-----------------", request.body)
    post_data = json.loads(request.body.decode("utf-8"))
    access_token = request.META.get("HTTP_ACCESS_TOKEN", post_data.get("access_token", None)) 
    userinfo = get_user(access_token)

    return JsonResponse(userinfo, safe=False)


@csrf_exempt
def check_user(request):
    post_data = json.loads(request.body.decode("utf-8"))
    access_token = request.META.get("HTTP_ACCESS_TOKEN", post_data.get("access_token", None)) 
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
            "org_id", "org_title", "role__role_name", "org_status"
        )
        user_roles_res = []
        for role in user_roles:
            user_roles_res.append(
                {
                    "org_id": role["org_id"],
                    "org_title": role["org_title"],
                    "role": role["role__role_name"],
                    "status": role["org_status"],
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
    access_token = request.META.get("HTTP_ACCESS_TOKEN", post_data.get("access_token", None)) 
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
    access_token = request.META.get("HTTP_ACCESS_TOKEN", post_data.get("access_token", None)) 
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
def modify_org_status(request):

    print("-----------------", request.body)
    post_data = json.loads(request.body.decode("utf-8"))
    access_token = request.META.get("HTTP_ACCESS_TOKEN", post_data.get("access_token", None)) 
    org_list = post_data.get("org_list", None)
    org_status = post_data.get("org_status", None)

    userinfo = get_user(access_token)

    if userinfo["success"] == False:
        context = {
            "Success": False,
            "error": userinfo["error"],
            "error_description": userinfo["error_description"],
        }
        return JsonResponse(context, safe=False)

    if len(org_list) == 0:
        context = {
            "Success": False,
            "error": "wrong org_id",
            "error_description": "org_list is blank",
        }
        return JsonResponse(context, safe=False)

    if org_status not in ["created", "approved", "rejected"]:
        context = {
            "Success": False,
            "error": "wrong status",
            "error_description": "please send correct status",
        }
        return JsonResponse(context, safe=False)

    username = userinfo["preferred_username"]

    ispmu = False
    ispra = False
    userroleobj = UserRole.objects.filter(
        username__username=username, org_id__in=org_list
    ).values("org_id", "role__role_name")
    if len(userroleobj) == 0 or True:
        userroleobj = UserRole.objects.filter(username__username=username).values(
            "org_id", "role__role_name"
        )
        if len(userroleobj) != 0 and "PMU" in [
            each["role__role_name"] for each in userroleobj
        ]:
            ispmu = True
    else:
        if "DPA" in [each["role__role_name"] for each in userroleobj]:
            ispra = True

    if ispmu == False:
        context = {
            "Success": False,
            "error": "Access Denied",
            "error_description": "User is not Authorized",
        }
        return JsonResponse(context, safe=False)

    try:
        UserRoleObjs = UserRole.objects.filter(org_id__in=org_list)
        UserRoleObjCount = UserRoleObjs.count()
        if UserRoleObjCount == 0:
            context = {
                "Success": False,
                "error": "no matching org found",
                "error_description": "please send correct org_list",
            }
            return JsonResponse(context, safe=False)
        UserRoleObjs.update(org_status=org_status)
        context = {"Success": True, "comment": "org status updated successfully"}
        return JsonResponse(context, safe=False)
    except Exception as e:
        context = {"Success": False, "error": str(e), "error_description": str(e)}
        return JsonResponse(context, safe=False)


@csrf_exempt
def get_users(request):

    print("-----------------", request.body)
    post_data = json.loads(request.body.decode("utf-8"))
    access_token = request.META.get("HTTP_ACCESS_TOKEN", post_data.get("access_token", None)) 
    org_id = post_data.get("org_id", None)
    user_type = post_data.get("user_type", None)

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

    if userrole == "PMU" and org_id == "":
        users = CustomUser.objects.exclude(username=username).values(
            "username", "email"
        )
        users_list = []
        for user in users:
            user_roles = UserRole.objects.filter(
                username__username=user["username"], role__role_name__in=user_type
            ).values("org_id", "org_title", "role__role_name", "org_status")
            if len(user_roles) == 0:
                continue
            user_roles_res = []
            for role in user_roles:
                user_roles_res.append(
                    {
                        "org_id": role["org_id"],
                        "org_title": role["org_title"],
                        "role": role["role__role_name"],
                        "status": role["org_status"],
                        "updated": role["updated"],
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

    if userrole in ["DPA", "PMU"] and org_id != "":
        user_roles = (
            UserRole.objects.filter(org_id=org_id, role__role_name__in=user_type)
            # .exclude(role__role_name__in=["PMU", "DPA"])
            .exclude(username__username=username).values(
                "username__username",
                "username__email",
                "org_id",
                "org_title",
                "role__role_name",
                "org_status",
                "updated",
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
                        "status": role["org_status"],
                        "updated": role["updated"],
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
                            "status": role["org_status"],
                            "updated": role["updated"],
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
    access_token = request.META.get("HTTP_ACCESS_TOKEN", post_data.get("access_token", None)) 
    org_id = post_data.get("org_id", None)
    org_title = post_data.get("org_title", None)
    role_name = post_data.get("role_name", None)
    tgt_user_name  = post_data.get("tgt_user_name", None)
    tgt_user_email = post_data.get("tgt_user_email", None)
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
        if len(userroleobj) != 0 and "PMU" in [
            each["role__role_name"] for each in userroleobj
        ]:
            ispmu = True
    else:
        if "DPA" in [each["role__role_name"] for each in userroleobj]:
            ispra = True

    if ispmu == False and ispra == False:
        context = {
            "Success": False,
            "error": "Access Denied",
            "error_description": "User is not Authorized",
        }
        return JsonResponse(context, safe=False)
    #TO Do: mark status as "approved" if update if new role create
    if action == "update":
        try:
            role = Role.objects.get(role_name=role_name)
            user = CustomUser.objects.get(username=tgt_user_name) if (tgt_user_email == None or tgt_user_email == "") else CustomUser.objects.get(email=tgt_user_email)

            UserRoleObjs = UserRole.objects.filter(username=user, org_id=org_id)
            UserRoleObjCount = UserRoleObjs.count()
            if UserRoleObjCount == 0:
                newUserRole = UserRole(
                    username=user, org_id=org_id, org_title=org_title, role=role, org_status="approved"
                )
                newUserRole.save()
            else:
                UserRoleObjs.update(role=role)
                UserRoleObjs.update(org_status="approved")
            context = {"Success": True, "comment": "User Role Updated/Added Successfully"}
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
    access_token = request.META.get("HTTP_ACCESS_TOKEN", post_data.get("access_token", None)) 
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
    access_token = request.META.get("HTTP_ACCESS_TOKEN", post_data.get("access_token", None)) 
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
def get_user_datasets(request):

    print("-----------------", request.body)
    post_data = json.loads(request.body.decode("utf-8"))
    access_token = request.META.get("HTTP_ACCESS_TOKEN", post_data.get("access_token", None)) 

    userinfo = get_user(access_token)
    if userinfo["success"] == False:
        context = {
            "Success": False,
            "error": userinfo["error"],
            "error_description": userinfo["error_description"],
        }
        return JsonResponse(context, safe=False)
    username = userinfo["preferred_username"]


    user_datasets = list(DatasetOwner.objects.filter(username__username=username).values_list(
        "dataset_id", flat=True
    ))
    
    context = {
        "Success": True,
        "datasets": user_datasets,
    }
    return JsonResponse(context, safe=False)


@csrf_exempt
def get_sys_token(request):

    # system config
    sys_user = os.environ.get('SYSTEM_USER', config.get("sysuser", "sys_user")),
    sys_pass = os.environ.get('SYSTEM_USER_PASS', config.get("sysuser", "sys_pass")),

    try:

        token = keycloak_openid.token(sys_user, sys_pass)
        access_token = token["access_token"]
        info = {
            "success": True,
            "access_token": access_token,
        }

    except Exception as error:
        print(error)
        info = {
            "success": False,
            "error": "Token generation failed",
            "error_description": str(error),
        }

    return JsonResponse(info, safe=False)


@csrf_exempt
def get_user_info(request):

    post_data = json.loads(request.body.decode("utf-8"))
    user_name = post_data.get("user_name", None)

    try:
        users = CustomUser.objects.filter(username=user_name).values(
            "username", "email"
        )

        context = {
            "Success": True,
            "username": user_name,
            "email": users[0]["email"],
        }
        return JsonResponse(context, safe=False)

    except Exception as error:
        info = {
            "Success": False,
            "error": "User Info Fetch Failed",
            "error_description": str(error),
        }

        return JsonResponse(info, safe=False)


@csrf_exempt
def update_datasetreq(request):

    post_data = json.loads(request.body.decode("utf-8"))
    username = post_data.get("username", "Anonymous")
    data_request_id = post_data.get("data_request_id", None)
    dataset_access_model_request_id = post_data.get(
        "dataset_access_model_request_id", None
    )
    dataset_access_model_id = post_data.get("dataset_access_model_id", None)
    dataset_id = post_data.get("dataset_id", None)
    username = "Anonymous" if (username == "" or username == None) else username

    try:
        user = CustomUser.objects.get(username=username)
        DataSetReqObjs = Datasetrequest.objects.filter(
            username=user,
            data_request_id=data_request_id,
            dataset_access_model_request_id=dataset_access_model_request_id,
            dataset_access_model_id=dataset_access_model_id,
            dataset_id=dataset_id,
        ).values("download_count")

        DataSetReqObjCount = DataSetReqObjs.count()
        if DataSetReqObjCount == 0:
            newDataSetReqObj = Datasetrequest(
                username=user,
                data_request_id=data_request_id,
                dataset_access_model_request_id=dataset_access_model_request_id,
                dataset_access_model_id=dataset_access_model_id,
                dataset_id=dataset_id,
                download_count=1,
            )
            newDataSetReqObj.save()
        else:
            download_count = DataSetReqObjs[0]["download_count"]
            DataSetReqObjs.update(download_count=download_count + 1)
        context = {"Success": True, "comment": "Datasetrequest updated Successfully"}
        return JsonResponse(context, safe=False)
    except Exception as e:
        context = {"Success": False, "error": str(e), "error_description": str(e)}
        return JsonResponse(context, safe=False)


@csrf_exempt
def get_org_requestor(request):

    print("-----------------", request.body)
    post_data = json.loads(request.body.decode("utf-8"))
    access_token = request.META.get("HTTP_ACCESS_TOKEN", post_data.get("access_token", None)) 
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
    userroleobj = UserRole.objects.filter(username__username=username).values(
        "org_id", "role__role_name"
    )
    if len(userroleobj) != 0 and "PMU" in [
        each["role__role_name"] for each in userroleobj
    ]:
        ispmu = True

    if ispmu == False:
        context = {
            "Success": False,
            "error": "Access Denied",
            "error_description": "No access for the org for this user",
        }
        return JsonResponse(context, safe=False)

    try:
        org_roles = UserRole.objects.filter(
            org_id=org_id, role__role_name__in=["DPA"]
        ).values(
            "username__username",
            "username__email",
            "org_id",
            "org_title",
            "role__role_name",
        )
        context = {
            "Success": True,
            "username": org_roles[0]["username__username"],
            "email": org_roles[0]["username__email"],
            "org_id": org_roles[0]["org_id"],
            "org_title": org_roles[0]["org_title"],
            "role": org_roles[0]["role__role_name"],
        }
    except Exception as e:
        context = {
            "Success": False,
            "error": str(e),
            "error_description": "Matching organization requestor not found",
        }
    return JsonResponse(context, safe=False)


@csrf_exempt
def get_user_orgs(request):

    print("-----------------", request.body)
    post_data = json.loads(request.body.decode("utf-8"))
    access_token = request.META.get("HTTP_ACCESS_TOKEN", post_data.get("access_token", None)) 

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
        userroleobj = UserRole.objects.filter(username__username=username, role__role_name="DPA").values(
            "org_id", "role__role_name"
        )
        orgs = []
        for roles in userroleobj:
            if roles["org_id"] != None:
                orgs.append(roles["org_id"])

        context = {"Success": True, "orgs": orgs}
    except Exception as e:
        context = {
            "Success": False,
            "error": str(e),
            "error_description": "Matching organization requestor not found",
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
