#!/usr/bin/env python3

import requests
import json

from urllib3.exceptions import InsecureRequestWarning
from time import sleep
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class ApiSession:

    _session = None
    __request_number = 0

    def __init__(self, url, adom, user, password):
        self.url = url
        self.adom = adom
        self.login(user, password)

    def __is_task_finished(self, id):

        payload = {
            "session": self._session,
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

        response = requests.request("POST", self.url, data=json.dumps(
            payload), headers=headers, verify=False)

        if not self.__is_request_status_ok(response):
            print(" \033[31Error in request.\033[39m")
            print(response.text)
            raise Exception(response.text)

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


    @staticmethod
    def __is_request_status_ok(response):
        content = json.loads(response.content)

        return response.status_code == 200 and \
            content["result"][0]["status"]["code"] == 0 and \
            content["result"][0]["status"]["message"] == "OK"


    def _run_request(self, payload, name=""):
        print("Running request \033[33m" + str(self.__request_number) +
              "\033[39m. \033[93m" + name + "\033[39m")
        self.__request_number += 1

        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }

        response = requests.request("POST", self.url, data=json.dumps(
            payload), headers=headers, verify=False)

        if not ApiSession.__is_request_status_ok(response):
            print(" Error in request.")
            print(response.text)
            raise Exception(response.text)

        content = json.loads(response.content)

        print(" \033[92mCompleted\033[39m")
        return content


    def _run_request_async(self, payload, name=""):
        print("Running request \033[33m" + str(self.__request_number) +
              "\033[39m. \033[93m" + name + "\033[39m")
        self.__request_number += 1

        headers = {
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }

        response = requests.request("POST", self.url, data=json.dumps(
            payload), headers=headers, verify=False)

        if not ApiSession.__is_request_status_ok(response):
            print(" Error in request.")
            print(response.text)
            raise Exception(response.text)

        content = json.loads(response.content)
        try:
            task_id = content["result"][0]["data"]["taskid"]
        except:
            task_id = content["result"][0]["data"]["task"]

        print(" Asynchronous task created: " +
              str(task_id) + " ", end="", flush=False)
        while not self.__is_task_finished(task_id):
            print(".", end="", flush=True)
            sleep(5)

        print("\n \033[92mCompleted\033[39m")
        return content

    ##############################################################
    # Login
    ##############################################################
    def login(self, user, password):

        payload = {
            "session": 1,
            "id": 1,
            "method": "exec",
            "params": [
                {
                    "url": "sys/login/user",
                    "data": [
                        {
                            "user": user,
                            "passwd": password
                        }
                    ]
                }
            ]
        }

        content = self._run_request(payload, "Login")
        self._session = content["session"]
