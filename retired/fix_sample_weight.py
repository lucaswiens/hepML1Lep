#!/usr/bin/env python
import ROOT
import array
import sys 
import os
indir = sys.argv[-1]
jects = ["2016_FR_","2016_FR_JEC_up_","2016_FR_JEC_down_"]

filelist = [] 
flist = ["evVarFriend_TTJets_LO_HT600to800_ext.root",
            "evVarFriend_TTJets_LO_HT800to1200_ext.root",
            "evVarFriend_TTJets_LO_HT1200to2500_ext.root",
            "evVarFriend_TTJets_LO_HT2500toInf_ext.root",
            "evVarFriend_TTJets_SingleLeptonFromT_ext.root"]

for dir_ in jects : 
    if os.path.exists(os.path.join(indir,dir_)): 
        for f in flist : 
            filelist.append(os.path.join(indir,os.path.join(dir_,f)))

for f in filelist : 
    print(f)
    file_in = ROOT.TFile(f,"READ")
    tree_in = file_in.Get("sf/t")
    file_out = ROOT.TFile(f.replace(".root","_fixed.root"), "RECREATE")
    file_out.mkdir('sf')
    file_out.cd('sf')
    val = array.array('f', [0.])
    if "TTJets_SingleLeptonFromT_ext" in f : tree_in.SetBranchStatus("sumOfWeights2",0)
    tree_out = tree_in.CopyTree("")
    bran  = tree_out.Branch('sumOfWeights2', val, 'sumOfWeights2/F')
    for i_ev in range(tree_out.GetEntries()):
        tree_out.GetEntry(i_ev)
        if "TTJets_SingleLeptonFromT_ext" in f : val[0] = 61.198124 * (10**6)
        else : val[0] = tree_out.sumOfWeights
        bran.Fill()
    tree_out.Write("t", ROOT.TObject.kOverwrite)
    file_out.Close()