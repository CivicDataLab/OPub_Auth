import requests
import pandas as pd
# resp = requests.get("https://data.gov.in/backend/dmspublic/v1/resources?offset=0&limit=10&sort[published_date]=desc&filters[sector]=Agriculture", verify=False)
# # data = resp.text
# data = resp.json()

# print (type(data))

# temp = pd.json_normalize(data, max_level=2)
# # print(temp.columns)
# list_cols = []
# all_cols = []
# for v in list(temp.columns):
#     if '.' in v:
#         all_cols.append(v.split('.'))
#     else:
#         all_cols.append(v)
#     keys = v.split('.')
#     rv = data
#     for key in keys:
#         rv = rv[key]
#     # print(rv)
#     if type(rv) == list:
#         list_cols.append(v)
# df = data
# for col_path in list_cols:
#     meta = all_cols.copy()
#     if '.' in col_path:
#         path_list = col_path.split('.')
#         meta.remove(path_list)
#     else:
#         meta.remove(col_path)
    
#     df = pd.json_normalize(df, record_path=col_path.split('.'), meta=meta)
# # df = pd.json_normalize(data, record_path=['data','rows'], meta=['version', 'total', ['data', 'aggregations']])
# # df = pd.read_json(data, orient='records')
# # df['main_col'] = df.index
# # df = df.reset_index(drop=True)
# # d1 = df.to_dict(orient='records')
# # d2 = pd.json_normalize(d1)
# # df = df.explode(list(df.columns))

# print (df)

# email_url = "https://mailer.idp.civicdatalab.in/send-email/backgroundtasks"
# body = {
#     "actor": "abhinav",
#     "action": "Approved",
#     "tgt_obj": 1,
#     "tgt_group": "Dataset",
#     "extras": {"tgt_org": 20},
# }
# headers = {}
# response = requests.request("POST", email_url, json=body, headers=headers)
# response_json = response.text
# print(response_json)

data = pd.read_csv("/home/abhinav/data/output.csv")
old_cols =  (list(data.columns))

new_cols = [col.replace(": ", "_") if ":" in col else "sample" if col == "" else col for col in old_cols]
data.columns = new_cols

# print (new_cols, '--', data.columns)
data.at[0, 'id'] = "[1,2,3]"


data.drop(columns=data.columns[0], 
        axis=1, 
        inplace=True)
print (data)