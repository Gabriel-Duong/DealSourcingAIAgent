import requests
import json


# Replace with your own
DECILE_API_URL = "https://expara.decilehub.com/api/v1"
DECILE_TOKEN = "4ZW8M6LEvTQ8peVqFU9StLdo"

def fetch_organization(org_id: int):
    url = f"{DECILE_API_URL}/organizations/{org_id}"
    headers = {"Authorization": f"Bearer {DECILE_TOKEN}"}
    resp = requests.get(url, headers=headers)

    # Stop if something went wrong
    resp.raise_for_status()

    data = resp.json()
    return data

if __name__ == "__main__":
    # Example: org_id from your database
    org_id = 805274
    org_data = fetch_organization(org_id)
    print(json.dumps(org_data, indent=2))

    # # Print out fields
    # print("Name:", org_data.get("name"))
    # print("Country:", org_data.get("country"))
    # print("Short description:", org_data.get("short_description"))
    # print("Notes:", org_data.get("notes"))
