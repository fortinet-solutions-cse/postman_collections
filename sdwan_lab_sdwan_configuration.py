#!/usr/bin/env python3

import requests
import json

from urllib3.exceptions import InsecureRequestWarning
from time import sleep
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

USER = "admin"
PASSWD = "fortinet"
URL = "https://PUT-FMG-IP-HERE:10411//jsonrpc" # Set correct FMG IP:port here!
ADOM = "DEMO"
BRANCH1_IP = "172.16.1.1"
BRANCH2_IP = "172.16.1.2"
DATACENTER_IP = "172.16.2.5"
BRANCH1_NAME = "" # This will be discovered automatically by the script
BRANCH2_NAME = "" # This will be discovered automatically by the script
DATACENTER_NAME = "" # This will be discovered automatically by the script

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
    sn_fgt = content["result"][0]["data"]["device"]["sn"]
    name_fgt = content["result"][0]["data"]["device"]["hostname"]
    return sn_fgt, name_fgt


##############################################################
# Enable SD-WAN in ADOM
##############################################################
def enableSDWANinADOM():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/dvmdb/adom/",
                "data":
                {
                    "flags": ["central_sdwan"],
                    "name": ADOM
                }

            }
        ]
    }

    run_request(payload, name="Enable SD-WAN in ADOM")


##############################################################
# Create SD-WAN Interface OL_INET
##############################################################
def createSDWANInterfaceOLINET():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/pm/config/adom/" + ADOM + "/obj/dynamic/virtual-wan-link/members/OL_INET",
                "data": {
                    "name": "OL_INET",
                    "comment": None,
                    "interface": "OL_INET_0",
                    "gateway": "0.0.0.0",
                    "cost": 0,
                    "weight": 1,
                    "volume-ratio": 1,
                    "dynamic_mapping": [
                        {
                            "_scope": [
                                {
                                    "name": BRANCH2_NAME,
                                    "vdom": "root"
                                }
                            ],
                            "interface": "OL_INET_0",
                            "gateway": "10.0.11.5",
                            "weight": 1,
                            "cost": 0,
                            "volume-ratio": 1,
                            "gateway6": "::",
                            "ingress-spillover-threshold": 0,
                            "priority": 0,
                            "source": "0.0.0.0",
                            "source6": "::",
                            "spillover-threshold": 0,
                            "status": 1
                        },
                        {
                            "_scope": [
                                {
                                    "name": BRANCH1_NAME,
                                    "vdom": "root"
                                }
                            ],
                            "interface": "OL_INET_0",
                            "gateway": "10.0.11.5",
                            "weight": 1,
                            "cost": 0,
                            "volume-ratio": 1,
                            "gateway6": "::",
                            "ingress-spillover-threshold": 0,
                            "priority": 0,
                            "source": "0.0.0.0",
                            "source6": "::",
                            "spillover-threshold": 0,
                            "status": 1
                        },
                        {
                            "_scope": [
                                {
                                    "name": DATACENTER_NAME,
                                    "vdom": "root"
                                }
                            ],
                            "interface": "OL_INET_0",
                            "gateway": "0.0.0.0",
                            "weight": 1,
                            "cost": 0,
                            "volume-ratio": 1,
                            "gateway6": "::",
                            "ingress-spillover-threshold": 0,
                            "priority": 0,
                            "source": "0.0.0.0",
                            "source6": "::",
                            "spillover-threshold": 0,
                            "status": 1
                        }
                    ],
                    "gateway6": "::",
                    "ingress-spillover-threshold": 0,
                    "priority": 20,
                    "source": "0.0.0.0",
                    "source6": "::",
                    "spillover-threshold": 0,
                    "status": 1
                }
            }
        ]
    }
    run_request(payload, name="Create SD-WAN Interface OL_INET")


