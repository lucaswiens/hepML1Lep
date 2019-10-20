#!/usr/bin/env python
import sys,os
#sys.path.append("/nfs/dust/cms/user/amohamed/anaconda3/envs/hepML/lib/python3.6/site-packages/")
import htcondor
import argparse

import time 
def find_all_matching(substring, path):
    result = []
    for root, dirs, files in os.walk(path):
        for thisfile in files:
            if thisfile.startswith("."): continue 
            if substring in thisfile:
                result.append(os.path.join(root, thisfile ))
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runs a NAF batch system for 1l plotter', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--indir', help='exec dir', metavar='indir')
    parser.add_argument('--exec', help="wight directory", default='./batch/plotter_exec.sh', metavar='exec')
    

    
    args = parser.parse_args()
    dirname = args.indir
    logdir = './Logs' 
    excu = args.exec

    wdir = os.getcwd()

    if not os.path.exists(logdir):
        os.makedirs(logdir) 
    
    schedd = htcondor.Schedd()  

    Filenamelist = find_all_matching(".sh",dirname)

    for fc in Filenamelist : 
        ##Condor configuration
        submit_parameters = { 
            "executable"                : excu,
            "arguments"                 : " ".join([fc,wdir]),
            "universe"                  : "vanilla",
            "should_transfer_files"     : "YES",
            "log"                       : "{}/job_$(Cluster)_$(Process).log".format(logdir),
            "output"                    : "{}/job_$(Cluster)_$(Process).out".format(logdir),
            "error"                     : "{}/job_$(Cluster)_$(Process).err".format(logdir),
            "when_to_transfer_output"   : "ON_EXIT",
            'Requirements'              : 'OpSysAndVer == "CentOS7"',

         }
        job = htcondor.Submit(submit_parameters)
        #with schedd.transaction() as txn:
        #        job.queue(txn)
        #        print ("Submit job for file {}".format(fc))
        while(True):
            try: 
                with schedd.transaction() as txn:
                    job.queue(txn)
                    print ("Submit job for file {}".format(fc))
                break    

            except: 
                pass
