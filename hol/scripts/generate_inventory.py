#!/usr/bin/env python3

# generate_inventory.py                                                      #
# Uni-SASE HoL, Version 4.0 b100                                             #
# -------------------------------------------------------------------------- #
# Maintainers: CSE Telco/MSSP EMEA, Fortinet                                 #
# -------------------------------------------------------------------------- #

import csv, io, sys
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


def printInventory(cfg, in_file, out_file=''):
    with open(in_file, 'r', encoding='utf-8-sig') as f, io.StringIO() as s:
        csvIn = csv.DictReader(f)
        csvOut = csv.DictWriter(s, csvIn.fieldnames)
        csvOut.writeheader()
        for d in csvIn:
            d['Serial Number'] = getSN(d['Name'], cfg)
            csvOut.writerow(d)
        print(s.getvalue())
        if out_file: 
            print(f"Saving to {out_file}...", end="")
            print(s.getvalue().strip(), file=open(out_file, 'w'))
            print("done!")



def main():

    cfg = readConfig(silent=True)
    invFile = "inventory." + cfg['fmg_adom']
    outFile = cfg['tenantdir']+'/'+invFile+'.csv' if '-w' in sys.argv else ''

    print()
    print(invFile+'.csv')
    print(f"{'':=>{len(invFile+'.csv')}}")
    printInventory(cfg, cfg['tenantdir']+'/'+invFile+'.j2', outFile)


if __name__ == "__main__":
    main()
