from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import Http404
from keycloak import KeycloakOpenID
import requests
import json
from django.views.decorators.csrf import csrf_exempt

#configure client
keycloak_openid = KeycloakOpenID(server_url="https://kc.ndp.civicdatalab.in/auth/",
                                 client_id="opub-idp",
                                 realm_name="external",
                                 client_secret_key="YCsLCvO3kNIMcx6tz24jEzAmiHKxpErs")

# Get WellKnow
config_well_known = keycloak_openid.well_known()

#password
password = "supersecretpassword$123"

auth_url = 'http://127.0.0.1:8000/graphql'

@csrf_exempt
def register(request):
    post_data = json.loads(request.body.decode('utf-8'))
    email    = post_data.get('email', None)
    username = post_data.get('username', None)
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
        print(response_json)        


        return JsonResponse(response_json, safe=False) 
    except Exception as e:
        raise Http404("user already exists")

@csrf_exempt
def get_user(token):
    userinfo = keycloak_openid.userinfo(token['access_token'])
    return userinfo
    
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
