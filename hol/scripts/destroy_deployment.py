#!/usr/bin/env python3

# destroy_deployment.py                                                      #
# Uni-SASE HoL, Version 5.0 b500                                             #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet                                 #
# -------------------------------------------------------------------------- #

from orch_base import readConfig, getApiSession


def main():

   cfg = readConfig(silent=True)
   session = getApiSession(cfg)

   print("Destroying deployment...")

   todo = [ a['name'] for a in session.getAdoms() ]
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