import json
import requests
import random
import string
from string import Template
from tkinter import *
import os

# Define the headers (including your Meraki API key)
headers = {
    "Content-Type": "application/json",
    "X-Cisco-Meraki-API-Key": os.environ.get('Meraki_API_Key')
}

headers_SSID = {
    "Content-Type": "application/json",
    "X-Cisco-Meraki-API-Key": os.environ.get('Meraki_API_Key'),
    "number": "0"
}


def skip():
    window.destroy()
    exit

def next_Organization():
    
    
    #Load the JSON payload for creating a new organization from a file
    with open("create_org_payload.json", "r") as f:
        org_payload_template = f.read()

    #fill in the variables using string template 
    org_payload = Template(org_payload_template).substitute(
        org_name=org_Name.get()
        )
    
    #Convert the payload to JSON format
    json_payload = json.loads(org_payload)
    

    #Send the POST request to create the new organization
    response = requests.post(
        "https://api.meraki.com/api/v1/organizations",
        data=json.dumps(json_payload),
        headers=headers
    )

    # Check the response status code
    if response.status_code == 201:
        print(f"Organization '{org_Name.get()}' created successfully!")
    else:
        print(f"Error creating organization: {response.text}")
        exit()

    #Get organization ID
    organizations = requests.get(
            "https://api.meraki.com/api/v1/organizations",
            headers=headers
            )
    if organizations.status_code >= 200 and organizations.status_code < 300:
        for org in organizations.json():
            if org.get('name') == org_Name.get():
                org_id = org.get('id')
    # print(org_id)

    window.destroy()

def next_Network():
    
    #make appliance network
    #Load the JSON payload for creating a new network from a file
    with open("create_network_payload.json", "r") as f:
        network_payload_template = f.read()

    #fill in the variables using string template
    network_payload = Template(network_payload_template).substitute(
        network_Name = "appliance",
        type = "appliance",
        productTypes = "appliance",
        )
    
    #Convert the payload to JSON format
    network_json_payload = json.loads(network_payload)

    response = requests.post(
    f"https://api.meraki.com/api/v1/organizations/{org_id}/networks",
    data=json.dumps(network_json_payload),
    headers=headers
    )

    if response.status_code == 201:
            data = json.loads(response.text)
            network_Id1 = data['id']
    else:
        print(f"Error adding network: {response.text}")
        exit()


    #make switch network
    #Load the JSON payload for creating a new network from a file
    with open("create_network_payload.json", "r") as f:
        network_payload_template = f.read()

    #fill in the variables using string template
    network_payload = Template(network_payload_template).substitute(
        network_Name = "switch",
        type = "switch",
        productTypes = "switch",
    )
    
    #Convert the payload to JSON format
    network_json_payload = json.loads(network_payload)

    response = requests.post(
    f"https://api.meraki.com/api/v1/organizations/{org_id}/networks",
    data=json.dumps(network_json_payload),
    headers=headers
    )

    if response.status_code == 201:
        data = json.loads(response.text)
        network_Id2 = data['id']
    else:
        print(f"Error adding network2: {response.text}")
        exit()

    #Make Wireless network
    #Load the JSON payload for creating a new network from a file
    with open("create_network_payload.json", "r") as f:
        network_payload_template = f.read()

    #fill in the variables using string template
    network_payload = Template(network_payload_template).substitute(
        network_Name = "wireless",
        type = "wireless",
        productTypes = "wireless",
        )
    
    #Convert the payload to JSON format
    network_json_payload = json.loads(network_payload)

    response = requests.post(
    f"https://api.meraki.com/api/v1/organizations/{org_id}/networks",
    data=json.dumps(network_json_payload),
    headers=headers
    )

    if response.status_code == 201:
            data = json.loads(response.text)
            network_Id3 = data['id']
    else:
        print(f"Error adding network: {response.text}")
        exit()
    
    #combine the two created networks
    #Load the JSON payload for combining networks from a file
    with open("combine_networks_payload.json", "r") as f:
        combine_network_payload_template = f.read()

    #fill in the variables using string template
    combine_network_payload = Template(combine_network_payload_template).substitute(
        network_Name = network_Name.get(),
        network_Id1 = network_Id1,
        network_Id2 = network_Id2,
        network_Id3 = network_Id3,
        )
    
    
    #Convert the payload to JSON format
    combine_network_json_payload = json.loads(combine_network_payload)

    response = requests.post(
    f"https://api.meraki.com/api/v1/organizations/{org_id}/networks/combine",
    data=json.dumps(combine_network_json_payload),
    headers=headers
    )
    if response.status_code:
        data = json.loads(response.text)
        network_id = data['id']
    print(f"Network'{network_Name.get}' created succesfully!")

    window.destroy()

