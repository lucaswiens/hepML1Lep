#!/usr/bin/env python

import sys
sys.argv.append( '-b-' )
import ROOT
from ROOT import std
ROOT.gROOT.SetBatch(True)
sys.argv.remove( '-b-' )

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

from plotClass.rootplot  import rootplot
from plotClass.search_regions_2SigCla import All_files

import plotClass.search_regions_2SigCla as sr

import os 
import datetime

from math import hypot, sqrt, ceil

currentDT = datetime.datetime.now()

import argparse
import htcondor

selected_vars = sr.categories
SRs_LDM_cut_strings =  sr.SRs_LDM_cut_strings
SRs_HDM_cut_strings = sr.SRs_HDM_cut_strings
CRs1_cut_strings = sr.CRs_1_cut_strings
CRs2_cut_strings = sr.CRs_2_cut_strings
CRs3_cut_strings = sr.CRs_3_cut_strings
#CRs4_cut_strings = sr.CRs_4_cut_strings

def make1D(var,style,name,ranges):
    '''  A functon to make a 1D histogram and set it's style '''
    hist = ROOT.TH1F(name,name,ranges[0],ranges[1],ranges[2])
    #hist.Draw('goff')
    if style["fill"]:
        style["fill"].Copy(hist)
    if style["line"]:
        style["line"].Copy(hist)
    if style["marker"]:
        style["marker"].Copy(hist)
    hist.GetYaxis().SetTitle('Events')
    hist.GetYaxis().SetTitleSize(0.07)
    hist.GetYaxis().SetTitleFont(42)
    hist.GetYaxis().SetTitleOffset(1.2)
    hist.GetXaxis().SetTitle(var[2])
    hist.GetXaxis().SetLabelFont(42)
    hist.GetYaxis().SetLabelSize(0.05)
    hist.GetXaxis().SetTitleOffset(1.1)
    hist.SetTitle(style["Label"])
    return hist

def hadd1ds(histList):
    '''  A functon to hadd background and set it's style '''
    sumbkg = ROOT.TH1F(histList[0].Clone())
    sumbkg.Reset()
    for bkghist in histList :
        sumbkg.Add(bkghist)
    #sumbkg.Draw('goff')
    sumbkg.SetTitle('Total BKG')
    sumbkg.SetName('sumbkg')
    return sumbkg

