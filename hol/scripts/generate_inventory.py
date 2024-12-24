#!/usr/bin/env python3

# generate_inventory.py                                                      #
# Solution Deployer, Version 7.4.x b110                                      #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet (internal use only)             #
# -------------------------------------------------------------------------- #

import csv, io
from orch_base import *


def getSN(fgt_name, cfg):
    task = {
        'site': fgt_name,
        'cli': 'get system status'
    }
    devStatus = getSystemStatus(
        runCLICommandTask(cfg, task, silent=True)
    )
    return devStatus['Serial-Number']


def printInventory(cfg, in_file):
    with open(in_file, 'r', encoding='utf-8-sig') as f, io.StringIO() as s:
        csvIn = csv.DictReader(f)
        csvOut = csv.DictWriter(s, csvIn.fieldnames)
        csvOut.writeheader()
        for d in csvIn:
            d['Serial Number'] = getSN(d['Name'], cfg)
            csvOut.writerow(d)
        print(s.getvalue())


def main():

    cfg = readConfig(silent=True)
    invFile = "inventory." + cfg['fmg_adom']

    print()
    print(invFile+'.csv')
    print(f"{'':=>{len(invFile+'.csv')}}")
    printInventory(cfg, cfg['tenantdir']+'/'+invFile+'.j2')


if __name__ == "__main__":
    main()