def next_SSID():
    #Load the JSON payload for combining networks from a file
    with open("create_SSID_payload.json", "r") as f:
        create_SSID_payload_template = f.read()

    #fill in the variables using string template
    create_SSID_payload = Template(create_SSID_payload_template).substitute(
        SSID_Name = SSID_Name.get()
        )
    
    
    #Convert the payload to JSON format
    create_SSID_json_payload = json.loads(create_SSID_payload)

    response = requests.post(
    f"https://api.meraki.com/api/v1/organizations/{org_id}/",
    data=json.dumps(create_SSID_json_payload),
    headers=headers_SSID
    )

    if response.status_code == 201:
        print(f"SSID'{SSID_Name.get()}' created succesfully!")
    else:
        print(f"Error creating SSID: {response.text}")
        exit()

    window.destroy() 

def next_Switch():

#     #Load the JSON payload for creating a new switch from a file
#     with open("create_switch_payload.json", "r") as f:
#         switch_payload_template = f.read()

#     #fill in the variables using string template 
#     switch_payload = Template(switch_payload_template).substitute(
    
#         switch_Name = switch_Name.get(),
#         switch_IP = switch_IP.get(),
#         switch_Subnet = switch_Subnet.get(),
#         switch_Gateway = switch_Gateway.get(),
#         switch_Vlan = switch_Vlan.get(),

#         )
    
#     #Convert the payload to JSON format
#     switch_json_payload = json.loads(switch_payload)
    

#     #Send the POST request to create the new switch
#     response = requests.post(
#         f"https://api.meraki.com/api/v1/organizations/{org_id}/networks",
#         data=json.dumps(switch_json_payload),
#         headers=headers
#         )

#     # Check the response status code
#     if response.status_code == 201:
#         print(f"Organization '{org_Name.get()}' created successfully!")
#     else:
#         print(f"Error creating organization: {response.text}")
#         exit()

#     window.destroy()
    exit

def next_devices():
    
    #Load the JSON payload for creating a new client VPN from a file
    with open("claim_devices_payload.json", "r") as f:
        devices_payload_template = f.read()

    #fill in the variables using string template
    devices_payload = Template(devices_payload_template).substitute(
        serial1 = switch_serial.get(),
        serial2 = router_serial.get(),
        serial3 = AP_serial.get(),
        )
    
    #Convert the payload to JSON format
    devices_json_payload = json.loads(devices_payload)

    #Send the POST request to create the new client VPN
    response = requests.post(
        f"https://api.meraki.com/api/v1/networks/{network_id}/devices/claim",
        data=json.dumps(devices_json_payload),
        headers=headers
        )
    
    if response.status_code == 201:
        print("Devices added successfully!")
    else:
        print(f"Error adding devices: {response.text}")
        exit()

def yes_FW_Rules():
    #Load the JSON payload for adding firewall rules from a file
    with open("create_firewall_rules_payload.json", "r") as f:
        FW_Rules_payload = f.read()

    #Convert the payload to JSON format
    json_payload = json.loads(FW_Rules_payload)
    

    #Send the POST request to create the new rules
    response = requests.put(
        "https://api.meraki.com/api/v1/networks/{network_id}/l3FirewallRules",
        data=json.dumps(FW_Rules_payload),
        headers=headers
    )

    # Check the response status code
    if response.status_code == 201:
        print("Firewall rules added successfully!")
    else:
        print(f"Error adding firewall rules: {response.text}")
        exit()


org_id = ""
network_id = ""
org_Name = ""


#GUI window for the creation of an organization
window = Tk()
window.geometry('550x300')
window.title("Setup organization")

org_Name_lbl = Label(window, text="Fill in organization name")
org_Name_lbl.grid(column=0, row=1)
org_Name = Entry(window, width=50)
org_Name.grid(column=1, row=1)

next_Btn = Button(window, text="next",command=next_Organization)
next_Btn.grid(column=3, row=2)
skip_Btn = Button(window,text="skip",command=skip)
skip_Btn.grid(column=2,row=2)

window.mainloop()

#GUI for the setup of a network
window = Tk()
window.geometry('550x300')
window.title("Setup Network")

network_Name_lbl = Label(window, text= "Network name: ")
network_Name_lbl.grid(column=0,row=1)
network_Name = Entry(window, width=50)
network_Name.grid(column=1, row=1)

next_Btn = Button(window, text="next",command=next_Network)
next_Btn.grid(column=3, row=2)
skip_Btn = Button(window, text="skip",command=skip)
skip_Btn.grid(column=2, row=2)