##############################################################
# Create SD-WAN Interface OL_MPLS
##############################################################
def createSDWANInterfaceOLMPLS():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/pm/config/adom/" + ADOM + "/obj/dynamic/virtual-wan-link/members/OL_MPLS",
                "data": {
                    "name": "OL_MPLS",
                    "comment": None,
                    "interface": "OL_MPLS_0",
                    "gateway": "10.0.10.5",
                    "cost": 0,
                    "weight": 1,
                    "volume-ratio": 1,
                    "dynamic_mapping": [
                        {
                            "_scope": [
                                {
                                    "name": DATACENTER_NAME,
                                    "vdom": "root"
                                }
                            ],
                            "interface": "OL_MPLS_0",
                            "gateway": "0.0.0.0",
                            "weight": 1,
                            "cost": 0,
                            "volume-ratio": 1,
                            "gateway6": "::",
                            "ingress-spillover-threshold": 0,
                            "priority": 0,
                            "source": "0.0.0.0",
                            "source6": "::",
                            "spillover-threshold": 0,
                            "status": 1
                        }
                    ],
                    "gateway6": "::",
                    "ingress-spillover-threshold": 0,
                    "priority": 20,
                    "source": "0.0.0.0",
                    "source6": "::",
                    "spillover-threshold": 0,
                    "status": 1
                }
            }
        ]
    }

    run_request(payload, name="Create SD-WAN Interface OL_MPLS")


##############################################################
# Create SD-WAN Interface Port1
##############################################################
def createSDWANInterfacePort1():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/pm/config/adom/" + ADOM + "/obj/dynamic/virtual-wan-link/members/port1",
                "data": {
                    "name": "port1",
                    "comment": None,
                    "interface": "port1",
                    "gateway": "0.0.0.0",
                    "cost": 0,
                    "weight": 1,
                    "volume-ratio": 1,
                    "dynamic_mapping": [
                        {
                            "_scope": [
                                {
                                    "name": BRANCH1_NAME,
                                    "vdom": "root"
                                }
                            ],
                            "interface": "port1",
                            "gateway": "192.2.0.2",
                            "weight": 1,
                            "cost": 0,
                            "volume-ratio": 1,
                            "gateway6": "::",
                            "ingress-spillover-threshold": 0,
                            "priority": 0,
                            "source": "0.0.0.0",
                            "source6": "::",
                            "spillover-threshold": 0,
                            "status": 1
                        },
                        {
                            "_scope": [
                                {
                                    "name": BRANCH2_NAME,
                                    "vdom": "root"
                                }
                            ],
                            "interface": "port1",
                            "gateway": "203.0.113.1",
                            "weight": 1,
                            "cost": 0,
                            "volume-ratio": 1,
                            "gateway6": "::",
                            "ingress-spillover-threshold": 0,
                            "priority": 0,
                            "source": "0.0.0.0",
                            "source6": "::",
                            "spillover-threshold": 0,
                            "status": 1
                        }
                    ],
                    "gateway6": "::",
                    "ingress-spillover-threshold": 0,
                    "priority": 10,
                    "source": "0.0.0.0",
                    "source6": "::",
                    "spillover-threshold": 0,
                    "status": 1
                }
            }
        ]
    }
    run_request(payload, name="Create SD-WAN Interface Port1")


##############################################################
# Create Health Check Servers
##############################################################
def createHealthCheckServers():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/pm/config/adom/" + ADOM + "/obj/dynamic/virtual-wan-link/server",
                "data": [
                    {
                        "name": "DC Host",
                        "description": None,
                        "server": [
                            "172.16.0.7"
                        ],
                        "dynamic_mapping": None
                    },
                    {
                        "name": "Internet Host",
                        "description": None,
                        "server": [
                            "www.fortinet.com"
                        ],
                        "dynamic_mapping": None
                    }
                ]
            }
        ]
    }

    run_request(payload, name="Create Health Check Servers")


##############################################################
# Create BGP Neighbors
##############################################################
def createBGPNeighbors():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/pm/config/adom/" + ADOM + "/obj/dynamic/virtual-wan-link/neighbor",
                "data": [
                    {
                        "name": "OL_INET",
                        "description": None,
                        "ip": "10.0.11.5",
                        "role": 3,
                        "dynamic_mapping": None
                    },
                    {
                        "name": "OL_MPLS",
                        "description": None,
                        "ip": "10.0.10.5",
                        "role": 3,
                        "dynamic_mapping": None
                    }
                ]
            }
        ]
    }

    run_request(payload, name="Create BGP Neighbors")


