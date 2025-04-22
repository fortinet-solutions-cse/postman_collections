#!/usr/bin/env python3

# configure_devices.py                                                       #
# Uni-SASE HoL, Version 4.0 b100                                             #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet                                 #
# -------------------------------------------------------------------------- #

from orch_base import readConfig, applyCLIConfigTask
from yaml import safe_load

def main():
    
    cfg = readConfig(shared=True, silent=True)

    for d in [ 'site1-1', 'site1-2', 'site1-H1', 'site1-H2', 'site2-1', 'site2-H1' ]:
        task = {
            'site': d,
            'src': 'tenants/shared/all_fgt.j2'
        }
        applyCLIConfigTask(cfg, task)

if __name__ == "__main__":
    main()    