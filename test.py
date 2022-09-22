from keycloak import KeycloakOpenID
from keycloak import KeycloakAdmin


# keycloak_openid = KeycloakOpenID(server_url="https://kc.ndp.civicdatalab.in/auth/",
#                                  client_id="opub-idp",
#                                  realm_name="external",
#                                  client_secret_key="YCsLCvO3kNIMcx6tz24jEzAmiHKxpErs")

# # Get WellKnow
# config_well_known = keycloak_openid.well_known()

# token = keycloak_openid.token("abhinav", "abhinav")
# access_token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJCdXFLSkxZRUo0azdxc2M3RHItRjRZYlY0YWVsTzNMUnEtaDZWR3ZZR0ZNIn0.eyJleHAiOjE2NjM4MjA2NzQsImlhdCI6MTY2MzgyMDM3NCwianRpIjoiNGQxM2ZhZDMtNjc4Yi00Zjg1LWI1ZDktYjM5ZjY1MTdkOTZjIiwiaXNzIjoiaHR0cHM6Ly9rYy5uZHAuY2l2aWNkYXRhbGFiLmluL2F1dGgvcmVhbG1zL2V4dGVybmFsIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6ImE3M2EyZThlLWQ3NjktNDA5OC1iNzAxLWFmMjAzN2M5OGY5ZCIsInR5cCI6IkJlYXJlciIsImF6cCI6Im9wdWItaWRwIiwic2Vzc2lvbl9zdGF0ZSI6IjRlNjY4OWZhLWFmNmItNDM5Ni1hMTUzLTFlYTBjNDY5N2IxNiIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiKiJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJkZWZhdWx0LXJvbGVzLWV4dGVybmFsIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6InByb2ZpbGUgZW1haWwiLCJzaWQiOiI0ZTY2ODlmYS1hZjZiLTQzOTYtYTE1My0xZWEwYzQ2OTdiMTYiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicHJlZmVycmVkX3VzZXJuYW1lIjoiYWJoaW5hdiJ9.VGnYWJahehNmH17-kznfNErWWv20Hpg9D3wP2VWTGoAiryKvI7J293VXYONsIj_ki6Oqu6cg6-KYUJBSyPzUeNrU9wLyMS7LNOzWi4pkzWdDGhXSQaqJnvxvdwvjk6_rkDwllI0C7w_OPfOgM1NT_bTQqC8zqZESgr-FARx7MSTjkzeGACoynC-6nuKrUSuNv7zJpdB96JYCqZK66Rj6ArQ2l4cEQwi7lq3jl65KHYOSL-FwRw1TlhX6NBsVnXKDKFQNRzBHM7ZBbYkoMZ-ZgxFJLaU6goXDGUkdg8Rasu78KC7rjs-dzixxr-lKxbK-J4xrz3Acybq2cPxTyfewGA'

# userinfo = keycloak_openid.userinfo(token['access_token'])

# KEYCLOAK_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\n" + keycloak_openid.public_key() + "\n-----END PUBLIC KEY-----"
# options = {"verify_signature": True, "verify_aud": True, "verify_exp": True}
# token_info = keycloak_openid.decode_token(token['access_token'], key=KEYCLOAK_PUBLIC_KEY, options=options)


# print (userinfo, token)
# print (keycloak_openid)

# keycloak_admin = KeycloakAdmin(server_url="https://kc.ndp.civicdatalab.in/auth",
#                                username='example-admin',
#                                password='secret',
#                                realm_name="opub-idp",
#                                user_realm_name="only_if_other_realm_than_master",
#                                client_secret_key="YCsLCvO3kNIMcx6tz24jEzAmiHKxpErs",
#                                verify=True)

# # Get WellKnow
# # config_well_known = keycloak_openid.well_known()

# new_user = keycloak_admin.create_user({"email": "abhinav@civicdatalab.in",
#                                        "username": "abhinav@civicdatalab.in",
#                                        "enabled": True,
#                                        "firstName": "Abhinav",
#                                        "lastName": "Abhinav",
#                     "credentials": [{"value": "secret","type": "password",}]})



import requests
import json



query = f"""
        mutation {{
            register(
            email: "new_user2@email.com",
            username: "new_user2",
            password1: "supersecretpassword",
            password2: "supersecretpassword",
        ) {{
            success,
            errors,
            token,
            refresh_token
        }}
}}"""


headers = {} 
response = requests.post('http://127.0.0.1:8000/graphql', json = {"query": query},  headers=headers)

response_json = json.loads(response.text)
print(response_json)
