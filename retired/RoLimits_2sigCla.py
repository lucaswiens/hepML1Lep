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

Sig_shapesLDM = []
Sig_shapesHDM = []
BKG_shapesLDM = []
BKG_shapesHDM = []

#channels = [['T1tttt_Scan','background']]#,['T1tttt_Scan_','background']]
channels = ['Signal_1','SemiLepTT','DiLepTT','WJ','DY','QCD','SingleT','TTV','VV']
Signal_shapes = ['signal_LDM','signal_HDM']

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

def simpleAsimov(s,b):
    sign = s/sqrt(s+b+(0.2*b)**2)
    return sign

def getSFs(sffile,which='alpha') : 
    token = open(sffile,'r')
    linestoken=token.readlines()
    if which == 'alpha' :  tokens_column_number = 0
    if which == 'alphaE' :  tokens_column_number = 1
    if which == 'beta' :  tokens_column_number = 2
    if which == 'betaE' :  tokens_column_number = 3
    if which == 'gamma' :  tokens_column_number = 4
    if which == 'gammaE' :  tokens_column_number = 5
    resulttoken=[]
    #masstoken=[]
    for x in linestoken:
        resulttoken.append(x.split()[tokens_column_number])
        #masstoken.append(x.split()[0])
    token.close()
    #idx = masstoken.index(mass)
    return resulttoken[1]


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Runs a NAF batch system for nanoAOD', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--infile', help='List of Signals to process', metavar='infile')
    #prser.add_argument('--indirB', help='List of BKGs to process', metavar='indirB')
    parser.add_argument('--outdir', help='output directory',default=None, metavar='outdir')
    parser.add_argument('--Limit','-L', help='calculate the limit after making the datacards',default=False, action='store_true')
    parser.add_argument('--cmsswdir', help='cmssw directory',default='/nfs/dust/cms/user/amohamed/susy-desy/deepAK8/CMSSW_9_4_11/src/', metavar='cmsswdir')
    parser.add_argument('--execu', help="wight directory",default='./batch/Limit_exec.sh' ,metavar='execu')
    parser.add_argument('--sfs', help="the text file that has alpha beta gamma",default=None ,metavar='sfs')
    parser.add_argument('--shapeAna','-shape', help='calculate the limit after making the datacards',default=False, action='store_true')
    parser.add_argument('--blind', help='calculate the limit after making the datacards',default=True, action='store_true')

    
    binned = False
    args = parser.parse_args()
    inFile = args.infile
    Limit = args.Limit
    cmsswdir = args.cmsswdir
    outdir = args.outdir
    execu = args.execu   
    sfs = args.sfs
    shapeAna = args.shapeAna
    blind = args.blind
    
    datacardsdirLDM = os.path.join(outdir+"_LDM",'datacards/combinedCards')
    if not os.path.exists(datacardsdirLDM):os.makedirs(datacardsdirLDM)     

    datacardsdirHDM = os.path.join(outdir+"_HDM",'datacards/combinedCards')
    if not os.path.exists(datacardsdirHDM):os.makedirs(datacardsdirHDM)       
    
    shapes = ROOT.TFile.Open(inFile, "read")
    sign_dir = shapes.Get(channels[0])

    for sigdir in sign_dir.GetListOfKeys() : 
        Sig_shapesLDM.append(sign_dir.GetName()+'/'+sigdir.GetName()+'/signal_LDM_SRLDM')
        Sig_shapesHDM.append(sign_dir.GetName()+'/'+sigdir.GetName()+'/signal_HDM_SRHDM')
    
    background_List = channels[1:]
    BKG_shapesLDM = [x+'/signal_LDM_SRLDM' for x in background_List]
    BKG_shapesHDM = [x+'/signal_HDM_SRHDM' for x in background_List]
    #print(Sig_shapesLDM,Sig_shapesHDM)
    
    # make total background histograms 
    shapes = ROOT.TFile.Open(inFile, "UPDATE")
    shapes.cd()
    # Get 1st LDM hist
    hist = shapes.Get(BKG_shapesLDM[0])
    
    which = ''
    scalefactor = 1.0
    if BKG_shapesLDM[0].startswith('DiLepTT') : which = 'beta'
    elif BKG_shapesLDM[0].startswith('SemiLepTT') :which = 'alpha'
    elif not BKG_shapesLDM[0].startswith('Data') : which = 'gamma'
    
    scalefactor = float(getSFs(sfs,which=which))
    
    hist.Scale(scalefactor)
    hist.SetTitle('Total BKG LDM')
    hist.SetName('sumbkg_LDM')

    for i,bkg in enumerate(BKG_shapesLDM) :
        if i == 0 : continue 
        hist_ = shapes.Get(bkg)
        which = ''
        scalefactor = 1.0
        if bkg.startswith('DiLepTT') : which = 'beta'
        elif bkg.startswith('SemiLepTT') :which = 'alpha'
        elif not bkg.startswith('Data') : which = 'gamma'
    
        scalefactor = float(getSFs(sfs,which=which))
    
        hist_.Scale(scalefactor)
        hist.Add(hist_)

    hist.Write("", ROOT.TObject.kOverwrite)
    del hist
    # Get 1st LDM hist
    hist = shapes.Get(BKG_shapesHDM[0])
    which = ''
    scalefactor = 1.0
    if BKG_shapesHDM[0].startswith('DiLepTT') : which = 'beta'
    elif BKG_shapesHDM[0].startswith('SemiLepTT') :which = 'alpha'
    elif not BKG_shapesHDM[0].startswith('Data') : which = 'gamma'
    
    scalefactor = float(getSFs(sfs,which=which))
    
    hist.Scale(scalefactor)
    hist.SetTitle('Total BKG HDM')
    hist.SetName('sumbkg_HDM')
    
    for i,bkg in enumerate(BKG_shapesHDM) :
        if i == 0 : continue 
        hist_ = shapes.Get(bkg)
        which = ''
        scalefactor = 1.0
        if bkg.startswith('DiLepTT') : which = 'beta'
        elif bkg.startswith('SemiLepTT') :which = 'alpha'
        elif not bkg.startswith('Data') : which = 'gamma'
        scalefactor = float(getSFs(sfs,which=which))
        hist_.Scale(scalefactor)
        hist.Add(hist_)
        
    
    hist.Write("", ROOT.TObject.kOverwrite)
    del hist
    
    alphaE  = float(getSFs(sfs,which='alphaE')) + 1.0
    betaE  = float(getSFs(sfs,which='betaE')) + 1.0
    gammaE  = float(getSFs(sfs,which='gammaE')) + 1.0    


    bestBin = 0 if shapeAna else 45

    for bkg_LDM in BKG_shapesLDM : 
        hist = shapes.Get(bkg_LDM)
        NBins = hist.GetNbinsX()
        bkgerr = ROOT.Double(0.)
        #bkgRate = hist.IntegralAndError(bestBin,NBins+1,bkgerr)
        #'SemiLepTT','DiLepTT','WJ','DY','QCD','SingleT','TTV','VV'
        if bkg_LDM.startswith('SemiLepTT') : SemiLepTT  = hist.IntegralAndError(bestBin,NBins+1,bkgerr) ;   SemiLepTTerr = bkgerr
        elif bkg_LDM.startswith('DiLepTT') : DiLepTT    = hist.IntegralAndError(bestBin,NBins+1,bkgerr) ;   DiLepTTerr = bkgerr
        elif bkg_LDM.startswith('WJ') :      WJ         = hist.IntegralAndError(bestBin,NBins+1,bkgerr) ;   WJerr = bkgerr
        elif bkg_LDM.startswith('DY') :      DY         = hist.IntegralAndError(bestBin,NBins+1,bkgerr) ;   DYerr = bkgerr
        elif bkg_LDM.startswith('QCD') :     QCD        = hist.IntegralAndError(bestBin,NBins+1,bkgerr) ;   QCDerr = bkgerr
        elif bkg_LDM.startswith('SingleT') : SingleT    = hist.IntegralAndError(bestBin,NBins+1,bkgerr) ;   SingleTerr = bkgerr
        elif bkg_LDM.startswith('TTV') :     TTV        = hist.IntegralAndError(bestBin,NBins+1,bkgerr) ;   TTVerr = bkgerr
        elif bkg_LDM.startswith('VV') :      VV         = hist.IntegralAndError(bestBin,NBins+1,bkgerr) ;   VVerr = bkgerr


    for bkg_HDM in BKG_shapesHDM : 
        hist = shapes.Get(bkg_HDM)
        NBins = hist.GetNbinsX()
        bkgerr = ROOT.Double(0.)
        #bkgRate = hist.IntegralAndError(bestBin,NBins+1,bkgerr)
        #'SemiLepTT','DiLepTT','WJ','DY','QCD','SingleT','TTV','VV'
        if bkg_HDM.startswith('SemiLepTT') : SemiLepTT_  = hist.IntegralAndError(bestBin,NBins+1,bkgerr) ;   SemiLepTTerr_ = bkgerr
        elif bkg_HDM.startswith('DiLepTT') : DiLepTT_    = hist.IntegralAndError(bestBin,NBins+1,bkgerr) ;   DiLepTTerr_   = bkgerr
        elif bkg_HDM.startswith('WJ') :      WJ_         = hist.IntegralAndError(bestBin,NBins+1,bkgerr) ;   WJerr_        = bkgerr
        elif bkg_HDM.startswith('DY') :      DY_         = hist.IntegralAndError(bestBin,NBins+1,bkgerr) ;   DYerr_        = bkgerr
        elif bkg_HDM.startswith('QCD') :     QCD_        = hist.IntegralAndError(bestBin,NBins+1,bkgerr) ;   QCDerr_       = bkgerr
        elif bkg_HDM.startswith('SingleT') : SingleT_    = hist.IntegralAndError(bestBin,NBins+1,bkgerr) ;   SingleTerr_   = bkgerr
        elif bkg_HDM.startswith('TTV') :     TTV_        = hist.IntegralAndError(bestBin,NBins+1,bkgerr) ;   TTVerr_       = bkgerr
        elif bkg_HDM.startswith('VV') :      VV_         = hist.IntegralAndError(bestBin,NBins+1,bkgerr) ;   VVerr_        = bkgerr

    alpha = float(getSFs(sfs,which='alpha'))
    beta  = float(getSFs(sfs,which='beta'))
    gamma = float(getSFs(sfs,which='gamma'))

    if not shapeAna: 
        for signalh in Sig_shapesLDM :
            if not shapes.Get(signalh) : 
                print('Could not find ', signalh , 'in the shapes will escape it, please check')
                continue
            mgo = signalh.split("/")[1].split("_")[0]
            mlsp = signalh.split("/")[1].split("_")[1]
            datacard = open(datacardsdirLDM+ '/T1tttt_Scan_mGo' +str(int(mgo))+ '_mLSP'+str(int(mlsp))+'.txt', 'w'); 
            datacard.write("## Datacard for signal %s (with bins from  LDM)\n"%('T1tttt_Scan_mGo' +str(int(mgo))+ '_mLSP'+str(int(mlsp))))
            datacard.write("imax 1 number of bins \n")
            datacard.write("jmax * number of processes minus 1 \n")
            datacard.write("kmax * number of nuisance parameters \n")
            datacard.write(130*'-')
            datacard.write('\n')
            if blind : 
                observation = shapes.Get("sumbkg_LDM").IntegralAndError(bestBin,NBins+1,bkgerr)
            else :observation = shapes.Get("Data/signal_LDM_SRLDM").IntegralAndError(bestBin,NBins+1,bkgerr)
            sigerr = ROOT.Double(0.)
            factor = 1.0 
            if float(mgo) <= 1400 : factor = 1.0 
            Signal = shapes.Get(signalh).IntegralAndError(bestBin,NBins+1,sigerr)
            
            datacard.write("shapes *    ch1  FAKE \n");
            datacard.write(130*'-')
            datacard.write('\n')
            datacard.write("{:<12}{:<12}".format("bin","ch1")+'\n')
            datacard.write("{:<12}{:<12}".format("observation",round(observation,2))+'\n')
            datacard.write(130*'-')
            datacard.write('\n')
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("bin","ch1","ch1","ch1","ch1","ch1","ch1","ch1","ch1","ch1")+'\n')
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("process",'T1tttt_Scan_mGo' +str(int(mgo))+ '_mLSP'+str(int(mlsp)),'SemiLepTT','DiLepTT','WJ','DY','QCD','SingleT','TTV','VV')+'\n')
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("process",'0','1','2','3','4','5','6','7','8')+'\n')
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("rate",round(Signal/factor,2),round(SemiLepTT,2),round(DiLepTT,2),round(WJ,2),round(DY,2),round(QCD,2),round(SingleT,2),round(TTV,2),round(VV,2))+'\n')
            datacard.write(130*'-')
            datacard.write('\n')
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("MCstats"+'T1tttt_Scan_mGo' +str(int(mgo))+ '_mLSP'+str(int(mlsp))+' lnN',round(1.0+(sigerr/((Signal/factor)+0.01)),2),'-','-','-','-','-','-','-','-')+'\n')
            
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("MCstatsSemiLepTT lnN",'-',round(1.0+(SemiLepTTerr*alpha  /(SemiLepTT +0.01)),2),'-','-','-','-','-','-','-')+'\n')
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("MCstatsDiLepTT   lnN",'-','-',round(1.0+(DiLepTTerr*beta /(DiLepTT   +0.01)),2),'-','-','-','-','-','-')+'\n')
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("MCstatsWJ        lnN",'-','-','-',round(1.0+(WJerr*gamma /(WJ        +0.01)),2),'-','-','-','-','-')+'\n')
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("MCstatsDY        lnN",'-','-','-','-',round(1.0+(DYerr*gamma /(DY        +0.01)),2),'-','-','-','-')+'\n')
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("MCstatsQCD       lnN",'-','-','-','-','-',round(1.0+(QCDerr*gamma  /(QCD       +0.01)),2),'-','-','-')+'\n')
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("MCstatsSingleT   lnN",'-','-','-','-','-','-',round(1.0+(SingleTerr*gamma /(SingleT   +0.01)),2),'-','-')+'\n')
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("MCstatsTTV       lnN",'-','-','-','-','-','-','-',round(1.0+(TTVerr*gamma   /(TTV       +0.01)),2),'-')+'\n')
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("MCstatsVV        lnN",'-','-','-','-','-','-','-','-',round(1.0+(VVerr*gamma  /(VV        +0.01)),2))+'\n')


            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("sigSyst lnN",1.2,'-','-','-','-','-','-','-','-')+'\n')
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("bkguncert lnN",'-',1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1)+'\n')
            datacard.write(130*'-'+'\n')

            '''datacard.write("{:<62}{:<30}".format("SemiLepTT_norm rateParam * SemiLepTT* ",1/float(getSFs(sfs,which='alpha')))+'\n')
            datacard.write("{:<62}{:<30}".format("DiLepTT_norm rateParam * DiLepTT*     ",1/float(getSFs(sfs,which='beta')))+'\n')
            datacard.write("{:<62}{:<30}".format("WJ_norm rateParam * WJ*               ",1/float(getSFs(sfs,which='gamma')))+'\n')
            datacard.write("{:<62}{:<30}".format("DY_norm rateParam * DY*               ",1/float(getSFs(sfs,which='gamma')))+'\n')
            datacard.write("{:<62}{:<30}".format("QCD_norm rateParam * QCD*             ",1/float(getSFs(sfs,which='gamma')))+'\n')
            datacard.write("{:<62}{:<30}".format("SingleT_norm rateParam * SingleT*     ",1/float(getSFs(sfs,which='gamma')))+'\n')
            datacard.write("{:<62}{:<30}".format("TTV_norm rateParam * TTV*             ",1/float(getSFs(sfs,which='gamma')))+'\n')
            datacard.write("{:<62}{:<30}".format("VV_norm rateParam * VV*               ",1/float(getSFs(sfs,which='gamma')))+'\n')'''



        for signalh in Sig_shapesHDM :
            if not shapes.Get(signalh) : 
                print('Could not find ', signalh , 'in the shapes will escape it, please check')
                continue
            #backgrounds_integrals = [SemiLepTT_,DiLepTT_,WJ_,DY_,QCD_,SingleT_,TTV_,VV_]
            #backgrounds_erroes    = [SemiLepTTerr_ ,DiLepTTerr_ ,WJerr_ ,DYerr_ ,QCDerr_ ,SingleTerr_ ,TTVerr_ ,VVerr_ ]
            mgo = signalh.split("/")[1].split("_")[0]
            mlsp = signalh.split("/")[1].split("_")[1]
            datacard = open(datacardsdirHDM+ '/T1tttt_Scan_mGo' +str(int(mgo))+ '_mLSP'+str(int(mlsp))+'.txt', 'w'); 
            datacard.write("## Datacard for signal %s (with bins from  HDM)\n"%('T1tttt_Scan_mGo' +str(int(mgo))+ '_mLSP'+str(int(mlsp))))
            datacard.write("imax 1 number of bins \n")
            datacard.write("jmax * number of processes minus 1 \n")
            datacard.write("kmax * number of nuisance parameters \n")
            datacard.write(130*'-')
            datacard.write('\n')
            if blind : 
                observation = shapes.Get("sumbkg_HDM").IntegralAndError(bestBin,NBins+1,bkgerr)
            else :observation = shapes.Get("Data/signal_HDM_SRHDM").IntegralAndError(bestBin,NBins+1,bkgerr)
            sigerr = ROOT.Double(0.)
            factor = 1.0 
            if float(mgo) <= 1400 : factor = 1.0 
            Signal = shapes.Get(signalh).IntegralAndError(bestBin,NBins+1,sigerr)
            
            datacard.write("shapes *    ch1  FAKE \n");
            datacard.write(130*'-')
            datacard.write('\n')
            datacard.write("{:<12}{:<12}".format("bin","ch1")+'\n')
            datacard.write("{:<12}{:<12}".format("observation",round(observation,2))+'\n')
            datacard.write(130*'-')
            datacard.write('\n')
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("bin","ch1","ch1","ch1","ch1","ch1","ch1","ch1","ch1","ch1")+'\n')
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("process",'T1tttt_Scan_mGo' +str(int(mgo))+ '_mLSP'+str(int(mlsp)),'SemiLepTT','DiLepTT','WJ','DY','QCD','SingleT','TTV','VV')+'\n')
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("process",'0','1','2','3','4','5','6','7','8')+'\n')
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("rate",round(Signal/factor,2),round(SemiLepTT_,2),round(DiLepTT_,2),round(WJ_,2),round(DY_,2),round(QCD_,2),round(SingleT_,2),round(TTV_,2),round(VV_,2))+'\n')
            datacard.write(130*'-')
            datacard.write('\n')
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("MCstats"+'T1tttt_Scan_mGo' +str(int(mgo))+ '_mLSP'+str(int(mlsp))+' lnN',round(1.0+(sigerr/((Signal/factor)+0.01)),2),'-','-','-','-','-','-','-','-')+'\n')
            
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("MCstatsSemiLepTT lnN",'-',round(1.0+(SemiLepTTerr_*alpha /(SemiLepTT_ +0.01)),2),'-','-','-','-','-','-','-')+'\n')
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("MCstatsDiLepTT   lnN",'-','-',round(1.0+(DiLepTTerr_*beta  /(DiLepTT_   +0.01)),2),'-','-','-','-','-','-')+'\n')
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("MCstatsWJ        lnN",'-','-','-',round(1.0+(WJerr_*gamma       /(WJ_        +0.01)),2),'-','-','-','-','-')+'\n')
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("MCstatsDY        lnN",'-','-','-','-',round(1.0+(DYerr_*gamma        /(DY_        +0.01)),2),'-','-','-','-')+'\n')
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("MCstatsQCD       lnN",'-','-','-','-','-',round(1.0+(QCDerr_*gamma       /(QCD_       +0.01)),2),'-','-','-')+'\n')
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("MCstatsSingleT   lnN",'-','-','-','-','-','-',round(1.0+(SingleTerr_*gamma   /(SingleT_   +0.01)),2),'-','-')+'\n')
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("MCstatsTTV       lnN",'-','-','-','-','-','-','-',round(1.0+(TTVerr_*gamma       /(TTV_       +0.01)),2),'-')+'\n')
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("MCstatsVV        lnN",'-','-','-','-','-','-','-','-',round(1.0+(VVerr_*gamma        /(VV_        +0.01)),2))+'\n')


            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("sigSyst lnN",1.2,'-','-','-','-','-','-','-','-')+'\n')
            datacard.write("{:<62}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}{:<30}".format("bkguncert lnN",'-',1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1)+'\n')
            datacard.write(130*'-'+'\n')

            '''datacard.write("{:<62}{:<30}".format("SemiLepTT_norm rateParam * SemiLepTT* ",1/float(getSFs(sfs,which='alpha')))+'\n')
            datacard.write("{:<62}{:<30}".format("DiLepTT_norm rateParam * DiLepTT*     ",1/float(getSFs(sfs,which='beta')))+'\n')
            datacard.write("{:<62}{:<30}".format("WJ_norm rateParam * WJ*               ",1/float(getSFs(sfs,which='gamma')))+'\n')
            datacard.write("{:<62}{:<30}".format("DY_norm rateParam * DY*               ",1/float(getSFs(sfs,which='gamma')))+'\n')
            datacard.write("{:<62}{:<30}".format("QCD_norm rateParam * QCD*             ",1/float(getSFs(sfs,which='gamma')))+'\n')
            datacard.write("{:<62}{:<30}".format("SingleT_norm rateParam * SingleT*     ",1/float(getSFs(sfs,which='gamma')))+'\n')
            datacard.write("{:<62}{:<30}".format("TTV_norm rateParam * TTV*             ",1/float(getSFs(sfs,which='gamma')))+'\n')
            datacard.write("{:<62}{:<30}".format("VV_norm rateParam * VV*               ",1/float(getSFs(sfs,which='gamma')))+'\n')'''


    if Limit : 
        print ('limit will be calculated on HTC from ', datacardsdirHDM , 'and ',datacardsdirLDM )
        print ('in this step you will need a valid cmssw dir with higgscombne tools compiled, please check https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/ ')
        print ('you have scpecified CMSSW in this place, ', cmsswdir )

        logdir_1 = outdir+'_LDM/Logs' 
        logdir_2 = outdir+'_HDM/Logs' 
        if not os.path.exists(logdir_1) :  os.makedirs(logdir_1)
        if not os.path.exists(logdir_2) :  os.makedirs(logdir_2)
        schedd = htcondor.Schedd()
        limitOutputdir_1 = os.path.join(outdir+'_LDM','datacards/limitOutput')
        if not os.path.exists(limitOutputdir_1) : os.makedirs(limitOutputdir_1)  
        
        limitOutputdir_2 = os.path.join(outdir+'_HDM','datacards/limitOutput')
        if not os.path.exists(limitOutputdir_2) : os.makedirs(limitOutputdir_2)  

        file_list_1 = glob.glob(datacardsdirLDM+"/*.txt")
        file_list_2 = glob.glob(datacardsdirHDM+"/*.txt")

        import itertools

        for card in file_list_1 : 
            cardname = card.split('/')[-1]
            cmd = '../combinedCards/'+cardname
            submit_parameters = { 
                "executable"                : execu,
                "arguments"                 : " ".join([' '+ cmsswdir, ' '+ os.path.join(os.getcwd(),limitOutputdir_1),' '+ cmd, cardname.replace('.txt','')]),
                "universe"                  : "vanilla",
                "should_transfer_files"     : "YES",
                "log"                       : "{}/job_$(Cluster)_$(Process).log".format(logdir_1),
                "output"                    : "{}/job_$(Cluster)_$(Process).out".format(logdir_1),
                "error"                     : "{}/job_$(Cluster)_$(Process).err".format(logdir_1),
                "when_to_transfer_output"   : "ON_EXIT",
                #'Requirements'              : 'OpSysAndVer == "CentOS7"',

            }
            job = htcondor.Submit(submit_parameters)
            print('going to submit the jobs to HTC')
            with schedd.transaction() as txn:
                job.queue(txn)
                print ("Submit job for configurations of {}".format(card))

        for card in file_list_2 : 
            cardname = card.split('/')[-1]
            cmd = '../combinedCards/'+cardname
            submit_parameters = { 
                "executable"                : execu,
                "arguments"                 : " ".join([' '+ cmsswdir, ' '+ os.path.join(os.getcwd(),limitOutputdir_2),' '+ cmd, cardname.replace('.txt','')]),
                "universe"                  : "vanilla",
                "should_transfer_files"     : "YES",
                "log"                       : "{}/job_$(Cluster)_$(Process).log".format(logdir_2),
                "output"                    : "{}/job_$(Cluster)_$(Process).out".format(logdir_2),
                "error"                     : "{}/job_$(Cluster)_$(Process).err".format(logdir_2),
                "when_to_transfer_output"   : "ON_EXIT",
                #'Requirements'              : 'OpSysAndVer == "CentOS7"',

            }
            job = htcondor.Submit(submit_parameters)
            print('going to submit the jobs to HTC')
            with schedd.transaction() as txn:
                job.queue(txn)
                print ("Submit job for configurations of {}".format(card))


                
                
                