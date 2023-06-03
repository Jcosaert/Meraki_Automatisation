import requests
import time
import os
# Define your base URL
base_url = "https://api.meraki.com/api/v1"

# Define the headers with your API key

headers = {
    "Content-Type": "application/json",
    "X-Cisco-Meraki-API-Key": os.environ.get('Meraki_API_Key')
}

# Get the list of organizations
organizations_url = f"{base_url}/organizations"
response = requests.get(organizations_url, headers=headers)
organizations = response.json()

# Iterate over each organization
for org in organizations:
    org_id = org["id"]
    org_name = org["name"]
    print(f"Organization: {org_name}")

    
    # Get the list of network IDs for the organization
    networks_url = f"{base_url}/organizations/{org_id}/networks"
    response = requests.get(networks_url, headers=headers)
    
    if response.status_code == 429: #getaround for the time-out rule
        time.sleep(int(response.headers["Retry-After"]))
        response = requests.get(networks_url, headers=headers)
        data = response.json() if response.ok else response.text
    else:
        data = response.json() if response.ok else response.text
    
    networks = response.json()


    # Iterate over each network
    
    for network in networks:
        network_id = network["id"]
        network_name = network["name"]
        print(f"\tNetwork: {network_name}")

        # Get the list of port forward rules for the network
        port_forwarding_url = f"{base_url}/networks/{network_id}/appliance/portForwardingRules"
        response = requests.get(port_forwarding_url, headers=headers)

        if response.status_code == 429: #getaround for the time-out rule
            time.sleep(int(response.headers["Retry-After"]))
            response = requests.get(networks_url, headers=headers)
            data = response.json() if response.ok else response.text
        else:
            data = response.json() if response.ok else response.text

        port_forwarding_rules = response.json()

        # Iterate over each port forward rule and print the details
        for rule in port_forwarding_rules:
            rule_name = rule["name"]
            protocol = rule["protocol"]
            public_port = rule["publicPort"]
            local_ip = rule["localIp"]
            local_port = rule["localPort"]
            print(f"\t\tRule: {rule_name}")
            print(f"\t\tProtocol: {protocol}")
            print(f"\t\tPublic Port: {public_port}")
            print(f"\t\tLocal IP: {local_ip}")
            print(f"\t\tLocal Port: {local_port}")
            print()

    print()