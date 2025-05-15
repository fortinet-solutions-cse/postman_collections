#!/bin/bash

# setup_deployer.sh                                                          #
# Uni-SASE HoL, Version 3.5 b110                                             #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet                                 #
# -------------------------------------------------------------------------- #

# Local: solution_deployer.tgz (core Deployer files)
# Remote: tenants and scripts stored on GitHub
# Local: hol_files.tgz (additional files not stored on remote repo)

cd /fortipoc
rm -rf autodeploy 

hol_ver=${HOL_VER:-hol-3.5}

wget -O $hol_ver.zip https://github.com/fortinet-solutions-cse/postman_collections/archive/refs/tags/$hol_ver.zip

shopt -s dotglob
tar xfz solution-deployer.tgz
solution-deployer/install.sh autodeploy

unzip -o $hol_ver.zip "postman_collections-$hol_ver/hol/scripts/*"
unzip -o $hol_ver.zip "postman_collections-$hol_ver/hol/tenants/*"
mv postman_collections-$hol_ver/hol/scripts/* autodeploy
mv postman_collections-$hol_ver/hol/tenants/* autodeploy/tenants

tar xfz hol_files.tgz -C autodeploy

# Cleanup
rm -rf solution-deployer
rm -rf postman_collections-$hol_ver
rm $hol_ver.zip
