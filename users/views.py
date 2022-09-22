from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from keycloak import KeycloakOpenID
import requests
import json

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


def register(request):
    try:

        query = f"""
                mutation {{
                    register(
                    email: "new_user3@email.com",
                    username: "new_user3",
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


        return HttpResponse(response_json) 
    except Exception as e:
        raise Http404("user doesn't exist")

def get_user(token):
    userinfo = keycloak_openid.userinfo(token['access_token'])
