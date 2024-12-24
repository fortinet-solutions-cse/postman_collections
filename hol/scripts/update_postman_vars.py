#!/usr/bin/env python3

# update_postman_vars.py                                                     #
# Solution Deployer, Version 7.4.x b110                                      #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet (internal use only)             #
# -------------------------------------------------------------------------- #

from orch_base import runCLICommandTask
from yaml import safe_load, safe_dump

def get_public_ip(cfg, fgt, intf):
    
    task = {
        'site': fgt,
        'cli': 'diagnose sys waninfo ipify ' + intf
    }
    output = runCLICommandTask(cfg, task)
    
    str = [ s for s in output if 'Public/WAN IP:' in s ][0]
    return str.split(':')[-1].strip()

def main():
    
    with open('tenants/shared/config.yaml', 'r') as cfgfile:
        cfg = safe_load(cfgfile)

    print("--> ISP1")
    isp1_ip = get_public_ip(cfg, "site1-H1", "port1")
    print("Public IP: " + isp1_ip)
    print()
    print("--> ISP2")
    isp2_ip = get_public_ip(cfg, "site1-H1", "port2")
    print("Public IP: " + isp2_ip)
    print()

    with open('tenants/CustomerU/postman.vars.yaml', 'r') as varfile:
        vars = safe_load(varfile)
    with open('tenants/CustomerU/postman.vars.yaml', 'w') as varfile:        
        vars['west_h1_isp1'] = isp1_ip
        vars['west_h1_isp2'] = isp2_ip
        safe_dump(vars, varfile, sort_keys=False, explicit_start=True)

if __name__ == "__main__":
    main()   