##############################################################
# Create SD-WAN Branch Template
##############################################################
def createSDWANBranchTemplate():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/pm/wanprof/adom/" + ADOM + "/",
                "data": {
                    "name": "Branch-Template",
                    "type": "wanprof"

                }
            }

        ]
    }

    run_request(payload, name="Create SD-WAN Branch Template")


##############################################################
# Populate SD-WAN Branch Template
##############################################################
def populateSDWANBranchTemplate():

    payload = {
        "session": session,
        "id": 1,
        "method": "replace",
        "params": [
            {
                "url": "/pm/config/adom/" + ADOM + "/wanprof/Branch-Template/system/virtual-wan-link",
                "data": {
                    "status": 1,
                    "load-balance-mode": 1,
                    "fail-detect": "disable",
                    "neighbor-hold-boot-time": 0,
                    "neighbor-hold-down": 0,
                    "neighbor-hold-down-time": 0,
                    "neighbor": [
                        {
                            "health-check": [
                                "Datacenter"
                            ],
                            "ip": [
                                "OL_INET"
                            ],
                            "member": [
                                1
                            ],
                            "role": 3,
                            "sla-id": 1
                        },
                        {
                            "health-check": [
                                "Datacenter"
                            ],
                            "ip": [
                                "OL_MPLS"
                            ],
                            "member": [
                                2
                            ],
                            "role": 3,
                            "sla-id": 1
                        }
                    ],
                    "members": [
                        {
                            "_dynamic-member": [
                                "OL_INET"
                            ],
                            "cost": 0,
                            "gateway": "0.0.0.0",
                            "gateway6": "::",
                            "ingress-spillover-threshold": 0,
                            "interface": [],
                            "priority": 0,
                            "source": "0.0.0.0",
                            "source6": "::",
                            "spillover-threshold": 0,
                            "status": 1,
                            "volume-ratio": 1,
                            "weight": 1
                        },
                        {
                            "_dynamic-member": [
                                "OL_MPLS"
                            ],
                            "cost": 0,
                            "gateway": "0.0.0.0",
                            "gateway6": "::",
                            "ingress-spillover-threshold": 0,
                            "interface": [],
                            "priority": 0,
                            "source": "0.0.0.0",
                            "source6": "::",
                            "spillover-threshold": 0,
                            "status": 1,
                            "volume-ratio": 1,
                            "weight": 1
                        },
                        {
                            "_dynamic-member": [
                                "port1"
                            ],
                            "cost": 0,
                            "gateway": "0.0.0.0",
                            "gateway6": "::",
                            "ingress-spillover-threshold": 0,
                            "interface": [],
                            "priority": 0,
                            "source": "0.0.0.0",
                            "source6": "::",
                            "spillover-threshold": 0,
                            "status": 1,
                            "volume-ratio": 1,
                            "weight": 1
                        }
                    ],
                    "service": [
                        {
                            "addr-mode": 7,
                            "default": 0,
                            "dscp-forward": 0,
                            "dscp-forward-tag": "000000",
                            "dscp-reverse": 0,
                            "dscp-reverse-tag": "000000",
                            "dst": [
                                "all"
                            ],
                            "dst-negate": 0,
                            "end-port": 65535,
                            "gateway": 0,
                            "groups": [],
                            "hold-down-time": 0,
                            "id": 1,
                            "input-device": [],
                            "internet-service": 0,
                            "link-cost-threshold": 10,
                            "mode": 4,
                            "name": "ICMP",
                            "priority-members": [
                                "1",
                                "2"
                            ],
                            "protocol": 1,
                            "role": 3,
                            "route-tag": 0,
                            "sla": [
                                {
                                    "health-check": "Datacenter",
                                    "id": 1
                                }
                            ],
                            "sla-compare-method": 0,
                            "src": [
                                "all"
                            ],
                            "src-negate": 0,
                            "standalone-action": 0,
                            "start-port": 1,
                            "status": 1,
                            "tos": "0x00",
                            "tos-mask": "0x00",
                            "users": []
                        }
                    ],
                    "health-check": [
                        {
                            "name": "Datacenter",
                            "_dynamic-server": [
                                "DC Host"
                            ],
                            "protocol": 1,
                            "port": 80,
                            "members": [
                                1,
                                2
                            ],
                            "failtime": 5,
                            "recoverytime": 5,
                            "security-mode": 0,
                            "update-cascade-interface": 1,
                            "update-static-route": 1,
                            "sla": [
                                {
                                    "id": 1,
                                    "jitter-threshold": 5,
                                    "latency-threshold": 50,
                                    "link-cost-factor": 7,
                                    "packetloss-threshold": 0
                                }
                            ],
                            "addr-mode": 7,
                            "ha-priority": 1,
                            "http-agent": "Chrome/ Safari/",
                            "http-get": "/",
                            "interval": 500,
                            "packet-size": 64,
                            "probe-packets": 1,
                            "sla-fail-log-period": 0,
                            "sla-pass-log-period": 0,
                            "threshold-alert-jitter": 0,
                            "threshold-alert-latency": 0,
                            "threshold-alert-packetloss": 0,
                            "threshold-warning-jitter": 0,
                            "threshold-warning-latency": 0,
                            "threshold-warning-packetloss": 0
                        }
                    ]
                }
            }
        ]
    }

    run_request(payload, name="Populate SD-WAN Branch Template")


