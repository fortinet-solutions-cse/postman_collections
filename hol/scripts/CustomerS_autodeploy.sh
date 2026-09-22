#!/bin/bash

# CustomerS_autodeploy_west.sh                                               #
# Uni-SASE HoL, Version 4.5 b452                                             #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet                                 #
# -------------------------------------------------------------------------- #

# $@ : optional Deployer args (e.g. '--verbose')


ORCH_TENANT=CustomerS ./hol_autodeploy.sh "$@"
