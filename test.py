# keycloak integration
from keycloak import KeycloakOpenID
from keycloak import KeycloakAdmin


# keycloak_admin = KeycloakAdmin(server_url="https://kc.ndp.civicdatalab.in/auth/",
#                                username='admin',
#                                password='Pa55w0rd',
#                                realm_name="master",
#                                user_realm_name="only_if_other_realm_than_master",
#                                client_secret_key="YCsLCvO3kNIMcx6tz24jEzAmiHKxpErs",
#                                verify=True)


keycloak_openid = KeycloakOpenID(
    server_url="https://kc.ndp.civicdatalab.in/auth/",
    client_id="opub-idp",
    realm_name="external",
    client_secret_key="YCsLCvO3kNIMcx6tz24jEzAmiHKxpErs",
)

# # Get WellKnow
config_well_known = keycloak_openid.well_known()

token = keycloak_openid.token("testuser", "testuser")
# access_token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJCdXFLSkxZRUo0azdxc2M3RHItRjRZYlY0YWVsTzNMUnEtaDZWR3ZZR0ZNIn0.eyJleHAiOjE2NjQyMjkyNzUsImlhdCI6MTY2NDIyODk3NSwianRpIjoiNDgxNGUxYzgtMjJjMy00NzM4LWIxMmMtNTJhNGIxNjViZDRjIiwiaXNzIjoiaHR0cHM6Ly9rYy5uZHAuY2l2aWNkYXRhbGFiLmluL2F1dGgvcmVhbG1zL2V4dGVybmFsIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6ImE3M2EyZThlLWQ3NjktNDA5OC1iNzAxLWFmMjAzN2M5OGY5ZCIsInR5cCI6IkJlYXJlciIsImF6cCI6Im9wdWItaWRwIiwic2Vzc2lvbl9zdGF0ZSI6IjliZDU0ODg0LWU4MTgtNDg0MS1iOGMxLTI3Mjc3Y2RjMzNiNiIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiKiJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJkZWZhdWx0LXJvbGVzLWV4dGVybmFsIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6InByb2ZpbGUgZW1haWwiLCJzaWQiOiI5YmQ1NDg4NC1lODE4LTQ4NDEtYjhjMS0yNzI3N2NkYzMzYjYiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IkFiaGluYXYiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhYmhpbmF2IiwiZ2l2ZW5fbmFtZSI6IkFiaGluYXYiLCJlbWFpbCI6ImFiaGluYXZAY2l2aWNkYXRhbGFiLmluIn0.gdORLcy_9BTjzvciTjtuHF72G5p4d4U8ByBvllR4LvJV6sbdUruI1XK_lbTOCBs0Gq8gc1BxZ9tXD-i0ZE0UR18y_IZSysYBWci62tdLJ4Ou9mUgBh_14SvL0J_eGbafT4nLCMx9VQFohu_d-jjuPmodow32iZ6WGO_bHAUz6jhAxLJzEC6EMdDzKAEsTVY2DuxLTApSUH7MD9WQ6bCnpDZFofrcWtpssS3EAiWFk0HDr0vkG_74yT5GGGyS4E42EfrAnBJp3mUdZeCPF3eibHM-UYpOMH4pNVeaTl0z1qIqEA6yozDdVYA2L1SJ9fK9yDTQEQIe-qEZD0WSFmf5bA'
userinfo = keycloak_openid.userinfo(token["access_token"])  # (token['access_token'])


print(token["access_token"], userinfo)


# decorators
# def inc(x):
#     return x + 1


# def dec(x):
#     return x - 1


# def operate(func, x):
#     result = func(x)
#     return result

# def operate1(func, x):
#     return func


# op = (operate1(inc, 5))
# print (op(7))

# def make_pretty(func):
#     def inner():
#         print("I got decorated")
#         func()
#     return inner

# @make_pretty
# def ordinary():
#     print("I am ordinary")


# # ordinary = (make_pretty(ordinary))
# ordinary()

# def smart_divide(func):
#     def inner(*args, **kwargs):
#         print("I am going to divide", args[0], "and", args[1])
#         if args[1] == 0:
#             print("Whoops! cannot divide")
#             return

#         return func(*args, **kwargs)
#     return inner


# @smart_divide
# def divide(a, b):
#     return a/b

# print(divide(4,2))

# # decorator for getting username
# import requests
# import json

# auth_url = 'http://127.0.0.1:8000/users/verify_token'
# def validate_token(func):

#     def inner(*args, **kwargs):
#         print("checking token ", kwargs['user'], " validity")
#         if kwargs['user'] == "":
#             print("Whoops! Empty user")
#             return {"Success":False, "error":"Empty user", "error_description":"Empty user"}


#         headers = {}
#         response = requests.post(auth_url, data = json.dumps({"access_token": kwargs['user']}),  headers=headers)
#         response_json = json.loads(response.text)
#         if response_json['success'] == False:
#             return {"Success":False, "error":response_json['error'], "error_description":response_json['error_description']}

#         kwargs['user'] = response_json['preferred_username']
#         return func(*args, **kwargs)

#     return inner


# @validate_token
# def setrequest(req, user):
#     return(req, user)

