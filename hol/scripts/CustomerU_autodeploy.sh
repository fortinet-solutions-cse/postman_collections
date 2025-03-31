#!/bin/bash

# CustomerU_autodeploy.sh                                                    #
# Uni-SASE HoL, Version 4.0 b100                                             #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet                                 #
# -------------------------------------------------------------------------- #

# $@ : optional Deployer args (e.g. '--verbose')

ORCH_TENANT=CustomerU ./hol_autodeploy.sh "$@"
