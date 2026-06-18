#!/usr/bin/env python3

# configure_custom_vpn.py                                                       #
# Uni-SASE HoL, Version 3.0 b158                                             #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet                                 #
# -------------------------------------------------------------------------- #

from orch_base import readConfig, applyCLIConfigTask
from yaml import safe_load

def main():

    cfg = readConfig(shared=True, silent=True)

    for d in ['site1-1']:
        task = {
            'site': d,
            'src': 'tenants/CustomerU/site1-1-customvpn.j2'
        }
        applyCLIConfigTask(cfg, task)


if __name__ == "__main__":
    main()