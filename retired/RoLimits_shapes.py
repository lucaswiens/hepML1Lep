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

#channels = ['Data','Signal_1','SemiLepTT','DiLepTT','WJ','DY','QCD','SingleT','TTV','VV']
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
    elif (mgo > 1500 and mgo <1600 and mlsp >= 800 ) : mass = '1500_1100' 
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
    elif which == 'alphaE' :  tokens_column_number = 2
    elif which == 'beta' :  tokens_column_number = 3
    elif which == 'betaE' :  tokens_column_number = 4
    elif which == 'gamma' :  tokens_column_number = 5
    elif which == 'gammaE' :  tokens_column_number = 6
    else : return 1.0
    resulttoken=[]
    masstoken=[]
    for x in linestoken:
        resulttoken.append(x.split()[tokens_column_number])
        masstoken.append(x.split()[0])
    token.close()
    idx = masstoken.index(mass)
    return resulttoken[idx]


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Runs a NAF batch system 1Lep Limits', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--infile', help='List of Signals to process', metavar='infile')
    #prser.add_argument('--indirB', help='List of BKGs to process', metavar='indirB')
    parser.add_argument('--outdir', help='output directory',default=None, metavar='outdir')
    parser.add_argument('--Limit','-L', help='calculate the limit after making the datacards',default=False, action='store_true')
    parser.add_argument('--cmsswdir', help='cmssw directory',default='/nfs/dust/cms/user/amohamed/susy-desy/deepAK8/CMSSW_9_4_11/src/', metavar='cmsswdir')
    parser.add_argument('--execu', help="wight directory",default='./batch/Limit_exec.sh' ,metavar='execu')
    parser.add_argument('--sfs', help="the text file that has alpha beta gamma",default=None ,metavar='sfs')
    parser.add_argument('--year','-Y', help="year to be analyzed 2016/17/18",default=None ,metavar='year')
    parser.add_argument('--blind', help="blind or unblind analysis",default=True ,action='store_true')


    
    binned = False
    args = parser.parse_args()
    Limit = args.Limit
    cmsswdir = args.cmsswdir
    outdir = args.outdir
    execu = args.execu   
    sfs = args.sfs
    infile = ROOT.TFile.Open(args.infile)
    channels_dict = {}
    # step 1 getting the list of subdires and channels and form a dict with them
    for key in infile.GetListOfKeys():
        obj = infile.GetDirectory(key.GetName())
        channels_dict[key.GetName()] =  {'dir_list' : [key.GetName()+"/"+x.GetName() for x in obj.GetListOfKeys()]}
    # step 2 put the path to the histogram
    for key in channels_dict : 
        #if "Signal_1" in key : continue
        for i,list_ in enumerate(channels_dict[key]['dir_list']): 
            obj = infile.GetDirectory(list_)
            hist_list = [channels_dict[key]['dir_list'][i]+'/'+x.GetName() for x in obj.GetListOfKeys()]
            SR_histList = [x for x in hist_list if '_SR' in x ]
            channels_dict[key][list_] = SR_histList
    # step 3 clean it up 
    for key in  channels_dict :
        del channels_dict[key]['dir_list']
        #print(channels_dict[key])
    #print(channels_dict) 
    #step 4 make shape hist.root with all SFs applied
    outfile = ROOT.TFile(args.infile.replace(".root","_scaled.root"),"recreate")
    for key in channels_dict : 
        for subkey in channels_dict[key] : 
            outfile.cd()
            outfile.mkdir(subkey)
            if 'DiLepTT' in subkey                                  : which = 'beta'
            elif 'SemiLepTT' in subkey                              : which = 'alpha'
            elif not ('Data' in subkey or 'Signal_1' in  subkey)    : which = 'gamma'
            else : which = 'nottoscale'
            scalefactor = float(getSFs(sfs,mass=subkey.split('/')[-1],which=which))
            for hist in channels_dict[key][subkey] : 
                hist_ = infile.Get(hist)
                #print(hist)
                hist_.Scale(scalefactor)
                outfile.cd(subkey)
                if "up" in hist_.GetName() : hist_.SetName(hist_.GetName().replace("up","Up"))
                if "dn" in hist_.GetName() : hist_.SetName(hist_.GetName().replace("dn","Down"))
                hist_.Write()
    # outfile.Close()
    # Step 5 make total background shapes -- only for the nominals -- to be used in blind analysis when you use the backgroud shapes instead of data
    outfile.cd()
    total_bkg_hist = outfile.Get("VV/2200_100/sig_SR_nom").Clone()
    total_bkg_hist.SetTitle("total background")
    hists = {}
    for key in channels_dict : 
        if 'Data' in key or 'Signal_1' in  key : continue
        for subkey in channels_dict[key] : 
            #print(channels_dict[key][subkey])
            mass = subkey.split('/')[-1]
            #if mass in hists : 
            #    hists[mass].append(hist for hist in channels_dict[key][subkey] if (mass in hist and 'sig_SR_nom' in hist))
            #else : 
            #    hists[mass] = [hist for hist in channels_dict[key][subkey] if (mass in hist and 'sig_SR_nom' in hist)]
            for hist in channels_dict[key][subkey] : 
                if (mass in hist and 'sig_SR_nom' in hist) : 
                    hists.setdefault(mass, []).append(hist)
    #print(hists)
    for key in hists : 
        total_bkg_hist.Reset()
        outfile.cd()
        outfile.mkdir('background/'+key)
        total_bkg_hist.SetName(key+'sig_SR_nom')
        for hist in hists[key] : 
            
            histo = outfile.Get(hist)
            #print(hist,histo.Integral())
            total_bkg_hist.Add(histo)
        outfile.cd('background/'+key)
        #print("Total background : ",total_bkg_hist.Integral())
        total_bkg_hist.Write()
        total_bkg_hist.Reset()
    outfile.Close()
    
    # step 6 write the data cards
    shapes = ROOT.TFile.Open(args.infile.replace(".root","_scaled.root"))
    if not os.path.exists(outdir): os.makedirs(outdir)
    datacardsdir = os.path.join(outdir,'datacards/combinedCards')
    if not os.path.exists(datacardsdir):os.makedirs(datacardsdir)
    
    signal_List  = [x.GetName() for x in shapes.Get('Signal_1').GetListOfKeys()]
    background_List = [x.GetName() for x in shapes.Get('background').GetListOfKeys()]
    text = open(outdir+"/background_comp.txt", "w+")
    os.system("cp "+args.infile.replace(".root","_scaled.root")+" "+datacardsdir)
    for signal in signal_List : 
        shist = shapes.Get('Signal_1/'+signal+'/sig_SR_nom')
        mgo = float(signal.split('_')[0])
        mlsp = float(signal.split('_')[1])
        bkgToUse_ = bkgToUse(mgo,mlsp)
        datacard = open(datacardsdir+ '/T1tttt_Scan_mGo' +str(int(mgo))+ '_mLSP'+str(int(mlsp))+'.txt', 'w'); 
        #print('mgo ',mgo,' mlsp ',mlsp,' bkgToUse ', bkgToUse_)
        text.write("{:<10}{:<10}{:<10}{:<10}{:<10}{:<10}".format('mgo',mgo,'mlsp',mlsp,'bkgToUse', bkgToUse_)+"\n")
        for bkg in background_List : 
            if bkg != bkgToUse_ : continue 
            bkg_hists_SR = [x.GetName()+"/"+bkg+"/sig_SR_nom" for x in shapes.GetListOfKeys() if not 'Signal_1' in x.GetName()]
            bkg_hists_norms = []
            bkg_hists_names = []
            for bkghist in bkg_hists_SR : 
                bhist = shapes.Get(bkghist)
                bkg_hists_norms.append(round(bhist.Integral(),2))
                bkg_hists_names.append(bkghist.split('/')[0])
        data_hist_name = "background/"+bkgToUse_+"/sig_SR_nom" if args.blind else "Data/"+bkgToUse_+"/sig_SR_nom"
        shape_file_name = args.infile.replace(".root","_scaled.root")
        data_hist = shapes.Get(data_hist_name)
        datacard.write("## Datacard for signal %s \n"%('T1tttt_Scan_mGo' +str(int(mgo))+ '_mLSP'+str(int(mlsp))))
        datacard.write("imax 1 number of channels\n")
        datacard.write("jmax * number of backgrounds \n")
        datacard.write("kmax * number of nuisance parameters \n")
        datacard.write(130*'-')
        datacard.write('\n')
        datacard.write("shapes\tdata_obs\tch1\t %s \t %s \n"%(shape_file_name,data_hist_name))
        datacard.write("observation\t"+str(round(data_hist.Integral(),2))+'\n')
        datacard.write("shapes\t * \t ch1 \t"+shape_file_name+"\t$PROCESS/"+bkgToUse_+"/sig_SR_nom\t $PROCESS/"+bkgToUse_+"/sig_SR_$SYSTEMATIC\n")
        datacard.write("shapes\tSignal_1\tch1\t"+shape_file_name+"\t$PROCESS/"+signal+"/sig_SR_nom\t$PROCESS/"+signal+"/sig_SR_$SYSTEMATIC\n")
        datacard.write(130*'-')
        datacard.write('\n')
        datacard.write("{:<20}".format("bin"))
        for i in range(len(bkg_hists_SR)-1) : 
            datacard.write("{:20}".format("ch1"))
        datacard.write('\n')
        datacard.write("{:<20}".format("process"))
        datacard.write("{:20}".format("Signal_1"))
        for i in range(len(bkg_hists_SR)-1) : 
            if "background" in bkg_hists_names[i] or  "Data" in bkg_hists_names[i] : continue
            datacard.write("{:20}".format(bkg_hists_names[i]))
        datacard.write('\n')
        datacard.write("{:<20}".format("process"))
        for i in range(len(bkg_hists_SR)-1) : 
            datacard.write("{:20}".format(str(i)))
        datacard.write('\n')
        datacard.write("{:<20}".format("rate"))
        datacard.write("{:20}".format(str(round(shist.Integral(),2))))
        for i in range(len(bkg_hists_SR)-1) : 
            if "background" in bkg_hists_names[i] or "Data" in bkg_hists_names[i] : continue
            datacard.write("{:20}".format(str(bkg_hists_norms[i])))
        datacard.write('\n')
        datacard.write(130*'-')
        datacard.write('\n')
        datacard.write("{:20}".format("lumi lnN"))
        for i in range(len(bkg_hists_SR)-1) : 
            datacard.write("{:20}".format(str(1.023 if int(args.year) == 2017 else 1.025)))
        datacard.write('\n')
        datacard.write("{:20}".format("DNNshape lnN"))
        for i in range(len(bkg_hists_SR)-1) : 
            datacard.write("{:20}".format(str(1.1)))
        datacard.write('\n')
        datacard.write("{:20}".format("Jec_ shape"))
        for i in range(len(bkg_hists_SR)-1) : 
            if not "WJ" in bkg_hists_names[i] : datacard.write("{:20}".format(str(1.0)))
            else : datacard.write("{:20}".format("-"))
        datacard.write('\n')
        datacard.write("{:20}".format("btagSF_b_ shape"))
        for i in range(len(bkg_hists_SR)-1) : 
            datacard.write("{:20}".format(str(1.0)))
        datacard.write('\n')
        datacard.write("{:20}".format("btagSF_l_ shape"))
        for i in range(len(bkg_hists_SR)-1) : 
            datacard.write("{:20}".format(str(1.0)))
        datacard.write('\n')
        datacard.write("{:20}".format("lepSF_ shape"))
        for i in range(len(bkg_hists_SR)-1) : 
            datacard.write("{:20}".format(str(1.0)))
        datacard.write('\n')
        datacard.write("{:20}".format("PU_ shape"))
        for i in range(len(bkg_hists_SR)-1) : 
            datacard.write("{:20}".format(str(1.0)))
        datacard.write('\n')
        datacard.write("{:20}".format("TTxsec_ shape"))
        for i in range(len(bkg_hists_SR)-1) : 
            if not ("SemiLepTT" in bkg_hists_names[i] or "DiLepTT" in bkg_hists_names[i] ) : datacard.write("{:20}".format('-'))
            else : datacard.write("{:20}".format(str(1.0)))
        datacard.write('\n')
        datacard.write("{:20}".format("TTVxsec_Up lnN"))
        for i in range(len(bkg_hists_SR)-1) : 
            if not ("TTV" in bkg_hists_names[i] ) : datacard.write("{:20}".format('-'))
            else : datacard.write("{:20}".format(str(2.0)))
        datacard.write('\n')
        datacard.write("{:20}".format("TTVxsec_Down lnN"))
        for i in range(len(bkg_hists_SR)-1) : 
            if not ("TTV" in bkg_hists_names[i] ) : datacard.write("{:20}".format('-'))
            else : datacard.write("{:20}".format(str(0.0)))
        datacard.write('\n')
        datacard.write("{:20}".format("Wpol_ lnN"))
        for i in range(len(bkg_hists_SR)-1) : 
            datacard.write("{:20}".format(str(1.0)))
        datacard.write('\n')
        datacard.write("{:20}".format("Wxsec_ shape"))
        for i in range(len(bkg_hists_SR)-1) : 
            if not ("WJ" in bkg_hists_names[i] ) : datacard.write("{:20}".format('-'))
            else : datacard.write("{:20}".format(str(1.0)))
        datacard.write('\n')
        if int(args.year) == 2016 :
            datacard.write("{:20}".format("ISR_ shape"))
            for i in range(len(bkg_hists_SR)-1) : 
                if not ("SemiLepTT" in bkg_hists_names[i] or "DiLepTT" in bkg_hists_names[i] ) : datacard.write("{:20}".format('-'))
                else : datacard.write("{:20}".format(str(1.0)))
            datacard.write('\n')

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
