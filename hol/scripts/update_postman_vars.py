#!/usr/bin/env python3

# update_postman_vars.py                                                     #
# Uni-SASE HoL, Version 4.0 b110                                             #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet                                 #
# -------------------------------------------------------------------------- #

import sys, re
from orch_base import readConfig, runCLICommandTask
from yaml import safe_load, safe_dump

def __get_public_ip_with_ipify(cfg, fgt, intf):
    
    task = {
        'site': fgt,
        'cli': 'diagnose sys waninfo ipify ' + intf
    }
    output = runCLICommandTask(cfg, task)
    
    str = [ s for s in output if 'Public/WAN IP:' in s ][0]
    return str.split(':')[-1].strip()

def __get_public_ip_with_ident(cfg, fgt, intf):

    task = {
        'site': fgt,
        'cli': 'execute ssh-options interface ' + intf + '\nexecute ssh test@v4.ident.me'
    }
    output = runCLICommandTask(cfg, task)

    # IP address regex
    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    str = [ s for s in output if ip_pattern.search(s) ][0]
    return ip_pattern.search(str).group(0)

def get_public_ip(cfg, fgt, intf):
    try:
       ip = __get_public_ip_with_ipify(cfg, fgt, intf)
    except: 
       ip = __get_public_ip_with_ident(cfg, fgt, intf)
    return ip

def main():

    dry = "--dry" in sys.argv
    if dry: print("Dry-run mode ON.")    
    
    cfg = readConfig(shared=True, silent=True)        

    print("--> ISP1")
    isp1_ip = get_public_ip(cfg, "zz_ext", "port1")
    print("Public IP: " + isp1_ip)
    print()
    print("--> ISP2")
    isp2_ip = get_public_ip(cfg, "zz_ext", "port2")
    print("Public IP: " + isp2_ip)
    print()

    if not dry:
        with open('tenants/CustomerU/postman.vars.yaml', 'r') as varfile:
            vars = safe_load(varfile)
        with open('tenants/CustomerU/postman.vars.yaml', 'w') as varfile:        
            vars['west_h1_isp1'] = isp1_ip
            vars['west_h1_isp2'] = isp2_ip
            safe_dump(vars, varfile, sort_keys=False, explicit_start=True)

if __name__ == "__main__":
    main()   