# # # # keycloak integration
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
    server_url="https://dev.kc.idp.civicdatalab.in/auth/",
    client_id="opub-idp",
    realm_name="external",
    client_secret_key="YCsLCvO3kNIMcx6tz24jEzAmiHKxpErs",
)

# # # Get WellKnow
# # config_well_known = keycloak_openid.well_known()

# token = keycloak_openid.token("abhinav", "abcd1234") #("abhinav", "!Abcd1234@")  # ("sanjay", "abcd1234")
access_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJCdXFLSkxZRUo0azdxc2M3RHItRjRZYlY0YWVsTzNMUnEtaDZWR3ZZR0ZNIn0.eyJleHAiOjE2ODA1MDk1MDksImlhdCI6MTY4MDA3NzUwOSwiYXV0aF90aW1lIjoxNjgwMDc3NTA5LCJqdGkiOiJjMjFiN2YyOC01YWIxLTRlN2EtODMwZi03M2IxNDAzZmQ2MTYiLCJpc3MiOiJodHRwczovL2Rldi5rYy5pZHAuY2l2aWNkYXRhbGFiLmluL2F1dGgvcmVhbG1zL2V4dGVybmFsIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6ImE3M2EyZThlLWQ3NjktNDA5OC1iNzAxLWFmMjAzN2M5OGY5ZCIsInR5cCI6IkJlYXJlciIsImF6cCI6Im9wdWItaWRwIiwic2Vzc2lvbl9zdGF0ZSI6IjA1MzI1OTNmLWY4YWYtNDk5My1iOTcxLTBkOTdlYmVkOTlmMyIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiKiJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJkZWZhdWx0LXJvbGVzLWV4dGVybmFsIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwic2lkIjoiMDUzMjU5M2YtZjhhZi00OTkzLWI5NzEtMGQ5N2ViZWQ5OWYzIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5hbWUiOiJBYmhpbmF2IiwicHJlZmVycmVkX3VzZXJuYW1lIjoiYWJoaW5hdiIsImdpdmVuX25hbWUiOiJBYmhpbmF2IiwiZW1haWwiOiJhYmhpbmF2QGNpdmljZGF0YWxhYi5pbiJ9.f7gUiYL8ISUkJ2Q-yT575OqZrUkGZj4fbttTVYSUOYK_OfMll-vjh3MbEmHgRcKLggLiUg_rpma9f_7ji-JboUAfknvIIos7LYEn5JzIrEO-y_ZhvTXf9VR56icZk5czoFfJy3Zy_oRv3FGWYQlLD_afanb3CM0QhQzWErlgNIWIAQy5z10iWbjhjrD5zcdxwGz-6NHaes37Y8ubuzzfabR7uVpILsbZSuF8bBHdvrlT_fmX6Pez0QV4_EwBkEStnqOc8rQrtNuMc-o4K6O8RJUeCe6D6X3t1RoZpknSFmBm7qmnNODrZtS1B-B2ZduK_6522y_2-Q8vsJB7M12vnw"
userinfo = keycloak_openid.userinfo(access_token) #(token["access_token"])


print(userinfo)


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
#     return a / b


# print(divide(4, 0))

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
#             email: "new_user3@email.com",
#             username: "new_user3@email.com",
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
# response = requests.post(
#     "https://dev.auth.idp.civicdatalab.in/graphql",
#     json={"query": query},
#     headers=headers,
# )

# response_json = json.loads(response.text)
# print(response_json)


# decorator for getting sys token
# import requests
# import json

# auth_url = "https://auth.idp.civicdatalab.in/users/get_sys_token"


# def get_sys_token(func):
#     def inner(*args, **kwargs):
#         print("getting system token")

#         headers = {}
#         response = requests.get(auth_url, headers=headers)
#         response_json = json.loads(response.text)
#         if response_json["success"] == False:
#             return {
#                 "Success": False,
#                 "error": response_json["error"],
#                 "error_description": response_json["error_description"],
#             }

#         kwargs["access_token"] = response_json["access_token"]
#         return func(*args, **kwargs)

#     return inner

# import pandas as pd

# df = pd.DataFrame(
#     {
#         "A": [1, 2, 3],
#         "B": ["a", "b", ""],
#         "C": pd.date_range("2016-01-01", freq="d", periods=3),
#     },
#     index=pd.Index(range(3), name="idx"),
# )
# print(pd.io.json.build_table_schema(df, version=False))
# import json
# import genson


# def parse_schema(schema_dict, parent, schema):

#     for key in schema_dict:
#         if key == "required":
#             continue
#         print(key)
#         if key == "items":
#             schema.append(
#                 {
#                     "key": parent,
#                     "format": "array",
#                     "description": "",
#                     "parent": "",
#                     "array_field": "items",
#                 }
#             )
#             parse_schema(schema_dict["items"], key, schema)
#             continue
#         if key == "type":
#             continue

