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

content = json.loads(response.content)
print(content)

# TODO: get session only on succesful login
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

print(response.text)

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

print(response.text)

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

print(response.text)