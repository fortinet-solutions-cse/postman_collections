#!/usr/bin/env python3

import requests, json

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

user = "admin"
passwd = ""
url = "https://34.77.13.219:10419/jsonrpc"


##############################################################
# Login
##############################################################

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

# TODO: get session only on succesful login

content = json.loads(response.content)
print(content)
session = content["session"]


##############################################################
# 1
##############################################################


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

# TODO: exit if not on succesful login

content = json.loads(response.content)
sn_fgt_1 = content["result"][0]["data"]["device"]["sn"]

print(sn_fgt_1)

##############################################################
# 2
##############################################################


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

# TODO: exit if not on succesful login

content = json.loads(response.content)
sn_fgt_2 = content["result"][0]["data"]["device"]["sn"]

print(sn_fgt_2)

##############################################################
# 3
##############################################################


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

# TODO: exit if not on succesful login

content = json.loads(response.content)
sn_fgt_dc = content["result"][0]["data"]["device"]["sn"]

print(sn_fgt_dc)


#DEBUG
sn_fgt_1 = FGVM08TM19003292
sn_fgt_2
sn_fgt_dc
##############################################################
# 3
##############################################################

payload = {
    "session": "{{session}}",
    "id": 1,
    "method": "exec",
    "params": [
        {
            "url": "/dvm/cmd/add/dev-list",
            "data": {
                "adom": "{{adom}}",
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

print(response.text)