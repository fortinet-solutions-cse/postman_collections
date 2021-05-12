#!/usr/bin/env python3

from fmg_api.api_base import ApiSession

class DeviceManagerApi(ApiSession):

    ##############################################################
    # Get List of Managed Devices
    # - Returns a list of device names
    ##############################################################
    def getDevices(self):

        payload = {
            "session": self._session,
            "id": 1,
            "method": "get",
            "params": [
                {
                    "url": "/dvmdb/adom/" + self.adom + "/device",
                }
            ]
        }

        content = self._run_request(payload, name="Get Devices")
        return [ dev['name'] for dev in content["result"][0]["data"] ]


    ##############################################################
    # Set Device Attributes
    # - Receives a list of dicts, each dict describes a device
    # - Each dict can be:
    #   {
    #     'name': device_name,
    #     'location': { 'latitude': latitude, 'longitude': longitude },  <<< optional
    #     'vars': { 'var1': val1, 'var2': val2, ... }                   <<< meta fields
    #   }
    ##############################################################
    def setDeviceAttributes(self, dev_attr_list):

        set_dev_list = []
        for dev in dev_attr_list:
            set_dev_list.append({
                "name": dev['name'],
                "latitude": str(dev['location']['latitude']) if 'location' in dev else "",
                "longitude": str(dev['location']['longitude'] if 'location' in dev else ""),
                "meta fields": { k: str(v) for k, v in dev['vars'].items() }
            })

        payload = {
            "session": self._session,
            "id": 1,
            "method": "set",
            "params": [
                {
                    "url": "/dvmdb/adom/" + self.adom + "/device",
                    "data": set_dev_list
                }
            ]
        }

        self._run_request(payload, name="Set Device Attributes")


    ##############################################################
    # Assign CLI Template Group
    # - Receives a name of CLI Template Group and a list of device names
    ##############################################################
    def assignCLITemplateGroup(self, group_name, dev_list):

        assigned_dev_list = []
        for dev in dev_list:
            assigned_dev_list.append(
                {
                    "name": dev,
                    "vdom": "root"
                }
            )

        payload = {
            "session": self._session,
            "id": 1,
            "method": "add",
            "params": [
                {
                    "url": "/pm/config/adom/" + self.adom + "/obj/cli/template-group/" + group_name + "/scope member",
                    "data": assigned_dev_list
                }
            ]
        }

        self._run_request(payload, name=f"Assign CLI Template Group ({group_name})")


    ##############################################################
    # Add to Device Group
    # - Receives a name of Device Group and a list of device names
    ##############################################################
    def addToDeviceGroup(self, group_name, dev_list):

        assigned_dev_list = []
        for dev in dev_list:
            assigned_dev_list.append(
                {
                    "name": dev,
                    "vdom": "root"
                }
            )

        payload = {
            "session": self._session,
            "id": 1,
            "method": "add",
            "params": [
                {
                    "url": "/dvmdb/adom/" + self.adom + "/group/" + group_name + "/object member",
                    "data": assigned_dev_list
                }
            ]
        }

        self._run_request(payload, name=f"Add to Device Group ({group_name})")


    ##############################################################
    # Install Policy
    ##############################################################
    def installPolicy(self, package_name, target_group):

        payload = {
            "session": self._session,
            "id": 1,
            "method": "exec",
            "params": [
                {
                    "url": "/securityconsole/install/package",
                    "data": {
                        "adom": self.adom,
                        "pkg": package_name,
                        "scope": [
                            {
                                "name": target_group
                            }
                        ],
                        "flags": "none"
                    }
                }
            ]
        }

        self._run_request_async(payload, name=f"Install Policy ({package_name})")


    ##############################################################
    # Install Configuration
    ##############################################################
    def installConfiguration(self, dev_list, vdom_global=False):

        dev_scope = []
        for dev in dev_list:
            dev_scope.append(
                {
                    "name": dev,
                    "vdom": "global" if vdom_global else "root"
                }
            )


        payload = {
            "session": self._session,
            "id": 1,
            "method": "exec",
            "params": [
                {
                    "url": "/securityconsole/install/device",
                    "data": {
                        "adom": self.adom,
                        "scope": dev_scope,
                        "flags": "none"
                    }
                }
            ]
        }

        self._run_request_async(payload, name=f"Install Configuration")
