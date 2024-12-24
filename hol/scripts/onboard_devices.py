#!/usr/bin/env python3

# onboard_devices.py                                                         #
# Solution Deployer, Version 7.4.x b110                                      #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet (internal use only)             #
# -------------------------------------------------------------------------- #

import sys
from orch_base import *

def main():
  # Usage: 
  #   ./onboard_devices.py -> onboard all tenant sites
  #   ./onboard_devices.py site xyz -> onboard only site xyz
  #   ./onboard_devices.py src inventory.csv -> onboard all sites from inventory.csv
  # In any case, the sites must be defined in the tenant's config.yaml
  cfg = readConfig()
  task = { sys.argv[1]: sys.argv[2] } if len(sys.argv) == 3 else {}
  onboardDevicesTask(cfg, task)


if __name__ == "__main__":
    main()    