##############################################################
# Assign Template to Branches
##############################################################
def assignTemplateToBranches():

    payload = {
        "session": session,
        "id": 1,
        "method": "update",
        "params": [
            {
                "url": "/pm/wanprof/adom/" + ADOM + "/Branch-Template",
                "data": {
                    "name": "Branch-Template",
                    "description": "",
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
                    "type": "wanprof"
                }
            }
        ]
    }

    run_request(payload, name="Assign Template to Branches")


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
# Add Script - Branch Static Route SDWAN
##############################################################
def addScript_BranchStaticRouteSDWAN():

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
                        "content": "# Branch static Router \n\
config router static\n\
  edit 2\n\
    set virtual-wan-link enable\n\
  next\n\
end",
                        "target": "device_database"
                    }
                ]
            }
        ]
    }

    run_request(payload, name="Add Script - Branch Static Route SDWAN")


##############################################################
# Exec Script - Branch Static Route SD-WAN
##############################################################
def execScript_BranchStaticRouteSDWAN():

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
                    "script": "Branch-static-route-sdwan",
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

    run_request_async(payload, name="Exec Script - Branch Static Route SD-WAN")


##############################################################
# Create SD-WAN Hub Template
##############################################################
def createSDWANHubTemplate():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/pm/wanprof/adom/" + ADOM + "/",
                "data": {
                    "name": "Hub-Template",
                    "type": "wanprof"

                }
            }

        ]
    }

    run_request(payload, name="Create SD-WAN Hub Template")


