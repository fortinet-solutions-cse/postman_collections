#!/bin/bash

# CustomerU_autodeploy.sh                                                    #
# Uni-SASE HoL, Version 4.0 b100                                             #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet                                 #
# -------------------------------------------------------------------------- #

start=`date +%s`

api_ver=${API_VER:-hol-4.0}
jinja_ver=${JINJA_VER:-hol-4.0}

# echo -----------------------------------------------------------------------
# echo Downloading the latest version of the Jinja Orchestrator for $jinja_ver...
# echo -----------------------------------------------------------------------
# mkdir -p tenants/shared
# wget -O tenants/shared/jinja.zip https://github.com/fortinet-solutions-cse/sdwan-advpn-reference/archive/refs/tags/$jinja_ver.zip
# unzip -o tenants/shared/jinja.zip "sdwan-advpn-reference-$jinja_ver/dynamic-bgp-on-lo/*.j2" -d tenants/shared/

echo
echo -----------------------------------------------------------------------
echo Downloading the latest version of the Postman collection for $api_ver...
echo -----------------------------------------------------------------------
wget -O tenants/shared/Managed_SDWAN_7_6_x.postman.json https://raw.githubusercontent.com/fortinet-solutions-cse/postman_collections/refs/tags/$api_ver/Managed_SDWAN_7_6_x.postman.json

echo
echo ------------------------------
echo Generating device inventory...
echo ------------------------------
./generate_inventory.py | grep -A 9 "inventory.CustomerA.csv" | tail -n +3 > tenants/CustomerA/inventory.CustomerA.csv
cat tenants/CustomerU/inventory.CustomerU.csv

echo
echo ---------------------------------
echo Starting the Solution Deployer...
echo ---------------------------------
ORCH_TENANT=CustomerA ./autodeploy.py

end=`date +%s`
min=$((($end-$start)/60))
sec=$((($end-$start)%60))
echo Running time: $min minutes, $sec seconds
