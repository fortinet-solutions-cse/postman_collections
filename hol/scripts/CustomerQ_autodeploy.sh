#!/bin/bash

# CustomerQ_autodeploy.sh                                                    #
# Uni-SASE HoL, Version 4.0 b100                                             #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet                                 #
# -------------------------------------------------------------------------- #

# $@ : optional Deployer args (e.g. '--verbose')

API_VER=staging-4.0 ORCH_TENANT=CustomerQ ./hol_autodeploy.sh "$@"