# # setrequest("req_id1", "")
# print(setrequest("req_id1", user="eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJCdXFLSkxZRUo0azdxc2M3RHItRjRZYlY0YWVsTzNMUnEtaDZWR3ZZR0ZNIn0.eyJleHAiOjE2NjQyNjUxNjUsImlhdCI6MTY2NDI2NDg2NSwianRpIjoiZDIwMjk5ZmQtMWRjZC00ZmZhLTk5ZmItMWY4MTQ4ODg4YTc4IiwiaXNzIjoiaHR0cHM6Ly9rYy5uZHAuY2l2aWNkYXRhbGFiLmluL2F1dGgvcmVhbG1zL2V4dGVybmFsIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6ImE3M2EyZThlLWQ3NjktNDA5OC1iNzAxLWFmMjAzN2M5OGY5ZCIsInR5cCI6IkJlYXJlciIsImF6cCI6Im9wdWItaWRwIiwic2Vzc2lvbl9zdGF0ZSI6IjRmMGNlOGNkLTI1YzEtNGI1Ny1hYzU2LTIyMzYwYTRhYzlmYSIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiKiJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJkZWZhdWx0LXJvbGVzLWV4dGVybmFsIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6InByb2ZpbGUgZW1haWwiLCJzaWQiOiI0ZjBjZThjZC0yNWMxLTRiNTctYWM1Ni0yMjM2MGE0YWM5ZmEiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IkFiaGluYXYiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhYmhpbmF2IiwiZ2l2ZW5fbmFtZSI6IkFiaGluYXYiLCJlbWFpbCI6ImFiaGluYXZAY2l2aWNkYXRhbGFiLmluIn0.cnPbGoG3_Ha-kL1QZ8EyI0oq50XZyTjc802pxlzjr3QM8IKPw51xV_EH9Cl4D7Ck7CGEM2FzyMeooq0lB3SVUAbpl1nDC30g6C68t7MyCiXptKeumW1Lw7tYdwbJzd_w4eX1MGXCTCp47qF7pQbJgwTEii7IRxUuV5PVQ6G9bWjkFi4hkeyc5eTRPi6Ql4FQzK-wX01qTmcqO4DpusVfKo7-xbzTBuYYuFYiv-Ki3kiMg4WXIW06IMLSp5Rqh62_6dIzIJf_-rszVIllCvQdD_JkLCm50qtvZp_34H1DALb9ImXmNdKoZBcLzPHQXn7H2fMyZsKNWgCuy74sz1zbAA"))


# decorator for getting username
# import requests
# import json

# auth_url = 'http://127.0.0.1:8000/users/check_access'
# def validate_token(func):

#     def inner(*args, **kwargs):
#         print("checking ", kwargs['access_req'],  " access for ", kwargs['user'], " for organization", kwargs['access_org_id'])
#         if kwargs['user'] == "":
#             print("Whoops! Empty user")
#             return {"Success":False, "error":"Empty user", "error_description":"Empty user"}


#         headers = {}
#         response = requests.post(auth_url, data = json.dumps({"access_token": kwargs['user'], "access_org_id": kwargs['access_org_id'], "access_req"   : kwargs['access_req']}),  headers=headers)
#         response_json = json.loads(response.text)
#         if response_json['success'] == False:
#             return {"Success":False, "error":response_json['error'], "error_description":response_json['error_description']}

#         kwargs['user'] = response_json['preferred_username']
#         return func(*args, **kwargs)

#     return inner


# @validate_token
# def setrequest(req, user, access_org_id, access_req):
#     return(req, user, access_org_id, access_req)

# # setrequest("req_id1", "")
# print(setrequest("req_id1", user="eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJCdXFLSkxZRUo0azdxc2M3RHItRjRZYlY0YWVsTzNMUnEtaDZWR3ZZR0ZNIn0.eyJleHAiOjE2NjQyNjUxNjUsImlhdCI6MTY2NDI2NDg2NSwianRpIjoiZDIwMjk5ZmQtMWRjZC00ZmZhLTk5ZmItMWY4MTQ4ODg4YTc4IiwiaXNzIjoiaHR0cHM6Ly9rYy5uZHAuY2l2aWNkYXRhbGFiLmluL2F1dGgvcmVhbG1zL2V4dGVybmFsIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6ImE3M2EyZThlLWQ3NjktNDA5OC1iNzAxLWFmMjAzN2M5OGY5ZCIsInR5cCI6IkJlYXJlciIsImF6cCI6Im9wdWItaWRwIiwic2Vzc2lvbl9zdGF0ZSI6IjRmMGNlOGNkLTI1YzEtNGI1Ny1hYzU2LTIyMzYwYTRhYzlmYSIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiKiJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJkZWZhdWx0LXJvbGVzLWV4dGVybmFsIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6InByb2ZpbGUgZW1haWwiLCJzaWQiOiI0ZjBjZThjZC0yNWMxLTRiNTctYWM1Ni0yMjM2MGE0YWM5ZmEiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IkFiaGluYXYiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhYmhpbmF2IiwiZ2l2ZW5fbmFtZSI6IkFiaGluYXYiLCJlbWFpbCI6ImFiaGluYXZAY2l2aWNkYXRhbGFiLmluIn0.cnPbGoG3_Ha-kL1QZ8EyI0oq50XZyTjc802pxlzjr3QM8IKPw51xV_EH9Cl4D7Ck7CGEM2FzyMeooq0lB3SVUAbpl1nDC30g6C68t7MyCiXptKeumW1Lw7tYdwbJzd_w4eX1MGXCTCp47qF7pQbJgwTEii7IRxUuV5PVQ6G9bWjkFi4hkeyc5eTRPi6Ql4FQzK-wX01qTmcqO4DpusVfKo7-xbzTBuYYuFYiv-Ki3kiMg4WXIW06IMLSp5Rqh62_6dIzIJf_-rszVIllCvQdD_JkLCm50qtvZp_34H1DALb9ImXmNdKoZBcLzPHQXn7H2fMyZsKNWgCuy74sz1zbAA",
#                  access_org_id="123", access_req="APPROVE"))


# graphql mutation example
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
