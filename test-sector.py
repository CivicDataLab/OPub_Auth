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


for each in datajson["sectors"]:
    try:
        query = f"""
                mutation {{
                    create_sector(
                    sector_data: {{name:"{each}", description:"{each}"}},
                ) {{
                    success,
                    errors
                }}
        }}"""

        headers = {}
        response = requests.post(
            "https://dev.backend.idp.civicdatalab.in/graphql",
            json={"query": query},
            headers=headers,
        )

        response_json = json.loads(response.text)
        print(response_json)

    except Exception as e:
        print(e)
