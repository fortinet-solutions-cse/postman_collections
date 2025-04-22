#!/usr/bin/env python3

# check_devices.py                                                           #
# Uni-SASE HoL, Version 4.0 b100                                             #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet                                 #
# -------------------------------------------------------------------------- #

import os
from orch_base import readConfig, runCLICommandTask, getSystemStatus
from yaml import safe_load

def main():
    
    cfg = readConfig(shared=True, silent=True)

    fail = 0
    sdwan_only = os.environ.get("HOL_SDWAN")
    for d, v in cfg['sites'].items():
        if not sdwan_only or not v.get('sase_only'):
            print()
            print(f"--> {d}")
            task = {
                'site': d,
                'cli': 'get system status'
            }
            try:
                devStatus = getSystemStatus(
                    runCLICommandTask(cfg, task)
                )
                print(f"Version: {devStatus['Version']}")
                print(f"Serial-Number: {devStatus['Serial-Number']}")
                print(f"License Status: {devStatus['License Status']}")
                if devStatus['License Status'] != "Valid": fail+=1

            except Exception as e:
                print(f"\033[91m\033[1mFAILED:\033[0m {e}") 
                fail += 1
    
    if (fail): 
        print("\n\033[91m\033[1mWARNING:\033[0m At least some of the devices are not in a healthy state!") 
        exit(1)
    
if __name__ == "__main__":
    main()    