##############################################################
# Populate SD-WAN Hub Template
##############################################################
def populateSDWANHubTemplate():

    payload = {
        "session": session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/pm/config/adom/" + ADOM + "/wanprof/Hub-Template/system/virtual-wan-link",
                "data": {
                    "fail-detect": 0,
                    "health-check": None,
                    "load-balance-mode": 1,
                    "members": [
                        {
                            "_dynamic-member": [
                                "OL_INET"
                            ],
                            "cost": 0,
                            "gateway": "0.0.0.0",
                            "gateway6": "::",
                            "ingress-spillover-threshold": 0,
                            "priority": 0,
                            "source": "0.0.0.0",
                            "source6": "::",
                            "spillover-threshold": 0,
                            "status": 1,
                            "volume-ratio": 1,
                            "weight": 1
                        },
                        {
                            "_dynamic-member": [
                                "OL_MPLS"
                            ],
                            "cost": 0,
                            "gateway": "0.0.0.0",
                            "gateway6": "::",
                            "ingress-spillover-threshold": 0,
                            "priority": 0,
                            "source": "0.0.0.0",
                            "source6": "::",
                            "spillover-threshold": 0,
                            "status": 1,
                            "volume-ratio": 1,
                            "weight": 1
                        }
                    ],
                    "neighbor": None,
                    "neighbor-hold-boot-time": 0,
                    "neighbor-hold-down": 0,
                    "neighbor-hold-down-time": 0,
                    "service": [
                        {
                            "addr-mode": 7,
                            "default": 0,
                            "dscp-forward": 0,
                            "dscp-forward-tag": "000000",
                            "dscp-reverse": 0,
                            "dscp-reverse-tag": "000000",
                            "dst": [
                                "all"
                            ],
                            "dst-negate": 0,
                            "end-port": 65535,
                            "gateway": 0,
                            "groups": [],
                            "hold-down-time": 0,
                            "id": 1,
                            "input-device": [],
                            "internet-service": 0,
                            "link-cost-threshold": 10,
                            "member": [
                                "1"
                            ],
                            "mode": 1,
                            "name": "SLA_OK_INET",
                            "protocol": 0,
                            "role": 3,
                            "route-tag": 1,
                            "sla": None,
                            "src": [
                                "LAN_HUB"
                            ],
                            "src-negate": 0,
                            "standalone-action": 0,
                            "start-port": 1,
                            "status": 1,
                            "tos": "0x00",
                            "tos-mask": "0x00",
                            "users": []
                        },
                        {
                            "addr-mode": 7,
                            "default": 0,
                            "dscp-forward": 0,
                            "dscp-forward-tag": "000000",
                            "dscp-reverse": 0,
                            "dscp-reverse-tag": "000000",
                            "dst": [
                                "all"
                            ],
                            "dst-negate": 0,
                            "end-port": 65535,
                            "gateway": 0,
                            "groups": [],
                            "hold-down-time": 0,
                            "id": 2,
                            "input-device": [],
                            "internet-service": 0,
                            "link-cost-threshold": 10,
                            "member": [
                                "2"
                            ],
                            "mode": 1,
                            "name": "SLA_OK_MPLS",
                            "protocol": 0,
                            "role": 3,
                            "route-tag": 1,
                            "sla": None,
                            "src": [
                                "LAN_HUB"
                            ],
                            "src-negate": 0,
                            "standalone-action": 0,
                            "start-port": 1,
                            "status": 1,
                            "tos": "0x00",
                            "tos-mask": "0x00",
                            "users": []
                        },
                        {
                            "addr-mode": 7,
                            "default": 0,
                            "dscp-forward": 0,
                            "dscp-forward-tag": "000000",
                            "dscp-reverse": 0,
                            "dscp-reverse-tag": "000000",
                            "dst": [
                                "all"
                            ],
                            "dst-negate": 0,
                            "end-port": 65535,
                            "gateway": 0,
                            "groups": [],
                            "hold-down-time": 0,
                            "id": 3,
                            "input-device": [],
                            "internet-service": 0,
                            "link-cost-threshold": 10,
                            "member": [
                                "1"
                            ],
                            "mode": 1,
                            "name": "SLA_KO_INET",
                            "protocol": 0,
                            "role": 3,
                            "route-tag": 2,
                            "sla": None,
                            "src": [
                                "LAN_HUB"
                            ],
                            "src-negate": 0,
                            "standalone-action": 0,
                            "start-port": 1,
                            "status": 1,
                            "tos": "0x00",
                            "tos-mask": "0x00",
                            "users": []
                        },
                        {
                            "addr-mode": 7,
                            "default": 0,
                            "dscp-forward": 0,
                            "dscp-forward-tag": "000000",
                            "dscp-reverse": 0,
                            "dscp-reverse-tag": "000000",
                            "dst": [
                                "all"
                            ],
                            "dst-negate": 0,
                            "end-port": 65535,
                            "gateway": 0,
                            "groups": [],
                            "hold-down-time": 0,
                            "id": 4,
                            "input-device": [],
                            "internet-service": 0,
                            "link-cost-threshold": 10,
                            "member": [
                                "2"
                            ],
                            "mode": 1,
                            "name": "SLA_KO_MPLS",
                            "protocol": 0,
                            "role": 3,
                            "route-tag": 2,
                            "sla": None,
                            "src": [
                                "LAN_HUB"
                            ],
                            "src-negate": 0,
                            "standalone-action": 0,
                            "start-port": 1,
                            "status": 1,
                            "tos": "0x00",
                            "tos-mask": "0x00",
                            "users": []
                        }
                    ],
                    "status": 1
                }
            }
        ]
    }

    run_request(payload, name="Populate SD-WAN Hub Template")


