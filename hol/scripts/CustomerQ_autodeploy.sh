#!/bin/bash

# CustomerQ_autodeploy.sh                                                    #
# Uni-SASE HoL, Version 4.0 b100                                             #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet                                 #
# -------------------------------------------------------------------------- #

# $1 : optional Deployer args (e.g. '--verbose')

ORCH_TENANT=CustomerQ ./hol_autodeploy.sh $1
