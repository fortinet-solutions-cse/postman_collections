#!/usr/bin/env python3

# destroy_deployment.py                                                      #
# Uni-SASE HoL, Version 4.0 b105                                             #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet                                 #
# -------------------------------------------------------------------------- #

from orch_base import readConfig, getApiSession


def main():

   # Config from config.yaml
   cfg = readConfig()
   session = getApiSession(cfg)

   print("Destroying deployment...")

   # Destroy tenant ADOM + any extra ADOMs it uses, as per config
   todo = cfg.get('extra_adom', []) + [cfg['fmg_adom']]
   for adom in todo:
      try:
         session.deleteDevices(
            session.getDevices(adom=adom),
            adom=adom
         )
         session.deleteAdom(adom=adom)
      except:
         pass


if __name__ == "__main__":
    main()   