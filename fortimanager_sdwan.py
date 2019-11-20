#!/usr/bin/env python3

import requests, json

from urllib3.exceptions import InsecureRequestWarning
from time import sleep
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

user = "admin"
passwd = "fortinet"
url = "https://34.77.13.219:10419/jsonrpc"
adom = "root"

def is_task_finished(id):

    print(" Checking task: " + str(id) + " for completion.")

    payload = {
        "session": session,
        "id": 1,
        "method": "get",
        "params": [
            {
                "url": "/task/task/" + str(id)
            }
        ]
    }

    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)

    if not is_request_status_ok(response):
        print(" Error in request.")
        print(response.text)
        exit(-1)

    try:
        content = json.loads(response.content)
        line = content["result"][0]["data"]["line"]

        for l in line:
            if l["percent"] != 100:
                return False
    except:
        content = json.loads(response.content)
        if content["result"][0]["data"]["percent"] != 100:
            return False

    return True


def is_request_status_ok(response):
    content = json.loads(response.content)

    return response.status_code == 200 and \
        content["result"][0]["status"]["code"] == 0 and \
        content["result"][0]["status"]["message"] == "OK"
    


def run_request(num_id, payload):
    print("Running request " + str(num_id) + ".")

    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)

    if not is_request_status_ok(response):
        print(" Error in request.")
        print(response.text)
        exit(-1)

    content = json.loads(response.content)

    print (" Request completed")

def run_request_async(num_id, payload):
    print("Running request " + str(num_id) + ".")

    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)

    if not is_request_status_ok(response):
        print(" Error in request.")
        print(response.text)
        exit(-1)

    content = json.loads(response.content)
    try: 
        task_id = content["result"][0]["data"]["taskid"]
    except:
        task_id = content["result"][0]["data"]["task"]

    print(" Asynchronous task created: " + str(task_id))
    while not is_task_finished(task_id):
        sleep(1)

    print (" Request completed")


##############################################################
# Login
##############################################################

print("Running Login request")
payload = {
	"session" : 1,
	"id" : 1,
	"method" : "exec",
	"params" : [
		{
			"url" : "sys/login/user",
			"data" : [
				{
					"user" : user,
					"passwd" : passwd
				}
			]
		}
	]
}

headers = {
    'Content-Type': "application/json",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Host': "34.77.13.219:10419",
    'Accept-Encoding': "gzip, deflate",
    'Content-Length': "200",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

response = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)

if not is_request_status_ok(response):
    print(" Error in request.")
    print(response.text)
    exit(-1)

content = json.loads(response.content)
session = content["session"]
print(" Request completed. Session Id = " + session)

##############################################################
# 1
##############################################################
print("Running request 1.")

payload = {
    "session": session,
    "id": 1,
    "method": "exec",
    "params": [
        {
            "url": "/dvm/cmd/discover/device",
            "data": {
                "device": {
                    "adm_pass": passwd,
                    "adm_usr": user,
                    "ip": "192.168.0.1"
                }
            }
        }
    ]
}

headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
    }

response = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)

if not is_request_status_ok(response):
    print(" Error in request.")
    print(response.text)
    exit(-1)

content = json.loads(response.content)
sn_fgt_1 = content["result"][0]["data"]["device"]["sn"]

print (" Request completed. SN: " + str(sn_fgt_1))

##############################################################
# 2
##############################################################
print("Running request 2.")

payload = {
    "session": session,
    "id": 1,
    "method": "exec",
    "params": [
        {
            "url": "/dvm/cmd/discover/device",
            "data": {
                "device": {
                    "adm_pass": passwd,
                    "adm_usr": user,
                    "ip": "192.168.0.12"
                }
            }
        }
    ]
}

headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
    }

response = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)

if not is_request_status_ok(response):
    print(" Error in request.")
    print(response.text)
    exit(-1)

content = json.loads(response.content)
sn_fgt_2 = content["result"][0]["data"]["device"]["sn"]

print (" Request completed. SN: " + str(sn_fgt_2))

##############################################################
# 3
##############################################################
print("Running request 3.")

payload = {
    "session": session,
    "id": 1,
    "method": "exec",
    "params": [
        {
            "url": "/dvm/cmd/discover/device",
            "data": {
                "device": {
                    "adm_pass": passwd,
                    "adm_usr": user,
                    "ip": "192.168.0.5"
                }
            }
        }
    ]
}

headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
    }

response = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)

if not is_request_status_ok(response):
    print(" Error in request.")
    print(response.text)
    exit(-1)

content = json.loads(response.content)
sn_fgt_dc = content["result"][0]["data"]["device"]["sn"]

print (" Request completed. SN: " + str(sn_fgt_dc))

##############################################################
# 4
##############################################################
print("Running request 4.")

payload = {
    "session": session,
    "id": 1,
    "method": "exec",
    "params": [
        {
            "url": "/dvm/cmd/add/dev-list",
            "data": {
                "adom": adom,
                "flags": ["create_task", "nonblocking"],
                "add-dev-list": [
                    {
                        "adm_pass": passwd,
                        "adm_usr": user,
                        "ip": "192.168.0.1",
                        "name": "FGT-1",
                        "sn": sn_fgt_1,
                        "mgmt_mode": "fmgfaz",
                        "flags": 24
                    },
                    {
                        "adm_pass": passwd,
                        "adm_usr": user,
                        "ip": "192.168.0.12",
                        "name": "FGT-2",
                        "sn": sn_fgt_2,
                        "mgmt_mode": "fmgfaz",
                        "flags": 24
                    },
                    {
                        "adm_pass": passwd,
                        "adm_usr": user,
                        "ip": "192.168.0.5",
                        "name": "FGT-DC-5",
                        "sn": sn_fgt_dc,
                        "mgmt_mode": "fmgfaz",
                        "flags": 24
                    }
                ]
            }
        }
    ]
}
headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
}

response = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)

if not is_request_status_ok(response):
    print(" Error in request.")
    print(response.text)
    exit(-1)

content = json.loads(response.content)

task_id = content["result"][0]["data"]["taskid"]
print(" Asynchronous task created: " + str(task_id))
while not is_task_finished(task_id):
    sleep(1)

print (" Request completed")


##############################################################
# 5
##############################################################
print("Running request 5.")

payload = {
    "session": session,
    "id": 1,
    "method": "set",
    "params": [
        {
            "url": "/pm/config/adom/" + adom + "/obj/dynamic/interface/",
            "data": [
                {
                    "dynamic_mapping": None,
                    "name": "port1",
                    "description": None,
                    "single-intf": 1,
                    "default-mapping": 1,
                    "defmap-intf": "port1",
                    "defmap-zonemember": [],
                    "defmap-intrazone-deny": 0,
                    "egress-shaping-profile": [],
                    "color": 0
                },
                {
                    "dynamic_mapping": None,
                    "name": "port4",
                    "description": None,
                    "single-intf": 1,
                    "default-mapping": 1,
                    "defmap-intf": "port4",
                    "defmap-zonemember": [],
                    "defmap-intrazone-deny": 0,
                    "egress-shaping-profile": [],
                    "color": 0
                },
                {
                    "dynamic_mapping": None,
                    "name": "port5",
                    "description": None,
                    "single-intf": 1,
                    "default-mapping": 1,
                    "defmap-intf": "port5",
                    "defmap-zonemember": [],
                    "defmap-intrazone-deny": 0,
                    "egress-shaping-profile": [],
                    "color": 0
                },
                {
                    "dynamic_mapping": None,
                    "name": "WirelessVLAN",
                    "description": None,
                    "single-intf": 1,
                    "default-mapping": 1,
                    "defmap-intf": "WirelessVLAN",
                    "defmap-zonemember": [],
                    "defmap-intrazone-deny": 0,
                    "egress-shaping-profile": [],
                    "color": 0
                },
                {
                    "dynamic_mapping": [
                        {
                            "_scope": [
                                {
                                    "name": "FGT-1",
                                    "vdom": "root"
                                }
                            ],
                            "egress-shaping-profile": [],
                            "intrazone-deny": 0,
                            "local-intf": [
                                "Clients-BR1"
                            ]
                        },
                        {
                            "_scope": [
                                {
                                    "name": "FGT-2",
                                    "vdom": "root"
                                }
                            ],
                            "egress-shaping-profile": [],
                            "intrazone-deny": 0,
                            "local-intf": [
                                "Clients-BR2"
                            ]
                        }
                    ],
                    "name": "Clients-BR",
                    "description": None,
                    "single-intf": 1,
                    "default-mapping": 0,
                    "defmap-intf": None,
                    "defmap-zonemember": [],
                    "defmap-intrazone-deny": 0,
                    "egress-shaping-profile": [],
                    "color": 0
                }
            ]
        }
    ]
}
headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
}

response = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)

if not is_request_status_ok(response):
    print(" Error in request.")
    print(response.text)
    exit(-1)

content = json.loads(response.content)

print (" Request completed")


##############################################################
# 6
##############################################################
print("Running request 6.")

payload = {
    "session": session,
    "id": 1,
    "method": "set",
    "params": [
        {
            "url": "/pm/config/adom/" + adom + "/obj/vpnmgr/vpntable",
            "data": [
                {
                    "name": "OL_INET",
                    "description": None,
                    "topology": 2,
                    "psk-auto-generate": "disable",
                    "psksecret": "!123fortinet123!",
                    "ike1keylifesec": 28800,
                    "ike1dpd": 1,
                    "ike1natkeepalive": 10,
                    "dpd-retrycount": 0,
                    "dpd-retryinterval": [],
                    "ike1localid": None,
                    "ike2keylifesec": 1800,
                    "ike2keylifekbs": 5120,
                    "ike2keepalive": 1,
                    "intf-mode": 0,
                    "fcc-enforcement": 0,
                    "ike-version": 2,
                    "negotiate-timeout": 30,
                    "inter-vdom": 0,
                    "certificate": [],
                    "auto-zone-policy": 0,
                    "vpn-zone": None,
                    "spoke2hub-zone": [],
                    "hub2spoke-zone": [],
                    "npu-offload": 1,
                    "authmethod": 1,
                    "ike1dhgroup": 12,
                    "dpd": 3,
                    "localid-type": 0,
                    "ike1mode": 1,
                    "ike1nattraversal": 1,
                    "ike1proposal": [
                        "aes128-sha256",
                        "aes256-sha256"
                    ],
                    "ike2autonego": 0,
                    "ike2dhgroup": 12,
                    "ike2keylifetype": 1,
                    "pfs": 1,
                    "ike2proposal": [
                        "aes128-sha256",
                        "aes256-sha256"
                    ],
                    "replay": 1
                },
                {
                    "name": "OL_MPLS",
                    "description": None,
                    "topology": 2,
                    "psk-auto-generate": "disable",
                    "psksecret": "!123fortinet123!",
                    "ike1keylifesec": 28800,
                    "ike1dpd": 1,
                    "ike1natkeepalive": 10,
                    "dpd-retrycount": 0,
                    "dpd-retryinterval": [],
                    "ike1localid": None,
                    "ike2keylifesec": 1800,
                    "ike2keylifekbs": 5120,
                    "ike2keepalive": 1,
                    "intf-mode": 0,
                    "fcc-enforcement": 0,
                    "ike-version": 2,
                    "negotiate-timeout": 30,
                    "inter-vdom": 0,
                    "certificate": [],
                    "auto-zone-policy": 0,
                    "vpn-zone": None,
                    "spoke2hub-zone": [],
                    "hub2spoke-zone": [],
                    "npu-offload": 1,
                    "authmethod": 1,
                    "ike1dhgroup": 12,
                    "dpd": 3,
                    "localid-type": 0,
                    "ike1mode": 1,
                    "ike1nattraversal": 1,
                    "ike1proposal": [
                        "aes128-sha256",
                        "aes256-sha256"
                    ],
                    "ike2autonego": 0,
                    "ike2dhgroup": 12,
                    "ike2keylifetype": 1,
                    "pfs": 1,
                    "ike2proposal": [
                        "aes128-sha256",
                        "aes256-sha256"
                    ],
                    "replay": 1
                }
            ]
        }
    ]
}

headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
}

response = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)

if not is_request_status_ok(response):
    print(" Error in request.")
    print(response.text)
    exit(-1)

content = json.loads(response.content)

print (" Request completed")

##############################################################
# 7
##############################################################
print("Running request 7.")

payload = {
    "session": session,
    "id": 1,
    "method": "set",
    "params": [
        {
            "url": "/pm/config/adom/" + adom + "/obj/vpnmgr/node",
            "data": [
                {
                    "ip-range": None,
                    "ipv4-exclude-range": None,
                    "protected_subnet": [
                        {
                            "addr": [
                                "all"
                            ]
                        }
                    ],
                    "summary_addr": None,
                    "id": 1,
                    "vpntable": [
                        "OL_INET"
                    ],
                    "role": 1,
                    "usrgrp": [],
                    "iface": [
                        "port1"
                    ],
                    "hub_iface": [],
                    "peer": [],
                    "automatic_routing": 0,
                    "extgw": None,
                    "extgwip": [],
                    "extgw_hubip": [],
                    "extgw_p2_per_net": 0,
                    "route-overlap": 0,
                    "vpn-zone": [],
                    "spoke-zone": [],
                    "vpn-interface-priority": 0,
                    "auto-configuration": 1,
                    "default-gateway": "0.0.0.0",
                    "dns-service": 5,
                    "dhcp-server": 1,
                    "ipsec-lease-hold": 60,
                    "add-route": 0,
                    "assign-ip": 0,
                    "assign-ip-from": 0,
                    "authpasswd": "!123fortinet123!",
                    "authusr": None,
                    "authusrgrp": [],
                    "banner": None,
                    "dns-mode": 1,
                    "domain": None,
                    "exchange-interface-ip": 0,
                    "ipv4-dns-server1": "0.0.0.0",
                    "ipv4-dns-server2": "0.0.0.0",
                    "ipv4-dns-server3": "0.0.0.0",
                    "ipv4-end-ip": "0.0.0.0",
                    "ipv4-netmask": "255.255.255.255",
                    "ipv4-split-include": [],
                    "ipv4-start-ip": "0.0.0.0",
                    "ipv4-wins-server1": "0.0.0.0",
                    "ipv4-wins-server2": "0.0.0.0",
                    "localid": None,
                    "mode-cfg": 0,
                    "mode-cfg-ip-version": 0,
                    "net-device": 0,
                    "peergrp": [],
                    "peerid": None,
                    "peertype": 8,
                    "tunnel-search": 1,
                    "unity-support": 1,
                    "xauthtype": 1,
                    "scope member": [
                        {
                            "name": "FGT-1",
                            "vdom": "root"
                        }
                    ]
                },
                {
                    "ip-range": None,
                    "ipv4-exclude-range": None,
                    "protected_subnet": [
                        {
                            "addr": [
                                "all"
                            ]
                        }
                    ],
                    "summary_addr": None,
                    "id": 2,
                    "vpntable": [
                        "OL_INET"
                    ],
                    "role": 1,
                    "usrgrp": [],
                    "iface": [
                        "port1"
                    ],
                    "hub_iface": [],
                    "peer": [],
                    "automatic_routing": 0,
                    "extgw": None,
                    "extgwip": [],
                    "extgw_hubip": [],
                    "extgw_p2_per_net": 0,
                    "route-overlap": 0,
                    "vpn-zone": [],
                    "spoke-zone": [],
                    "vpn-interface-priority": 0,
                    "auto-configuration": 1,
                    "default-gateway": "0.0.0.0",
                    "dns-service": 5,
                    "dhcp-server": 1,
                    "ipsec-lease-hold": 60,
                    "add-route": 0,
                    "assign-ip": 0,
                    "assign-ip-from": 0,
                    "authpasswd": "!123fortinet123!",
                    "authusr": None,
                    "authusrgrp": [],
                    "banner": None,
                    "dns-mode": 1,
                    "domain": None,
                    "exchange-interface-ip": 0,
                    "ipv4-dns-server1": "0.0.0.0",
                    "ipv4-dns-server2": "0.0.0.0",
                    "ipv4-dns-server3": "0.0.0.0",
                    "ipv4-end-ip": "0.0.0.0",
                    "ipv4-netmask": "255.255.255.255",
                    "ipv4-split-include": [],
                    "ipv4-start-ip": "0.0.0.0",
                    "ipv4-wins-server1": "0.0.0.0",
                    "ipv4-wins-server2": "0.0.0.0",
                    "localid": None,
                    "mode-cfg": 0,
                    "mode-cfg-ip-version": 0,
                    "net-device": 0,
                    "peergrp": [],
                    "peerid": None,
                    "peertype": 8,
                    "tunnel-search": 1,
                    "unity-support": 1,
                    "xauthtype": 1,
                    "scope member": [
                        {
                            "name": "FGT-2",
                            "vdom": "root"
                        }
                    ]
                },
                {
                    "ip-range": None,
                    "ipv4-exclude-range": None,
                    "protected_subnet": [
                        {
                            "addr": [
                                "all"
                            ]
                        }
                    ],
                    "summary_addr": None,
                    "id": 3,
                    "vpntable": [
                        "OL_INET"
                    ],
                    "role": 0,
                    "usrgrp": [],
                    "iface": [
                        "port1"
                    ],
                    "hub_iface": [],
                    "peer": [],
                    "automatic_routing": 0,
                    "extgw": None,
                    "extgwip": [],
                    "extgw_hubip": [],
                    "extgw_p2_per_net": 0,
                    "route-overlap": 0,
                    "vpn-zone": [],
                    "spoke-zone": [],
                    "vpn-interface-priority": 0,
                    "auto-configuration": 0,
                    "default-gateway": "0.0.0.0",
                    "dns-service": 5,
                    "dhcp-server": 0,
                    "ipsec-lease-hold": 60,
                    "add-route": 0,
                    "assign-ip": 1,
                    "assign-ip-from": 0,
                    "authpasswd": "!123fortinet123!",
                    "authusr": None,
                    "authusrgrp": [],
                    "banner": None,
                    "dns-mode": 1,
                    "domain": None,
                    "exchange-interface-ip": 0,
                    "ipv4-dns-server1": "0.0.0.0",
                    "ipv4-dns-server2": "0.0.0.0",
                    "ipv4-dns-server3": "0.0.0.0",
                    "ipv4-end-ip": "0.0.0.0",
                    "ipv4-netmask": "255.255.255.255",
                    "ipv4-split-include": [],
                    "ipv4-start-ip": "0.0.0.0",
                    "ipv4-wins-server1": "0.0.0.0",
                    "ipv4-wins-server2": "0.0.0.0",
                    "localid": None,
                    "mode-cfg": 0,
                    "mode-cfg-ip-version": 0,
                    "net-device": 0,
                    "peergrp": [],
                    "peerid": None,
                    "peertype": 1,
                    "tunnel-search": 1,
                    "unity-support": 1,
                    "xauthtype": 1,
                    "scope member": [
                        {
                            "name": "FGT-DC-5",
                            "vdom": "root"
                        }
                    ]
                },
                {
                    "ip-range": None,
                    "ipv4-exclude-range": None,
                    "protected_subnet": [
                        {
                            "addr": [
                                "all"
                            ]
                        }
                    ],
                    "summary_addr": None,
                    "id": 4,
                    "vpntable": [
                        "OL_MPLS"
                    ],
                    "role": 1,
                    "usrgrp": [],
                    "iface": [
                        "port4"
                    ],
                    "hub_iface": [],
                    "peer": [],
                    "automatic_routing": 0,
                    "extgw": None,
                    "extgwip": [],
                    "extgw_hubip": [],
                    "extgw_p2_per_net": 0,
                    "route-overlap": 0,
                    "vpn-zone": [],
                    "spoke-zone": [],
                    "vpn-interface-priority": 0,
                    "auto-configuration": 1,
                    "default-gateway": "0.0.0.0",
                    "dns-service": 5,
                    "dhcp-server": 1,
                    "ipsec-lease-hold": 60,
                    "add-route": 0,
                    "assign-ip": 0,
                    "assign-ip-from": 0,
                    "authpasswd": "!123fortinet123!",
                    "authusr": None,
                    "authusrgrp": [],
                    "banner": None,
                    "dns-mode": 1,
                    "domain": None,
                    "exchange-interface-ip": 0,
                    "ipv4-dns-server1": "0.0.0.0",
                    "ipv4-dns-server2": "0.0.0.0",
                    "ipv4-dns-server3": "0.0.0.0",
                    "ipv4-end-ip": "0.0.0.0",
                    "ipv4-netmask": "255.255.255.255",
                    "ipv4-split-include": [],
                    "ipv4-start-ip": "0.0.0.0",
                    "ipv4-wins-server1": "0.0.0.0",
                    "ipv4-wins-server2": "0.0.0.0",
                    "localid": None,
                    "mode-cfg": 0,
                    "mode-cfg-ip-version": 0,
                    "net-device": 0,
                    "peergrp": [],
                    "peerid": None,
                    "peertype": 8,
                    "tunnel-search": 1,
                    "unity-support": 1,
                    "xauthtype": 1,
                    "scope member": [
                        {
                            "name": "FGT-1",
                            "vdom": "root"
                        }
                    ]
                },
                {
                    "ip-range": None,
                    "ipv4-exclude-range": None,
                    "protected_subnet": [
                        {
                            "addr": [
                                "all"
                            ]
                        }
                    ],
                    "summary_addr": None,
                    "id": 5,
                    "vpntable": [
                        "OL_MPLS"
                    ],
                    "role": 1,
                    "usrgrp": [],
                    "iface": [
                        "port4"
                    ],
                    "hub_iface": [],
                    "peer": [],
                    "automatic_routing": 0,
                    "extgw": None,
                    "extgwip": [],
                    "extgw_hubip": [],
                    "extgw_p2_per_net": 0,
                    "route-overlap": 0,
                    "vpn-zone": [],
                    "spoke-zone": [],
                    "vpn-interface-priority": 0,
                    "auto-configuration": 1,
                    "default-gateway": "0.0.0.0",
                    "dns-service": 5,
                    "dhcp-server": 1,
                    "ipsec-lease-hold": 60,
                    "add-route": 0,
                    "assign-ip": 0,
                    "assign-ip-from": 0,
                    "authpasswd": "!123fortinet123!",
                    "authusr": None,
                    "authusrgrp": [],
                    "banner": None,
                    "dns-mode": 1,
                    "domain": None,
                    "exchange-interface-ip": 0,
                    "ipv4-dns-server1": "0.0.0.0",
                    "ipv4-dns-server2": "0.0.0.0",
                    "ipv4-dns-server3": "0.0.0.0",
                    "ipv4-end-ip": "0.0.0.0",
                    "ipv4-netmask": "255.255.255.255",
                    "ipv4-split-include": [],
                    "ipv4-start-ip": "0.0.0.0",
                    "ipv4-wins-server1": "0.0.0.0",
                    "ipv4-wins-server2": "0.0.0.0",
                    "localid": None,
                    "mode-cfg": 0,
                    "mode-cfg-ip-version": 0,
                    "net-device": 0,
                    "peergrp": [],
                    "peerid": None,
                    "peertype": 8,
                    "tunnel-search": 1,
                    "unity-support": 1,
                    "xauthtype": 1,
                    "scope member": [
                        {
                            "name": "FGT-2",
                            "vdom": "root"
                        }
                    ]
                },
                {
                    "ip-range": None,
                    "ipv4-exclude-range": None,
                    "protected_subnet": [
                        {
                            "addr": [
                                "all"
                            ]
                        }
                    ],
                    "summary_addr": None,
                    "id": 6,
                    "vpntable": [
                        "OL_MPLS"
                    ],
                    "role": 0,
                    "usrgrp": [],
                    "iface": [
                        "port4"
                    ],
                    "hub_iface": [],
                    "peer": [],
                    "automatic_routing": 0,
                    "extgw": None,
                    "extgwip": [],
                    "extgw_hubip": [],
                    "extgw_p2_per_net": 0,
                    "route-overlap": 0,
                    "vpn-zone": [],
                    "spoke-zone": [],
                    "vpn-interface-priority": 0,
                    "auto-configuration": 0,
                    "default-gateway": "0.0.0.0",
                    "dns-service": 5,
                    "dhcp-server": 0,
                    "ipsec-lease-hold": 60,
                    "add-route": 0,
                    "assign-ip": 1,
                    "assign-ip-from": 0,
                    "authpasswd": "!123fortinet123!",
                    "authusr": None,
                    "authusrgrp": [],
                    "banner": None,
                    "dns-mode": 1,
                    "domain": None,
                    "exchange-interface-ip": 0,
                    "ipv4-dns-server1": "0.0.0.0",
                    "ipv4-dns-server2": "0.0.0.0",
                    "ipv4-dns-server3": "0.0.0.0",
                    "ipv4-end-ip": "0.0.0.0",
                    "ipv4-netmask": "255.255.255.255",
                    "ipv4-split-include": [],
                    "ipv4-start-ip": "0.0.0.0",
                    "ipv4-wins-server1": "0.0.0.0",
                    "ipv4-wins-server2": "0.0.0.0",
                    "local-gw": "0.0.0.0",
                    "localid": None,
                    "mode-cfg": 0,
                    "mode-cfg-ip-version": 0,
                    "net-device": 0,
                    "peergrp": [],
                    "peerid": None,
                    "peertype": 1,
                    "tunnel-search": 1,
                    "unity-support": 1,
                    "xauthtype": 1,
                    "scope member": [
                        {
                            "name": "FGT-DC-5",
                            "vdom": "root"
                        }
                    ]
                }
            ]
        }
    ]
}

headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache"
}

response = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=False)

if not is_request_status_ok(response):
    print(" Error in request.")
    print(response.text)
    exit(-1)

content = json.loads(response.content)

print (" Request completed")


##############################################################
# 8
##############################################################

payload = {
    "session": session,
    "id": 1,
    "method": "set",
    "params": [
        {
            "url": "/pm/pkg/adom/" + adom,
             "data": [

                {
                    "name": "Branches-PP",
                    "obj ver": 11,
                    "oid": 1456,
                    "package settings": {
                        "central-nat": 0,
                        "consolidated-firewall-mode": 0,
                        "fwpolicy-implicit-log": 0,
                        "fwpolicy6-implicit-log": 0,
                        "ngfw-mode": 0
                    },
                    "scope member": [
                        {
                            "name": "FGT-1",
                            "vdom": "root"
                        },
                        {
                            "name": "FGT-2",
                            "vdom": "root"
                        }
                    ],
                    "type": "pkg"
                },
                {
                    "name": "DataCenter-PP",
                    "obj ver": 16,
                    "oid": 1461,
                    "package settings": {
                        "central-nat": 0,
                        "consolidated-firewall-mode": 0,
                        "fwpolicy-implicit-log": 0,
                        "fwpolicy6-implicit-log": 0,
                        "ngfw-mode": 0
                    },
                    "scope member": [
                        {
                            "name": "FGT-DC-5",
                            "vdom": "root"
                        }
                    ],
                    "type": "pkg"
                }
            ]
        }
    ]
}

run_request(8, payload)

##############################################################
# 9
##############################################################

payload = {
    "session": session,
    "id": 1,
    "method": "set",
    "params": [
        {
            "url": "/pm/config/adom/" + adom + "/pkg/Branches-PP/firewall/policy/",
            "data": [
                {
                    "vpn_dst_node": None,
                    "vpn_src_node": None,
                    "policyid": 1,
                    "srcintf": [
                        "any",
                        "any"
                    ],
                    "dstintf": [
                        "any",
                        "any"
                    ],
                    "srcaddr": [
                        "all"
                    ],
                    "dstaddr": [
                        "all"
                    ],
                    "action": 1,
                    "status": 1,
                    "schedule": [
                        "always"
                    ],
                    "service": [
                        "ALL"
                    ],
                    "logtraffic": 2,
                    "nat": 0,
                    "disclaimer": 0,
                    "natip": [
                        "0.0.0.0",
                        "0.0.0.0"
                    ],
                    "diffserv-forward": 0,
                    "diffserv-reverse": 0,
                    "tcp-mss-sender": 0,
                    "tcp-mss-receiver": 0,
                    "groups": [],
                    "custom-log-fields": [],
                    "wccp": 0,
                    "session-ttl": 0,
                    "match-vip": 0,
                    "traffic-shaper": [],
                    "traffic-shaper-reverse": [],
                    "rtp-nat": 0,
                    "per-ip-shaper": [],
                    "utm-status": 1,
                    "application-list": [
                        "default"
                    ],
                    "profile-type": 0,
                    "profile-protocol-options": [],
                    "schedule-timeout": 0,
                    "auto-asic-offload": 1,
                    "webproxy-forward-server": [],
                    "replacemsg-override-group": [],
                    "fsso": 1,
                    "fsso-agent-for-ntlm": [],
                    "logtraffic-start": 0,
                    "capture-packet": 0,
                    "webcache-https": 0,
                    "block-notification": 0,
                    "srcaddr-negate": 0,
                    "dstaddr-negate": 0,
                    "service-negate": 0,
                    "permit-any-host": 0,
                    "timeout-send-rst": 0,
                    "vlan-cos-fwd": 255,
                    "vlan-cos-rev": 255,
                    "users": [],
                    "ssl-ssh-profile": [
                        "certificate-inspection"
                    ],
                    "captive-portal-exempt": 0,
                    "name": "Branch to Overlay",
                    "ssl-mirror-intf": [],
                    "ssl-mirror": 0,
                    "dsri": 0,
                    "delay-tcp-npu-session": 0,
                    "internet-service": 0,
                    "radius-mac-auth-bypass": 0,
                    "tcp-session-without-syn": 2,
                    "internet-service-src": 0,
                    "internet-service-src-id": [],
                    "internet-service-src-custom": [],
                    "app-group": [],
                    "internet-service-src-negate": 0,
                    "vlan-filter": None,
                    "np-acceleration": 1,
                    "internet-service-src-group": [],
                    "internet-service-src-custom-group": [],
                    "tos": "0x00",
                    "tos-mask": "0x00",
                    "tos-negate": 0,
                    "reputation-minimum": 0,
                    "reputation-direction": 2,
                    "webproxy-profile": [],
                    "geoip-anycast": 0,
                    "anti-replay": 1,
                    "inspection-mode": 1,
                    "email-collect": 0,
                    "match-vip-only": 0,
                    "fsso-groups": []
                },
                {
                    "vpn_dst_node": None,
                    "vpn_src_node": None,
                    "policyid": 2,
                    "srcintf": [
                        "any",
                        "any"
                    ],
                    "dstintf": [
                        "port1"
                    ],
                    "srcaddr": [
                        "all"
                    ],
                    "dstaddr": [
                        "all"
                    ],
                    "action": 1,
                    "status": 1,
                    "schedule": [
                        "always"
                    ],
                    "service": [
                        "ALL"
                    ],
                    "logtraffic": 2,
                    "nat": 1,
                    "disclaimer": 0,
                    "natip": [
                        "0.0.0.0",
                        "0.0.0.0"
                    ],
                    "diffserv-forward": 0,
                    "diffserv-reverse": 0,
                    "tcp-mss-sender": 0,
                    "tcp-mss-receiver": 0,
                    "groups": [],
                    "custom-log-fields": [],
                    "wccp": 0,
                    "session-ttl": 0,
                    "match-vip": 0,
                    "traffic-shaper": [],
                    "traffic-shaper-reverse": [],
                    "rtp-nat": 0,
                    "per-ip-shaper": [],
                    "utm-status": 1,
                    "application-list": [
                        "default"
                    ],
                    "profile-type": 0,
                    "profile-protocol-options": [],
                    "schedule-timeout": 0,
                    "auto-asic-offload": 1,
                    "webproxy-forward-server": [],
                    "replacemsg-override-group": [],
                    "fsso": 1,
                    "fsso-agent-for-ntlm": [],
                    "logtraffic-start": 0,
                    "capture-packet": 0,
                    "webcache-https": 0,
                    "block-notification": 0,
                    "srcaddr-negate": 0,
                    "dstaddr-negate": 0,
                    "service-negate": 0,
                    "permit-any-host": 0,
                    "timeout-send-rst": 0,
                    "vlan-cos-fwd": 255,
                    "vlan-cos-rev": 255,
                    "users": [],
                    "ssl-ssh-profile": [
                        "certificate-inspection"
                    ],
                    "captive-portal-exempt": 0,
                    "name": "Branch to INET",
                    "ssl-mirror-intf": [],
                    "ssl-mirror": 0,
                    "dsri": 0,
                    "delay-tcp-npu-session": 0,
                    "internet-service": 0,
                    "radius-mac-auth-bypass": 0,
                    "tcp-session-without-syn": 2,
                    "internet-service-src": 0,
                    "internet-service-src-id": [],
                    "internet-service-src-custom": [],
                    "app-group": [],
                    "internet-service-src-negate": 0,
                    "vlan-filter": None,
                    "np-acceleration": 1,
                    "internet-service-src-group": [],
                    "internet-service-src-custom-group": [],
                    "tos": "0x00",
                    "tos-mask": "0x00",
                    "tos-negate": 0,
                    "reputation-minimum": 0,
                    "reputation-direction": 2,
                    "webproxy-profile": [],
                    "geoip-anycast": 0,
                    "anti-replay": 1,
                    "inspection-mode": 1,
                    "email-collect": 0,
                    "match-vip-only": 0,
                    "fsso-groups": []
                },
                {
                    "vpn_dst_node": None,
                    "vpn_src_node": None,
                    "policyid": 3,
                    "srcintf": [
                        "any",
                        "any"
                    ],
                    "dstintf": [
                        "any",
                        "any"
                    ],
                    "srcaddr": [
                        "all"
                    ],
                    "dstaddr": [
                        "all"
                    ],
                    "action": 1,
                    "status": 1,
                    "schedule": [
                        "always"
                    ],
                    "service": [
                        "ALL"
                    ],
                    "logtraffic": 2,
                    "nat": 0,
                    "disclaimer": 0,
                    "natip": [
                        "0.0.0.0",
                        "0.0.0.0"
                    ],
                    "diffserv-forward": 0,
                    "diffserv-reverse": 0,
                    "tcp-mss-sender": 0,
                    "tcp-mss-receiver": 0,
                    "groups": [],
                    "custom-log-fields": [],
                    "wccp": 0,
                    "session-ttl": 0,
                    "match-vip": 0,
                    "traffic-shaper": [],
                    "traffic-shaper-reverse": [],
                    "rtp-nat": 0,
                    "per-ip-shaper": [],
                    "utm-status": 1,
                    "application-list": [
                        "default"
                    ],
                    "profile-type": 0,
                    "profile-protocol-options": [],
                    "schedule-timeout": 0,
                    "auto-asic-offload": 1,
                    "webproxy-forward-server": [],
                    "replacemsg-override-group": [],
                    "fsso": 1,
                    "fsso-agent-for-ntlm": [],
                    "logtraffic-start": 0,
                    "capture-packet": 0,
                    "webcache-https": 0,
                    "block-notification": 0,
                    "srcaddr-negate": 0,
                    "dstaddr-negate": 0,
                    "service-negate": 0,
                    "permit-any-host": 0,
                    "timeout-send-rst": 0,
                    "vlan-cos-fwd": 255,
                    "vlan-cos-rev": 255,
                    "users": [],
                    "ssl-ssh-profile": [
                        "certificate-inspection"
                    ],
                    "captive-portal-exempt": 0,
                    "name": "Overlay to Branch",
                    "ssl-mirror-intf": [],
                    "ssl-mirror": 0,
                    "dsri": 0,
                    "delay-tcp-npu-session": 0,
                    "internet-service": 0,
                    "radius-mac-auth-bypass": 0,
                    "tcp-session-without-syn": 2,
                    "internet-service-src": 0,
                    "internet-service-src-id": [],
                    "internet-service-src-custom": [],
                    "app-group": [],
                    "internet-service-src-negate": 0,
                    "vlan-filter": None,
                    "np-acceleration": 1,
                    "internet-service-src-group": [],
                    "internet-service-src-custom-group": [],
                    "tos": "0x00",
                    "tos-mask": "0x00",
                    "tos-negate": 0,
                    "reputation-minimum": 0,
                    "reputation-direction": 2,
                    "webproxy-profile": [],
                    "geoip-anycast": 0,
                    "anti-replay": 1,
                    "inspection-mode": 1,
                    "email-collect": 0,
                    "match-vip-only": 0,
                    "fsso-groups": []
                }
            ]
        }
    ]
}

