#!/usr/bin/env python3

# configure_devices.py                                                       #
# Solution Deployer, Version 7.4.x b110                                      #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet (internal use only)             #
# -------------------------------------------------------------------------- #

from orch_base import applyCLIConfigTask
from yaml import safe_load

def main():
    
    with open('tenants/shared/config.yaml', 'r') as cfgfile:
        cfg = safe_load(cfgfile)

    for d in [ 'site1-1', 'site1-2', 'site1-H1', 'site1-H2', 'site2-1', 'site2-H1' ]:
        task = {
            'site': d,
            'src': 'tenants/shared/all_fgt.j2'
        }
        applyCLIConfigTask(cfg, task)

if __name__ == "__main__":
    main()    