#!/usr/bin/env python3

import requests
import json

from urllib3.exceptions import InsecureRequestWarning
from time import sleep
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

USER = "admin"
PASSWD = "fortinet"
URL = "https://104.199.86.56:10411//jsonrpc"
ADOM = "DEMO"
BRANCH1_IP = "172.16.1.1"
BRANCH2_IP = "172.16.1.2"
DATACENTER_IP = "172.16.2.5"
BRANCH1_NAME = "branch1_fgt"
BRANCH2_NAME = "branch2_fgt"
DATACENTER_NAME = "datacenter_fgt"

request_number = 0


def is_task_finished(id):

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

    response = requests.request("POST", URL, data=json.dumps(
        payload), headers=headers, verify=False)

    if not is_request_status_ok(response):
        print(" \033[31Error in request.\033[39m")
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


def run_request(payload, name=""):
    global request_number
    print("Running request \033[33m" + str(request_number) +
          "\033[39m. \033[93m" + name + "\033[39m")
    request_number += 1

    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", URL, data=json.dumps(
        payload), headers=headers, verify=False)

    if not is_request_status_ok(response):
        print(" Error in request.")
        print(response.text)
        exit(-1)

    content = json.loads(response.content)

    print(" \033[92mCompleted\033[39m")
    return content


def run_request_async(payload, name=""):
    global request_number
    print("Running request \033[33m" + str(request_number) +
          "\033[39m. \033[93m" + name + "\033[39m")
    request_number += 1

    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", URL, data=json.dumps(
        payload), headers=headers, verify=False)

    if not is_request_status_ok(response):
        print(" Error in request.")
        print(response.text)
        exit(-1)

    content = json.loads(response.content)
    try:
        task_id = content["result"][0]["data"]["taskid"]
    except:
        task_id = content["result"][0]["data"]["task"]

    print(" Asynchronous task created: " +
          str(task_id) + " ", end="", flush=False)
    while not is_task_finished(task_id):
        print(".", end="", flush=True)
        sleep(1)

    print("\n \033[92mCompleted\033[39m")
    return content


##############################################################
# Login
##############################################################
def login():

    global session

    payload = {
        "session": 1,
        "id": 1,
        "method": "exec",
        "params": [
            {
                "url": "sys/login/user",
                "data": [
                    {
                        "user": USER,
                        "passwd": PASSWD
                    }
                ]
            }
        ]
    }

    content = run_request(payload, "Login")
    session = content["session"]
    return session


##############################################################
# Discover / Probe Devices FGT
##############################################################
def probeFortiGateDevice(branch_ip):

    payload = {
        "session": session,
        "id": 1,
        "method": "exec",
        "params": [
            {
                "url": "/dvm/cmd/discover/device",
                "data": {
                    "device": {
                        "adm_pass": PASSWD,
                        "adm_usr": USER,
                        "ip": branch_ip
                    }
                }
            }
        ]
    }

    content = run_request(payload, name="Discover / Probe FGT Devices")
    sn_fgt_1 = content["result"][0]["data"]["device"]["sn"]
    return sn_fgt_1


##############################################################
# Add Devices
##############################################################
def addDevices(sn_fgt_1, sn_fgt_2, sn_fgt_dc):

    payload = {
        "session": session,
        "id": 1,
        "method": "exec",
        "params": [
            {
                "url": "/dvm/cmd/add/dev-list",
                "data": {
                    "adom": ADOM,
                    "flags": ["create_task", "nonblocking"],
                    "add-dev-list": [
                        {
                            "adm_pass": PASSWD,
                            "adm_usr": USER,
                            "ip": BRANCH1_IP,
                            "name": BRANCH1_NAME,
                            "sn": sn_fgt_1,
                            "mgmt_mode": "fmgfaz",
                            "flags": 24
                        },
                        {
                            "adm_pass": PASSWD,
                            "adm_usr": USER,
                            "ip": BRANCH2_IP,
                            "name": BRANCH2_NAME,
                            "sn": sn_fgt_2,
                            "mgmt_mode": "fmgfaz",
                            "flags": 24
                        },
                        {
                            "adm_pass": PASSWD,
                            "adm_usr": USER,
                            "ip": DATACENTER_IP,
                            "name": DATACENTER_NAME,
                            "sn": sn_fgt_dc,
                            "mgmt_mode": "fmgfaz",
                            "flags": 24
                        }
                    ]
                }
            }
        ]
    }

    run_request_async(payload, name="Add Devices")


##############################################################
# Get FMG Serial Number
##############################################################
def getFmgSerialNumber():

    payload = {
        "session": session,
        "id": 1,
        "method": "get",
        "params": [
            {
                "url": "/sys/status"
            }
        ]
    }

    content = run_request(payload, name="Get FMG Serial Number")
    sn_fmg = content["result"][0]["data"]["Serial Number"]
    return sn_fmg