run_request(9, payload)

##############################################################
# 10
##############################################################

payload = {
    "session": session,
    "id": 1,
    "method": "set",
    "params": [
        {
            "url": "/pm/config/adom/" + adom + "/pkg/DataCenter-PP/firewall/policy/",
            "data": [
                {
                    "vpn_dst_node": None,
                    "vpn_src_node": None,
                    "policyid": 1,
                    "srcintf": [
                        "port5"
                    ],
                    "dstintf": [
                        "any",
                        "any"
                    ],
                    "srcaddr": [
                        "all"
                    ],
                    "dstaddr": [
                        "all"
                    ],
                    "action": 1,
                    "status": 1,
                    "schedule": [
                        "always"
                    ],
                    "service": [
                        "ALL"
                    ],
                    "logtraffic": 2,
                    "nat": 0,
                    "disclaimer": 0,
                    "natip": [
                        "0.0.0.0",
                        "0.0.0.0"
                    ],
                    "diffserv-forward": 0,
                    "diffserv-reverse": 0,
                    "tcp-mss-sender": 0,
                    "tcp-mss-receiver": 0,
                    "groups": [],
                    "custom-log-fields": [],
                    "wccp": 0,
                    "session-ttl": 0,
                    "match-vip": 0,
                    "traffic-shaper": [],
                    "traffic-shaper-reverse": [],
                    "rtp-nat": 0,
                    "per-ip-shaper": [],
                    "utm-status": 1,
                    "application-list": [
                        "default"
                    ],
                    "profile-type": 0,
                    "profile-protocol-options": [],
                    "schedule-timeout": 0,
                    "auto-asic-offload": 1,
                    "webproxy-forward-server": [],
                    "replacemsg-override-group": [],
                    "fsso": 1,
                    "fsso-agent-for-ntlm": [],
                    "logtraffic-start": 0,
                    "capture-packet": 0,
                    "webcache-https": 0,
                    "block-notification": 0,
                    "srcaddr-negate": 0,
                    "dstaddr-negate": 0,
                    "service-negate": 0,
                    "permit-any-host": 0,
                    "timeout-send-rst": 0,
                    "uuid": "618ef1ae-e8f0-51e9-8287-6b29e2edb23a",
                    "vlan-cos-fwd": 255,
                    "vlan-cos-rev": 255,
                    "users": [],
                    "ssl-ssh-profile": [
                        "certificate-inspection"
                    ],
                    "captive-portal-exempt": 0,
                    "name": "DC to Overlay",
                    "ssl-mirror-intf": [],
                    "ssl-mirror": 0,
                    "dsri": 0,
                    "delay-tcp-npu-session": 0,
                    "internet-service": 0,
                    "radius-mac-auth-bypass": 0,
                    "tcp-session-without-syn": 2,
                    "internet-service-src": 0,
                    "internet-service-src-id": [],
                    "internet-service-src-custom": [],
                    "app-group": [],
                    "internet-service-src-negate": 0,
                    "vlan-filter": None,
                    "np-acceleration": 1,
                    "internet-service-src-group": [],
                    "internet-service-src-custom-group": [],
                    "tos": "0x00",
                    "tos-mask": "0x00",
                    "tos-negate": 0,
                    "reputation-minimum": 0,
                    "reputation-direction": 2,
                    "webproxy-profile": [],
                    "geoip-anycast": 0,
                    "anti-replay": 1,
                    "inspection-mode": 1,
                    "email-collect": 0,
                    "match-vip-only": 0,
                    "fsso-groups": []
                },
                {
                    "vpn_dst_node": None,
                    "vpn_src_node": None,
                    "policyid": 2,
                    "srcintf": [
                        "any",
                        "any"
                    ],
                    "dstintf": [
                        "port5"
                    ],
                    "srcaddr": [
                        "all"
                    ],
                    "dstaddr": [
                        "all"
                    ],
                    "action": 1,
                    "status": 1,
                    "schedule": [
                        "always"
                    ],
                    "service": [
                        "ALL"
                    ],
                    "logtraffic": 2,
                    "nat": 0,
                    "disclaimer": 0,
                    "natip": [
                        "0.0.0.0",
                        "0.0.0.0"
                    ],
                    "diffserv-forward": 0,
                    "diffserv-reverse": 0,
                    "tcp-mss-sender": 0,
                    "tcp-mss-receiver": 0,
                    "groups": [],
                    "custom-log-fields": [],
                    "wccp": 0,
                    "session-ttl": 0,
                    "match-vip": 0,
                    "traffic-shaper": [],
                    "traffic-shaper-reverse": [],
                    "rtp-nat": 0,
                    "per-ip-shaper": [],
                    "utm-status": 1,
                    "application-list": [
                        "default"
                    ],
                    "profile-type": 0,
                    "profile-protocol-options": [],
                    "schedule-timeout": 0,
                    "auto-asic-offload": 1,
                    "webproxy-forward-server": [],
                    "replacemsg-override-group": [],
                    "fsso": 1,
                    "fsso-agent-for-ntlm": [],
                    "logtraffic-start": 0,
                    "capture-packet": 0,
                    "webcache-https": 0,
                    "block-notification": 0,
                    "srcaddr-negate": 0,
                    "dstaddr-negate": 0,
                    "service-negate": 0,
                    "permit-any-host": 0,
                    "timeout-send-rst": 0,
                    "uuid": "6a689c26-e8f0-51e9-0c4c-f5a8f8d102e1",
                    "vlan-cos-fwd": 255,
                    "vlan-cos-rev": 255,
                    "users": [],
                    "ssl-ssh-profile": [
                        "certificate-inspection"
                    ],
                    "captive-portal-exempt": 0,
                    "name": "Overlay to DC",
                    "ssl-mirror-intf": [],
                    "ssl-mirror": 0,
                    "dsri": 0,
                    "delay-tcp-npu-session": 0,
                    "internet-service": 0,
                    "radius-mac-auth-bypass": 0,
                    "tcp-session-without-syn": 2,
                    "internet-service-src": 0,
                    "internet-service-src-id": [],
                    "internet-service-src-custom": [],
                    "app-group": [],
                    "internet-service-src-negate": 0,
                    "vlan-filter": None,
                    "np-acceleration": 1,
                    "internet-service-src-group": [],
                    "internet-service-src-custom-group": [],
                    "tos": "0x00",
                    "tos-mask": "0x00",
                    "tos-negate": 0,
                    "reputation-minimum": 0,
                    "reputation-direction": 2,
                    "webproxy-profile": [],
                    "geoip-anycast": 0,
                    "anti-replay": 1,
                    "inspection-mode": 1,
                    "email-collect": 0,
                    "match-vip-only": 0,
                    "fsso-groups": []
                },
                {
                    "vpn_dst_node": None,
                    "vpn_src_node": None,
                    "policyid": 3,
                    "srcintf": [
                        "port5"
                    ],
                    "dstintf": [
                        "port1"
                    ],
                    "srcaddr": [
                        "all"
                    ],
                    "dstaddr": [
                        "all"
                    ],
                    "action": 1,
                    "status": 1,
                    "schedule": [
                        "always"
                    ],
                    "service": [
                        "ALL"
                    ],
                    "logtraffic": 2,
                    "nat": 0,
                    "disclaimer": 0,
                    "natip": [
                        "0.0.0.0",
                        "0.0.0.0"
                    ],
                    "diffserv-forward": 0,
                    "diffserv-reverse": 0,
                    "tcp-mss-sender": 0,
                    "tcp-mss-receiver": 0,
                    "groups": [],
                    "custom-log-fields": [],
                    "wccp": 0,
                    "session-ttl": 0,
                    "match-vip": 0,
                    "traffic-shaper": [],
                    "traffic-shaper-reverse": [],
                    "rtp-nat": 0,
                    "per-ip-shaper": [],
                    "utm-status": 1,
                    "application-list": [
                        "default"
                    ],
                    "profile-type": 0,
                    "profile-protocol-options": [],
                    "schedule-timeout": 0,
                    "auto-asic-offload": 1,
                    "webproxy-forward-server": [],
                    "replacemsg-override-group": [],
                    "fsso": 1,
                    "fsso-agent-for-ntlm": [],
                    "logtraffic-start": 0,
                    "capture-packet": 0,
                    "webcache-https": 0,
                    "block-notification": 0,
                    "srcaddr-negate": 0,
                    "dstaddr-negate": 0,
                    "service-negate": 0,
                    "permit-any-host": 0,
                    "timeout-send-rst": 0,
                    "vlan-cos-fwd": 255,
                    "vlan-cos-rev": 255,
                    "users": [],
                    "ssl-ssh-profile": [
                        "certificate-inspection"
                    ],
                    "captive-portal-exempt": 0,
                    "name": "DC to INET",
                    "ssl-mirror-intf": [],
                    "ssl-mirror": 0,
                    "dsri": 0,
                    "delay-tcp-npu-session": 0,
                    "internet-service": 0,
                    "radius-mac-auth-bypass": 0,
                    "tcp-session-without-syn": 2,
                    "internet-service-src": 0,
                    "internet-service-src-id": [],
                    "internet-service-src-custom": [],
                    "app-group": [],
                    "internet-service-src-negate": 0,
                    "vlan-filter": None,
                    "np-acceleration": 1,
                    "internet-service-src-group": [],
                    "internet-service-src-custom-group": [],
                    "tos": "0x00",
                    "tos-mask": "0x00",
                    "tos-negate": 0,
                    "reputation-minimum": 0,
                    "reputation-direction": 2,
                    "webproxy-profile": [],
                    "geoip-anycast": 0,
                    "anti-replay": 1,
                    "inspection-mode": 1,
                    "email-collect": 0,
                    "match-vip-only": 0,
                    "fsso-groups": []
                },
                {
                    "vpn_dst_node": None,
                    "vpn_src_node": None,
                    "policyid": 4,
                    "srcintf": [
                        "any",
                        "any"
                    ],
                    "dstintf": [
                        "port1"
                    ],
                    "srcaddr": [
                        "all"
                    ],
                    "dstaddr": [
                        "all"
                    ],
                    "action": 1,
                    "status": 1,
                    "schedule": [
                        "always"
                    ],
                    "service": [
                        "ALL"
                    ],
                    "logtraffic": 2,
                    "nat": 1,
                    "disclaimer": 0,
                    "natip": [
                        "0.0.0.0",
                        "0.0.0.0"
                    ],
                    "diffserv-forward": 0,
                    "diffserv-reverse": 0,
                    "tcp-mss-sender": 0,
                    "tcp-mss-receiver": 0,
                    "groups": [],
                    "custom-log-fields": [],
                    "wccp": 0,
                    "session-ttl": 0,
                    "match-vip": 0,
                    "traffic-shaper": [],
                    "traffic-shaper-reverse": [],
                    "rtp-nat": 0,
                    "per-ip-shaper": [],
                    "utm-status": 1,
                    "application-list": [
                        "default"
                    ],
                    "profile-type": 0,
                    "profile-protocol-options": [],
                    "schedule-timeout": 0,
                    "auto-asic-offload": 1,
                    "webproxy-forward-server": [],
                    "replacemsg-override-group": [],
                    "fsso": 1,
                    "fsso-agent-for-ntlm": [],
                    "logtraffic-start": 0,
                    "capture-packet": 0,
                    "webcache-https": 0,
                    "block-notification": 0,
                    "srcaddr-negate": 0,
                    "dstaddr-negate": 0,
                    "service-negate": 0,
                    "permit-any-host": 0,
                    "timeout-send-rst": 0,
                    "vlan-cos-fwd": 255,
                    "vlan-cos-rev": 255,
                    "users": [],
                    "ssl-ssh-profile": [
                        "certificate-inspection"
                    ],
                    "captive-portal-exempt": 0,
                    "name": "Overlay to INET",
                    "ssl-mirror-intf": [],
                    "ssl-mirror": 0,
                    "dsri": 0,
                    "delay-tcp-npu-session": 0,
                    "internet-service": 0,
                    "radius-mac-auth-bypass": 0,
                    "tcp-session-without-syn": 2,
                    "internet-service-src": 0,
                    "internet-service-src-id": [],
                    "internet-service-src-custom": [],
                    "app-group": [],
                    "internet-service-src-negate": 0,
                    "vlan-filter": None,
                    "np-acceleration": 1,
                    "internet-service-src-group": [],
                    "internet-service-src-custom-group": [],
                    "tos": "0x00",
                    "tos-mask": "0x00",
                    "tos-negate": 0,
                    "reputation-minimum": 0,
                    "reputation-direction": 2,
                    "webproxy-profile": [],
                    "geoip-anycast": 0,
                    "anti-replay": 1,
                    "inspection-mode": 1,
                    "email-collect": 0,
                    "match-vip-only": 0,
                    "fsso-groups": []
                },
                {
                    "vpn_dst_node": None,
                    "vpn_src_node": None,
                    "policyid": 5,
                    "srcintf": [
                        "any",
                        "any"
                    ],
                    "dstintf": [
                        "any",
                        "any"
                    ],
                    "srcaddr": [
                        "all"
                    ],
                    "dstaddr": [
                        "all"
                    ],
                    "action": 1,
                    "status": 1,
                    "schedule": [
                        "always"
                    ],
                    "service": [
                        "ALL"
                    ],
                    "logtraffic": 2,
                    "nat": 0,
                    "disclaimer": 0,
                    "natip": [
                        "0.0.0.0",
                        "0.0.0.0"
                    ],
                    "diffserv-forward": 0,
                    "diffserv-reverse": 0,
                    "tcp-mss-sender": 0,
                    "tcp-mss-receiver": 0,
                    "groups": [],
                    "custom-log-fields": [],
                    "wccp": 0,
                    "session-ttl": 0,
                    "match-vip": 0,
                    "traffic-shaper": [],
                    "traffic-shaper-reverse": [],
                    "rtp-nat": 0,
                    "per-ip-shaper": [],
                    "utm-status": 1,
                    "application-list": [
                        "default"
                    ],
                    "profile-type": 0,
                    "profile-protocol-options": [],
                    "schedule-timeout": 0,
                    "auto-asic-offload": 1,
                    "webproxy-forward-server": [],
                    "replacemsg-override-group": [],
                    "fsso": 1,
                    "fsso-agent-for-ntlm": [],
                    "logtraffic-start": 0,
                    "capture-packet": 0,
                    "webcache-https": 0,
                    "block-notification": 0,
                    "srcaddr-negate": 0,
                    "dstaddr-negate": 0,
                    "service-negate": 0,
                    "permit-any-host": 0,
                    "timeout-send-rst": 0,
                    "vlan-cos-fwd": 255,
                    "vlan-cos-rev": 255,
                    "users": [],
                    "ssl-ssh-profile": [
                        "certificate-inspection"
                    ],
                    "captive-portal-exempt": 0,
                    "name": "Branch to Branch",
                    "ssl-mirror-intf": [],
                    "ssl-mirror": 0,
                    "dsri": 0,
                    "delay-tcp-npu-session": 0,
                    "internet-service": 0,
                    "radius-mac-auth-bypass": 0,
                    "tcp-session-without-syn": 2,
                    "internet-service-src": 0,
                    "internet-service-src-id": [],
                    "internet-service-src-custom": [],
                    "app-group": [],
                    "internet-service-src-negate": 0,
                    "vlan-filter": None,
                    "np-acceleration": 1,
                    "internet-service-src-group": [],
                    "internet-service-src-custom-group": [],
                    "tos": "0x00",
                    "tos-mask": "0x00",
                    "tos-negate": 0,
                    "reputation-minimum": 0,
                    "reputation-direction": 2,
                    "webproxy-profile": [],
                    "geoip-anycast": 0,
                    "anti-replay": 1,
                    "inspection-mode": 1,
                    "email-collect": 0,
                    "match-vip-only": 0,
                    "fsso-groups": []
                }
            ]
        }
    ]
}

