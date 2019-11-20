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

    content = json.loads(response.content)
    line = content["result"][0]["data"]["line"]

    for l in line:
        if l["percent"] != 100:
            return False

    return True


def is_request_status_ok(response):
    content = json.loads(response.content)

    return response.status_code == 200 and \
        content["result"][0]["status"]["code"] == 0 and \
        content["result"][0]["status"]["message"] == "OK"
    



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
