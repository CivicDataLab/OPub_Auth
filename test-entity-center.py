import requests
import json


dgov_min_url = "https://data.gov.in/backend/dms/v1/ogdp/api/hierarchical/ministry_department"
dgov_state_url = "https://data.gov.in/backend/dms/v1/ogdp/api/hierarchical/state_department"
dgov_sector_url = "https://data.gov.in/backend/dms/v1/ogdp/api/hierarchical/sector"

headers = {"Authorization": "Bearer 42d65c201641942b755f8fafb4a1d850d6367d22e95fac2ae913b7597d81c9efe52c29909eee3a7a7773090560c7923064e1fc3ae2a016d954cc9b0a178dcbc6"}

resp = requests.get(dgov_min_url, headers=headers)
min_data = resp.json()
min_data = min_data["data"]

print ('---data', min_data)


def iterate_data(data, parent_key, idp_parent_id):
    for key in list(data.keys()):
        
        try:
            
            if data[key]["parent"] == "0":
                idp_parent_id = create_org(data[key]["key"], data[key]["key"], "India", "CENTRAL_GOVERNMENT", "MINISTRY", idp_parent_id)
            
            if data[key]["parent"] != "0" and parent_key == "0":
                idp_parent_id = create_org(data[key]["key"], data[key]["key"], "India", "CENTRAL_GOVERNMENT", "DEPARTMENT", idp_parent_id)
                
            if data[key]["parent"] != "0" and parent_key != "0":
                idp_parent_id = create_org(data[key]["key"], data[key]["key"], "India", "CENTRAL_GOVERNMENT", "ORGANISATION", idp_parent_id)           
                
            if "child" in data[key]:
                iterate_data(data[key]["child"], data[key]["parent"], idp_parent_id)
                
        except Exception as e:
            print (e) 



def create_org(title, desc, state, type, sub_type, parent_id):
             
    query = f"""
            mutation {{
                create_organization(
                organization_data:  {{title:"{title}", 
                                    description:"{desc}",
                                    state:"{state}",
                                    organization_types:{type},
                                    gov_sub_type:{sub_type},
                                    parent_id:"{parent_id}",
                                    homepage:"",
                                    sample_data_url:""
                                    }},
            ) {{
                success,
                errors,
                organization {{
                    id
                }}
            }}
    }}"""

    headers = {"Authorization": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJCdXFLSkxZRUo0azdxc2M3RHItRjRZYlY0YWVsTzNMUnEtaDZWR3ZZR0ZNIn0.eyJleHAiOjE2NzgwNzA5MDgsImlhdCI6MTY3NzYzODkwOCwianRpIjoiN2RiOWEwMTQtYmVhYy00N2FhLWJhZmItYTUxMGRhOGIzYzRmIiwiaXNzIjoiaHR0cHM6Ly9kZXYua2MuaWRwLmNpdmljZGF0YWxhYi5pbi9hdXRoL3JlYWxtcy9leHRlcm5hbCIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiJhNzNhMmU4ZS1kNzY5LTQwOTgtYjcwMS1hZjIwMzdjOThmOWQiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJvcHViLWlkcCIsInNlc3Npb25fc3RhdGUiOiI5ZDdlZGYwNS1mMDAzLTRkZjAtOTc5Ny02Nzg0MDdjY2I4NzQiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwiZGVmYXVsdC1yb2xlcy1leHRlcm5hbCIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJwcm9maWxlIGVtYWlsIiwic2lkIjoiOWQ3ZWRmMDUtZjAwMy00ZGYwLTk3OTctNjc4NDA3Y2NiODc0IiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5hbWUiOiJBYmhpbmF2IiwicHJlZmVycmVkX3VzZXJuYW1lIjoiYWJoaW5hdiIsImdpdmVuX25hbWUiOiJBYmhpbmF2IiwiZW1haWwiOiJhYmhpbmF2QGNpdmljZGF0YWxhYi5pbiJ9.ffFZH5EtLPlnkAGKYpUFY0un6T_o2cmetVv5ODn7S-Cyk6usHU48AG3oD5-ZeZunxYEIzr-J1XZkoeJ-pTY7TnLe7EjQhMT1tyEBPvKlsJ3qYD940JszMQ9H2UwAcBzF5_NtJdk1kP8rQ2P8i8squYqn8WPaaWxaNIHMh7zR8kZOpjXipVoS0u0O5wL4rQ1CbRDozPdXFia4VqedHPudyJ7kQEf0npfBzpvhNeYWOtlh4Gfyg1C-qFORuA-NMhsD7n_g7F8WCHUCyKnsa4gtwbaWy04dHY4Ru07kzSDT8vZ7pVyxboPwUBGIFFoaIibb5HWNJl1X1GdxNPLlV5qRDQ"}
    response = requests.post(
        "https://dev.backend.idp.civicdatalab.in/graphql",
        json={"query": query},
        headers=headers,
    )

    response_json = json.loads(response.text)
    print(response_json) 
    return response_json["data"]["create_organization"]["organization"]["id"]
    
iterate_data(min_data, 0, "")   