run_request(10, payload)


##############################################################
# 11
##############################################################

payload = {
    "session": session,
    "id": 1,
    "method": "exec",
    "params": [
        {
            "url": "/securityconsole/install/package",
            "data": [
                {
                    "adom": adom,
                    "pkg": "DataCenter-PP",
                    "scope": [
                        {
                            "name": "FGT-DC-5",
                            "vdom": "root"
                        }
                    ],
                    "flags": "none"
                }
            ]
        }
    ]
}

run_request_async(11, payload)

##############################################################
# 12
##############################################################

payload = {
    "session": session,
    "id": 1,
    "method": "exec",
    "params": [
        {
            "url": "/securityconsole/install/package",
            "data": [
                {
                    "adom": adom,
                    "pkg": "Branches-PP",
                    "scope": [
                        {
                            "name": "FGT-1",
                            "vdom": "root"
                        },
                        {
                            "name": "FGT-2",
                            "vdom": "root"
                        }
                    ],
                    "flags": "none"
                }
            ]
        }
    ]
}

run_request_async(12, payload)


##############################################################
# 13
##############################################################

payload = {
    "session": session,
    "id": 1,
    "method": "set",
    "params": [
        {
            "url": "/pm/config/device/FGT-1/global/system/interface",
            "data": [
                {
                    "name": "OL_MPLS_0",
                    "vdom": "root",
                    "ip": [
                        "10.0.10.1",
                        "255.255.255.255"
                    ],
                    "allowaccess": "ping",
                    "type": "tunnel",
                    "remote-ip": [
                        "10.0.10.5",
                        "255.255.255.0"
                    ],
                    "fortiheartbeat": "enable",
                    "interface": "port4"
                },
                                {
                    "name": "OL_INET_0",
                    "vdom": "root",
                    "ip": [
                        "10.0.11.1",
                        "255.255.255.255"
                    ],
                    "allowaccess": "ping",
                    "type": "tunnel",
                    "remote-ip": [
                        "10.0.11.5",
                        "255.255.255.0"
                    ],
                    "fortiheartbeat": "enable",
                    "interface": "port1"
                }

            ]
        }
    ]
}

