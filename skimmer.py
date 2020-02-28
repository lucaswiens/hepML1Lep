#!/usr/bin/env python
import sys,os
import ROOT
import htcondor
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
        schedd = htcondor.Schedd()  
        sub = htcondor.Submit("")
        sub["executable"]               = args.exec
        sub["universe"]                 = "vanilla"
        sub["should_transfer_files"]    = "YES"
        sub["log"]                      = "{}/job_$(Cluster)_$(Process).log".format(logdir)
        sub["output"]                   = "{}/job_$(Cluster)_$(Process).out".format(logdir)
        sub["error"]                    = "{}/job_$(Cluster)_$(Process).err".format(logdir)
        sub["when_to_transfer_output"]  = "ON_EXIT"
        sub['Requirements']             = 'OpSysAndVer == "CentOS7"'

        while(True):
            try: 
                with schedd.transaction() as txn:
                    for fc in Filenamelist : 
                        print(fc)
                        sub["arguments"] = " ".join([fc,wdir,outdir,args.tree,args.tdir,"'"+args.cuts.replace("(","").replace(")","")+"'"])
                        sub.queue(txn)
                    print ("Submit jobs for the batch system")
                break
            except: 
                pass