##############################################################
# Add Script - FAZ Configuration
##############################################################
def addScript_FAZConfiguration():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/dvmdb/adom/" + ADOM + "/script",
                "data": [
                    {
                        "script_schedule": None,
                        "name": "FAZ Configuration",
                        "type": "cli",
                        "desc": "",
                        "content": "# FAZ Configuration \n\
config log fortianalyzer setting \n\
  set status enable \n\
  set server 192.168.0.15 \n\
  set upload-option realtime \n\
  set serial FMG-VMTM19006959 \n\
  set certificate-verification disable \n\
  set reliable enable \n\
end",
                        "target": "device_database"
                    }
                ]
            }
        ]
    }

    run_request(payload, name="Add Script - FAZ Configuration")


##############################################################
# Exec Script - FAZ Configuration
##############################################################
def execScript_FAZConfiguration():

    payload = {
        "session": session,
        "id": 1,
        "method": "exec",
        "params": [
            {
                "url": "/dvmdb/adom/" + ADOM + "/script/execute",
                "data":
                    {
                        "adom": ADOM,
                        "script": "FAZ Configuration",
                        "scope": [
                            {
                                "name": BRANCH1_NAME,
                                "vdom": "root"
                            },
                            {
                                "name": BRANCH2_NAME,
                                "vdom": "root"
                            },
                            {
                                "name": DATACENTER_NAME,
                                "vdom": "root"
                            }
                        ]
                    }

            }
        ]
    }

    run_request_async(payload, name="Exec Script - FAZ Configuration")


##############################################################
# Add Dynamic Interface
##############################################################
def addDynamicInterface():
    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/pm/config/adom/" + ADOM + "/obj/dynamic/interface/",
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
                        "color": 2
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
                        "color": 2
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
                        "color": 2
                    },
                    {
                        "dynamic_mapping": None,
                        "name": "vl_fap_mgmt",
                        "description": None,
                        "single-intf": 1,
                        "default-mapping": 1,
                        "defmap-intf": "vl_fap_mgmt",
                        "defmap-zonemember": [],
                        "defmap-intrazone-deny": 0,
                        "egress-shaping-profile": [],
                        "color": 3
                    },
                    {
                        "dynamic_mapping": None,
                        "name": "vl_lan",
                        "description": None,
                        "single-intf": 1,
                        "default-mapping": 1,
                        "defmap-intf": "vl_lan",
                        "defmap-zonemember": [],
                        "defmap-intrazone-deny": 0,
                        "egress-shaping-profile": [],
                        "color": 3
                    }
                ]
            }
        ]
    }

    run_request(payload, name="Add Dynamic Interface")


##############################################################
# Add VPN Manager VPN Table
##############################################################
def addVPNManagerVPNTable():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/pm/config/adom/" + ADOM + "/obj/vpnmgr/vpntable",
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

    run_request(payload, name="Add VPN Manager VPN Table")


##############################################################
# Add VPN Manager Node
##############################################################
def addVPNManagerNode():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/pm/config/adom/" + ADOM + "/obj/vpnmgr/node",
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
                                "name": BRANCH1_NAME,
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
                                "name": BRANCH2_NAME,
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
                                "name": DATACENTER_NAME,
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
                                "name": BRANCH1_NAME,
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
                                "name": BRANCH2_NAME,
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
                                "name": DATACENTER_NAME,
                                "vdom": "root"
                            }
                        ]
                    }
                ]
            }
        ]
    }

    run_request(payload, name="Add VPN Manager Node")


##############################################################
# Add Policy Package
##############################################################
def addPolicyPackage():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/pm/pkg/adom/" + ADOM,
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
                                "name": BRANCH1_NAME,
                                "vdom": "root"
                            },
                            {
                                "name": BRANCH2_NAME,
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
                                "name": DATACENTER_NAME,
                                "vdom": "root"
                            }
                        ],
                        "type": "pkg"
                    }
                ]
            }
        ]
    }

    run_request(payload, name="Add Policy Package")


##############################################################
# Add Firewall Policy - Branches PP - No Interfaces
##############################################################
def addFirewallPolicy_Branches_PP_No_Interfaces():
    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/pm/config/adom/" + ADOM + "/pkg/Branches-PP/firewall/policy/",
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

    run_request(
        payload, name="Add Firewall Policy - Branches PP - No Interfaces")