run_request(13, payload)

##############################################################
# 14
##############################################################

payload = {
    "session": session,
    "id": 1,
    "method": "set",
    "params": [
        {
            "url": "/pm/config/device/FGT-2/global/system/interface",
            "data": [
                {
                    "name": "OL_MPLS_0",
                    "vdom": "root",
                    "ip": [
                        "10.0.10.2",
                        "255.255.255.255"
                    ],
                    "allowaccess": "ping",
                    "type": "tunnel",
                    "remote-ip": [
                        "10.0.10.5",
                        "255.255.255.0"
                    ],
                    "fortiheartbeat": "enable",
                    "interface": "port4"
                },
                                {
                    "name": "OL_INET_0",
                    "vdom": "root",
                    "ip": [
                        "10.0.11.2",
                        "255.255.255.255"
                    ],
                    "allowaccess": "ping",
                    "type": "tunnel",
                    "remote-ip": [
                        "10.0.11.5",
                        "255.255.255.0"
                    ],
                    "fortiheartbeat": "enable",
                    "interface": "port1"
                }

            ]
        }
    ]
}

run_request(14, payload)


##############################################################
# 15
##############################################################

payload = {
    "session": session,
    "id": 1,
    "method": "set",
    "params": [
        {
            "url": "/pm/config/device/FGT-DC-5/global/system/interface",
            "data": [
                {
                    "name": "OL_MPLS_0",
                    "vdom": "root",
                    "ip": [
                        "10.0.10.5",
                        "255.255.255.255"
                    ],
                    "allowaccess": "ping",
                    "type": "tunnel",
                    "remote-ip": [
                        "10.0.10.254",
                        "255.255.255.0"
                    ],
                    "fortiheartbeat": "enable",
                    "interface": "port4",
                    "alias": "OL_MPLS"
                },
                {
                    "name": "OL_INET_0",
                    "vdom": "root",
                    "ip": [
                        "10.0.11.5",
                        "255.255.255.255"
                    ],
                    "allowaccess": "ping",
                    "type": "tunnel",
                    "remote-ip": [
                        "10.0.11.254",
                        "255.255.255.0"
                    ],
                    "fortiheartbeat": "enable",
                    "interface": "port1",
                    "alias": "OL_INET"
                }

            ]
        }
    ]
}

run_request(15, payload)


##############################################################
# 16
##############################################################

payload = {
    "session": session,
    "id": 1,
    "method": "set",
    "params": [
        {
            "url": "/dvmdb/adom/" + adom + "/script",
            "data": [
                {
                    "script_schedule": None,
                    "name": "Fix vpn in branches",
                    "type": "cli",
                    "desc": "",
                    "content": "config vpn ipsec phase1-interface\n edit OL_MPLS_0\n set tunnel-search nexthop\n set auto-discovery-receiver enable\n next\n edit OL_INET_0\n set tunnel-search nexthop\n set auto-discovery-receiver enable\n next\n end",
                    "target": "device_database"
                }
            ]
        }
    ]
}

run_request(16, payload)


##############################################################
# 17
##############################################################

payload = {
    "session": session,
    "id": 1,
    "method": "set",
    "params": [
        {
            "url": "/dvmdb/adom/" + adom + "/script",
            "data": [
                {
                    "script_schedule": None,
                    "name": "Fix vpn in hub",
                    "type": "cli",
                    "desc": "",
                    "content": "config vpn ipsec phase1-interface\n edit OL_MPLS_0\n set auto-discovery-sender enable\n next\n edit OL_INET_0\n set auto-discovery-sender enable\n next\n end",
                    "target": "device_database"
                }
            ]
        }
    ]
}

run_request(17, payload)


##############################################################
# 18
##############################################################

payload = {
    "session": session,
    "id": 1,
    "method": "exec",
    "params": [
        {
            "url": "/dvmdb/adom/" + adom + "/script/execute",
            "data": 
                {
                	"adom": adom,
                    "script": "Fix vpn in branches",
                    "scope": [
                        {
                            "name": "FGT-1",
                            "vdom": "root"
                        },
                        {
                            "name": "FGT-2",
                            "vdom": "root"
                        }
                    ]
                }
            
        }
    ]
}

run_request_async(18, payload)

##############################################################
# 19
##############################################################

payload = {
    "session": session,
    "id": 1,
    "method": "exec",
    "params": [
        {
            "url": "/dvmdb/adom/" + adom + "/script/execute",
            "data": 
                {
                	"adom": adom,
                    "script": "Fix vpn in hub",
                    "scope": [
                        {
                            "name": "FGT-DC-5",
                            "vdom": "root"
                        }
                    ]
                }
            
        }
    ]
}

run_request_async(19, payload)

##############################################################
# 20
##############################################################

payload = {
    "session": session,
    "id": 1,
    "method": "set",
    "params": [
        {
            "url": "/pm/config/adom/" + adom + "/obj/dynamic/interface/",
            "data": [
                {
                    "dynamic_mapping": None,
                    "name": "OL_INET",
                    "description": None,
                    "single-intf": 1,
                    "default-mapping": 1,
                    "defmap-intf": "OL_INET_0",
                    "defmap-zonemember": [],
                    "defmap-intrazone-deny": 0,
                    "egress-shaping-profile": [],
                    "color": 0
                },
                {
                    "dynamic_mapping": None,
                    "name": "OL_MPLS",
                    "description": None,
                    "single-intf": 1,
                    "default-mapping": 1,
                    "defmap-intf": "OL_MPLS_0",
                    "defmap-zonemember": [],
                    "defmap-intrazone-deny": 0,
                    "egress-shaping-profile": [],
                    "color": 0
                }
            ]
        }
    ]
}

run_request(20, payload)

##############################################################
# 21
##############################################################

payload = {
    "session": session,
    "id": 1,
    "method": "set",
    "params": [
        {
            "url": "/pm/config/adom/" + adom + "/pkg/Branches-PP/firewall/policy/",
            "data": [
                {
                    "vpn_dst_node": None,
                    "vpn_src_node": None,
                    "policyid": 1,
                    "srcintf": [
                        "Clients-BR",
                        "WirelessVLAN"
                    ],
                    "dstintf": [
                        "OL_INET",
                        "OL_MPLS"
                    ],
                    "srcaddr": [
                        "all"
                    ],
                    "dstaddr": [
                        "all"
                    ],
                    "action": 1,
                    "status": 1,
                    "schedule": [
                        "always"
                    ],
                    "service": [
                        "ALL"
                    ],
                    "logtraffic": 2,
                    "nat": 0,
                    "disclaimer": 0,
                    "natip": [
                        "0.0.0.0",
                        "0.0.0.0"
                    ],
                    "diffserv-forward": 0,
                    "diffserv-reverse": 0,
                    "tcp-mss-sender": 0,
                    "tcp-mss-receiver": 0,
                    "groups": [],
                    "custom-log-fields": [],
                    "wccp": 0,
                    "session-ttl": 0,
                    "match-vip": 0,
                    "traffic-shaper": [],
                    "traffic-shaper-reverse": [],
                    "rtp-nat": 0,
                    "per-ip-shaper": [],
                    "utm-status": 1,
                    "application-list": [
                        "default"
                    ],
                    "profile-type": 0,
                    "profile-protocol-options": [],
                    "schedule-timeout": 0,
                    "auto-asic-offload": 1,
                    "webproxy-forward-server": [],
                    "replacemsg-override-group": [],
                    "fsso": 1,
                    "fsso-agent-for-ntlm": [],
                    "logtraffic-start": 0,
                    "capture-packet": 0,
                    "webcache-https": 0,
                    "block-notification": 0,
                    "srcaddr-negate": 0,
                    "dstaddr-negate": 0,
                    "service-negate": 0,
                    "permit-any-host": 0,
                    "timeout-send-rst": 0,
                    "vlan-cos-fwd": 255,
                    "vlan-cos-rev": 255,
                    "users": [],
                    "ssl-ssh-profile": [
                        "certificate-inspection"
                    ],
                    "captive-portal-exempt": 0,
                    "name": "Branch to Overlay",
                    "ssl-mirror-intf": [],
                    "ssl-mirror": 0,
                    "dsri": 0,
                    "delay-tcp-npu-session": 0,
                    "internet-service": 0,
                    "radius-mac-auth-bypass": 0,
                    "tcp-session-without-syn": 2,
                    "internet-service-src": 0,
                    "internet-service-src-id": [],
                    "internet-service-src-custom": [],
                    "app-group": [],
                    "internet-service-src-negate": 0,
                    "vlan-filter": None,
                    "np-acceleration": 1,
                    "internet-service-src-group": [],
                    "internet-service-src-custom-group": [],
                    "tos": "0x00",
                    "tos-mask": "0x00",
                    "tos-negate": 0,
                    "reputation-minimum": 0,
                    "reputation-direction": 2,
                    "webproxy-profile": [],
                    "geoip-anycast": 0,
                    "anti-replay": 1,
                    "inspection-mode": 1,
                    "email-collect": 0,
                    "match-vip-only": 0,
                    "fsso-groups": []
                },
                {
                    "vpn_dst_node": None,
                    "vpn_src_node": None,
                    "policyid": 2,
                    "srcintf": [
                        "Clients-BR",
                        "WirelessVLAN"
                    ],
                    "dstintf": [
                        "port1"
                    ],
                    "srcaddr": [
                        "all"
                    ],
                    "dstaddr": [
                        "all"
                    ],
                    "action": 1,
                    "status": 1,
                    "schedule": [
                        "always"
                    ],
                    "service": [
                        "ALL"
                    ],
                    "logtraffic": 2,
                    "nat": 1,
                    "disclaimer": 0,
                    "natip": [
                        "0.0.0.0",
                        "0.0.0.0"
                    ],
                    "diffserv-forward": 0,
                    "diffserv-reverse": 0,
                    "tcp-mss-sender": 0,
                    "tcp-mss-receiver": 0,
                    "groups": [],
                    "custom-log-fields": [],
                    "wccp": 0,
                    "session-ttl": 0,
                    "match-vip": 0,
                    "traffic-shaper": [],
                    "traffic-shaper-reverse": [],
                    "rtp-nat": 0,
                    "per-ip-shaper": [],
                    "utm-status": 1,
                    "application-list": [
                        "default"
                    ],
                    "profile-type": 0,
                    "profile-protocol-options": [],
                    "schedule-timeout": 0,
                    "auto-asic-offload": 1,
                    "webproxy-forward-server": [],
                    "replacemsg-override-group": [],
                    "fsso": 1,
                    "fsso-agent-for-ntlm": [],
                    "logtraffic-start": 0,
                    "capture-packet": 0,
                    "webcache-https": 0,
                    "block-notification": 0,
                    "srcaddr-negate": 0,
                    "dstaddr-negate": 0,
                    "service-negate": 0,
                    "permit-any-host": 0,
                    "timeout-send-rst": 0,
                    "vlan-cos-fwd": 255,
                    "vlan-cos-rev": 255,
                    "users": [],
                    "ssl-ssh-profile": [
                        "certificate-inspection"
                    ],
                    "captive-portal-exempt": 0,
                    "name": "Branch to INET",
                    "ssl-mirror-intf": [],
                    "ssl-mirror": 0,
                    "dsri": 0,
                    "delay-tcp-npu-session": 0,
                    "internet-service": 0,
                    "radius-mac-auth-bypass": 0,
                    "tcp-session-without-syn": 2,
                    "internet-service-src": 0,
                    "internet-service-src-id": [],
                    "internet-service-src-custom": [],
                    "app-group": [],
                    "internet-service-src-negate": 0,
                    "vlan-filter": None,
                    "np-acceleration": 1,
                    "internet-service-src-group": [],
                    "internet-service-src-custom-group": [],
                    "tos": "0x00",
                    "tos-mask": "0x00",
                    "tos-negate": 0,
                    "reputation-minimum": 0,
                    "reputation-direction": 2,
                    "webproxy-profile": [],
                    "geoip-anycast": 0,
                    "anti-replay": 1,
                    "inspection-mode": 1,
                    "email-collect": 0,
                    "match-vip-only": 0,
                    "fsso-groups": []
                },
                {
                    "vpn_dst_node": None,
                    "vpn_src_node": None,
                    "policyid": 3,
                    "srcintf": [
                        "OL_INET",
                        "OL_MPLS"
                    ],
                    "dstintf": [
                        "Clients-BR",
                        "WirelessVLAN"
                    ],
                    "srcaddr": [
                        "all"
                    ],
                    "dstaddr": [
                        "all"
                    ],
                    "action": 1,
                    "status": 1,
                    "schedule": [
                        "always"
                    ],
                    "service": [
                        "ALL"
                    ],
                    "logtraffic": 2,
                    "nat": 0,
                    "disclaimer": 0,
                    "natip": [
                        "0.0.0.0",
                        "0.0.0.0"
                    ],
                    "diffserv-forward": 0,
                    "diffserv-reverse": 0,
                    "tcp-mss-sender": 0,
                    "tcp-mss-receiver": 0,
                    "groups": [],
                    "custom-log-fields": [],
                    "wccp": 0,
                    "session-ttl": 0,
                    "match-vip": 0,
                    "traffic-shaper": [],
                    "traffic-shaper-reverse": [],
                    "rtp-nat": 0,
                    "per-ip-shaper": [],
                    "utm-status": 1,
                    "application-list": [
                        "default"
                    ],
                    "profile-type": 0,
                    "profile-protocol-options": [],
                    "schedule-timeout": 0,
                    "auto-asic-offload": 1,
                    "webproxy-forward-server": [],
                    "replacemsg-override-group": [],
                    "fsso": 1,
                    "fsso-agent-for-ntlm": [],
                    "logtraffic-start": 0,
                    "capture-packet": 0,
                    "webcache-https": 0,
                    "block-notification": 0,
                    "srcaddr-negate": 0,
                    "dstaddr-negate": 0,
                    "service-negate": 0,
                    "permit-any-host": 0,
                    "timeout-send-rst": 0,
                    "vlan-cos-fwd": 255,
                    "vlan-cos-rev": 255,
                    "users": [],
                    "ssl-ssh-profile": [
                        "certificate-inspection"
                    ],
                    "captive-portal-exempt": 0,
                    "name": "Overlay to Branch",
                    "ssl-mirror-intf": [],
                    "ssl-mirror": 0,
                    "dsri": 0,
                    "delay-tcp-npu-session": 0,
                    "internet-service": 0,
                    "radius-mac-auth-bypass": 0,
                    "tcp-session-without-syn": 2,
                    "internet-service-src": 0,
                    "internet-service-src-id": [],
                    "internet-service-src-custom": [],
                    "app-group": [],
                    "internet-service-src-negate": 0,
                    "vlan-filter": None,
                    "np-acceleration": 1,
                    "internet-service-src-group": [],
                    "internet-service-src-custom-group": [],
                    "tos": "0x00",
                    "tos-mask": "0x00",
                    "tos-negate": 0,
                    "reputation-minimum": 0,
                    "reputation-direction": 2,
                    "webproxy-profile": [],
                    "geoip-anycast": 0,
                    "anti-replay": 1,
                    "inspection-mode": 1,
                    "email-collect": 0,
                    "match-vip-only": 0,
                    "fsso-groups": []
                }
            ]
        }
    ]
}

