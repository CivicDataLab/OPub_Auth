from keycloak import KeycloakOpenID
from keycloak import KeycloakAdmin


keycloak_openid = KeycloakOpenID(server_url="https://kc.ndp.civicdatalab.in/auth/",
                                 client_id="opub-idp",
                                 realm_name="external",
                                 client_secret_key="YCsLCvO3kNIMcx6tz24jEzAmiHKxpErs")

# Get WellKnow
config_well_known = keycloak_openid.well_known()

token = keycloak_openid.token("abhinav", "abhinav")
access_token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJCdXFLSkxZRUo0azdxc2M3RHItRjRZYlY0YWVsTzNMUnEtaDZWR3ZZR0ZNIn0.eyJleHAiOjE2NjQxODQ1MjUsImlhdCI6MTY2NDE4NDIyNSwiYXV0aF90aW1lIjoxNjY0MTgzOTI0LCJqdGkiOiIxMGQ5OWZkYy00ZjZkLTQ2NWMtODdhMS1mNjAwOTY4OTZiMGYiLCJpc3MiOiJodHRwczovL2tjLm5kcC5jaXZpY2RhdGFsYWIuaW4vYXV0aC9yZWFsbXMvZXh0ZXJuYWwiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiYTczYTJlOGUtZDc2OS00MDk4LWI3MDEtYWYyMDM3Yzk4ZjlkIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoib3B1Yi1pZHAiLCJub25jZSI6ImQ2YjA3NDkwLTRjYWUtNDFiZS04OGY3LWI5NTNmYjg2MDQ1YSIsInNlc3Npb25fc3RhdGUiOiJiNWIxMTEwMy02ZWM5LTQ1MTQtODcyYS1kNzM4NmMzNDgxMjkiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwiZGVmYXVsdC1yb2xlcy1leHRlcm5hbCIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInNpZCI6ImI1YjExMTAzLTZlYzktNDUxNC04NzJhLWQ3Mzg2YzM0ODEyOSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhYmhpbmF2In0.rFPEBvshSYZ-m2f65zvX7DQ-QNsZy7eIbrmjRdPulC7iZJo8MLYkwz1emORTs2veia2zyazf0SVaPBMTmI8j4vWx-rvELz0ZJQ2ET7L8WT1kBnDBXe_pDd7y4WBwRrLO0jdfsZM58hboWSNwrgYVhGyvOtmcAVMKIeY7BXyk8MlPUwnw2Vta2xYrTS7LDvZDfrC_7qJz81DxvKq-KT_QwCCjF5nHyNPa9yUKAkdO63dfVriw5VNsy1JVv7-bn3Lj1NHdaEWMTJ74RaGi3CCXQ6oLWVWijCp2f_YJYxH8xl-YZ5XXI72I3IMFqoyo4HbE2r77k2JvZ0d3OkJMuRnfzA'
userinfo = keycloak_openid.userinfo(access_token)    #(token['access_token'])



print (userinfo)


# KEYCLOAK_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\n" + keycloak_openid.public_key() + "\n-----END PUBLIC KEY-----"
# options = {"verify_signature": True, "verify_aud": True, "verify_exp": True}
# token_info = keycloak_openid.decode_token(token['access_token'], key=KEYCLOAK_PUBLIC_KEY, options=options)


# print (userinfo, access_token)
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





# import requests
# import json



# query = f"""
#         mutation {{
#             register(
#             email: "new_user2@email.com",
#             username: "new_user2",
#             password1: "supersecretpassword",
#             password2: "supersecretpassword",
#         ) {{
#             success,
#             errors,
#             token,
#             refresh_token
#         }}
# }}"""


# headers = {} 
# response = requests.post('http://127.0.0.1:8000/graphql', json = {"query": query},  headers=headers)

# response_json = json.loads(response.text)
# print(response_json)
