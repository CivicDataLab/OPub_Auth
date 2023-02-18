from ..models import *


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