run_request(21, payload)


##############################################################
# 22
##############################################################

payload = {
    "session": session,
    "id": 1,
    "method": "set",
    "params": [
        {
            "url": "/pm/config/adom/" + adom + "/pkg/DataCenter-PP/firewall/policy/",
            "data": [
                {
                    "vpn_dst_node": None,
                    "vpn_src_node": None,
                    "policyid": 1,
                    "srcintf": [
                        "port5"
                    ],
                    "dstintf": [
                        "OL_INET",
                        "OL_MPLS"
                    ],
                    "srcaddr": [
                        "all"
                    ],
                    "dstaddr": [
                        "all"
                    ],
                    "action": 1,
                    "status": 1,
                    "schedule": [
                        "always"
                    ],
                    "service": [
                        "ALL"
                    ],
                    "logtraffic": 2,
                    "nat": 0,
                    "disclaimer": 0,
                    "natip": [
                        "0.0.0.0",
                        "0.0.0.0"
                    ],
                    "diffserv-forward": 0,
                    "diffserv-reverse": 0,
                    "tcp-mss-sender": 0,
                    "tcp-mss-receiver": 0,
                    "groups": [],
                    "custom-log-fields": [],
                    "wccp": 0,
                    "session-ttl": 0,
                    "match-vip": 0,
                    "traffic-shaper": [],
                    "traffic-shaper-reverse": [],
                    "rtp-nat": 0,
                    "per-ip-shaper": [],
                    "utm-status": 1,
                    "application-list": [
                        "default"
                    ],
                    "profile-type": 0,
                    "profile-protocol-options": [],
                    "schedule-timeout": 0,
                    "auto-asic-offload": 1,
                    "webproxy-forward-server": [],
                    "replacemsg-override-group": [],
                    "fsso": 1,
                    "fsso-agent-for-ntlm": [],
                    "logtraffic-start": 0,
                    "capture-packet": 0,
                    "webcache-https": 0,
                    "block-notification": 0,
                    "srcaddr-negate": 0,
                    "dstaddr-negate": 0,
                    "service-negate": 0,
                    "permit-any-host": 0,
                    "timeout-send-rst": 0,
                    "uuid": "618ef1ae-e8f0-51e9-8287-6b29e2edb23a",
                    "vlan-cos-fwd": 255,
                    "vlan-cos-rev": 255,
                    "users": [],
                    "ssl-ssh-profile": [
                        "certificate-inspection"
                    ],
                    "captive-portal-exempt": 0,
                    "name": "DC to Overlay",
                    "ssl-mirror-intf": [],
                    "ssl-mirror": 0,
                    "dsri": 0,
                    "delay-tcp-npu-session": 0,
                    "internet-service": 0,
                    "radius-mac-auth-bypass": 0,
                    "tcp-session-without-syn": 2,
                    "internet-service-src": 0,
                    "internet-service-src-id": [],
                    "internet-service-src-custom": [],
                    "app-group": [],
                    "internet-service-src-negate": 0,
                    "vlan-filter": None,
                    "np-acceleration": 1,
                    "internet-service-src-group": [],
                    "internet-service-src-custom-group": [],
                    "tos": "0x00",
                    "tos-mask": "0x00",
                    "tos-negate": 0,
                    "reputation-minimum": 0,
                    "reputation-direction": 2,
                    "webproxy-profile": [],
                    "geoip-anycast": 0,
                    "anti-replay": 1,
                    "inspection-mode": 1,
                    "email-collect": 0,
                    "match-vip-only": 0,
                    "fsso-groups": []
                },
                {
                    "vpn_dst_node": None,
                    "vpn_src_node": None,
                    "policyid": 2,
                    "srcintf": [
                        "OL_INET",
                        "OL_MPLS"
                    ],
                    "dstintf": [
                        "port5"
                    ],
                    "srcaddr": [
                        "all"
                    ],
                    "dstaddr": [
                        "all"
                    ],
                    "action": 1,
                    "status": 1,
                    "schedule": [
                        "always"
                    ],
                    "service": [
                        "ALL"
                    ],
                    "logtraffic": 2,
                    "nat": 0,
                    "disclaimer": 0,
                    "natip": [
                        "0.0.0.0",
                        "0.0.0.0"
                    ],
                    "diffserv-forward": 0,
                    "diffserv-reverse": 0,
                    "tcp-mss-sender": 0,
                    "tcp-mss-receiver": 0,
                    "groups": [],
                    "custom-log-fields": [],
                    "wccp": 0,
                    "session-ttl": 0,
                    "match-vip": 0,
                    "traffic-shaper": [],
                    "traffic-shaper-reverse": [],
                    "rtp-nat": 0,
                    "per-ip-shaper": [],
                    "utm-status": 1,
                    "application-list": [
                        "default"
                    ],
                    "profile-type": 0,
                    "profile-protocol-options": [],
                    "schedule-timeout": 0,
                    "auto-asic-offload": 1,
                    "webproxy-forward-server": [],
                    "replacemsg-override-group": [],
                    "fsso": 1,
                    "fsso-agent-for-ntlm": [],
                    "logtraffic-start": 0,
                    "capture-packet": 0,
                    "webcache-https": 0,
                    "block-notification": 0,
                    "srcaddr-negate": 0,
                    "dstaddr-negate": 0,
                    "service-negate": 0,
                    "permit-any-host": 0,
                    "timeout-send-rst": 0,
                    "uuid": "6a689c26-e8f0-51e9-0c4c-f5a8f8d102e1",
                    "vlan-cos-fwd": 255,
                    "vlan-cos-rev": 255,
                    "users": [],
                    "ssl-ssh-profile": [
                        "certificate-inspection"
                    ],
                    "captive-portal-exempt": 0,
                    "name": "Overlay to DC",
                    "ssl-mirror-intf": [],
                    "ssl-mirror": 0,
                    "dsri": 0,
                    "delay-tcp-npu-session": 0,
                    "internet-service": 0,
                    "radius-mac-auth-bypass": 0,
                    "tcp-session-without-syn": 2,
                    "internet-service-src": 0,
                    "internet-service-src-id": [],
                    "internet-service-src-custom": [],
                    "app-group": [],
                    "internet-service-src-negate": 0,
                    "vlan-filter": None,
                    "np-acceleration": 1,
                    "internet-service-src-group": [],
                    "internet-service-src-custom-group": [],
                    "tos": "0x00",
                    "tos-mask": "0x00",
                    "tos-negate": 0,
                    "reputation-minimum": 0,
                    "reputation-direction": 2,
                    "webproxy-profile": [],
                    "geoip-anycast": 0,
                    "anti-replay": 1,
                    "inspection-mode": 1,
                    "email-collect": 0,
                    "match-vip-only": 0,
                    "fsso-groups": []
                },
                {
                    "vpn_dst_node": None,
                    "vpn_src_node": None,
                    "policyid": 3,
                    "srcintf": [
                        "port5"
                    ],
                    "dstintf": [
                        "port1"
                    ],
                    "srcaddr": [
                        "all"
                    ],
                    "dstaddr": [
                        "all"
                    ],
                    "action": 1,
                    "status": 1,
                    "schedule": [
                        "always"
                    ],
                    "service": [
                        "ALL"
                    ],
                    "logtraffic": 2,
                    "nat": 0,
                    "disclaimer": 0,
                    "natip": [
                        "0.0.0.0",
                        "0.0.0.0"
                    ],
                    "diffserv-forward": 0,
                    "diffserv-reverse": 0,
                    "tcp-mss-sender": 0,
                    "tcp-mss-receiver": 0,
                    "groups": [],
                    "custom-log-fields": [],
                    "wccp": 0,
                    "session-ttl": 0,
                    "match-vip": 0,
                    "traffic-shaper": [],
                    "traffic-shaper-reverse": [],
                    "rtp-nat": 0,
                    "per-ip-shaper": [],
                    "utm-status": 1,
                    "application-list": [
                        "default"
                    ],
                    "profile-type": 0,
                    "profile-protocol-options": [],
                    "schedule-timeout": 0,
                    "auto-asic-offload": 1,
                    "webproxy-forward-server": [],
                    "replacemsg-override-group": [],
                    "fsso": 1,
                    "fsso-agent-for-ntlm": [],
                    "logtraffic-start": 0,
                    "capture-packet": 0,
                    "webcache-https": 0,
                    "block-notification": 0,
                    "srcaddr-negate": 0,
                    "dstaddr-negate": 0,
                    "service-negate": 0,
                    "permit-any-host": 0,
                    "timeout-send-rst": 0,
                    "vlan-cos-fwd": 255,
                    "vlan-cos-rev": 255,
                    "users": [],
                    "ssl-ssh-profile": [
                        "certificate-inspection"
                    ],
                    "captive-portal-exempt": 0,
                    "name": "DC to INET",
                    "ssl-mirror-intf": [],
                    "ssl-mirror": 0,
                    "dsri": 0,
                    "delay-tcp-npu-session": 0,
                    "internet-service": 0,
                    "radius-mac-auth-bypass": 0,
                    "tcp-session-without-syn": 2,
                    "internet-service-src": 0,
                    "internet-service-src-id": [],
                    "internet-service-src-custom": [],
                    "app-group": [],
                    "internet-service-src-negate": 0,
                    "vlan-filter": None,
                    "np-acceleration": 1,
                    "internet-service-src-group": [],
                    "internet-service-src-custom-group": [],
                    "tos": "0x00",
                    "tos-mask": "0x00",
                    "tos-negate": 0,
                    "reputation-minimum": 0,
                    "reputation-direction": 2,
                    "webproxy-profile": [],
                    "geoip-anycast": 0,
                    "anti-replay": 1,
                    "inspection-mode": 1,
                    "email-collect": 0,
                    "match-vip-only": 0,
                    "fsso-groups": []
                },
                {
                    "vpn_dst_node": None,
                    "vpn_src_node": None,
                    "policyid": 4,
                    "srcintf": [
                        "OL_INET",
                        "OL_MPLS"
                    ],
                    "dstintf": [
                        "port1"
                    ],
                    "srcaddr": [
                        "all"
                    ],
                    "dstaddr": [
                        "all"
                    ],
                    "action": 1,
                    "status": 1,
                    "schedule": [
                        "always"
                    ],
                    "service": [
                        "ALL"
                    ],
                    "logtraffic": 2,
                    "nat": 1,
                    "disclaimer": 0,
                    "natip": [
                        "0.0.0.0",
                        "0.0.0.0"
                    ],
                    "diffserv-forward": 0,
                    "diffserv-reverse": 0,
                    "tcp-mss-sender": 0,
                    "tcp-mss-receiver": 0,
                    "groups": [],
                    "custom-log-fields": [],
                    "wccp": 0,
                    "session-ttl": 0,
                    "match-vip": 0,
                    "traffic-shaper": [],
                    "traffic-shaper-reverse": [],
                    "rtp-nat": 0,
                    "per-ip-shaper": [],
                    "utm-status": 1,
                    "application-list": [
                        "default"
                    ],
                    "profile-type": 0,
                    "profile-protocol-options": [],
                    "schedule-timeout": 0,
                    "auto-asic-offload": 1,
                    "webproxy-forward-server": [],
                    "replacemsg-override-group": [],
                    "fsso": 1,
                    "fsso-agent-for-ntlm": [],
                    "logtraffic-start": 0,
                    "capture-packet": 0,
                    "webcache-https": 0,
                    "block-notification": 0,
                    "srcaddr-negate": 0,
                    "dstaddr-negate": 0,
                    "service-negate": 0,
                    "permit-any-host": 0,
                    "timeout-send-rst": 0,
                    "vlan-cos-fwd": 255,
                    "vlan-cos-rev": 255,
                    "users": [],
                    "ssl-ssh-profile": [
                        "certificate-inspection"
                    ],
                    "captive-portal-exempt": 0,
                    "name": "Overlay to INET",
                    "ssl-mirror-intf": [],
                    "ssl-mirror": 0,
                    "dsri": 0,
                    "delay-tcp-npu-session": 0,
                    "internet-service": 0,
                    "radius-mac-auth-bypass": 0,
                    "tcp-session-without-syn": 2,
                    "internet-service-src": 0,
                    "internet-service-src-id": [],
                    "internet-service-src-custom": [],
                    "app-group": [],
                    "internet-service-src-negate": 0,
                    "vlan-filter": None,
                    "np-acceleration": 1,
                    "internet-service-src-group": [],
                    "internet-service-src-custom-group": [],
                    "tos": "0x00",
                    "tos-mask": "0x00",
                    "tos-negate": 0,
                    "reputation-minimum": 0,
                    "reputation-direction": 2,
                    "webproxy-profile": [],
                    "geoip-anycast": 0,
                    "anti-replay": 1,
                    "inspection-mode": 1,
                    "email-collect": 0,
                    "match-vip-only": 0,
                    "fsso-groups": []
                },
                {
                    "vpn_dst_node": None,
                    "vpn_src_node": None,
                    "policyid": 5,
                    "srcintf": [
                        "OL_INET",
                        "OL_MPLS"
                    ],
                    "dstintf": [
                        "OL_INET",
                        "OL_MPLS"
                    ],
                    "srcaddr": [
                        "all"
                    ],
                    "dstaddr": [
                        "all"
                    ],
                    "action": 1,
                    "status": 1,
                    "schedule": [
                        "always"
                    ],
                    "service": [
                        "ALL"
                    ],
                    "logtraffic": 2,
                    "nat": 0,
                    "disclaimer": 0,
                    "natip": [
                        "0.0.0.0",
                        "0.0.0.0"
                    ],
                    "diffserv-forward": 0,
                    "diffserv-reverse": 0,
                    "tcp-mss-sender": 0,
                    "tcp-mss-receiver": 0,
                    "groups": [],
                    "custom-log-fields": [],
                    "wccp": 0,
                    "session-ttl": 0,
                    "match-vip": 0,
                    "traffic-shaper": [],
                    "traffic-shaper-reverse": [],
                    "rtp-nat": 0,
                    "per-ip-shaper": [],
                    "utm-status": 1,
                    "application-list": [
                        "default"
                    ],
                    "profile-type": 0,
                    "profile-protocol-options": [],
                    "schedule-timeout": 0,
                    "auto-asic-offload": 1,
                    "webproxy-forward-server": [],
                    "replacemsg-override-group": [],
                    "fsso": 1,
                    "fsso-agent-for-ntlm": [],
                    "logtraffic-start": 0,
                    "capture-packet": 0,
                    "webcache-https": 0,
                    "block-notification": 0,
                    "srcaddr-negate": 0,
                    "dstaddr-negate": 0,
                    "service-negate": 0,
                    "permit-any-host": 0,
                    "timeout-send-rst": 0,
                    "vlan-cos-fwd": 255,
                    "vlan-cos-rev": 255,
                    "users": [],
                    "ssl-ssh-profile": [
                        "certificate-inspection"
                    ],
                    "captive-portal-exempt": 0,
                    "name": "Branch to Branch",
                    "ssl-mirror-intf": [],
                    "ssl-mirror": 0,
                    "dsri": 0,
                    "delay-tcp-npu-session": 0,
                    "internet-service": 0,
                    "radius-mac-auth-bypass": 0,
                    "tcp-session-without-syn": 2,
                    "internet-service-src": 0,
                    "internet-service-src-id": [],
                    "internet-service-src-custom": [],
                    "app-group": [],
                    "internet-service-src-negate": 0,
                    "vlan-filter": None,
                    "np-acceleration": 1,
                    "internet-service-src-group": [],
                    "internet-service-src-custom-group": [],
                    "tos": "0x00",
                    "tos-mask": "0x00",
                    "tos-negate": 0,
                    "reputation-minimum": 0,
                    "reputation-direction": 2,
                    "webproxy-profile": [],
                    "geoip-anycast": 0,
                    "anti-replay": 1,
                    "inspection-mode": 1,
                    "email-collect": 0,
                    "match-vip-only": 0,
                    "fsso-groups": []
                }
            ]
        }
    ]
}

run_request(22, payload)


##############################################################
# 23 - This one is like 11
##############################################################

payload = {
    "session": session,
    "id": 1,
    "method": "exec",
    "params": [
        {
            "url": "/securityconsole/install/package",
            "data": [
                {
                    "adom": adom,
                    "pkg": "DataCenter-PP",
                    "scope": [
                        {
                            "name": "FGT-DC-5",
                            "vdom": "root"
                        }
                    ],
                    "flags": "none"
                }
            ]
        }
    ]
}

run_request_async(23, payload)

##############################################################
# 24 - This one is like 12
##############################################################

payload = {
    "session": session,
    "id": 1,
    "method": "exec",
    "params": [
        {
            "url": "/securityconsole/install/package",
            "data": [
                {
                    "adom": adom,
                    "pkg": "Branches-PP",
                    "scope": [
                        {
                            "name": "FGT-1",
                            "vdom": "root"
                        },
                        {
                            "name": "FGT-2",
                            "vdom": "root"
                        }
                    ],
                    "flags": "none"
                }
            ]
        }
    ]
}

run_request_async(24, payload)
