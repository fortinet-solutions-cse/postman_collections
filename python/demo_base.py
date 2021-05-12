#!/usr/bin/env python3

import yaml
from jinja2 import Template
from os import environ


def readConfig():

    print("========================")
    print(" Tenant: " + environ.get("FMG_TENANT"))
    print("========================")
    tenantdir = "tenants/" + environ.get("FMG_TENANT") + "/"

    with open('config.yaml', 'r') as cfgfile, open(tenantdir + 'tenant.yaml.j2', 'r') as tntfile:
        cfg = yaml.safe_load(cfgfile) | yaml.safe_load(Template(tntfile.read()).render())

    print("     FMG URL = " + cfg['fmg_api'])
    print("     Tenant ADOM = " + cfg['adom'])

    return cfg