##############################################################
# Add Firewall Policy - DataCenter PP - No Interfaces
##############################################################
def addFirewallPolicy_DataCenter_PP_No_Interfaces():
    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/pm/config/adom/" + ADOM + "/pkg/DataCenter-PP/firewall/policy/",
                "data": [
                    {
                        "vpn_dst_node": None,
                        "vpn_src_node": None,
                        "policyid": 1,
                        "srcintf": [
                            "port5",
                            "port4"
                        ],
                        "dstintf": [
                            "port4",
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
                        "vlan-cos-fwd": 255,
                        "vlan-cos-rev": 255,
                        "users": [],
                        "ssl-ssh-profile": [
                            "certificate-inspection"
                        ],
                        "captive-portal-exempt": 0,
                        "name": "FortiManager Access",
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
                        "policyid": 3,
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
                        "policyid": 4,
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
                        "policyid": 5,
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
                        "policyid": 6,
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

    run_request(
        payload, name="Add Firewall Policy - DataCenter PP - No Interfaces")


##############################################################
# Install policy - Hub
##############################################################
def installPolicy_Hub():

    payload = {
        "session": session,
        "id": 1,
        "method": "exec",
        "params": [
            {
                "url": "/securityconsole/install/package",
                "data": [
                    {
                        "adom": ADOM,
                        "pkg": "DataCenter-PP",
                        "scope": [
                            {
                                "name": DATACENTER_NAME,
                                "vdom": "root"
                            }
                        ],
                        "flags": "none"
                    }
                ]
            }
        ]
    }

    run_request_async(payload, name="Install policy - Hub")


##############################################################
# Install policy - Branches
##############################################################
def installPolicy_Branches():

    payload = {
        "session": session,
        "id": 1,
        "method": "exec",
        "params": [
            {
                "url": "/securityconsole/install/package",
                "data": [
                    {
                        "adom": ADOM,
                        "pkg": "Branches-PP",
                        "scope": [
                            {
                                "name": BRANCH1_NAME,
                                "vdom": "root"
                            },
                            {
                                "name": BRANCH2_NAME,
                                "vdom": "root"
                            }
                        ],
                        "flags": "none"
                    }
                ]
            }
        ]
    }

    run_request_async(payload, name="Install policy - Branches")


##############################################################
# Configure FGT-1 Interfaces
##############################################################
def configureInterfacesFGT1():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/pm/config/device/"+BRANCH1_NAME+"/global/system/interface",
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

    run_request(payload, name="Configure FGT-1 Interfaces")


##############################################################
# Configure FGT-2 Interfaces
##############################################################
def configureInterfacesFGT2():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/pm/config/device/"+BRANCH2_NAME+"/global/system/interface",
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

    run_request(payload, name="Configure FGT-2 Interfaces")


##############################################################
# Configure FGT-DC Interfaces
##############################################################
def configureInterfacesFGTDC():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/pm/config/device/"+DATACENTER_NAME+"/global/system/interface",
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

    run_request(payload, name="Configure FGT-DC Interfaces")


##############################################################
# Add Script - Fix VPN in Branches
##############################################################
def addScript_FixVPNinBranches():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/dvmdb/adom/" + ADOM + "/script",
                "data": [
                    {
                        "script_schedule": None,
                        "name": "Fix vpn in branches",
                        "type": "cli",
                        "desc": "",
                        "content": "# Fix VPN in Branches\n\
config vpn ipsec phase1-interface\n\
  edit OL_MPLS_0\n\
    set tunnel-search nexthop\n\
    set auto-discovery-receiver enable\n\
  next\n\
  edit OL_INET_0\n\
    set tunnel-search nexthop\n\
    set auto-discovery-receiver enable\n\
  next\n\
end",
                        "target": "device_database"
                    }
                ]
            }
        ]
    }

    run_request(payload, name="Add Script - Fix VPN in Branches")


##############################################################
# Add Script - Fix VPN in Hub
##############################################################
def addScript_FixVPNinHub():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/dvmdb/adom/" + ADOM + "/script",
                "data": [
                    {
                        "script_schedule": None,
                        "name": "Fix vpn in hub",
                        "type": "cli",
                        "desc": "",
                        "content": "# Fix VPN in Hub\n\
config vpn ipsec phase1-interface\n\
  edit OL_MPLS_0\n\
    set auto-discovery-sender enable\n\
    next\n\
  edit OL_INET_0\n\
    set auto-discovery-sender enable\n\
  next\n\
end",
                        "target": "device_database"
                    }
                ]
            }
        ]
    }

    run_request(payload, name="Add Script - Fix VPN in Hub")


##############################################################
# Exec Script - Fix VPN in Branches
##############################################################
def execScript_FixVPNinBranches():

    payload = {
        "session": session,
        "id": 1,
        "method": "exec",
        "params": [
            {
                "url": "/dvmdb/adom/" + ADOM + "/script/execute",
                "data":
                    {
                        "adom": ADOM,
                        "script": "Fix vpn in branches",
                        "scope": [
                            {
                                "name": BRANCH1_NAME,
                                "vdom": "root"
                            },
                            {
                                "name": BRANCH2_NAME,
                                "vdom": "root"
                            }
                        ]
                    }

            }
        ]
    }

    run_request_async(payload, name="Exec Script - Fix VPN in Branches")


##############################################################
# Exec Script - Fix VPN in Hub
##############################################################
def execScript_FixVPNinHub():

    payload = {
        "session": session,
        "id": 1,
        "method": "exec",
        "params": [
            {
                "url": "/dvmdb/adom/" + ADOM + "/script/execute",
                "data":
                    {
                        "adom": ADOM,
                        "script": "Fix vpn in hub",
                        "scope": [
                            {
                                "name": DATACENTER_NAME,
                                "vdom": "root"
                            }
                        ]
                    }

            }
        ]
    }

    run_request_async(payload, name="Exec Script - Fix VPN in Hub")


