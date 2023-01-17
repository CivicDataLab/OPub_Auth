datajson = {
    "states": [
        {"state": {"state_id": "AN", "state_name": "Andaman and Nicobar Island (UT)"}},
        {"state": {"state_id": "AP", "state_name": "Andhra Pradesh"}},
        {"state": {"state_id": "AR", "state_name": "Arunachal Pradesh"}},
        {"state": {"state_id": "AS", "state_name": "Assam"}},
        {"state": {"state_id": "BR", "state_name": "Bihar"}},
        {"state": {"state_id": "CH", "state_name": "Chandigarh (UT)"}},
        {"state": {"state_id": "CG", "state_name": "Chhattisgarh"}},
        {"state": {"state_id": "DN", "state_name": "Dadra and Nagar Haveli (UT)"}},
        {"state": {"state_id": "DD", "state_name": "Daman and Diu (UT)"}},
        {"state": {"state_id": "DL", "state_name": "Delhi (NCT)"}},
        {"state": {"state_id": "GA", "state_name": "Goa"}},
        {"state": {"state_id": "GJ", "state_name": "Gujarat"}},
        {"state": {"state_id": "HR", "state_name": "Haryana"}},
        {"state": {"state_id": "HP", "state_name": "Himachal Pradesh"}},
        {"state": {"state_id": "JK", "state_name": "Jammu and Kashmir (UT)"}},
        {"state": {"state_id": "JH", "state_name": "Jharkhand"}},
        {"state": {"state_id": "KA", "state_name": "Karnataka"}},
        {"state": {"state_id": "KL", "state_name": "Kerala"}},
        {"state": {"state_id": "LK", "state_name": "Ladakh(UT)"}},
        {"state": {"state_id": "LD", "state_name": "Lakshadweep (UT)"}},
        {"state": {"state_id": "MP", "state_name": "Madhya Pradesh"}},
        {"state": {"state_id": "MH", "state_name": "Maharashtra"}},
        {"state": {"state_id": "MN", "state_name": "Manipur"}},
        {"state": {"state_id": "ML", "state_name": "Meghalaya"}},
        {"state": {"state_id": "MZ", "state_name": "Mizoram"}},
        {"state": {"state_id": "NL", "state_name": "Nagaland"}},
        {"state": {"state_id": "OR", "state_name": "Odisha"}},
        {"state": {"state_id": "PY", "state_name": "Puducherry (UT)"}},
        {"state": {"state_id": "PB", "state_name": "Punjab"}},
        {"state": {"state_id": "RJ", "state_name": "Rajasthan"}},
        {"state": {"state_id": "SK", "state_name": "Sikkim"}},
        {"state": {"state_id": "TN", "state_name": "Tamil Nadu"}},
        {"state": {"state_id": "TG", "state_name": "Telangana"}},
        {"state": {"state_id": "TR", "state_name": "Tripura"}},
        {"state": {"state_id": "UK", "state_name": "Uttarakhand"}},
        {"state": {"state_id": "UP", "state_name": "Uttar Pradesh"}},
        {"state": {"state_id": "WB", "state_name": "West Bengal"}},
    ]
}
import requests
import json

for each in datajson["states"]:
    try:
        query = f"""
                mutation {{
                    update_geography(
                    geography_data: {{name:"{each["state"]["state_name"]}", official_id:"{each["state"]["state_id"]}"}},
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
        
        if  "errors" in response_json:
            
            query = f"""
                    mutation {{
                        create_geography(
                        geography_data: {{name:"{each["state"]["state_name"]}", official_id:"{each["state"]["state_id"]}"}},
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

        district = each["state"]["state_id"]
        district_url = f"http://vocab.nic.in/rest.php/district/{district.lower()}/json"
        print(district_url)

        # resp = requests.get("http://vocab.nic.in/rest.php/district/tn/json")
        resp = requests.get(district_url)
        dist_data = resp.json()

        for dist in dist_data["districts"]:
            query = f"""
                    mutation {{
                        update_geography(
                        geography_data: {{name:"{dist["district"]["district_name"]}", official_id:"{dist["district"]["district_id"]}"}},
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
            
            if  "errors" in response_json:
                
                query = f"""
                        mutation {{
                            create_geography(
                            geography_data:  {{name:"{dist["district"]["district_name"]}", official_id:"{dist["district"]["district_id"]}"}},
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
    except Exception as e:
        print(e)
