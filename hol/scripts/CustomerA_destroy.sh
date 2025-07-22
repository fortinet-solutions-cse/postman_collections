#!/bin/bash

# CustomerA_destroy.sh (Destroy CustomerA)                                   #
# Uni-SASE HoL, Version 4.0 b105                                             #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet                                 #
# -------------------------------------------------------------------------- #

ORCH_TENANT=CustomerA ./destroy_deployment.py

echo Restoring site2-H1 to initial config...
fgt_password=$(grep 'fgt_password:' tenants/shared/.secrets.yaml | awk '{print $2}')
sshpass -p $fgt_password scp -O /fortipoc/backup/site2-H1 FGT2H1:fgt-restore-config

echo Please wait for the site2-H1 to reboot before starting your next deployment!
echo It will take around a minute (use 'fpoc_ver' to check)!