##############################################################
# Add Dynamic Interface - Overlays
##############################################################
def addDynamicInterface_Overlays():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/pm/config/adom/" + ADOM + "/obj/dynamic/interface/",
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
                        "color": 4
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
                        "color": 4
                    }
                ]
            }
        ]
    }

    run_request(payload, name="Add Dynamic Interface - Overlays")


##############################################################
# Add Firewall Policy - Branches PP
##############################################################
def addFirewallPolicy_BranchesPP():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/pm/config/adom/" + ADOM + "/pkg/Branches-PP/firewall/policy/",
                "data": [
                    {
                        "vpn_dst_node": None,
                        "vpn_src_node": None,
                        "policyid": 1,
                        "srcintf": [
                            "vl_lan",
                            "vl_fap_mgmt"
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
                            "vl_lan",
                            "vl_fap_mgmt"
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
                            "vl_lan",
                            "vl_fap_mgmt"
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

    run_request(payload, name="Add Firewall Policy - Branches PP")


##############################################################
# Add Firewall Policy - DataCenter PP
##############################################################
def addFirewallPolicy_DataCenterPP():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/pm/config/adom/" + ADOM + "/pkg/DataCenter-PP/firewall/policy/",
                "data": [
                    {
                        "vpn_dst_node": None,
                        "vpn_src_node": None,
                        "policyid": 1,
                        "srcintf": [
                            "port5",
                            "port4"
                        ],
                        "dstintf": [
                            "port4",
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
                        "vlan-cos-fwd": 255,
                        "vlan-cos-rev": 255,
                        "users": [],
                        "ssl-ssh-profile": [
                            "certificate-inspection"
                        ],
                        "captive-portal-exempt": 0,
                        "name": "FortiManager Access",
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
                        "policyid": 3,
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
                        "policyid": 4,
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
                        "policyid": 5,
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
                        "policyid": 6,
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

    run_request(payload, name="Add Firewall Policy - DataCenter PP")


##############################################################
# Add Dynamic Routing CLI Template - Hub
##############################################################
def addDynamicRoutingCLITemplate_Hub():

    payload = {
        "session": session,
     "id": 1,
    "method": "set",
    "params": [
        {
            "url": "/pm/config/adom/" + ADOM + "/obj/cli/template",
            "data": {
                "name": "Hub-Routing",
                "scope member": [
                    {
                        "name": DATACENTER_NAME,
                        "vdom": "root"
                    }
                ],
                "script": "# Define BGP Communities \n\
config router community-list \n\
    edit \"SLA_KO_MPLS\" \n\
        config rule \n\
            edit 1 \n\
                set action permit \n\
                set match \"65000:200\" \n\
            next \n\
        end \n\
    next \n\
    edit \"SLA_KO_INET\" \n\
        config rule \n\
            edit 1 \n\
                set action permit \n\
                set match \"65000:201\" \n\
            next \n\
        end \n\
    next \n\
    edit \"SLA_OK_INET\" \n\
        config rule \n\
            edit 1 \n\
                set action permit \n\
                set match \"65000:101\" \n\
            next \n\
        end \n\
    next \n\
    edit \"SLA_OK_MPLS\" \n\
        config rule \n\
            edit 1 \n\
                set action permit \n\
                set match \"65000:100\" \n\
            next \n\
        end \n\
    next \n\
end \n\
 \n\
# Match Communities with route-maps \n\
config router route-map \n\
	edit \"OL_MPLS_IN\" \n\
		config rule \n\
			edit 3 \n\
				set match-community \"SLA_KO_MPLS\" \n\
				set set-weight 100 \n\
				set set-route-tag 2 \n\
			next \n\
			edit 100 \n\
				set set-weight 200 \n\
				set set-route-tag 1 \n\
			next \n\
		end \n\
	next \n\
	edit \"OL_INET_IN\" \n\
		config rule \n\
			edit 1 \n\
				set match-community \"SLA_KO_INET\" \n\
				set set-weight 100 \n\
				set set-route-tag 2 \n\
			next \n\
			edit 100 \n\
				set set-weight 200 \n\
				set set-route-tag 1 \n\
			next \n\
		end \n\
	next \n\
	edit \"OL_MPLS_OUT\" \n\
		config rule \n\
			edit 1 \n\
				set action deny \n\
				set match-community \"SLA_OK_INET\" \n\
			next \n\
			edit 2 \n\
				set action deny \n\
				set match-community \"SLA_KO_INET\" \n\
			next \n\
			edit 100 \n\
			next \n\
		end \n\
	next \n\
	edit \"OL_INET_OUT\" \n\
		config rule \n\
			edit 1 \n\
				set action deny \n\
				set match-community \"SLA_OK_MPLS\" \n\
			next \n\
			edit 2 \n\
				set action deny \n\
				set match-community \"SLA_KO_MPLS\" \n\
			next \n\
			edit 100 \n\
			next \n\
		end \n\
	next \n\
end \n\
 \n\
# Configure BGP neighbors \n\
config router bgp \n\
    set as 65000 \n\
    set keepalive-timer 5 \n\
    set holdtime-timer 15 \n\
    set ibgp-multipath enable \n\
    set network-import-check disable \n\
    set additional-path enable \n\
    set scan-time 20 \n\
    config neighbor-group \n\
        edit \"OL_MPLS\" \n\
            set soft-reconfiguration enable \n\
            set advertisement-interval 1 \n\
            set remote-as 65000 \n\
            set route-map-in \"OL_MPLS_IN\" \n\
            set route-map-out \"OL_MPLS_OUT\" \n\
            set additional-path both \n\
            set route-reflector-client enable \n\
        next \n\
        edit \"OL_INET\" \n\
            set soft-reconfiguration enable \n\
            set advertisement-interval 1 \n\
            set remote-as 65000 \n\
            set route-map-in \"OL_INET_IN\" \n\
            set route-map-out \"OL_INET_OUT\" \n\
            set additional-path both \n\
            set route-reflector-client enable \n\
        next \n\
    end \n\
    config neighbor-range \n\
        edit 1 \n\
            set prefix 10.0.10.0 255.255.255.0 \n\
            set neighbor-group \"OL_MPLS\" \n\
        next \n\
        edit 2 \n\
            set prefix 10.0.11.0 255.255.255.0 \n\
            set neighbor-group \"OL_INET\" \n\
        next \n\
    end \n\
    config network \n\
        edit 1 \n\
            set prefix 172.16.0.0 255.255.255.0 \n\
        next \n\
    end \n\
end \n\
 \n\
# Overlay stickiness \n\
config router policy \n\
  edit 1 \n\
    set input-device \"OL_MPLS_0\" \n\
    set output-device \"OL_MPLS_0\" \n\
  next \n\
  edit 2 \n\
    set input-device \"OL_INET_0\" \n\
    set output-device \"OL_INET_0\" \n\
  next \n\
end"
            }
        }
    ]
}
    run_request(payload, name="Add Dynamic Routing CLI Template - Hub")


##############################################################
# Add Dynamic Routing CLI Template - Branches
##############################################################
def addDynamicRoutingCLITemplate_Branches():

    payload = {
        "session": session,
    "id": 1,
    "method": "set",
    "params": [
        {
            "url": "/pm/config/adom/" + ADOM + "/obj/cli/template",
            "data": {
                "name": "Branch-Routing",
                "scope member": [
                    {
                        "name": BRANCH1_NAME,
                        "vdom": "root"
                    },
                    {
                        "name": BRANCH2_NAME,
                        "vdom": "root"
                    }
                ],
                "script": "# Set BGP Communities with route-maps \n\
config router route-map \n\
  edit \"SLA_OK_MPLS\" \n\
      config rule \n\
          edit 1 \n\
              set set-community \"65000:100\" \n\
          next \n\
      end \n\
  next \n\
  edit \"SLA_KO_MPLS\" \n\
      config rule \n\
          edit 1 \n\
              set set-community \"65000:200\" \n\
          next \n\
      end \n\
  next \n\
  edit \"SLA_OK_INET\" \n\
      config rule \n\
          edit 1 \n\
              set set-community \"65000:101\" \n\
          next \n\
      end \n\
  next \n\
  edit \"SLA_KO_INET\" \n\
      config rule \n\
          edit 1 \n\
              set set-community \"65000:201\" \n\
          next \n\
      end \n\
  next \n\
end \n\
 \n\
# BGP to Hub \n\
config router bgp \n\
  set as 65000 \n\
  set keepalive-timer 5 \n\
  set holdtime-timer 15 \n\
  set ibgp-multipath enable \n\
  set scan-time 20 \n\
  config neighbor \n\
    edit \"10.0.10.5\" \n\
        set soft-reconfiguration enable \n\
        set interface \"OL_MPLS_0\" \n\
        set remote-as 65000 \n\
        set route-map-out \"SLA_KO_MPLS\" \n\
        set route-map-out-preferable \"SLA_OK_MPLS\" \n\
        set additional-path receive \n\
    next \n\
    edit \"10.0.11.5\" \n\
        set soft-reconfiguration enable \n\
        set interface \"OL_INET_0\" \n\
        set remote-as 65000 \n\
        set route-map-out \"SLA_KO_INET\" \n\
        set route-map-out-preferable \"SLA_OK_INET\" \n\
        set additional-path receive \n\
    next \n\
  end \n\
  config network \n\
    edit 1 \n\
      set prefix 10.0.1.0 255.255.255.0 \n\
    next \n\
    edit 2 \n\
      set prefix 10.1.1.0 255.255.255.0 \n\
    next \n\
    edit 3 \n\
      set prefix 10.0.2.0 255.255.255.0 \n\
    next \n\
    edit 4 \n\
      set prefix 10.1.2.0 255.255.255.0 \n\
    next \n\
  end \n\
end"
            }
        }
    ]
}
    run_request(payload, name="Add Dynamic Routing CLI Template - Branch")

"""
##############################################################
# Add Script - Hub Community List
##############################################################
def addScript_Hub_Community_list():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/dvmdb/adom/" + ADOM + "/script",
                "data": [
                    {
                        "script_schedule": None,
                        "name": "Hub-Community-list",
                        "type": "cli",
                        "desc": "",
                        "content": "config router community-list\n edit SLA_KO_MPLS\n config rule\n edit 1\n set action permit\n set match 65000:200\n next \n end \n next \n edit SLA_KO_INET \n config rule \n edit 1 \n set action permit \n set match 65000:201 \n next \n end \n next \n edit SLA_OK_INET \n config rule \n edit 1 \n set action permit \n set match 65000:101 \n next \n end \n next \n edit SLA_OK_MPLS \n config rule\n edit 1\n set action permit\n set match 65000:100\n next\n end\n next\n end",
                        "target": "device_database"
                    }
                ]
            }
        ]
    }

    run_request(payload, name="Add Script - Hub Community List")


##############################################################
# Add Script - Hub Route Map
##############################################################
def addScript_Hub_Route_Map():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/dvmdb/adom/" + ADOM + "/script",
                "data": [
                    {
                        "script_schedule": None,
                        "name": "Hub Route Map",
                        "type": "cli",
                        "desc": "",
                        "content": "config router route-map \n edit OL_MPLS_IN \n config rule \n edit 3 \n set match-community SLA_KO_MPLS \n set set-weight 100 \n set set-route-tag 2 \n next \n edit 100 \n set set-weight 200 \n set set-route-tag 1 \n next \n end \n next \n edit OL_INET_IN \n config rule \n edit 1 \n set match-community SLA_KO_INET \n set set-weight 100 \n set set-route-tag 2 \n next \n edit 100 \n set set-weight 200 \n set set-route-tag 1 \n next \n end \n next \n edit OL_MPLS_OUT \n config rule \n edit 1 \n set action deny \n set match-community SLA_OK_INET \n next \n edit 2 \n set action deny \n set match-community SLA_KO_INET \n next \n edit 100 \n next \n end \n next \n edit OL_INET_OUT \n config rule \n edit 1 \n set action deny \n set match-community SLA_OK_MPLS \n next \n edit 2\n set action deny \n set match-community SLA_KO_MPLS \n next \n edit 100 \n next \n end \n next \nend",
                        "target": "device_database"
                    }
                ]
            }
        ]
    }

    run_request(payload, name="Add Script - Hub Route Map")


##############################################################
# Add Script - Hub Router BGP
##############################################################
def addScript_Hub_Router_BGP():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/dvmdb/adom/" + ADOM + "/script",
                "data": [
                    {
                        "script_schedule": None,
                        "name": "Hub Router Bgp",
                        "type": "cli",
                        "desc": "",
                        "content": "config router bgp \n set as 65000 \n set keepalive-timer 5 \n set holdtime-timer 15 \n set ibgp-multipath enable \n set network-import-check disable \n set additional-path enable \n set scan-time 20 \n config neighbor-group \n edit OL_MPLS \n set soft-reconfiguration enable \n set advertisement-interval 1 \n set remote-as 65000 \n set route-map-in OL_MPLS_IN \n set route-map-out OL_MPLS_OUT \n set additional-path both \n set route-reflector-client enable \n next \n edit OL_INET \n set soft-reconfiguration enable \n set advertisement-interval 1 \n set remote-as 65000 \n set route-map-in OL_INET_IN \n set route-map-out OL_INET_OUT \n set additional-path both \n set route-reflector-client enable \n next \n end \n config neighbor-range \n edit 1 \n set prefix 10.0.10.0 255.255.255.0 \n set neighbor-group OL_MPLS \n next \n edit 2 \n set prefix 10.0.11.0 255.255.255.0 \n set neighbor-group OL_INET \n next \n end \n config network \n edit 1 \n set prefix 172.16.0.0 255.255.255.0 \n next \n end \nend",
                        "target": "device_database"
                    }
                ]
            }
        ]
    }

    run_request(payload, name="Add Script - Hub Router BGP")


##############################################################
# Add Script - Hub Router Policy
##############################################################
def addScript_Hub_Router_Policy():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/dvmdb/adom/" + ADOM + "/script",
                "data": [
                    {
                        "script_schedule": None,
                        "name": "Hub Router Policy",
                        "type": "cli",
                        "desc": "",
                        "content": "config router policy \nedit 1 \nset input-device OL_MPLS_0 \nset output-device OL_MPLS_0 \nnext \nedit 2 \nset input-device OL_INET_0 \nset output-device OL_INET_0 \nnext \n end",
                        "target": "device_database"
                    }
                ]
            }
        ]
    }

    run_request(payload, name="Add Script - Hub Router Policy")


##############################################################
# Add Script - Branches route map
##############################################################
def addScript_Branches_Route_Map():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/dvmdb/adom/" + ADOM + "/script",
                "data": [
                    {
                        "script_schedule": None,
                        "name": "Branches Route map",
                        "type": "cli",
                        "desc": "",
                        "content": "config router route-map \n edit SLA_OK_MPLS \n config rule \n edit 1 \n set set-community 65000:100 \n next \n end \n next \n edit SLA_KO_MPLS \n config rule \n edit 1 \n set set-community 65000:200 \n next \n end \n next \n edit SLA_OK_INET \n config rule \n edit 1 \n set set-community 65000:101 \n next \n end \n next \n edit SLA_KO_INET \n config rule \n edit 1 \n set set-community 65000:201 \n next \n end \n next \n end",
                        "target": "device_database"
                    }
                ]
            }
        ]
    }

    run_request(payload, name="Add Script - Branches route map")


##############################################################
# Add Script - Branches router static
##############################################################
def addScript_Branches_Router_Static():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/dvmdb/adom/" + ADOM + "/script",
                "data": [
                    {
                        "script_schedule": None,
                        "name": "Branch-static-route-sdwan",
                        "type": "cli",
                        "desc": "",
                        "content": "config router static\n edit 2\n set virtual-wan-link enable \n next\n end",
                        "target": "device_database"
                    }
                ]
            }
        ]
    }

    run_request(payload, name="Add Script - Branches router static")


##############################################################
# Add Script - Branch1 static route
##############################################################
def addScript_Branch1_Static_Route():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/dvmdb/adom/" + ADOM + "/script",
                "data": [
                    {
                        "script_schedule": None,
                        "name": "Branch1 static route",
                        "type": "cli",
                        "desc": "",
                        "content": "config router static \n edit 3 \n set dst 100.64.1.5 255.255.255.255 \n set gateway 192.2.0.2\n set device port1 \n end ",
                        "target": "device_database"
                    }
                ]
            }
        ]
    }

    run_request(payload, name="Add Script - Branch1 static route")


##############################################################
# Add Script - Branch2 static route
##############################################################
def addScript_Branch2_Static_Route():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/dvmdb/adom/" + ADOM + "/script",
                "data": [
                    {
                        "script_schedule": None,
                        "name": "Branch2 static route",
                        "type": "cli",
                        "desc": "",
                        "content": "config router static \n edit 3 \n set dst 100.64.1.5 255.255.255.255 \n set gateway 203.0.113.1\n set device port1 \n end ",
                        "target": "device_database"
                    }
                ]
            }
        ]
    }

    run_request(payload, name="Add Script - Branch2 static route")


##############################################################
# Add Script - Branch1 router bgp
##############################################################
def addScript_Branch1_Router_BGP():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/dvmdb/adom/" + ADOM + "/script",
                "data": [
                    {
                        "script_schedule": None,
                        "name": "Branch1 router bgp",
                        "type": "cli",
                        "desc": "",
                        "content": "config router bgp \n set as 65000 \n set keepalive-timer 5 \n set holdtime-timer 15 \n set ibgp-multipath enable \n set scan-time 20 \n config neighbor \n edit 10.0.10.5 \n set soft-reconfiguration enable \n set interface OL_MPLS_0 \n set remote-as 65000 \n set route-map-out SLA_KO_MPLS \n set route-map-out-preferable SLA_OK_MPLS \n set additional-path receive \n next \n edit 10.0.11.5 \n set soft-reconfiguration enable \n set interface OL_INET_0 \n set remote-as 65000 \n set route-map-out SLA_KO_INET \n set route-map-out-preferable SLA_OK_INET \n set additional-path receive \n next \n end \n config network \n edit 1 \n set prefix 10.0.1.0 255.255.255.0 \n next \n edit 2 \n set prefix 10.1.1.0 255.255.255.0 \n next \n end \nend",
                        "target": "device_database"
                    }
                ]
            }
        ]
    }

    run_request(payload, name="Add Script - Add Script - Branch1 router bgp")


##############################################################
# Add Script - Branch2 router bgp
##############################################################
def addScript_Branch2_Router_BGP():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/dvmdb/adom/" + ADOM + "/script",
                "data": [
                    {
                        "script_schedule": None,
                        "name": "Branch2 router bgp",
                        "type": "cli",
                        "desc": "",
                        "content": "config router bgp \n set as 65000 \n set keepalive-timer 5 \n set holdtime-timer 15 \n set ibgp-multipath enable \n set scan-time 20 \n config neighbor \n edit 10.0.10.5 \n set soft-reconfiguration enable \n set interface OL_MPLS_0 \n set remote-as 65000 \n set route-map-out SLA_KO_MPLS \n set route-map-out-preferable SLA_OK_MPLS \n set additional-path receive \n next \n edit 10.0.11.5 \n set soft-reconfiguration enable \n set interface OL_INET_0 \n set remote-as 65000 \n set route-map-out SLA_KO_INET \n set route-map-out-preferable SLA_OK_INET \n set additional-path receive \n next \n end \n config network \n edit 1 \n set prefix 10.0.2.0 255.255.255.0 \n next \n edit 2 \n set prefix 10.1.2.0 255.255.255.0 \n next \n end \nend",
                        "target": "device_database"
                    }
                ]
            }
        ]
    }

    run_request(payload, name="Add Script - Branch2 router bgp")
"""

session = None


def main():

    # Login
    ##############################################################
    login()
    print("     Session Id = " + session)

    # 1,2,3 - Discover / Probe Devices FGT
    ##############################################################
    sn_fgt_1 = probeFortiGateDevice(BRANCH1_IP)
    print("     SN FGT 1 = " + sn_fgt_1)

    sn_fgt_2 = probeFortiGateDevice(BRANCH2_IP)
    print("     SN FGT 2 = " + sn_fgt_2)

    sn_fgt_dc = probeFortiGateDevice(DATACENTER_IP)
    print("     SN FGT DC = " + sn_fgt_dc)

    # 4 - Add Devices
    ##############################################################
    addDevices(sn_fgt_1, sn_fgt_2, sn_fgt_dc)

    # 4.1 - Add Devices
    ##############################################################
    sn_fmg = getFmgSerialNumber()
    print("     SN FMG = " + sn_fmg)

    # 4.2 - Add Script - FAZ Configuration
    ##############################################################
    addScript_FAZConfiguration()

    # 4.3 - Exec Script - FAZ Configuration
    ##############################################################
    execScript_FAZConfiguration()

    # 5 - Add Dynamic Interface
    ##############################################################
    addDynamicInterface()

    # 6 - Add VPN Manager VPN Table
    ##############################################################
    addVPNManagerVPNTable()

    # 7 - Add VPN Manager Node
    ##############################################################
    addVPNManagerNode()

    # 8 - Add Policy Package
    ##############################################################
    addPolicyPackage()

    # 9 - Add Firewall Policy - Branches PP - No Interfaces
    ##############################################################
    addFirewallPolicy_Branches_PP_No_Interfaces()

    # 10 - Add Firewall Policy - DataCenter PP - No Interfaces
    ##############################################################
    addFirewallPolicy_DataCenter_PP_No_Interfaces()

    # 11 - Install policy - Hub
    ##############################################################
    installPolicy_Hub()

    # 12 - Install policy - Branches
    ##############################################################
    installPolicy_Branches()

    # 13 - Configure FGT-1 Interfaces
    ##############################################################
    configureInterfacesFGT1()

    # 14 - Configure FGT-2 Interfaces
    ##############################################################
    configureInterfacesFGT2()

    # 15 - Configure FGT-DC Interfaces
    ##############################################################
    configureInterfacesFGTDC()

    # 16 - Add Script - Fix VPN in Branches
    ##############################################################
    addScript_FixVPNinBranches()

    # 17 - Add Script - Fix VPN in Hub
    ##############################################################
    addScript_FixVPNinHub()

    # 18 - Exec Script - Fix VPN in Branches
    ##############################################################
    execScript_FixVPNinBranches()

    # 19 - Exec Script - Fix VPN in Hub
    ##############################################################
    execScript_FixVPNinHub()

    # 20 - Add Dynamic Interface - Overlays
    ##############################################################
    addDynamicInterface_Overlays()

    # 21 - Add Firewall Policy - Branches PP
    ##############################################################
    addFirewallPolicy_BranchesPP()

    # 22 - Add Firewall Policy - DataCenter PP
    ##############################################################
    addFirewallPolicy_DataCenterPP()

    # 22.1 - Add Dynamic Routing CLI Template - Hub
    ##############################################################
    addDynamicRoutingCLITemplate_Hub()

    # 22.2 - Add Dynamic Routing CLI Template - Branches
    ##############################################################
    addDynamicRoutingCLITemplate_Branches()

    # 23 - This one is like 11
    ##############################################################
    installPolicy_Hub()

    # 24 - This one is like 12
    ##############################################################
    installPolicy_Branches()

    """
    ##############################################################
    # 25 - Add Script - Hub Community-list
    ##############################################################
    addScript_Hub_Community_list()

    ##############################################################
    # 26 - Add Script - Hub Route Map
    ##############################################################
    addScript_Hub_Route_Map()

    ##############################################################
    # 27 - Add Script - Hub Router BGP
    ##############################################################
    addScript_Hub_Router_BGP()

    ##############################################################
    # 28 - Add Script - Hub Router Policy
    ##############################################################
    addScript_Hub_Router_Policy()

    ##############################################################
    # 30 - Add Script - Branches route map
    ##############################################################
    addScript_Branches_Route_Map()

    ##############################################################
    # 31 - Add Script - Branches router static
    ##############################################################
    addScript_Branches_Router_Static()

    ##############################################################
    # 32 - Add Script - Branch1 static route
    ##############################################################
    addScript_Branch1_Static_Route()

    ##############################################################
    # 33 - Add Script - Branch2 static route
    ##############################################################
    addScript_Branch2_Static_Route()

    ##############################################################
    # 34 - Add Script - Branch1 router bgp
    ##############################################################
    addScript_Branch1_Router_BGP()

    ##############################################################
    # 35 - Add Script - Branch2 router bgp
    ##############################################################
    addScript_Branch2_Router_BGP()
    """

if __name__ == "__main__":
    main()
