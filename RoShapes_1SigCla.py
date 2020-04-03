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
from plotClass.SRs.search_regions_1SigCla import All_files

import plotClass.SRs.search_regions_1SigCla as sr

import os 
import datetime

from math import hypot, sqrt, ceil

currentDT = datetime.datetime.now()

import argparse

selected_vars = sr.categories
SRs_cut_strings =  sr.SRs_cut_strings
CRs1_cut_strings = sr.CRs_1_cut_strings
CRs2_cut_strings = sr.CRs_2_cut_strings
CRs3_cut_strings = sr.CRs_3_cut_strings
CRs4_cut_strings = sr.CRs_4_cut_strings

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
    hist.GetXaxis().SetTitle(var)
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
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Runs a NAF batch system for nanoAOD', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--indir', help='List of datasets to process', metavar='indir')
    parser.add_argument('--outdir', help='output directory',default=None, metavar='outdir')
    parser.add_argument('--exec', help="wight directory",default='./batch/shape_exec_1SigCla.sh' ,metavar='exec')
    parser.add_argument('--lumi', help='name of the model with out extensions',default='0', metavar='lumi')
    parser.add_argument('--scan', help='signal or background shapes',default=False, action='store_true')
    parser.add_argument('--batch','-b', help=' set it to true if you want to evaluate paramtric training for each mass point',default=False,action='store_true')
    parser.add_argument('--group','-g', help='which background/signal list to be analyzed',default='SemiLepTT', metavar='group')
    parser.add_argument('--cutdict','-cut' ,help='which cut dicts to be applied SR/CR1/CR2...etc',default='SR', metavar='cutdict')
    parser.add_argument('--doSyst','-syst' ,help='save the systematic shapes',default=False, action='store_true')
    parser.add_argument("-Y", "--year", default=2016, help="which ear to run on 2016/17/18",metavar='year')
    parser.add_argument('--mass','-m' ,help='which cut dicts to be applied',default='1500_1000', metavar='mass')

    args = parser.parse_args()

    if int(args.year) != 2016 : 
        for key in All_files : 
            All_files[key]['scale']  = All_files[key]['scale'].replace("*nISRttweight","")
    elif int(args.year) == 2018 :
        for key in All_files: 
            if "Data" in key or "Signal_" in key : continue 
            All_files[key]['scale']  = All_files[key]['scale'].replace('*lepSF',"*lepSF*HEM_MC_SF")
    indir = args.indir
    if args.doSyst : 
        import copy
        # staff for JEC
        All_files_Jec_up = copy.deepcopy(All_files)
        All_files_Jec_dn = copy.deepcopy(All_files)
        ext_JecUp = args.indir.split("/")[-2]+"JEC_up_"
        indirJecUp = args.indir.replace(args.indir.split("/")[-2],ext_JecUp)
        indirJecdown = indirJecUp.replace("JEC_up_","JEC_down_")
        if not os.path.exists(indirJecUp) or not os.path.exists(indirJecdown) : 
            print(indirJecUp,"and",indirJecdown, "are not existing but you instructed me to doSyst, check the paths or remove the argument --doSyst/-syst, for the moment i will brack until you decide. Have fun!!" )
            sys.exit()
        # staff for other norm Systmatics, 
        from plotClass.norm_syst import *
        systList = {"btagSF_b" : btagSF_b,
                    "btagSF_l" : btagSF_l,
                    "ISR" : ISR,
                    "lepSF" : lepSF,
                    "PU" : PU,
                    "TTxsec" : TTxsec,
                    "TTVxsec" : TTVxsec,
                    "Wpol" : Wpol,
                    "Wxsec" : Wxsec}
        # remove the ISR for 2017/2018
        if int(args.year) != 2016 : 
            #del systList["ISR"]
            for syst in systList : 
                for key in systList[syst] : 
                    systList[syst][key]['scale_up']  = systList[syst][key]['scale_up'].replace("*nISRttweightsyst_up","").replace("*nISRttweight","")
                    systList[syst][key]['scale_dn']  = systList[syst][key]['scale_dn'].replace("*nISRttweightsyst_down","").replace("*nISRttweight","")
        elif int(args.year) == 2018 :
            for syst in systList : 
                for key in systList[syst] : 
                    if "Data" in key or "Signal_" in key : continue 
                    systList[syst][key]['scale_up']  = systList[syst][key]['scale_up'].replace("*lepSF","").replace("*lepSF*HEM_MC_SF","")
                    systList[syst][key]['scale_dn']  = systList[syst][key]['scale_dn'].replace("*lepSF","").replace("*lepSF*HEM_MC_SF","")        
        #sys.exit()
               
    outdir = args.outdir
    execu = args.exec
    logdir = outdir+'/Logs' 
    lumi = args.lumi
    batch = args.batch
    sig = args.scan
    group = args.group
    cutdict = args.cutdict
    mass = args.mass


    print('configs are : ', indir , outdir , lumi , batch ,cutdict ,sig)
    ranges = [1000,0.0,1.0]
    if cutdict == 'SR' : cutdict_ = SRs_cut_strings
    elif cutdict == 'CR1' : cutdict_ = CRs1_cut_strings
    elif cutdict == 'CR2' : cutdict_ = CRs2_cut_strings
    elif cutdict == 'CR3' : cutdict_ = CRs3_cut_strings
    elif cutdict == 'CR4' : cutdict_ = CRs4_cut_strings
    if int(args.year) == 2018 :
        cutdict_+="&& (!isData || (Run < 319077) || ( nHEMJetVeto == 0 && nHEMEleVeto == 0))"

    wdir = os.getcwd()
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if not os.path.exists(logdir):
        os.makedirs(logdir) 
    
    

    if sig : massdir = os.path.join(outdir,'scan/'+mass)
    else :  massdir = os.path.join(outdir,'grid/')
    
    print ('output will be written in ', massdir)
    #massdir = os.path.join(outdir,mass)
    
    if not os.path.exists(massdir): os.makedirs(massdir)

    instPlot = rootplot(indir,outdir,All_files=All_files)
    if args.doSyst : 
        instPlot_Jec_up = rootplot(indirJecUp,outdir,All_files=All_files_Jec_up)
        instPlot_Jec_dn = rootplot(indirJecdown,outdir,All_files=All_files_Jec_dn)
    cuttext = open(massdir+"/"+cutdict+".txt", "w+")
    if not batch : 
        cuts = cutdict_
        g  = group
        if sig : g  = 'Signal_1'
        print ('producing the shapes for :',g )
        # fill the dictionary with all the files founded under the indir under each category 
        All_files[g]['files'] = instPlot.group[g]
        if args.doSyst : 
            All_files_Jec_up[g]['files'] = instPlot_Jec_up.group[g]
            All_files_Jec_dn[g]['files'] = instPlot_Jec_dn.group[g]
        # make chain with proposed cuts
        if not sig : 
            extraCuts = All_files[g]['select']
            scale = All_files[g]['scale']
        else : 
            All_files['Signal_1']['files'] = instPlot.group['Signal_1']
            if args.doSyst : All_files_Jec_up['Signal_1']['files'] = instPlot_Jec_up.group['Signal_1'] ; All_files_Jec_dn['Signal_1']['files'] = instPlot_Jec_dn.group['Signal_1']
            extraCuts = "&& mGo =="+mass.split('_')[0]+ "&& mLSP == "+mass.split('_')[1]
            scale = All_files['Signal_1']['scale']
        print (cuts + extraCuts)
        cuttext.write('cuts applied are :'+cuts + extraCuts+'\n')
        chain = instPlot.chain_and_cut(filesList = All_files[g]['files'],Tname = "sf/t",cutstring = cuts,extraCuts =extraCuts)
        if args.doSyst : 
            chain_Jec_up = instPlot_Jec_up.chain_and_cut(filesList = All_files_Jec_up[g]['files'],Tname = "sf/t",cutstring = cuts,extraCuts =extraCuts)
            chain_Jec_dn = instPlot_Jec_dn.chain_and_cut(filesList = All_files_Jec_dn[g]['files'],Tname = "sf/t",cutstring = cuts,extraCuts =extraCuts)
            print(chain_Jec_up.GetEntries())
            print(chain_Jec_dn.GetEntries())
        print(chain.GetEntries())
        # create the output root file
        if sig : 
            outroot = ROOT.TFile(massdir+"/shapes_{0}_{1}_{2}".format(g,mass,cutdict)+".root","recreate")
        else : outroot = ROOT.TFile(massdir+"/shapes_{0}_{1}".format(g,cutdict)+".root","recreate")
        outroot.mkdir(g)
        outroot.cd(g)
        if sig : 
            ROOT.gDirectory.mkdir(mass)
            ROOT.gDirectory.cd(mass)

        error = ROOT.Double(0.)
        for var in selected_vars :
            v = var
            print(v)
            # draw the variable to the hist created 
            if 'Data' in g : lum = '1.0' 
            else  : lum = lumi
            # make the hist 
            hist = make1D(v,All_files[g],v+'_'+cutdict+"_nom",ranges)
            chain.Draw(v +' >> '+v+'_'+cutdict+"_nom", scale+'*'+lum+'*(1)',"goff")
            if args.doSyst : 
                # JEC comes from differnt nTuples
                hist_jec_up = make1D(v,All_files_Jec_up[g],v+'_'+cutdict+"_Jec_Up",ranges)
                chain_Jec_up.Draw(v +' >> '+v+'_'+cutdict+"_Jec_Up", scale+'*'+lum+'*(1)',"goff")
                hist_jec_dn = make1D(v,All_files_Jec_dn[g],v+'_'+cutdict+"_Jec_Down",ranges)
                chain_Jec_dn.Draw(v +' >> '+v+'_'+cutdict+"_Jec_Down", scale+'*'+lum+'*(1)',"goff")
                hist_jec_up.Write()
                hist_jec_dn.Write()
                # nomalization systematics
                if not 'Data' in g : 
                    for syst in systList : 
                        hist_norm_syst_up = make1D(v,All_files[g],v+'_'+cutdict+'_'+syst+"_Up",ranges)
                        hist_norm_syst_dn = make1D(v,All_files[g],v+'_'+cutdict+'_'+syst+"_Down",ranges)
                        scale_up = systList[syst][g]['scale_up']
                        scale_dn = systList[syst][g]['scale_dn']
                        chain.Draw(v +' >> '+v+'_'+cutdict+'_'+syst+"_Up", scale_up+'*'+lum+'*(1)',"goff")
                        chain.Draw(v +' >> '+v+'_'+cutdict+'_'+syst+"_Down", scale_dn+'*'+lum+'*(1)',"goff")
                        hist_norm_syst_up.Write()
                        hist_norm_syst_dn.Write()
            #print (hist)
            #hist.Sumw2()
            hist.Write()
        outroot.cd('')
        outroot.Close()
    elif batch :
        import htcondor
        schedd = htcondor.Schedd()
        cmd_array = []
        print('batch mode activated ...')
        regions = ['SR','CR1','CR2','CR3','CR4']
        #sub = htcondor.Submit("")
        ##Condor configuration
        
        if not sig : 
            print('going to run on backgrounds')
            m = "1500_1000"
            for reg in regions : 
                if args.doSyst :
                    for g in instPlot.group :
                        if  'Sig' in g : continue
                        cmd_array.append(" ".join([wdir,indir,outdir,lumi,g,reg,m,args.year,"--doSyst"]))
                        print ("Submit job for configurations of {}{}{}{}{}".format(m,' ',g,' ',reg))
                else : 
                    for g in instPlot.group :
                        if  'Sig' in g : continue
                        cmd_array.append(" ".join([wdir,indir,outdir,lumi,g,reg,m,args.year]))
                        print ("Submit job for configurations of {}{}{}{}{}".format(m,' ',g,' ',reg))

        else : 
            regions = ['SR']
            mList = masslist('mass_list_all.txt')
            print('going to run on signals')
            for m in mList : 
                #for g in instPlot.group :
                #    if g != 'Signal_1' : continue
                #    for reg in regions : 
                        ##Condor configuration
                if args.doSyst : 
                    for g in instPlot.group :
                        if g != 'Signal_1' : continue
                        for reg in regions : 
                            cmd_array.append(" ".join([wdir,indir,outdir,lumi,g,reg,m,args.year,'--doSyst','--scan']))
                            #print ("Submit job for configurations of {}{}{}{}{}".format(m,' ',g,' ',reg))
                else : 
                    for g in instPlot.group :
                        if g != 'Signal_1' : continue
                        for reg in regions : 
                            cmd_array.append(" ".join([wdir,indir,outdir,lumi,g,reg,m,args.year,'--scan']))
                            #print ("Submit job for configurations of {}{}{}{}{}".format(m,' ',g,' ',reg))
        
        
        for comd in cmd_array : 
            submit_parameters = { 
                "executable"                : execu,
                "arguments"                 : comd,
                "universe"                  : "vanilla",
                "should_transfer_files"     : "YES",
                "log"                       : "{}/job_$(Cluster)_$(Process).log".format(logdir),
                "output"                    : "{}/job_$(Cluster)_$(Process).out".format(logdir),
                "error"                     : "{}/job_$(Cluster)_$(Process).err".format(logdir),
                "when_to_transfer_output"   : "ON_EXIT",
                #'Requirements'              : 'OpSysAndVer == "CentOS7"',
            }
            job = htcondor.Submit(submit_parameters)
            #print('going to submit the jobs to HTC')
            with schedd.transaction() as txn:
                job.queue(txn)
                print ("Submit job for configurations of {}".format(comd))

    

