import sys

import os ,glob
import datetime

from math import hypot, sqrt, ceil

currentDT = datetime.datetime.now()

import argparse

path = sys.argv[-1]

datacardsdir = os.path.join(path,"datacards/combinedCards/")
cmsswdir = "/nfs/dust/cms/user/amohamed/susy-desy/deepAK8/CMSSW_9_4_11/src/"
outdir = path
execu = "./batch/Limit_exec.sh"
logdir = outdir+'/Logs'
if not os.path.exists(logdir) :  os.makedirs(logdir)
limitOutputdir = os.path.join(outdir,'datacards/limitOutput')
if not os.path.exists(limitOutputdir) : os.makedirs(limitOutputdir)

file_list = glob.glob(datacardsdir+"/*.txt")

import socket
host = socket.gethostname()
JDir = outdir

file_list = glob.glob(datacardsdir+"/*.txt")
for i,card in enumerate(file_list) : 
    cardname = card.split('/')[-1]
    cmd = '../combinedCards/'+cardname
    confDir = os.path.join(JDir,"job_"+str(i))
    if not os.path.exists(confDir) : 
        os.makedirs(confDir)
    print(cmd)
    exec = open(confDir+"/exec.sh","w+")
    exec.write("#"+"!"+"/bin/bash"+"\n")
    exec.write("source /etc/profile"+"\n")
    exec.write("source /cvmfs/cms.cern.ch/cmsset_default.sh"+"\n")
    exec.write("echo 'running job' >> "+os.path.abspath(confDir)+"/processing"+"\n")
    exec.write("workdir="+cmsswdir+"\n")
    exec.write("melalibdir=${CMSSW_BASE}/lib/slc6_amd64_gcc630/"+"\n")
    exec.write("exedir=`echo "+os.path.join(os.getcwd(),limitOutputdir)+"`"+"\n")
    exec.write("export LD_LIBRARY_PATH=${melalibdir}:$LD_LIBRARY_PATH"+"\n")
    exec.write("cd ${workdir}"+"\n")
    exec.write("eval `scramv1 runtime -sh`"+"\n")
    exec.write("cd ${exedir}"+"\n")
    exec.write("combine -M Asymptotic "+cmd+" -n "+cardname.replace('.txt','')+" "+"\n")
    exec.write("rm -rf "+os.path.abspath(confDir))
    exec.close()

subFilename = os.path.join(JDir,"submitAlllimits.conf")
subFile = open(subFilename,"w+")
subFile.write("executable = $(DIR)/exec.sh"+"\n")
subFile.write("universe =  vanilla")
subFile.write("\n")
subFile.write("should_transfer_files = YES")
subFile.write("\n")
subFile.write("log = "+"{}/job_$(Cluster)_$(Process).log".format(os.path.abspath(logdir)))
subFile.write("\n")
subFile.write("output = "+"{}/job_$(Cluster)_$(Process).out".format(os.path.abspath(logdir)))
subFile.write("\n")
subFile.write("error = "+"{}/job_$(Cluster)_$(Process).err".format(os.path.abspath(logdir)))
subFile.write("\n")
subFile.write("when_to_transfer_output   = ON_EXIT")
#subFile.write("\n")
#subFile.write('Requirements  = (OpSysAndVer == "SL6")')
subFile.write("\n")
subFile.write("queue DIR matching dirs "+JDir+"/job_*/")
subFile.close()
os.system("condor_submit "+subFilename)

