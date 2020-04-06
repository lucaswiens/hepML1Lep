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

channels = [['T5qqqq_Scan','background']]#,['T5qqqq_Scan_','background']]
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
    if (mgo <= 1500 and mlsp <= 800): mass = '1500_1000'
    elif (mgo <= 1500 and mlsp > 800): mass = '1500_1000'
    elif (mgo > 1500 and mgo <= 1900 and mlsp < 800) : mass = '1900_100'
    elif (mgo > 1500 and mgo <= 1900 and mlsp >= 800 and mlsp < 1000 ) : mass = '1900_800'
    elif (mgo > 1900 and mlsp < 800): mass = '2200_100'
    elif (mgo > 1900 and mlsp >= 800 ) :  mass = '2200_800'
    elif (mgo > 1800 and mgo <=1900 and mlsp > 800 and mlsp < 1000) :mass = '1900_1000'
    elif (mgo > 1800 and mgo <=1900 and mlsp >= 1000): mass = '1800_1300'
    elif (mgo >= 1700 and mgo <= 1800 and mlsp >= 1000 ) : mass = '1700_1200'
    elif (mgo >= 1600 and mgo < 1700 and mlsp >= 1000 ) : mass = '1600_1100'
    elif (mgo > 1500 and mgo <1600 and mlsp >= 800 ) : mass = '1500_1000' 
    else : 
        print(mgo,' ',mlsp, 'could not fit into any of you modes please check')
        mass = ''
    return mass

def simpleAsimov(s,b):
    sign = s/sqrt(s+b+(0.2*b)**2)
    return sign

