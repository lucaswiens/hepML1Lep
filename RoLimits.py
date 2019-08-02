#!/usr/bin/env python

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

channels = [['T1tttt_Scan','background']]#,['T1tttt_Scan_','background']]
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

def bkgToUse(mgo,mlsp) : 
    #print('mgo ',mgo,' mlsp ',mlsp)
    if mgo <= 1500 : mass = '1500_1000'
    elif (mgo > 1500 and mgo <= 1900 and mlsp < 800) : mass = '1900_100'
    elif (mgo > 1500 and mgo <= 1900 and mlsp >= 800 and mlsp < 1000 ) : mass = '1900_800'

    elif (mgo > 1900 and mlsp < 800): mass = '2200_100'
    elif (mgo > 1900 and mlsp >= 800 ) :  mass = '2200_800'

    elif (mgo > 1800 and mgo <=1900 and mlsp > 800 and mlsp < 1000) :mass = '1900_1000'
    elif (mgo > 1800 and mgo <=1900 and mlsp >= 1000): mass = '1800_1300'

    elif (mgo > 1700 and mgo <= 1800 and mlsp >= 1000 ) : mass = '1700_1200'
    elif (mgo > 1600 and mgo <= 1700 and mlsp >= 1000 ) : mass = '1600_1100'
    elif (mgo > 1500 and mgo <=1600 and mlsp >= 1000 ) : mass = '1500_1200' 
    else : 
        print(mgo,' ',mlsp, 'could not fit into any of you modes please check')
        mass = ''
    return mass

