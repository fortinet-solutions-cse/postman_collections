#!/bin/bash

# setup_deployer.sh                                                          #
# Uni-SASE HoL, Version 4.5 b100                                             #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet                                 #
# -------------------------------------------------------------------------- #

# Remote: the Deployer core files, tenants and scripts stored on GitHub
# Local: hol_files.tgz (additional files not stored on remote repo)

cd /fabric
rm -rf autodeploy 

deployer_ver=${DEPLOYER_VER:-7.6.x}
hol_ver=${HOL_VER:-hol-4.5}

wget -O solution_deployer.tgz https://github.com/fortinet-solutions-cse/solution-deployer/archive/refs/tags/$deployer_ver.tar.gz
wget -O $hol_ver.tgz https://github.com/fortinet-solutions-cse/postman_collections/archive/refs/tags/$hol_ver.tar.gz

shopt -s dotglob
tar --overwrite -xzvf solution_deployer.tgz
solution-deployer-$deployer_ver/install.sh autodeploy

tar --overwrite --wildcards -xzvf $hol_ver.tgz "postman_collections-$hol_ver/hol/scripts/*" 
tar --overwrite --wildcards -xzvf $hol_ver.tgz "postman_collections-$hol_ver/hol/tenants/*"
mv postman_collections-$hol_ver/hol/scripts/* autodeploy
mv postman_collections-$hol_ver/hol/tenants/* autodeploy/tenants

tar --overwrite -xzvf hol_files.tgz -C autodeploy

# Cleanup
rm -rf solution-deployer-$deployer_ver
rm -rf postman_collections-$hol_ver
rm $hol_ver.tgz
rm solution_deployer.tgz