window.mainloop()

#add switch, router and firewall to the organisation
window = Tk()
window.geometry('500x300')
window.title("Add devices")

switch_Serial_lbl = Label(window, text="Switch Serial Number:")
switch_Serial_lbl.grid(column=0, row=0)
switch_serial = Entry(window, width=50)
switch_serial.grid(column=1, row=0)

router_Serial_lbl = Label(window, text="Router Serial Number:")
router_Serial_lbl.grid(column=0, row=1)
router_serial = Entry(window, width=50)
router_serial.grid(column=1, row=1)

AP_Serial_lbl = Label(window, text="firewall Serial Number:")
AP_Serial_lbl.grid(column=0, row=2)
AP_serial = Entry(window, width=50)
AP_serial.grid(column=1, row=2)

next_Btn = Button(window, text="next",command=next_devices)
next_Btn.grid(column=3, row=3)
skip_Btn = Button(window, text="skip",command=skip)
skip_Btn.grid(column=2, row=3)

window.mainloop()

#GUI for the creation of a new SSID

window = Tk()
window.geometry('500x300')
window.title("Add SSID")

SSID_Name_lbl = Label(window, text="Switch Serial Number:")
SSID_Name_lbl.grid(column=0, row=0)
SSID_Name = Entry(window, width=50)
SSID_Name.grid(column=1, row=0)

next_Btn = Button(window, text="next",command=next_SSID)
next_Btn.grid(column=3, row=1)
skip_Btn = Button(window, text="skip",command=skip)
skip_Btn.grid(column=2, row=1)
window.mainloop()

# Add Firewall rules
window = Tk()
window.geometry('500x300')
window.title("Add SSID")

firewall_rules_lbl = Label(window, text="Add Firewall rules?")
firewall_rules_lbl.grid(column=0, row=0)

yes_Btn = Button(window, text="yes",command=yes_FW_Rules)
yes_Btn.grid(column=1, row=0)
no_Btn = Button(window, text="no", command=skip)

window.mainloop()

# #GUI for the setup for a switch
# window = Tk()
# window.geometry('500x300')
# window.title("Setup switch")

# switch_Name_lbl = Label(window, text="switch name:")
# switch_Name_lbl.grid(column=0, row=0)
# switch_Name = Entry(window, width=50)
# switch_Name.grid(column=1, row=0)

# switch_IP_lbl = Label(window, text="switch IP:")
# switch_IP_lbl.grid(column=0, row=1)
# switch_IP = Entry(window, width=50)
# switch_IP.grid(column=1, row=1)

# switch_Subnet_lbl = Label(window, text="switch subnet:")
# switch_Subnet_lbl.grid(column=0, row=2)
# switch_Subnet = Entry(window, width=50)
# switch_Subnet.grid(column=1, row=2)

# switch_Gateway_lbl = Label(window, text="default gateway:")
# switch_Gateway_lbl.grid(column=0, row=3)
# switch_Gateway = Entry(window, width=50)
# switch_Gateway.grid(column=1, row=3)

# switch_Vlan_lbl = Label(window, text="Switch VLAN:")
# switch_Vlan_lbl.grid(column=0, row=4)
# switch_Vlan = Entry(window, width=50)
# switch_Vlan.grid(column=1, row=4)

# next_Btn = Button(window, text="next",command=next_Switch)
# next_Btn.grid(column=3, row=5)
# skip_Btn = Button(window, text="skip",command=skip)
# skip_Btn.grid(column=2, row=5)

# window.mainloop()


#GUI for the setup of a client VPN
window = Tk()
window.geometry('500x300')
window.title("Setup Client VPN")

VPN_Name_lbl = Label(window, text="Client VPN Name:")
VPN_Name_lbl.grid(column=0, row=0)
VPN_Name = Entry(window, width=50)
VPN_Name.grid(column=1, row=0)

private_Subnets_lbl = Label(window, text="Private subnets (ip/xx):")
private_Subnets_lbl.grid(column=0, row=1)
private_Subnets = Entry(window, width=50)
private_Subnets.grid(column=1, row=1)

public_IP_lbl = Label(window, text="Public IP:")
public_IP_lbl.grid(column=0, row=4)
public_IP = Entry(window, width=50)
public_IP.grid(column=1, row=4)

vpn_secret = "".join(random.choices(string.ascii_letters + string.digits, k=16))

next_Btn = Button(window, text="next",command=next)
next_Btn.grid(column=3, row=20)
skip_Btn = Button(window, text="skip",command=skip)
skip_Btn.grid(column=2, row=20)

window.mainloop()