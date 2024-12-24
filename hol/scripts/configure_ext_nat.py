#!/usr/bin/env python3

# configure_ext_nat.py                                                       #
# Solution Deployer, Version 7.4.x b110.1                                    #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet (internal use only)             #
# -------------------------------------------------------------------------- #

import re
from orch_base import runCLICommandTask, applyCLIConfigTask
from yaml import safe_load

def main():
    
    with open('tenants/shared/config.yaml', 'r') as cfgfile:
        cfg = safe_load(cfgfile)

    task = {
        'site': 'zz_ext',
        'cli': 'diagnose ip address list'
    }
    ip_list = runCLICommandTask(cfg, task)

    task = {
        'site': 'zz_ext',
        'cli': 'get router info routing-table static'
    }
    static_routes = runCLICommandTask(cfg, task)

    vars = {}
    for str in ip_list:
        # group(1) = intf IP, group(2) = intf name
        ip_match = re.search('.*IP=(.*)->.*devname=(\w*)', str)
        if ip_match:
          vars[ip_match.group(2)] = ip_match.group(1)
          for route in static_routes:
            # group(1) = next-hop gw
            route_match = re.search('via (.*), '+ip_match.group(2)+',', route)
            if route_match:
              vars[ip_match.group(2)+'_gw'] = route_match.group(1)
   
    task = {
        'src': 'tenants/shared/zz_ext.j2',
        'vars': vars
    }
    applyCLIConfigTask(cfg, task)

if __name__ == "__main__":
    main()    