##############################################################
# Assign Template to Hub
##############################################################
def assignTemplateToHub():

    payload = {
        "session": session,
        "id": 1,
        "method": "update",
        "params": [
            {
                "url": "/pm/wanprof/adom/" + ADOM + "/Hub-Template",
                "data": {
                    "name": "Hub-Template",
                    "description": "",
                    "scope member": [
                        {
                            "name": DATACENTER_NAME,
                            "vdom": "root"
                        }
                    ],
                    "type": "wanprof"
                }
            }
        ]
    }

    run_request(payload, name="Assign Template to Hub")


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


session = None


def main():

    global BRANCH1_NAME, BRANCH2_NAME, DATACENTER_NAME

    # Login
    ##############################################################
    login()
    print("     Session Id = " + session)

    # Discover / Probe Devices FGT
    ##############################################################
    sn_fgt_1, BRANCH1_NAME = probeFortiGateDevice(BRANCH1_IP)
    print("     SN FGT 1 = " + sn_fgt_1 + " Name: " + BRANCH1_NAME)

    sn_fgt_2, BRANCH2_NAME = probeFortiGateDevice(BRANCH2_IP)
    print("     SN FGT 2 = " + sn_fgt_2 + " Name: " + BRANCH2_NAME)

    sn_fgt_dc, DATACENTER_NAME = probeFortiGateDevice(DATACENTER_IP)
    print("     SN FGT DC = " + sn_fgt_dc + " Name: " + DATACENTER_NAME)

    # Enable SD-WAN in ADOM
    ##############################################################
    enableSDWANinADOM()

    # Create SD-WAN Interface OL_INET
    ##############################################################
    createSDWANInterfaceOLINET()

    # Create SD-WAN Interface OL_MPLS
    ##############################################################
    createSDWANInterfaceOLMPLS()

    # Create SD-WAN Interface Port1
    ##############################################################
    createSDWANInterfacePort1()

    # Create Health Check Servers
    ##############################################################
    createHealthCheckServers()

    # Create BGP Neighbours
    ##############################################################
    createBGPNeighbors()

    # Create SD-WAN Branch Template
    ##############################################################
    createSDWANBranchTemplate()

    # Populate SD-WAN Branch Template
    ##############################################################
    populateSDWANBranchTemplate()

    # Assign Template to Branches
    ##############################################################
    assignTemplateToBranches()

    # Install policy - Branches
    ##############################################################
    installPolicy_Branches()

    # Add Script - Branch Static Route SDWAN
    ##############################################################
    addScript_BranchStaticRouteSDWAN()

    # Exec Script - Branch Static Route SDWAN
    ##############################################################
    execScript_BranchStaticRouteSDWAN()

    # Install policy - Branches
    ##############################################################
    installPolicy_Branches()

    # Create SD-WAN Hub Template
    ##############################################################
    createSDWANHubTemplate()

    # Populate SD-WAN Hub Template
    ##############################################################
    populateSDWANHubTemplate()

    # Assign Template to Hub
    ##############################################################
    assignTemplateToHub()

    # Install policy - Hub
    ##############################################################
    installPolicy_Hub()


if __name__ == "__main__":
    main()