def getSFs(sffile,mass='1900_100',which='alpha') : 
    token = open(sffile,'r')
    linestoken=token.readlines()
    if which == 'alpha' :  tokens_column_number = 1
    if which == 'alphaE' :  tokens_column_number = 2
    if which == 'beta' :  tokens_column_number = 3
    if which == 'betaE' :  tokens_column_number = 4
    resulttoken=[]
    masstoken=[]
    for x in linestoken:
        resulttoken.append(x.split()[tokens_column_number])
        masstoken.append(x.split()[0])
    token.close()
    idx = masstoken.index(mass)
    return resulttoken[idx]


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Runs a NAF batch system for nanoAOD', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--indir', help='List of Signals to process', metavar='indirS')
    #prser.add_argument('--indirB', help='List of BKGs to process', metavar='indirB')
    parser.add_argument('--outdir', help='output directory',default=None, metavar='outdir')
    parser.add_argument('--Limit','-L', help='calculate the limit after making the datacards',default=False, action='store_true')
    parser.add_argument('--cmsswdir', help='cmssw directory',default='/nfs/dust/cms/user/amohamed/susy-desy/deepAK8/CMSSW_9_4_11/src/', metavar='cmsswdir')
    parser.add_argument('--execu', help="wight directory",default='./batch/Limit_exec.sh' ,metavar='execu')
    parser.add_argument('--sfs', help="the text file that has alpha beta gamma",default=None ,metavar='sfs')
    parser.add_argument('--year','--Y', help="Year of the data taken",default=None ,metavar="year")
    parser.add_argument('--oneBin','--ob',help="do one bin analysis or multibins",default=False , action='store_true')


    args = parser.parse_args()
    indirS = args.indir+'/scan'
    indirB = args.indir+'/grid'
    Limit = args.Limit
    cmsswdir = args.cmsswdir
    outdir = args.outdir
    execu = args.execu   
    sfs = args.sfs
    oneBin= args.oneBin

    if not os.path.exists(outdir): os.makedirs(outdir)
    
    datacardsdir = os.path.join(outdir,'datacards/combinedCards')
    if not os.path.exists(datacardsdir):os.makedirs(datacardsdir)       
    signal_List  = os.listdir(indirS)
    background_List = os.listdir(indirB)
    text = open(outdir+"/background_comp.txt", "w+")

    for signal in signal_List : 
        systList = { 
                "Jec_Up"            :    []  ,
                "Jec_Down"          :    []  ,
                "btagSF_b_Up"       :    []  ,
                "btagSF_b_Down"     :    []  ,
                "btagSF_l_Up"       :    []  ,
                "btagSF_l_Down"     :    []  ,
                "ISR_Up"            :    []  ,
                "ISR_Down"          :    []  ,
                "lepSF_Up"          :    []  ,
                "lepSF_Down"        :    []  ,
                "PU_Up"             :    []  ,
                "PU_Down"           :    []  ,
                #"TTxsec_Up"         :    []  ,
                #"TTxsec_Down"       :    []  ,
                #"TTVxsec_Up"        :    []  ,
                #"TTVxsec_Down"      :    []  ,
                "Wpol_Up"           :    []  ,
                "Wpol_Down"         :    []  ,
                #"Wxsec_Up"          :    []  ,
                #"Wxsec_Down"        :    []
                }
        SigsystList = { 
                "Jec_Up"            :    []  ,
                "Jec_Down"          :    []  ,
                "btagSF_b_Up"       :    []  ,
                "btagSF_b_Down"     :    []  ,
                "btagSF_l_Up"       :    []  ,
                "btagSF_l_Down"     :    []  ,
                "ISR_Up"            :    []  ,
                "ISR_Down"          :    []  ,
                "lepSF_Up"          :    []  ,
                "lepSF_Down"        :    []  ,
                "Wpol_Up"           :    []  ,
                "Wpol_Down"         :    []  ,
                }
        if int(args.year) != 2016 : 
            systList.pop('ISR_Up', None)
            systList.pop('ISR_Down', None)
        
        SigsystList.pop('ISR_Up', None)
        SigsystList.pop('ISR_Down', None)
        
        intersection_syst = set(systList).intersection(set(SigsystList))
        #print(intersection_syst)

        lists = []
        signal_files = glob.glob(os.path.join(indirS,signal+'/*SR.root'))
        if not signal_files : 
            print("cannot find this file for ", signal,"will escape it, please check")
            continue
        sf = ROOT.TFile.Open(signal_files[0], "read")
        shist = sf.Get('Signal_1/'+signal+'/sig_0b_SR_nom')
        for skey in SigsystList : 
            SigsystList[skey].append(sf.Get('Signal_1/'+signal+'/sig_0b_SR_'+skey))

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
            hist = ROOT.TH1F('background','background',1000,0.0,1.0)
            for key in systList : 
                systList[key].append(ROOT.TH1F('background_'+key,'background_'+key,1000,0.0,1.0))
            #print(systList)
            
            for bkgf in bkg_files_SR : 
                bkg_name = bkgf.split('/')[-1].split('_')[1]
                if bkg_name == 'Data' : continue 
                bf = ROOT.TFile.Open(bkgf, "read")
                #print(bkg_name+'/'+bkg+'/'+bkg_name+bkg+'sig_SR_nominal')
                bhist = bf.Get(bkg_name+'/'+bkg+'/sig_0b_SR_nom')
                for key in systList : 
                    systList[key].append(bf.Get(bkg_name+'/'+bkg+'/sig_0b_SR_'+key))
                #print(bhist.Integral())
                which = ''
                scalefactor = 1.0
                if bkg_name == 'WJ' : which = 'beta'
                elif bkg_name != 'Data' : which = 'alpha'
                scalefactor = float(getSFs(sfs,mass=bkg,which=which))
                #print(bkg,bkgf)
                #print(bkg)
                bhist.Scale(scalefactor)
                for key in systList : 
                    for i,syst in enumerate(systList[key]) : 
                        scalefactor_syst = float(getSFs(sfs.replace("nom",key),mass=bkg,which=which))
                        if i == 0 : continue
                        syst.Scale(scalefactor_syst)
                        systList[key][0].Add(syst)
                    del systList[key][1:]
                hist.Add(bhist)
                lists.append(hist)
                #blisthist.append(bhist)
            #print('totalBKG ',hist.Integral())
            NBins = hist.GetNbinsX()
            prevSigni = 0.0
            factor = 1.0 
            if mgo < 1400 : factor = 1.0
            bestBin = 0.0
                
            for i in range(NBins,900,-1):
                s = shist.Integral(i,NBins+1)/factor
                b = hist.Integral(i,NBins+1)

                #signi = simpleAsimov(s ,b)

                #if signi > prevSigni or b < 1.0: 
                if b < 0.35 : 
                    #print('better significance when merged ', i ,' to ', NBins+1, ' oldsign =  ',prevSigni , ' newsign = ',  signi)
                    bestBin = i
                 #   prevSigni = signi
                else : 
                    #print('better significance when merged ', i-1 ,' to ', NBins+1, ' oldsign =  ',prevSigni , ' newsign = ',  signi)
                    bestBin = i-1
                    break 
            # this is to inforce the best bin to be 96 which corresponding to DNN >= 0.95, this will ignor the significance calculations above
        lastbinW = NBins+1 - bestBin
        beforelastbin = bestBin -1 
        otherWs = []
        otherbins = []
        for i in range(0,5) : 
            if beforelastbin < 900 : continue 
            otherbinW = (2+i)*lastbinW
            bin = beforelastbin - otherbinW
            otherWs.append(otherbinW)
            otherbins.append([bin,beforelastbin])
            beforelastbin = bin -1 
        #otherbins.append([800,beforelastbin-1])
        otherbins = otherbins[::-1]
        #print(otherbins)
        SRbins = otherbins
        SRbins.append([bestBin,1001])
        #print(SRbins)
        if not oneBin : 
            for num, bin in enumerate(SRbins) : 
                #print(bestBin)
                bestBin = int(bin[0])
                NBins = int(bin[1]-1)
                sigerr = ROOT.Double(0.)
                bkgerr = ROOT.Double(0.)
                shist.Scale(1.0/factor)
                sigRate = shist.IntegralAndError(bestBin,NBins+1,sigerr)
                bkgRate = hist.IntegralAndError(bestBin,NBins+1,bkgerr)
                
                for key in systList : 
                    syst_int = systList[key][0].Integral(bestBin,NBins+1)
                    systList[key].append(syst_int)
                    impact = round((syst_int/(bkgRate+0.01)),2)
                    invimpact = round((1/(impact+0.001)),2)
                    systList[key].append(impact if impact >= 1.0 else invimpact )

                for key in SigsystList : 
                    syst_int = SigsystList[key][0].Integral(bestBin,NBins+1)
                    SigsystList[key].append(syst_int)
                    impact = round((syst_int/((sigRate)+0.01))/factor,2)
                    invimpact = round((1/(impact+0.001)),2)
                    SigsystList[key].append(impact if impact >= 1.0 else invimpact )

                if sigRate == 0.0 : 
                    print ('Signal',mgo,mlsp, 'has zero rate will not write the datacard for it ')
                    continue 
                #sigerr  = 1.0 + sqrt(sigRate)/(sigRate+0.01)
                #bkgerr  = 1.0 + sqrt(bkgRate)/(bkgRate + 0.01)
                alphaE  = float(getSFs(sfs,mass=bkg,which='alphaE')) + 1.0
                betaE  = float(getSFs(sfs,mass=bkg,which='betaE')) + 1.0
     
                #del systList , SigsystList
                datacardsdir = os.path.join(outdir,'datacards/T5qqqq_Scan_mGo'+str(int(mgo))+ '_mLSP'+str(int(mlsp)))
                if not os.path.exists(datacardsdir):
                    os.makedirs(datacardsdir)
                datacard = open(datacardsdir+'/bin_'+str(num)+'.txt', 'w'); 
                datacard.write("## Datacard for signal %s (with bins from  %s to %s)\n"%('T5qqqq_Scan_mGo' +str(int(mgo))+ '_mLSP'+str(int(mlsp)),str(bestBin),str(NBins+1)))
                datacard.write("imax 1 number of bins \n")
                datacard.write("jmax * number of processes minus 1 \n")
                datacard.write("kmax * number of nuisance parameters \n")
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
                datacard.write("{:<62}{:<30}{:<30}".format("process",'T5qqqq_Scan_mGo' +str(int(mgo))+ '_mLSP'+str(int(mlsp)),"background")+'\n')
                datacard.write("{:<62}{:<30}{:<30}".format("process",'0',"1")+'\n')
                datacard.write("{:<62}{:<30}{:<30}".format("rate",round(sigRate,2),round(bkgRate,2))+'\n')
                datacard.write(130*'-')
                datacard.write('\n')
                datacard.write("{:<62}{:<30}{:<30}".format("MCstats"+'T5qqqq_Scan_mGo' +str(int(mgo))+ '_mLSP'+str(int(mlsp))+' lnN',round(1.0+(sigerr/((sigRate)+0.01)),2),'-')+'\n')
                datacard.write("{:<62}{:<30}{:<30}".format("MCstatsbackground lnN",'-',round(1.0+(bkgerr/(bkgRate+0.01)),2))+'\n')
                datacard.write("{:<62}{:<30}{:<30}".format("lumi lnN",str(1.023 if int(args.year) == 2017 else 1.025),str(1.023 if int(args.year) == 2017 else 1.025))+'\n')
                datacard.write("{:<62}{:<30}{:<30}".format("DNNshape lnN",str(1.1),str(1.1))+'\n')
                for syst in systList : 
                    if "Down" in syst : continue
                    if syst in intersection_syst : 
                        sigVar = 1/2*(SigsystList[syst][2*(num+1)]+SigsystList[syst.replace("Up","Down")][2*(num+1)])
                        bkgVar = 1/2*(systList[syst][2*(num+1)]+systList[syst.replace("Up","Down")][2*(num+1)])
                        datacard.write("{:<62}{:<30}{:<30}".format(syst.replace("_Up","")+args.year[-2:]+" lnN",str(round(sigVar,2)),str(round(bkgVar,2)))+'\n')
                    else :
                        bkgVar = 1/2*(systList[syst][2*(num+1)]+systList[syst.replace("Up","Down")][2*(num+1)])
                        datacard.write("{:<62}{:<30}{:<30}".format(syst.replace("_Up","")+args.year[-2:]+" lnN",'-',str(round(bkgVar,2)))+'\n')
                for syst in SigsystList : 
                    if "Down" in syst : continue
                    if syst in intersection_syst : continue # already taken into account in the previous loop
                    else :
                        sigVar = 1/2*(SigsystList[syst][2*(num+1)]+SigsystList[syst.replace("Up","Down")][2*(num+1)])
                        datacard.write("{:<62}{:<30}{:<30}".format(syst.replace("_Up","")+args.year[-2:]+" lnN",str(round(sigVar,2)),'-')+'\n')
        if oneBin :
            bestBin = int(SRbins[-1][0])
            sigerr = ROOT.Double(0.)
            bkgerr = ROOT.Double(0.)
            shist.Scale(1.0/factor)
            sigRate = shist.IntegralAndError(bestBin,NBins+1,sigerr)
            bkgRate = hist.IntegralAndError(bestBin,NBins+1,bkgerr)
            
            for key in systList : 
                syst_int = systList[key][0].Integral(bestBin,NBins+1)
                systList[key].append(syst_int)
                impact = round((syst_int/(bkgRate+0.01)),2)
                invimpact = round((1/(impact+0.001)),2)
                systList[key].append(impact if impact >= 1.0 else invimpact )

            for key in SigsystList : 
                syst_int = SigsystList[key][0].Integral(bestBin,NBins+1)
                SigsystList[key].append(syst_int)
                impact = round((syst_int/((sigRate)+0.01))/factor,2)
                invimpact = round((1/(impact+0.001)),2)
                SigsystList[key].append(impact if impact >= 1.0 else invimpact )

            if sigRate == 0.0 : 
                print ('Signal',mgo,mlsp, 'has zero rate will not write the datacard for it ')
                continue 
            #sigerr  = 1.0 + sqrt(sigRate)/(sigRate+0.01)
            #bkgerr  = 1.0 + sqrt(bkgRate)/(bkgRate + 0.01)
            alphaE  = float(getSFs(sfs,mass=bkg,which='alphaE')) + 1.0
            betaE  = float(getSFs(sfs,mass=bkg,which='betaE')) + 1.0
            #del systList , SigsystList
            datacard = open(datacardsdir+ '/T5qqqq_Scan_mGo' +str(int(mgo))+ '_mLSP'+str(int(mlsp))+'.txt', 'w'); 
            datacard.write("## Datacard for signal %s (with bins from  %s to %s)\n"%('T5qqqq_Scan_mGo' +str(int(mgo))+ '_mLSP'+str(int(mlsp)),str(bestBin),str(NBins+1)))
            datacard.write("imax 1 number of bins \n")
            datacard.write("jmax * number of processes minus 1 \n")
            datacard.write("kmax * number of nuisance parameters \n")
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
            datacard.write("{:<62}{:<30}{:<30}".format("process",'T5qqqq_Scan_mGo' +str(int(mgo))+ '_mLSP'+str(int(mlsp)),"background")+'\n')
            datacard.write("{:<62}{:<30}{:<30}".format("process",'0',"1")+'\n')
            datacard.write("{:<62}{:<30}{:<30}".format("rate",round(sigRate,2),round(bkgRate,2))+'\n')
            datacard.write(130*'-')
            datacard.write('\n')
            datacard.write("{:<62}{:<30}{:<30}".format("MCstats"+'T5qqqq_Scan_mGo' +str(int(mgo))+ '_mLSP'+str(int(mlsp))+' lnN',round(1.0+(sigerr/((sigRate)+0.01)),2),'-')+'\n')
            datacard.write("{:<62}{:<30}{:<30}".format("MCstatsbackground lnN",'-',round(1.0+(bkgerr/(bkgRate+0.01)),2))+'\n')
            datacard.write("{:<62}{:<30}{:<30}".format("lumi lnN",str(1.023 if int(args.year) == 2017 else 1.025),str(1.023 if int(args.year) == 2017 else 1.025))+'\n')
            datacard.write("{:<62}{:<30}{:<30}".format("DNNshape lnN",str(1.1),str(1.1))+'\n')
            for syst in systList : 
                if "Down" in syst : continue
                if syst in intersection_syst : 
                    sigVar = 1/2*(SigsystList[syst][2]+SigsystList[syst.replace("Up","Down")][2])
                    bkgVar = 1/2*(systList[syst][2]+systList[syst.replace("Up","Down")][2])
                    datacard.write("{:<62}{:<30}{:<30}".format(syst.replace("_Up","")+args.year[-2:]+" lnN",str(round(sigVar,2)),str(round(bkgVar,2)))+'\n')
                else :
                    bkgVar = 1/2*(systList[syst][2]+systList[syst.replace("Up","Down")][2])
                    datacard.write("{:<62}{:<30}{:<30}".format(syst.replace("_Up","")+args.year[-2:]+" lnN",'-',str(round(bkgVar,2)))+'\n')
            for syst in SigsystList : 
                if "Down" in syst : continue
                if syst in intersection_syst : continue # already taken into account in the previous loop
                else :
                    sigVar = 1/2*(SigsystList[syst][2]+SigsystList[syst.replace("Up","Down")][2])
                    datacard.write("{:<62}{:<30}{:<30}".format(syst.replace("_Up","")+args.year[-2:]+" lnN",str(round(sigVar,2)),'-')+'\n')
        
        #datacard.write("{:<62}{:<30}{:<30}".format("bkguncert lnN",'-',1.1)+'\n')
        #datacard.write("{:<62}{:<30}{:<30}".format("alphauncert lnN",'-',alphaE)+'\n')
        #datacard.write("{:<62}{:<30}{:<30}".format("betauncert lnN",'-',betaE)+'\n')
        #datacard.write("{:<62}{:<30}{:<30}".format("gammauncert lnN",'-',gammaE)+'\n')

    if Limit and oneBin: 
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
                
                