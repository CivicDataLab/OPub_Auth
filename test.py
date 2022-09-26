from keycloak import KeycloakOpenID
from keycloak import KeycloakAdmin


# keycloak_admin = KeycloakAdmin(server_url="https://kc.ndp.civicdatalab.in/auth/",
#                                username='admin',
#                                password='Pa55w0rd',
#                                realm_name="master",
#                                user_realm_name="only_if_other_realm_than_master",
#                                client_secret_key="YCsLCvO3kNIMcx6tz24jEzAmiHKxpErs",
#                                verify=True)


keycloak_openid = KeycloakOpenID(server_url="https://kc.ndp.civicdatalab.in/auth/",
                                 client_id="opub-idp",
                                 realm_name="external",
                                 client_secret_key="YCsLCvO3kNIMcx6tz24jEzAmiHKxpErs")

# Get WellKnow
config_well_known = keycloak_openid.well_known()

token = keycloak_openid.token("abhinav", "abhinav")
# access_token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJCdXFLSkxZRUo0azdxc2M3RHItRjRZYlY0YWVsTzNMUnEtaDZWR3ZZR0ZNIn0.eyJleHAiOjE2NjQyMjkyNzUsImlhdCI6MTY2NDIyODk3NSwianRpIjoiNDgxNGUxYzgtMjJjMy00NzM4LWIxMmMtNTJhNGIxNjViZDRjIiwiaXNzIjoiaHR0cHM6Ly9rYy5uZHAuY2l2aWNkYXRhbGFiLmluL2F1dGgvcmVhbG1zL2V4dGVybmFsIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6ImE3M2EyZThlLWQ3NjktNDA5OC1iNzAxLWFmMjAzN2M5OGY5ZCIsInR5cCI6IkJlYXJlciIsImF6cCI6Im9wdWItaWRwIiwic2Vzc2lvbl9zdGF0ZSI6IjliZDU0ODg0LWU4MTgtNDg0MS1iOGMxLTI3Mjc3Y2RjMzNiNiIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiKiJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJkZWZhdWx0LXJvbGVzLWV4dGVybmFsIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6InByb2ZpbGUgZW1haWwiLCJzaWQiOiI5YmQ1NDg4NC1lODE4LTQ4NDEtYjhjMS0yNzI3N2NkYzMzYjYiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IkFiaGluYXYiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhYmhpbmF2IiwiZ2l2ZW5fbmFtZSI6IkFiaGluYXYiLCJlbWFpbCI6ImFiaGluYXZAY2l2aWNkYXRhbGFiLmluIn0.gdORLcy_9BTjzvciTjtuHF72G5p4d4U8ByBvllR4LvJV6sbdUruI1XK_lbTOCBs0Gq8gc1BxZ9tXD-i0ZE0UR18y_IZSysYBWci62tdLJ4Ou9mUgBh_14SvL0J_eGbafT4nLCMx9VQFohu_d-jjuPmodow32iZ6WGO_bHAUz6jhAxLJzEC6EMdDzKAEsTVY2DuxLTApSUH7MD9WQ6bCnpDZFofrcWtpssS3EAiWFk0HDr0vkG_74yT5GGGyS4E42EfrAnBJp3mUdZeCPF3eibHM-UYpOMH4pNVeaTl0z1qIqEA6yozDdVYA2L1SJ9fK9yDTQEQIe-qEZD0WSFmf5bA'
userinfo = keycloak_openid.userinfo(token['access_token'])    #(token['access_token'])



print (token['access_token'], userinfo)








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