def masslist(masslist):
    mass_list = []
    mGo = -999
    mLSP = -999 
    MASS_file = open(masslist,'r')
    for line in MASS_file : 
        if line.startswith("#") : continue 
        if line.startswith(" ") : continue 
        line_ = line.strip()
        #print (line.split(" "))
        mGo = line_.split(" ")[0]
        mLSP = line_.split(" ")[-1]
        mass_list.append(mGo+'_'+mLSP)
        #print (small_list)
    return mass_list

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Runs a NAF batch system for nanoAOD', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--indir', help='List of datasets to process', metavar='indir')
    parser.add_argument('--outdir', help='output directory',default=None, metavar='outdir')
    parser.add_argument('--exec', help="wight directory",default='./batch/shape_exec_2SigCla.sh' ,metavar='exec')
    parser.add_argument('--lumi', help='name of the model with out extensions',default='0', metavar='lumi')
    parser.add_argument('--scan', help='signal or background shapes',default=False, action='store_true')
    parser.add_argument('--batch','-b', help=' set it to true if you want to evaluate paramtric training for each mass point',default=False, action='store_true')
    parser.add_argument('--group','-g', help='which background/signal list to be analyzed',default='SemiLepTT', metavar='group')
    parser.add_argument('--cutdict','-cut' ,help='which cut dicts to be applied SRLDM/SRHDM/CR1/CR2...etc',default='SRLDM', metavar='cutdict')
    parser.add_argument('--mass','-m' ,help='which cut dicts to be applied',default=None, metavar='mass')

    
    args = parser.parse_args()
    indir = args.indir
    outdir = args.outdir
    execu = args.exec
    logdir = outdir+'/Logs' 
    lumi = args.lumi
    batch = args.batch
    sig = args.scan
    group = args.group
    cutdict = args.cutdict
    # restrict the mass to non when run on background

    print('configs are : ', indir , outdir , lumi , batch ,cutdict ,sig)
    ranges = [50,0.0,1.0]
    if cutdict == 'SRLDM' : 
        ranges = [50, 0.0, 1.0] 
        cutdict_ = SRs_LDM_cut_strings
    
    elif cutdict == 'SRHDM' : 
        ranges = [50, 0.0, 1.0] 
        cutdict_ = SRs_HDM_cut_strings

    elif cutdict == 'CR1' : cutdict_ = CRs1_cut_strings
    elif cutdict == 'CR2' : cutdict_ = CRs2_cut_strings
    elif cutdict == 'CR3' : cutdict_ = CRs3_cut_strings
    #elif cutdict == 'CR4' : cutdict_ = CRs4_cut_strings

    mass = args.mass
    if not sig : mass = None


    wdir = os.getcwd()
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if not os.path.exists(logdir):
        os.makedirs(logdir) 
    
    if mass != None : 
        mgo = int(mass.split("_")[0])
        mlsp = int(mass.split("_")[1])
        DM = mgo - mlsp 
    else : mass = 'background'

    if sig : massdir = os.path.join(outdir,'scan/'+mass)
    else :  massdir = os.path.join(outdir,'grid/')
    
    print ('output will be written in ', massdir)
    #massdir = os.path.join(outdir,mass)
    
    if not os.path.exists(massdir): os.makedirs(massdir)

    instPlot = rootplot(indir,outdir,All_files=All_files)
    cuttext = open(massdir+"/"+cutdict+".txt", "w+")
    if not batch : 
        cuts = cutdict_
        g  = group
        if sig : g  = 'Signal_1'
        print ('producing the shapes for :',g, ' for signal mass of : ', mass )
        # fill the dictionary with all the files founded under the indir under each category 
        All_files[g]['files'] = instPlot.group[g]
        # make chain with proposed cuts
        if not sig : 
            extraCuts = All_files[g]['select']
            scale = All_files[g]['scale']
        else : 
            All_files['Signal_1']['files'] = instPlot.group['Signal_1']
            extraCuts = "&& mGo =="+mass.split('_')[0]+ "&& mLSP == "+mass.split('_')[1]
            scale = All_files['Signal_1']['scale']
        print (cuts + extraCuts)
        cuttext.write('cuts applied are :'+cuts + extraCuts+'\n')
        chain = instPlot.chain_and_cut(filesList = All_files[g]['files'],Tname = "sf/t",cutstring = cuts,extraCuts =extraCuts)
        print(chain.GetEntries())
        # create the output root file
        outroot = ROOT.TFile(massdir+"/shapes_{0}_{1}_{2}".format(g,mass,cutdict)+".root","recreate")
        outroot.mkdir(g)
        outroot.cd(g)
        if sig : 
            ROOT.gDirectory.mkdir(mass)
            ROOT.gDirectory.cd(mass)

        error = ROOT.Double(0.)
        for var in selected_vars :
            print(var)
            # make the hist 
            hist = make1D(var,All_files[g],var+'_'+cutdict,ranges)
            # draw the variable to the hist created 
            if 'Data' in g : lum = '1.0' 
            else  : lum = lumi
            chain.Draw(var +' >> '+var+'_'+cutdict, scale+'*'+lum+'*(1)',"goff")
            #print (hist.Integral())
            #hist.Sumw2()
            hist.Write()
        outroot.cd('')
        outroot.Close()
    elif batch :
        print('batch mode activated ...')
        regions = ['SRLDM','SRHDM','CR1','CR2','CR3']
        schedd = htcondor.Schedd()  
            
        if not sig : 
            print('going to run on backgrounds')
            for g in instPlot.group :
                if  'Sig' in g : continue
                for reg in regions : 
                    ##Condor configuration
                    submit_parameters = { 
                        "executable"                : execu,
                        "arguments"                 : " ".join([wdir,indir, outdir,lumi,g,reg,"1500_1000"]),
                        "universe"                  : "vanilla",
                        "should_transfer_files"     : "YES",
                        "log"                       : "{}/job_$(Cluster)_$(Process).log".format(logdir),
                        "output"                    : "{}/job_$(Cluster)_$(Process).out".format(logdir),
                        "error"                     : "{}/job_$(Cluster)_$(Process).err".format(logdir),
                        "when_to_transfer_output"   : "ON_EXIT",
                        #'Requirements'              : 'OpSysAndVer == "CentOS7"',

                    }
                    job = htcondor.Submit(submit_parameters)
                    #with schedd.transaction() as txn:
                    #        job.queue(txn)
                    #        print ("Submit job for file {}".format(fc))
                    print('going to submit the jobs to HTC')
                    #while(True):
                    #    try: 
                    with schedd.transaction() as txn:
                        job.queue(txn)
                        print ("Submit job for configurations of {}{}{}".format(g,' ',reg))
                    #        break    
                    #    except: 
                    #        pass
        else : 
            regions = ['SRLDM','SRHDM']
            mList = masslist('mass_list_all.txt')
            print('going to run on signals')
            for m in mList : 
                for g in instPlot.group :
                    if g != 'Signal_1' : continue
                    for reg in regions : 
                        ##Condor configuration
                        submit_parameters = { 
                            "executable"                : execu,
                            "arguments"                 : " ".join([wdir,indir, outdir,lumi,g,reg,m,'--scan']),
                            "universe"                  : "vanilla",
                            "should_transfer_files"     : "YES",
                            "log"                       : "{}/job_$(Cluster)_$(Process).log".format(logdir),
                            "output"                    : "{}/job_$(Cluster)_$(Process).out".format(logdir),
                            "error"                     : "{}/job_$(Cluster)_$(Process).err".format(logdir),
                            "when_to_transfer_output"   : "ON_EXIT",
                            #'Requirements'              : 'OpSysAndVer == "CentOS7"',

                        }
                        job = htcondor.Submit(submit_parameters)
                        #with schedd.transaction() as txn:
                        #        job.queue(txn)
                        #        print ("Submit job for file {}".format(fc))
                        print('going to submit the jobs to HTC')
                        #while(True):
                        #    try: 
                        with schedd.transaction() as txn:
                            job.queue(txn)
                            print ("Submit job for configurations of {}{}{}{}{}".format(m,' ',g,' ',reg))
                        #        break    
                        #    except: 
                        #        pass


