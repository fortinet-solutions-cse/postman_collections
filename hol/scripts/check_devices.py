#!/usr/bin/env python3

# check_devices.py                                                           #
# Solution Deployer, Version 7.4.x b110                                      #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet (internal use only)             #
# -------------------------------------------------------------------------- #

from orch_base import runCLICommandTask, getSystemStatus
from yaml import safe_load

def main():
    
    with open('tenants/shared/config.yaml', 'r') as cfgfile:
        cfg = safe_load(cfgfile)

    fail = 0
    for d in cfg['sites'].keys():
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