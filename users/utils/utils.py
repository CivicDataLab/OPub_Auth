from ..models import *
import requests
import json


def check_user_role(calling_user, org_id):

    ispmu = False
    isdpa = False
    isdp = False
    iscr = False

    userroleobj = UserRole.objects.filter(username=calling_user)
    if "PMU" in [each.role.role_name for each in userroleobj]:
        ispmu = True

    user_org_roleobj = UserRole.objects.filter(username=calling_user, org_id=org_id)
    role_list = [each.role.role_name for each in user_org_roleobj]
    if "DPA" in role_list:
        isdpa = True
    else:
        org_roleobj = UserRole.objects.filter(org_id=org_id)
        org_role_list = [each.role.role_name for each in org_roleobj]
        if "DPA" not in org_role_list and len(org_role_list) > 0:
            isdpa = is_usr_parent_org_dpa(calling_user, org_id)

    if "DP" in role_list:
        isdp = True
    if "CR" in role_list:
        iscr = True

    return ispmu, isdpa, isdp, iscr


def is_usr_parent_org_dpa(calling_user, org_id, isdpa=False):

    parent_org_id = UserRole.objects.filter(org_id=org_id)[0].org_parent_id
    if parent_org_id != None:
        user_org_roleobj = UserRole.objects.filter(
            username=calling_user, org_id=parent_org_id
        )
        role_list = [each.role.role_name for each in user_org_roleobj]
        if "DPA" in role_list:
            isdpa = True
            return isdpa
        else:
            isdpa = is_usr_parent_org_dpa(calling_user, parent_org_id, isdpa)

    return isdpa

def get_child_orgs_without_dpa(org_id, child_org_list=[]):
    
    child_org_roleobjs = list(set(list(UserRole.objects.filter(org_parent_id=org_id).values_list("org_id", flat=True))))

    for each_org in child_org_roleobjs:
        
        org_roleobj = UserRole.objects.filter(org_id=each_org)
        org_role_list = [each.role.role_name for each in org_roleobj]
        if "DPA" not in org_role_list:
            child_org_list.append(each_org)
        get_child_orgs_without_dpa(each_org, child_org_list)
        
    return child_org_list

def create_user(auth_url, email, username, password):
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
    return response_json

    