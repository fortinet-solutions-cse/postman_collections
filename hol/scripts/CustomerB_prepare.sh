#!/bin/bash

# CustomerU_prepare.sh                                                    #
# Uni-SASE HoL, Version 5.0 b500                                             #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet                                 #
# -------------------------------------------------------------------------- #

# $@ : optional Deployer args (e.g. '--verbose')

ORCH_TENANT=CustomerB ./hol_autodeploy.sh --skip-tags lab "$@"