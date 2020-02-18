import sys
sys.argv.append( '-b-' )
import ROOT
from ROOT import std
ROOT.gROOT.SetBatch(True)
sys.argv.remove( '-b-' )
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

import os ,glob
import datetime

from math import hypot, sqrt, ceil

currentDT = datetime.datetime.now()

import argparse

import htcondor
datacardsdir = "datacards_161718_syst/datacards/combinedCards/"
cmsswdir = "/nfs/dust/cms/user/amohamed/susy-desy/deepAK8/CMSSW_9_4_11/src/"
outdir = "./datacards_161718_syst"
execu = "./batch/Limit_exec.sh"
logdir = outdir+'/Logs'
if not os.path.exists(logdir) :  os.makedirs(logdir)

schedd = htcondor.Schedd()
limitOutputdir = os.path.join(outdir,'datacards/limitOutput')
if not os.path.exists(limitOutputdir) : os.makedirs(limitOutputdir)

file_list = glob.glob(datacardsdir+"/*.txt")

for card in file_list :
    cardname = card.split('/')[-1]
    cmd = '../combinedCards/'+cardname
    submit_parameters = {
            "executable"                : execu,
            "arguments"                 : " ".join([' '+ cmsswdir, ' '+ os.path.join(os.getcwd(),limitOutputdir),' '+ cmd, cardname.replace('.txt','')]),
        "universe"                  : "vanilla",
            "should_transfer_files"     : "YES",
        "log"                       : "{}/job_$(Cluster)_$(Process).log".format(logdir),
        "output"                    : "{}/job_$(Cluster)_$(Process).out".format(logdir),
        "error"                     : "{}/job_$(Cluster)_$(Process).err".format(logdir),
        "when_to_transfer_output"   : "ON_EXIT",
        #'Requirements'              : 'OpSysAndVer == "CentOS7"',
    }
    job = htcondor.Submit(submit_parameters)
    print('going to submit the jobs to HTC')
    with schedd.transaction() as txn:
            job.queue(txn)
            print ("Submit job for configurations of {}".format(card))