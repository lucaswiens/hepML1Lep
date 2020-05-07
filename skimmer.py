#!/usr/bin/env python
import sys,os
import ROOT
#sys.path.append("/nfs/dust/cms/user/amohamed/anaconda3/envs/hepML/lib/python3.6/site-packages/")
import argparse
import glob
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
    parser.add_argument('--indir', help='input root files', metavar='indir')
    parser.add_argument('--infile', help='infile to process',default=None, metavar='infile')
    parser.add_argument('--tree', help='inTree to process',default="t", metavar='tree')
    parser.add_argument('--tdir', help='out Tdir to save the outtree in',default="sf", metavar='tdir')
    parser.add_argument('--exec', help="excutable", default='./batch/skim_exec.sh', metavar='exec')
    parser.add_argument('--outdir' ,help="outputdir", default=None, metavar='outdir')
    parser.add_argument('--cuts' ,help="cut string",default="",metavar='cuts')
    parser.add_argument('--batch','-b', help='run on batch',default=False,action='store_true')
    args = parser.parse_args()

    outdir = args.outdir
    logdir = outdir+'/Logs' 
    indir = args.indir
    wdir = os.getcwd()

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    if not args.batch and args.infile: 
        print(args.infile, "will be skimmed with", args.cuts, "and written to",outdir)
        file = ROOT.TFile.Open(args.infile)
        if args.tdir : 
            tree = file.Get(args.tdir+"/"+args.tree)
        else : 
            tree = file.Get(args.tree)
        file_out = ROOT.TFile(os.path.join(outdir,args.infile.split("/")[-1]), "RECREATE")
        tree_out = tree.CopyTree(str(args.cuts))
        if args.tdir : 
            file_out.mkdir(args.tdir)
            file_out.cd(args.tdir)
        tree_out.Write(args.tree, ROOT.TObject.kOverwrite)
        file_out.Close()

    else :    

        if not os.path.exists(logdir):
            os.makedirs(logdir) 
        
        Filenamelist = find_all_matching(".root",args.indir)

        import socket
        host = socket.gethostname()

        if "lxplus" in host : 
            path = "/afs/cern.ch/work/a/amohamed/anaconda3/bin"
            anaconda = "/afs/cern.ch/work/a/amohamed/anaconda3/bin/activate"
            pyth = "/afs/cern.ch/work/a/amohamed/anaconda3/envs/hepML/bin/python"
        elif "desy.de" in host : 
            path = "/nfs/dust/cms/user/amohamed/anaconda3/bin"
            anaconda = "/nfs/dust/cms/user/amohamed/anaconda3/bin/activate"
            pyth = "/nfs/dust/cms/user/amohamed/anaconda3/envs/hepML/bin/python"

        JDir = os.path.join(outdir,"jobs")

        for i,comd in enumerate(Filenamelist): 
            confDir = os.path.join(JDir,"job_"+str(i))
            if not os.path.exists(confDir) : 
                os.makedirs(confDir)
            #comd = comd.split()
            print(comd)
            exec = open(confDir+"/exec.sh","w+")
            exec.write("#"+"!"+"/bin/bash"+"\n")
            exec.write("eval "+'"'+"export PATH='"+path+":$PATH'"+'"'+"\n")
            exec.write("source "+anaconda+" hepML"+"\n")
            exec.write("cd "+wdir+"\n")
            exec.write("echo 'running job' >> "+confDir+"/processing"+"\n")
            exec.write("echo "+wdir+"\n")
            exec.write(pyth+" skimmer.py --infile "+comd+" --outdir "+outdir+" --tree "+args.tree+" --tdir "+args.tdir+" --cuts "+'"'+args.cuts+'"' )
            exec.write("\n")
            # let the script deletes itself after finishing the job
            exec.write("rm -rf "+confDir)
            exec.close()

        subFilename = os.path.join(JDir,"submitAllskimmer.conf")
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
        subFile.write("\n")
        subFile.write('Requirements  = ( OpSysAndVer == "CentOS7" || OpSysAndVer == "SL6")')
        subFile.write("\n")
        subFile.write("queue DIR matching dirs "+JDir+"/job_*/")
        if "lxplus" in host : 
            subFile.write("\n")
            subFile.write('+JobFlavour = "longlunch"')
        subFile.close()
        os.system("condor_submit "+subFilename)