def simpleAsimov(s,b):
    sign = s/sqrt(s+b+(0.2*b)**2)
    return sign
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Runs a NAF batch system for nanoAOD', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--indir', help='List of Signals to process', metavar='indirS')
    #prser.add_argument('--indirB', help='List of BKGs to process', metavar='indirB')
    parser.add_argument('--outdir', help='output directory',default=None, metavar='outdir')
    parser.add_argument('--Limit','-L', help='calculate the limit after making the datacards',default=False, action='store_true')
    parser.add_argument('--cmsswdir', help='cmssw directory',default='/nfs/dust/cms/user/amohamed/susy-desy/deepAK8/CMSSW_9_4_11/src/', metavar='cmsswdir')
    parser.add_argument('--exec', help="wight directory",default='./batch/Limit_exec.sh' ,metavar='exec')
    

    args = parser.parse_args()
    indirS = args.indir+'/scan'
    indirB = args.indir+'/grid'
    Limit = args.Limit
    cmsswdir = args.cmsswdir
    execu = args.exec

    outdir = args.outdir
    
    if not os.path.exists(outdir):os.makedirs(outdir)
    
    datacardsdir = os.path.join(outdir,'datacards/combinedCards')
    if not os.path.exists(datacardsdir):os.makedirs(datacardsdir)   

    signal_List  = os.listdir(indirS)
    background_List = os.listdir(indirB)
    text = open(outdir+"/background_comp.txt", "w+")

    for signal in signal_List : 
        lists = []
        signal_files = glob.glob(os.path.join(indirS,signal+'/*SR.root'))
        sf = ROOT.TFile.Open(signal_files[0], "read")
        shist = sf.Get('Signal_1/'+signal+'/Signal_11900_100sig_SR_nominal')
        lists.append(shist)
        mgo = float(signal.split('_')[0])
        mlsp = float(signal.split('_')[1])
        bkgToUse_ = bkgToUse(mgo,mlsp)
        print (signal_files)
        #print('mgo ',mgo,' mlsp ',mlsp,' bkgToUse ', bkgToUse_)
        text.write("{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}".format('mgo',mgo,'mlsp',mlsp,'bkgToUse', bkgToUse_)+"\n")
        for bkg in background_List : 
            if bkg != bkgToUse_ : continue 
            bkg_files_SR = glob.glob(os.path.join(indirB,bkg+'/*SR.root'))
            #print (bkg_files_SR)
            hist = ROOT.TH1F('background','background',100,0.0,1.0)
            for bkgf in bkg_files_SR : 
                bkg_name = bkgf.split('/')[-1].split('_')[1]
                if bkg_name == 'Data' : continue 
                bf = ROOT.TFile.Open(bkgf, "read")
                #print(bkg_name+'/'+bkg+'/'+bkg_name+bkg+'sig_SR_nominal')
                bhist = bf.Get(bkg_name+'/'+bkg+'/'+bkg_name+bkg+'sig_SR_nominal')
                #print(bhist.Integral())
                hist.Add(bhist)
                lists.append(hist)
                #blisthist.append(bhist)
            #print('totalBKG ',hist.Integral())
            NBins = hist.GetNbinsX()
            prevSigni = 0.0
            factor = 1.0 
            if mgo < 1400 : factor = 100
            bestBin = 0.0
            for i in range(NBins,1,-1):
                s = shist.Integral(i,NBins+1)/factor
                b = hist.Integral(i,NBins+1)
                signi = simpleAsimov(s ,b)
                if signi > prevSigni : 
                    #print('better significance when merged ', i ,' to ', NBins+1, ' oldsign =  ',prevSigni , ' newsign = ',  signi)
                    bestBin = i
                    prevSigni = signi
                else : 
                    #print('better significance when merged ', i-1 ,' to ', NBins+1, ' oldsign =  ',prevSigni , ' newsign = ',  signi)
                    bestBin = i-1
                    break 
            
            sigerr = ROOT.Double(0.)
            bkgerr = ROOT.Double(0.)

            sigRate = shist.IntegralAndError(bestBin,NBins+1,sigerr)/factor
            bkgRate = hist.IntegralAndError(bestBin,NBins+1,bkgerr)
            #sigerr  = 1.0 + sqrt(sigRate)/(sigRate+0.01)
            #bkgerr  = 1.0 + sqrt(bkgRate)/(bkgRate + 0.01)

            datacard = open(datacardsdir+ '/T1tttt_Scan_mGo' +str(int(mgo))+ '_mLSP'+str(int(mlsp))+'.txt', 'w'); 
            datacard.write("## Datacard for signal %s (with bins from  %s to %s)\n"%('T1tttt_Scan_mGo' +str(int(mgo))+ '_mLSP'+str(int(mlsp)),str(bestBin),str(NBins+1)))
            datacard.write("imax 1 number of bins \n")
            datacard.write("jmax 1 number of processes minus 1 \n")
            datacard.write("kmax 4 number of nuisance parameters \n")
            datacard.write(130*'-')
            datacard.write('\n')
            datacard.write("shapes *    ch1  FAKE \n");
            datacard.write(130*'-')
            datacard.write('\n')
            datacard.write("{:<12}{:<12}".format("bin","ch1")+'\n')
            datacard.write("{:<12}{:<12}".format("observation",round(hist.Integral(bestBin,NBins+1),2))+'\n')    
            datacard.write(130*'-')
            datacard.write('\n')
            datacard.write("{:<62}{:<30}{:<30}".format("bin","ch1","ch1")+'\n')
            datacard.write("{:<62}{:<30}{:<30}".format("process",'T1tttt_Scan_mGo' +str(int(mgo))+ '_mLSP'+str(int(mlsp)),"background")+'\n')
            datacard.write("{:<62}{:<30}{:<30}".format("process",'0',"1")+'\n')
            datacard.write("{:<62}{:<30}{:<30}".format("rate",round(sigRate,2),round(bkgRate,2))+'\n')
            datacard.write(130*'-')
            datacard.write('\n')
            datacard.write("{:<62}{:<30}{:<30}".format("MCstats"+'T1tttt_Scan_mGo' +str(int(mgo))+ '_mLSP'+str(int(mlsp))+' lnN',round(1.0+(sigerr/(sigRate+0.01)),2),'-')+'\n')
            datacard.write("{:<62}{:<30}{:<30}".format("MCstatsbackground lnN",'-',round(1.0+(bkgerr/(bkgRate+0.01)),2))+'\n')
            datacard.write("{:<62}{:<30}{:<30}".format("sigSyst lnN",1.2,'-')+'\n')
            datacard.write("{:<62}{:<30}{:<30}".format("bkguncert lnN",'-',1.1)+'\n')
    if Limit : 
        print ('limit will be calculated on HTC from ', datacardsdir)
        print ('in this step you will need a valid cmssw dir with higgscombne tools compiled, please check https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/ ')
        print ('you have scpecified CMSSW in this place, ', cmsswdir )

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
            #with schedd.transaction() as txn:
            #        job.queue(txn)
            #        print ("Submit job for file {}".format(fc))
            print('going to submit the jobs to HTC')
            #while(True):
            #    try: 
            with schedd.transaction() as txn:
                job.queue(txn)
                print ("Submit job for configurations of {}".format(card))
            #        break    
            #    except: 
            #        pass



                
                
                