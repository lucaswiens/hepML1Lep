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
from plotClass.plotting.plotGroups import All_files,cut_strings

import plotClass.search_regions as sr

import os 
import datetime

from math import hypot, sqrt, ceil

currentDT = datetime.datetime.now()

import argparse
import htcondor


SRs_cut_strings =  sr.SRs_cut_strings
CRs1_cut_strings = sr.CRs_1_cut_strings
CRs2_cut_strings = sr.CRs_2_cut_strings
CRs3_cut_strings = sr.CRs_3_cut_strings
CRs4_cut_strings = sr.CRs_4_cut_strings

selected_vars = sr.selected_var

def make1D(var,style,name):
    '''  A functon to make a 1D histogram and set it's style '''
    hist = ROOT.TH1F(name,name,100,0.0,1.0)
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
        line_ = line.strip()
        #print (line.split(" "))
        mGo = line_.split(" ")[0]
        mLSP = line_.split(" ")[-1]
        mass_list.append(mGo+'_'+mLSP)
        #print (small_list)
    return mass_list

def sigscoreToUse(mgo,mlsp) : 
    if mgo < 1500 : 
        mass = '1500_1000'
    elif (mgo > 1500 and mgo <= 1900) :
        if mlsp < 800 : mass = '1900_100'
        elif (mlsp >= 800 and mlsp < 1000 ) : mass = '1900_800'
    elif mgo > 1900 : 
        if mlsp < 800 : mass = '2200_100'
        else : mass = '2200_800'
    elif (mgo > 1800 and mgo <=1900 and mlsp > 800 and mlsp < 1000) : mass = '1900_1000'    
    elif (mgo > 1800 and mgo <=1900 and mlsp > 1000): mass = '1800_1300'
    elif (mgo > 1700 and mgo <= 1800 and mlsp >= 1000 ) : mass = '1700_1200'
    elif (mgo > 1600 and mgo <= 1700 and mlsp >= 1000 ) : mass = '1600_1100'
    elif (mgo >= 1500 and mgo <=1600 and mlsp >= 1000 ) : mass = '1500_1200' 
    return mass

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Runs a NAF batch system for nanoAOD', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--indir', help='List of datasets to process', metavar='indir')
    parser.add_argument('--outdir', help='output directory',default=None, metavar='outdir')
    parser.add_argument('--exec', help="wight directory",default='./batch/shape_exec.sh' ,metavar='exec')
    parser.add_argument('--lumi', help='name of the model with out extensions',default='0', metavar='lumi')
    parser.add_argument('--scan', help='signal or background shapes',default=False, action='store_true')
    parser.add_argument('--batch','-b', help=' set it to true if you want to evaluate paramtric training for each mass point',default=False, action='store_true')
    parser.add_argument('--group','-g', help='which background/signal list to be analyzed',default='SemiLepTT', metavar='group')
    parser.add_argument('--cutdict','-cut' ,help='which cut dicts to be applied SR/CR1/CR2...etc',default='SR', metavar='cutdict')
    parser.add_argument('--mass','-m' ,help='which cut dicts to be applied',default='1600_1100', metavar='mass')

    
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
    
    print('configs are : ', indir , outdir , lumi , batch ,cutdict ,sig)

    if cutdict == 'SR' : cutdict_ = SRs_cut_strings
    elif cutdict == 'CR1' : cutdict_ = CRs1_cut_strings
    elif cutdict == 'CR2' : cutdict_ = CRs2_cut_strings
    elif cutdict == 'CR3' : cutdict_ = CRs3_cut_strings
    elif cutdict == 'CR4' : cutdict_ = CRs4_cut_strings

    mass = args.mass


    wdir = os.getcwd()
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if not os.path.exists(logdir):
        os.makedirs(logdir) 
    
    
    if sig : massdir = os.path.join(outdir,'scan/'+mass)
    else :  massdir = os.path.join(outdir,'grid/'+mass)
    
    print ('output will be written in ', massdir)
    #massdir = os.path.join(outdir,mass)
    
    if not os.path.exists(massdir): os.makedirs(massdir)

    instPlot = rootplot(indir,outdir,All_files=All_files)

    if not batch : 
        cuts = cutdict_['1900_100'] if sig else cutdict_[mass]
        
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
        chain = instPlot.chain_and_cut (filesList = All_files[g]['files'],Tname = "sf/t",cutstring = cuts,extraCuts =extraCuts)
        print(chain.GetEntries())
        # create the output root file
        outroot = ROOT.TFile(massdir+"/shapes_{0}_{1}_{2}".format(g,mass,cutdict)+".root","recreate")
        outroot.mkdir(g)
        outroot.cd(g)
        ROOT.gDirectory.mkdir(mass)
        ROOT.gDirectory.cd(mass)

        error = ROOT.Double(0.)
        for var in selected_vars :
            if not sig : 
                if mass+'sig' != var[0]: continue
            if sig :
                if not var[0]=='1900_100sig'  : continue
            print (var)
            for v in var : 
                print (v)
                # make the hist 
                hist = make1D(v,All_files[g],g+v+'_'+cutdict+'_nominal')
                # draw the variable to the hist created 
                if 'Data' in g : lum = '1.0' 
                else  : lum = lumi
                chain.Draw(v +' >> '+g+v+'_'+cutdict+'_nominal', scale+'*'+lum+'*(1)',"goff")
                #print (hist)
                #hist.Sumw2()
                hist.Write()
        outroot.cd('')
        outroot.Close()
    elif batch :
        print('batch mode activated ...')
        regions = ['SR','CR1','CR2','CR3','CR4']
        schedd = htcondor.Schedd()  
            
        if not sig : 
            print('going to run on backgrounds')
            mList = masslist('mass_list.txt')
            for m in mList : 
                for g in instPlot.group :
                    if  'Sig' in g : continue
                    for reg in regions : 
                        ##Condor configuration
                        submit_parameters = { 
                            "executable"                : execu,
                            "arguments"                 : " ".join([wdir,indir, outdir,lumi,g,reg,m]),
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
        else : 
            regions = ['SR']
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



