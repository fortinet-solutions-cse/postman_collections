#!/bin/bash

# configure_instance.sh                                                      #
# Uni-SASE HoL, Version 3.0 b100                                             #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet                                 #
# -------------------------------------------------------------------------- #

status_fail=0

# Configure external NAT
./configure_ext_nat.py || status_fail=1

# Finalize FGT configuration
./configure_devices.py || status_fail=1

# Update public IPs in Postman variables (CustomerU)
retries=5 
until ./update_postman_vars.py || [ $retries -le 0 ]
do
    echo -e "\n\033[0;33mWARNING:\033[0m No Internet access for the lab FGTs yet (retries left = $retries)"
    sleep 5
    ((retries--))
done

[ $retries -gt 0 ] || status_fail=1 

exit $status_fail

