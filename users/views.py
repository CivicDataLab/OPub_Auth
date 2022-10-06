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
config.read('config.ini')


#configure keycloak client
keycloak_openid = KeycloakOpenID(server_url=config.get('keycloak', 'server_url'),
                                 client_id=config.get('keycloak', 'client_id'),
                                 realm_name=config.get('keycloak', 'realm_name'),
                                 client_secret_key=config.get('keycloak', 'client_secret_key'))
config_well_known = keycloak_openid.well_known()


#graphql
password = config.get('graphql', 'password') 
auth_url = config.get('graphql', 'base_url')



@csrf_exempt
def get_user(access_token):
    
    try:
        userinfo = keycloak_openid.userinfo(access_token)
        userinfo['success'] = True
    except Exception as error:
        print (error)
        userinfo = {'success':False, "error":"invalid_token", "error_description":"Token verification failed"}
        
    return userinfo

@csrf_exempt
def verify_token(request):

    print ('-----------------', request.body )
    post_data        = json.loads(request.body.decode('utf-8'))
    access_token     = post_data.get('access_token', None)
    userinfo         = get_user(access_token)  
    
    return JsonResponse(userinfo, safe=False)  

@csrf_exempt
def has_access(username, access_org_id, access_req):
    
    access_dict = {"PMU":['CREATE', 'UPDATE', 'DELETE', 'APPROVE', 'APPROVE PUB', 'VIEW'],
                   "PRA":['CREATE', 'UPDATE', 'DELETE', 'APPROVE', 'VIEW'],
                   "PR": ['CREATE', 'UPDATE', 'VIEW'],
                   "CR": ['VIEW']}  
    try:
        role_obj = UserRole.objects.get(username__username=username, org_id=access_org_id)
        role = getattr(role_obj, 'role')
    except Exception as e:
        return {"Success": False, "error":str(e), "error_description":str(e)}
    
    role_access = "Available" if access_req in access_dict.get(role) else "Denied"
    
    if role_access == "Denied":
        context = {"success": False, "username":username, "access_org_id":access_org_id, "role": role, "access_req":access_req, "access":role_access}
    else:
        context = {"success": True, "username":username, "access_org_id":access_org_id, "role": role, "access_req":access_req, "access":role_access}
    return context
    
@csrf_exempt
def check_access(request):
    
    print ('-----------------', request.body )
    post_data        = json.loads(request.body.decode('utf-8'))
    access_token     = post_data.get('access_token', None)
    access_org_id    = post_data.get('access_org_id', None)
    access_req       = post_data.get('access_req', None)
    userinfo         = get_user(access_token)  
    
    if userinfo['success'] == False:
        context = {"Success": False, "error":userinfo['error'], "error_description":userinfo['error_description']}    
        return JsonResponse(context, safe=False)
    
    username = userinfo['preferred_username']
    
    has_access_res   = has_access(username, access_org_id, access_req)

    return JsonResponse(has_access_res, safe=False)  
    

@csrf_exempt
def check_user(request):
    post_data        = json.loads(request.body.decode('utf-8'))
    access_token     = post_data.get('access_token', None)
    userinfo         = get_user(access_token)
    
    if userinfo['success'] == False:
        context = {"Success": False, "error":userinfo['error'], "error_description":userinfo['error_description']}    
        return JsonResponse(context, safe=False)
        
    username          = userinfo['preferred_username']
    email             = userinfo['email']
    
    #check if username is in auth db
    num_users = CustomUser.objects.filter(username = username).count()
    
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
            response = requests.post(auth_url, json = {"query": query},  headers=headers)
            response_json = json.loads(response.text)
            print (response_json)
            
            if response_json['data']['register']['success'] == True:
                context = {"Success": True, "username":username, "email":email, "access_token":access_token, "Comment" : "User Registration successful"}
            else:
                context = {"Success": False, "errors":response_json['data']['register']['errors']}    
                        
            return JsonResponse(context, safe=False)
        
        except Exception as e:
            print (e)
            context = {"Success": False, "errors":response_json['data']['register']['errors']} 
            return JsonResponse(context, safe=False)
    else:
        user_roles = UserRole.objects.filter(username__username=username).values('org_id','role__role_name')
        user_roles_res = []
        for role in user_roles:
            user_roles_res.append({"org_id":role['org_id'], "role":role['role__role_name']})
        context = {"Success": True, "username":username, "email":email, "access_token":access_token, "access":user_roles_res, "Comment" : "User already exists"}
        return JsonResponse(context, safe=False)   
        
        
    
    
    
@csrf_exempt  
def login(request):
    
    post_data = json.loads(request.body.decode('utf-8'))
    token     = post_data.get('token', None)

    userinfo = get_user(token)
    user_name = userinfo['preferred_username']
    
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
        response = requests.post(auth_url, json = {"query": query},  headers=headers)

        response_json = json.loads(response.text)
        print(response_json)        


        return JsonResponse(response_json, safe=False) 
    except Exception as e:
        raise Http404("login failed")
