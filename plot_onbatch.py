#!/usr/bin/env python
import sys,os
#sys.path.append("/nfs/dust/cms/user/amohamed/anaconda3/envs/hepML/lib/python3.6/site-packages/")
import htcondor
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
    
def getSFs(sffile,mass='1900_100',which='alpha') : 
    token = open(sffile,'r')
    linestoken=token.readlines()
    if which == 'alpha' :  tokens_column_number = 1
    if which == 'alphaE' :  tokens_column_number = 2
    if which == 'beta' :  tokens_column_number = 3
    if which == 'betaE' :  tokens_column_number = 4
    if which == 'gamma' :  tokens_column_number = 5
    if which == 'gammaE' :  tokens_column_number = 6
    resulttoken=[]
    masstoken=[]
    for x in linestoken:
        resulttoken.append(x.split()[tokens_column_number])
        masstoken.append(x.split()[0])
    token.close()
    idx = masstoken.index(mass)
    return resulttoken[idx]
    
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runs a NAF batch system for 1l plotter', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--indir', help='input root files', metavar='indir')
    parser.add_argument('--exec', help="excutable", default='./batch/plotter_exec.sh', metavar='exec')
    parser.add_argument('--lumi','-L' ,help="", default="35.9", metavar='lumi')
    parser.add_argument('--outdir' ,help="outputdir", default=None, metavar='outdir')
    parser.add_argument('--scale' ,help="if YES scale MC to Data, if not use alpha/beta/gamma", default=False, action='store_true')
    parser.add_argument('--param','--parameter' ,help="parameters directory", default=None, metavar='param')
    parser.add_argument('--abg' ,help="text file that has the alpha/beta/gamma values to be used", default=None, metavar='abg')
    parser.add_argument('--only' ,help="choose a cut text to run with it only", default=None, metavar='only')
    parser.add_argument('--blind' ,help="to blind the inclusive distributions",default=False,action='store_true')
    parser.add_argument('--blindall' ,help="to blind the all distributions",default=False,action='store_true')
    args = parser.parse_args()

    if args.lumi == "35.9" : 
        year = "2016"
    elif args.lumi == "41.9" : 
        year = "2017"
    elif args.lumi == "59.74" : 
        year = "2018"
    else : print("lumi must be in [35.9,41.9,59.74]") ; sys.exit() 
    
    
        
    cmd = " --indir "+args.indir+" --lumi "+args.lumi+ " --YmaX 0.0  --YmiN 0.1 --rmax 1.95 --rmin 0.05 --doRatio --year "+year
    
    if not "_0b" in args.param : 
        cmd+= ' --mb '

    cmd+=" --cuts "+args.param+"/inclusive.txt --varList "+args.param+"/baseplots.py"
    if args.scale : 
        cmd+= " --scale_bkgd_toData "
    else : 
        cmd+=" --do_alphabetagamma --scale_bkgd_toData "
        if args.abg == None: 
            print("you've decided to use the alpha/beta/gamm to scale background to data, but you haven't used --abg to provide the text file that contain them")
            sys.exit()
    if args.blindall : 
        cmd+= " --blind "
    list_masses = [x[0] for x in os.walk(args.param)]
    list_masses_ = list_masses[1:]
    cmd_ = cmd
    cmd_array = []
    for mdir in list_masses_ : 
        #to retrive the common options in the cmd
        cmd = cmd_
        if args.only != None : 
            myFiles = glob.glob(mdir+"/*"+args.only+"*.txt")
        else : myFiles = glob.glob(mdir+"/*.txt")
        mgo = str(mdir.split("/")[-1]).split("_")[0]
        mlsp = str(mdir.split("/")[-1]).split("_")[1]
        cmd+=" --mGo1 "+mgo+" --mLSP1 "+mlsp+" --outdir "+os.path.join(args.outdir,mdir.split("/")[-1])

        if not args.scale : 
            alpha = (getSFs(args.abg,mass=mdir.split("/")[-1],which="alpha"))
            beta = (getSFs(args.abg,mass=mdir.split("/")[-1],which="beta"))
            gamma = (getSFs(args.abg,mass=mdir.split("/")[-1],which="gamma"))
            cmd+= " --alpha "+alpha+" --beta "+beta+" --gamma "+gamma
        if args.blind : 
            incl_cmd = cmd+" --mvarList "+mdir+"/mplots_blind.py "
        else : 
            incl_cmd = cmd+" --mvarList "+mdir+"/mplots.py "
        if args.only == None : 
            if os.path.exists(args.param+"/0bCS.txt") : 
                zerob_cmd = cmd+" --mvarList "+mdir+"/mplots.py "
                zerob_cmd = zerob_cmd.replace("inclusive.txt","0bCS.txt")
                cmd_array.append(zerob_cmd)
            if os.path.exists(args.param+"/2LCS.txt") : 
                diLepCS_cmd = cmd+" --mvarList "+mdir+"/mplots.py "
                diLepCS_cmd = diLepCS_cmd.replace("inclusive.txt","2LCS.txt")
                cmd_array.append(diLepCS_cmd)
            cmd_array.append(incl_cmd)
        
        for mcut in myFiles : 
            incl_cmd = cmd+" --mvarList "+mdir+"/mplots_blind.py "
            othercmd = cmd+" --mvarList "+mdir+"/mplots.py "
            if "inclusive" in mcut : 
                othercmd.replace("mplots.py","mplots_blind.py")
            othercmd+= " --mcuts "+mcut
            if ('Sig.txt' in mcut or "Sig_lastbin.txt" in mcut) and not "Anti" in mcut : othercmd +=' --blind '
            cmd_array.append(othercmd)
            
    
    cmd_array = [x.replace("//","/") for x in cmd_array]
    
    logdir = os.path.join(args.outdir,'Logs')
    excu = args.exec
    wdir = os.getcwd()
    if not os.path.exists(logdir):
        os.makedirs(logdir) 
    outtext = open(args.outdir+"/commands.txt", "w+")
    for cmd in cmd_array : 
        outtext.write(cmd+'\n')
    
    
    schedd = htcondor.Schedd() 
    
    sub = htcondor.Submit("")
    ##Condor configuration
    sub["executable"]               = excu
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
                for comd in cmd_array : 
                    print(comd)
                    sub["arguments"] = comd
                    sub.queue(txn)
                print ("Submit jobs for plotter")
            break
        except: 
            pass
