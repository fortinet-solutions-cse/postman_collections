#!/bin/bash

# CustomerU_destroy.sh                                                       #
# Uni-SASE HoL, Version 4.0 b100                                             #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet                                 #
# -------------------------------------------------------------------------- #

# $@ : optional Deployer args (e.g. '--verbose')

ORCH_TENANT=CustomerU ./destroy_deployment.py
