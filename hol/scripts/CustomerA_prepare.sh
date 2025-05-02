#!/bin/bash

# CustomerA_prepare.sh (Deploy CustomerA skeleton)                           #
# Uni-SASE HoL, Version 4.0 b100                                             #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet                                 #
# -------------------------------------------------------------------------- #

# $@ : optional Deployer args (e.g. '--verbose')

ORCH_TENANT=CustomerA ./hol_autodeploy.sh --skip-tags lab "$@"