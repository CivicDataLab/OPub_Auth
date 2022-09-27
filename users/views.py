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
    
    print (auth_url)
    post_data        = json.loads(request.body.decode('utf-8'))
    access_token     = post_data.get('access_token', None)
    userinfo         = get_user(access_token)  
    
    return JsonResponse(userinfo, safe=False)  
    

@csrf_exempt
def register(request):
    post_data        = json.loads(request.body.decode('utf-8'))
    access_token     = post_data.get('access_token', None)
    userinfo         = get_user(access_token)
    
    if userinfo['success'] == False:
        context = {"Success": False, "error":userinfo['error'], "error_description":userinfo['error_description']}    
        return JsonResponse(context, safe=False)
        
    username          = userinfo['preferred_username']
    email             = userinfo['email']

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
            context = {"Success": True, "username":username, "email":email, "access_token":access_token}
        else:
            context = {"Success": False, "errors":response_json['data']['register']['errors']}    
                    
        return JsonResponse(context, safe=False)
    
    except Exception as e:
        print (e)
        raise Http404("registration failed")
    
    
@csrf_exempt
def check(request):
    post_data        = json.loads(request.body.decode('utf-8'))
    access_token     = post_data.get('access_token', None)
    
    userinfo          = get_user(access_token)
    username          = userinfo['preferred_username']
    email             = userinfo['email']

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
            context = {"Success": True, "username":username, "email":email, "access_token":access_token}
        else:
            context = {"Success": False, "errors":response_json['data']['register']['errors']}    
                    
        return JsonResponse(context, safe=False)
    
    except Exception as e:
        raise Http404("registration failed")

    
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
