#!/usr/bin/env python3

from fmg_api.device_manager import DeviceManagerApi
from demo_base import *

def main():

    cfg = readConfig()

    session = DeviceManagerApi(
        url = cfg['fmg_api'],
        adom = cfg['adom'],
        user = cfg['fmg_user'],
        password = cfg['fmg_password']
    )

    managed_dev_list = session.getDevices()
    print("    Currently Managed Devices: " + str(len(managed_dev_list)))

    dev_attr_list = []
    for dev in managed_dev_list:
        print("    Processing " + dev)
        vars = {}

        # Add global meta vars
        for i in cfg['global']:
            vars[i] = cfg['global'][i]

        # Add per-device meta vars
        if dev in cfg['devices']:
            for i in cfg['devices'][dev]['vars']:
                vars[i] = cfg['devices'][dev]['vars'][i]

        dev_attr_list.append({
            "name": dev,
            "vars": vars
        })

        print("       List of meta variables: ")
        for v in vars:
            print(f"           {v} = {vars[v]}")

    session.setDeviceAttributes(dev_attr_list)

if __name__ == "__main__":
    main()
