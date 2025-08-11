#!/bin/bash

# DeploymentGuide_destroy.sh                                                       #
# Uni-SASE HoL, Version 4.0 b100                                             #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet                                 #
# -------------------------------------------------------------------------- #

# $@ : optional Deployer args (e.g. '--verbose')

ORCH_TENANT=DeploymentGuide ./destroy_deployment.py