#         if key == "properties":
#             schema.append(
#                 {
#                     "key": parent,
#                     "format": "json",
#                     "description": "",
#                     "parent": "",
#                     "array_field": "",
#                 }
#             )
#             parse_schema(schema_dict["properties"], parent, schema)
#             continue
#         if "type" in schema_dict[key] and schema_dict[key]["type"] not in [
#             "array",
#             "object",
#         ]:
#             schema.append(
#                 {
#                     "key": key,
#                     "format": "string",
#                     "description": "",
#                     "parent": parent,
#                     "array_field": "",
#                 }
#             )
#         else:
#             parse_schema(schema_dict[key], key, schema)

# def parse_schema(schema_dict, parent, schema, currentpath):
#     global count
#     for key in schema_dict:
#         if key == "required":
#             continue
#         # print(key)
#         if key == "items":
#             # print(count)
#             count = count + 1
#             # print(count)
#             schema.append(
#                 {
#                     "key": parent + str(count) if parent == "items" else parent,
#                     "format": "array",
#                     "description": "",
#                     "parent": "",
#                     "array_field": "items" + str(count),
#                     "path": currentpath + "." + parent + str(count) if parent == "items" else parent
#                 }
#             )
#             parse_schema(schema_dict["items"], key, schema, currentpath + "." + parent + str(count) if parent == "items" else parent)
#             continue
#         if key == "type":
#             continue

#         if key == "properties":
#             schema.append(
#                 {
#                     "key": parent + str(count) if parent == "items" else parent,
#                     "format": "json",
#                     "description": "",
#                     "parent": "",
#                     "array_field": "",
#                     "path": currentpath + "." + parent + str(count) if parent == "items" else parent
#                 }
#             )
#             parse_schema(schema_dict["properties"], parent, schema, currentpath + "." + parent + str(count) if parent == "items" else parent)
#             continue
#         if "type" in schema_dict[key] and schema_dict[key]["type"] not in [
#             "array",
#             "object",
#         ]:
#             schema.append(
#                 {
#                     "key": key,
#                     "format": "string",
#                     "description": "",
#                     "parent": parent + str(count) if parent == "items" else parent,
#                     "array_field": "",
#                     "path": currentpath + "." + key
#                 }
#             )
#         else:
#             parse_schema(schema_dict[key], key, schema, currentpath + "." + parent + "." + key )


# def abc():
#     builder = genson.SchemaBuilder()
#     jsondata = [{"people": [{"first_name": "a", "last_name": {"l1": 1, "l2":2}}]}]
#     # jsondata = {"people": {"first_name": "a", "last_name": "b"}}
#     # jsondata = {}
#     builder.add_object(jsondata)
#     schema_dict = builder.to_schema()
#     global count
#     count = 0
#     currentpath = "."

#     print(schema_dict)
#     schema = []
#     parse_schema(schema_dict.get("properties", schema_dict.get("items", {}).get("properties", {})), "", schema, currentpath)
#     print('-------------', schema)


# abc()


# a = [{"name": "a", "type": "integer"}]
# b = {}
# for each in a:
#     b[each["name"]] = {"type": each["type"]}

# print(b)


# def remove_a_key(d, remove_key):

#     for key in list(d.keys()):
#         if key not in remove_key:
#             del d[key]
#         else:
#             skip_col(d[key], remove_key)


# def skip_col(d, remove_key):
#     if isinstance(d, dict):
#         remove_a_key(d, remove_key)
#     if isinstance(d, list):
#         for each in d:
#             if isinstance(each, dict):
#                 remove_a_key(each, remove_key)

#     return d


# def abcd():
#     # data = {"a": {"b": [1, 2, 3], "c": {"b": 1, "c2": 2}, "d": 2}}
#     data = [
#     {"b": [1, 2, 3], "c": {"b": 1, "c2": 2}, "d": 2},
#     {"b": [1, 2, 3], "c": {"b": 1, "c2": 2}, "d": 2},
# ]
#     res = skip_col(data, ["a", "c", "c2"])

#     print(res)


# abcd()


# import requests
# import json


# query = f"""
#         {{
#         data_request(data_request_id: "03d376a1-82ac-4dff-b441-0546e7842da8") {{
#             id
#             status
#             resource {{
#                 id
#                 schema_exists
#             }}
#             parameters
#         }}
#     }}
#     """


# headers = {}
# response = requests.post('https://idpbe.civicdatalab.in/graphql', json = {"query": query},  headers=headers)

# response_json = json.loads(response.text)
# print(response_json)
# import pandas as pd

# data = { 
#   "name": ["Sally", "Mary", "John"],
#   "age": [50, 40, 30]
# }

# df = pd.DataFrame(data)
# schema_list = pd.io.json.build_table_schema(df, version=False)
# schema_list = schema_list.get("fields", [])
# print(schema_list)
# for each in schema_list[1:]:
#     print (each)
# print (df)
# df.to_csv('t1.csv', index=False)
# df1 = df[(df['age']>35) &  (df['name']=="Sally")]
# print (df1)
# print(df.query('age > 35 and name == "Sally"'))