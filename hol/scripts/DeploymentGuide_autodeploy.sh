#!/bin/bash

# DeploymentGuide_autodeploy.sh                                              #
# Uni-SASE HoL, Version 3.0 b100                                             #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet                                 #
# -------------------------------------------------------------------------- #

start=`date +%s`

api_ver=${API_VER:-hol-3.0}
jinja_ver=${JINJA_VER:-hol-3.0}

echo -----------------------------------------------------------------------
echo Downloading the latest version of the Jinja Orchestrator for $jinja_ver...
echo -----------------------------------------------------------------------
mkdir -p tenants/shared
wget -O tenants/shared/jinja.zip https://github.com/fortinet-solutions-cse/sdwan-advpn-reference/archive/refs/tags/$jinja_ver.zip
unzip -o tenants/shared/jinja.zip "sdwan-advpn-reference-$jinja_ver/dynamic-bgp-on-lo/*.j2" -d tenants/shared/

echo
echo ----------------------------------------------------------------------------------------
echo Downloading the latest version of the Postman collection for the Deployment Guide 7.4...
echo ----------------------------------------------------------------------------------------
wget -O tenants/shared/Deployment_Guide_SDWAN_7_4_x.postman.json https://raw.githubusercontent.com/fortinet-solutions-cse/postman_collections/refs/tags/$api_ver/Deployment_Guide_SDWAN_7_4_x.postman.json

echo
echo ------------------------------
echo Generating device inventory...
echo ------------------------------
ORCH_TENANT=DeploymentGuide ./generate_inventory.py | grep -A 9 "inventory.CustomerC.csv" | tail -n +3 > tenants/DeploymentGuide/inventory.CustomerC.csv
cat tenants/DeploymentGuide/inventory.CustomerC.csv

echo
echo ---------------------------------
echo Starting the Solution Deployer...
echo ---------------------------------
ORCH_TENANT=DeploymentGuide ./autodeploy.py

end=`date +%s`
min=$((($end-$start)/60))
sec=$((($end-$start)%60))
echo Running time: $min minutes, $sec seconds
