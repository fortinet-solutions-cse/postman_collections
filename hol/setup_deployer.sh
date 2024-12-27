#!/bin/bash

# setup_deployer.sh                                                          #
# Uni-SASE HoL, Version 3.0 b100                                             #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet                                 #
# -------------------------------------------------------------------------- #

# Local: solution_deployer.tgz (core Deployer files)
# Remote: tenants and scripts stored on GitHub
# Local: hol_files.tgz (additional files not stored on remote repo)

cd /fortipoc
rm -rf autodeploy 

wget -O hol-3.0.zip https://github.com/fortinet-solutions-cse/postman_collections/archive/refs/tags/hol-3.0.zip

shopt -s dotglob
tar xfz solution-deployer.tgz
solution-deployer/install.sh autodeploy

unzip -o hol-3.0.zip 'postman_collections-hol-3.0/hol/scripts/*' 
unzip -o hol-3.0.zip 'postman_collections-hol-3.0/hol/tenants/*'
mv postman_collections-hol-3.0/hol/scripts/* autodeploy
mv postman_collections-hol-3.0/hol/tenants/* autodeploy/tenants

tar xfz hol_files.tgz -C autodeploy

# Cleanup
rm -rf solution-deployer
rm -rf postman_collections-hol-3.0
rm hol-3.0.zip
