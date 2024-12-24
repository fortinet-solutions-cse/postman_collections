#!/bin/bash

start=`date +%s`

echo ---------------------------------------------------------------------------
echo Downloading the latest version of the Jinja Orchestrator for release/7.4...
echo ---------------------------------------------------------------------------
mkdir -p tenants/shared
wget -O tenants/shared/7.4.zip https://github.com/fortinet-solutions-cse/sdwan-advpn-reference/archive/refs/tags/hol-2.0.zip
unzip -o tenants/shared/7.4.zip 'sdwan-advpn-reference-hol-2.0/dynamic-bgp-on-lo/*.j2' -d tenants/shared/

echo
echo -----------------------------------------------------------------------------
echo Downloading the latest version of the Postman collection for CSE-SDWAN-74x...
echo -----------------------------------------------------------------------------
wget -O tenants/shared/Managed_SDWAN_7_4_x.postman.json https://raw.githubusercontent.com/fortinet-solutions-cse/postman_collections/refs/tags/hol-2.0/Managed_SDWAN_7_4_x.postman.json

echo
echo ---------------------------------------
echo Starting the Fancy Solution Deployer...
echo ---------------------------------------
ORCH_TENANT=CustomerU ./autodeploy.py --tags foundation,lab

end=`date +%s`
min=$((($end-$start)/60))
sec=$((($end-$start)%60))
echo Running time: $min minutes, $sec seconds
