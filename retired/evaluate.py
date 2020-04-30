#!/usr/bin/env python

from MLClass.eval import eval
import argparse
ClassList = ['TTSemiLep','TTDiLep','WJets','signal']
#Run:Lumi:Event
var_list = ['MET', 'MT', 'Jet2_pt','Jet1_pt', 'nLep', 'Lep_pt', 'Selected', 'nVeto', 'LT', 'HT', 'nBCleaned_TOTAL','nTop_Total_Combined', 'nJets30Clean', 'dPhi',"Lep_relIso","Lep_miniIso","iso_pt","iso_MT2","mGo", "mLSP"]
MultiClass = True
preselect = "nLep == 1 && nJets30Clean >= 3"
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runs a NAF batch system for nanoAOD', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--infile', help='inputFile', metavar='infile')
    parser.add_argument('--outdir', help='output directory',default=None, metavar='outdir')
    parser.add_argument('--model', help='name of the model with out extensions',default=None, metavar='model')
    parser.add_argument('--mGo', help=' gluino mass ',default=0.0, metavar='mGo')
    parser.add_argument('--mLSP', help='LSP mass',default=0.0, metavar='mLSP')
    parser.add_argument('--do_parametric', help=' set it to true if you want to evaluate paramtric training for each mass point',default=False, action='store_true')


    args = parser.parse_args()
    filename = args.infile
    outdir = args.outdir
    model = args.model
    mGo = args.mGo
    mLSP = args.mLSP

    ev = eval(filename,outdir,model,var_list,do_parametric = args.do_parametric,do_multiClass = MultiClass,mGo = mGo , mLSP = mLSP,preselect = preselect,ClassList = ClassList)

    if '.root' in filename : 
        if not args.do_parametric : savepredicOnly = False
        else : savepredicOnly = True
        ev.ev_score_toROOT(savepredicOnly=savepredicOnly)

    elif '.csv' in filename : 
        if not args.do_parametric : savepredicOnly = False
        else : savepredicOnly = True
        ev.ev_score_toDF(savepredicOnly=savepredicOnly)
    
