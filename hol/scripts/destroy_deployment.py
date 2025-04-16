#!/usr/bin/env python3

# destroy_deployment.py                                                      #
# Uni-SASE HoL, Version 4.0 b100                                             #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet                                 #
# -------------------------------------------------------------------------- #

from orch_base import readConfig, getApiSession

def main():

   # Config from config.yaml
   cfg = readConfig()
   session = getApiSession(cfg)

   print("Destroying deployment...")

   session.deleteDevices(
      session.getDevices()
   )
   session.deleteAdom()   


if __name__ == "__main__":
    main()   