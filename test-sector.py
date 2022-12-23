datajson = {
    "sectors": [
        "Health And Family Welfare",
        "Agriculture",
        "Census And Surveys",
        "Water And Sanitation",
        "Statistics",
        "Education",
        "Home Affairs And Enforcement",
        "Water Resources",
        "Transport",
        "Finance",
        "Governance And Administration",
        "Animal Husbandry",
        "Economy",
        "Environment And Forest",
        "Power And Energy",
        "Industries",
        "Food",
        "Infrastructure",
        "Travel And Tourism",
        "Parliament Of India",
        "Labour And Employment",
        "Commerce",
        "Information And Communications",
        "Art And Culture",
        "Rural",
        "Science And Technology",
        "Urban",
        "Youth And Sports",
        "Social Development",
        "Mining",
        "Information And Broadcasting",
        "Biotechnology",
        "Defence",
        "Housing",
        "Judiciary",
        "Foreign Affairs",
    ]
}
import requests
import json


# query = f"""
#         mutation {{
#             create_sector(
#             sector_data: {{name:"Finance1", description:"Finance1"}},
#         ) {{
#             success,
#             errors
#         }}
# }}"""

# headers = {}
# response = requests.post(
#     "https://dev.backend.idp.civicdatalab.in/graphql",
#     json={"query": query},
#     headers=headers,
# )

# response_json = json.loads(response.text)
# print(response_json)


for index,each in enumerate(datajson["sectors"]):
    
    try:
        query = f"""
                mutation {{
                    update_sector(
                    sector_data: {{name:"{each}", official_id:"{index}"}},
                ) {{
                    success,
                    errors
                }}
        }}"""

        headers = {}
        response = requests.post(
            "https://idpbe.civicdatalab.in/graphql",
            json={"query": query},
            headers=headers,
        )

        response_json = json.loads(response.text)
        print(response_json, index)

    except Exception as update_e:
        print('--------error', update_e)
       
    if  "errors" in response_json:   
        try:
            query = f"""
                    mutation {{
                        create_sector(
                        sector_data: {{name:"{each}", description:"{each}", official_id:"{index}"}},
                    ) {{
                        success,
                        errors
                    }}
            }}"""

            headers = {}
            response = requests.post(
                "https://idpbe.civicdatalab.in/graphql",
                json={"query": query},
                headers=headers,
            )

            response_json = json.loads(response.text)
            print(response_json)

        except Exception as create_e:
            print('--------error', create_e)
