#!/usr/bin/env python
import sys,os
import ROOT


branchlist_0b = ['TTJ_0b','WJ_0b','sig_0b']
              
branchlist_nb = ['TTS','TTDi','WJ','sig']

branchlist_all = branchlist_0b + branchlist_nb

def find_all_matching(substring, path):
    result = []
    for root, dirs, files in os.walk(path):
        for thisfile in files:
            if thisfile.startswith("."): continue 
            if substring in thisfile:
                result.append(os.path.join(root, thisfile ))
    return result

path1 = sys.argv[-1]

Filenamelist = find_all_matching(".root",path1) 
#print(Filenamelist)
for fc in Filenamelist : 
    print(fc)
    f = ROOT.TFile.Open(fc)
    tree = f.Get("sf/t")
    if not tree : 
        print("File is corrupted")
        continue
    if "T1tttt" in fc : branchlist = branchlist_nb
    elif "T5qqqq" in fc : branchlist = branchlist_0b
    else : branchlist = branchlist_all

    for br in branchlist : 
        br_ = tree.GetListOfBranches().FindObject(br)
        if not br_ : 
            print("branch names", br, "is not existing in  ",fc)
