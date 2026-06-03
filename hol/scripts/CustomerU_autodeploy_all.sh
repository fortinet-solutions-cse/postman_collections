#!/bin/bash

# CustomerU_autodeploy_all.sh                                                #
# Uni-SASE HoL, Version 4.5 b451                                             #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet                                 #
# -------------------------------------------------------------------------- #

# $@ : optional Deployer args (e.g. '--verbose')

[[ $HOL_SDWAN -eq 1 ]] && skip_tags="fine-tune-sase,"

ORCH_TENANT=CustomerU ./hol_autodeploy.sh --skip-tags ${skip_tags}west-only,bor "$@"
