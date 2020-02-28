#!/usr/bin/env python
import sys,os
import ROOT


branchlist_0b = ['1900_100TTJ_0b','1900_1000TTJ_0b','1900_800TTJ_0b','2200_100TTJ_0b','2200_800TTJ_0b','1500_1000TTJ_0b','1500_1200TTJ_0b',
              '1600_1100TTJ_0b','1700_1200TTJ_0b','1800_1300TTJ_0b','1900_100WJ_0b','1900_1000WJ_0b','1900_800WJ_0b','2200_100WJ_0b',
              '2200_800WJ_0b','1500_1000WJ_0b','1500_1200WJ_0b','1600_1100WJ_0b','1700_1200WJ_0b','1800_1300WJ_0b','1900_100sig_0b',
              '1900_1000sig_0b','1900_800sig_0b','2200_100sig_0b','2200_800sig_0b','1500_1000sig_0b','1500_1200sig_0b','1600_1100sig_0b',
              '1700_1200sig_0b','1800_1300sig_0b']
              
branchlist_nb = ['1900_100TTS','1900_1000TTS','1900_800TTS','2200_100TTS','2200_800TTS','1500_1000TTS',
              '1500_1200TTS','1600_1100TTS','1700_1200TTS','1800_1300TTS','1900_100TTDi','1900_1000TTDi','1900_800TTDi','2200_100TTDi',
              '2200_800TTDi','1500_1000TTDi','1500_1200TTDi','1600_1100TTDi','1700_1200TTDi','1800_1300TTDi','1900_100WJ','1900_1000WJ',
              '1900_800WJ','2200_100WJ','2200_800WJ','1500_1000WJ','1500_1200WJ','1600_1100WJ','1700_1200WJ','1800_1300WJ','1900_100sig',
              '1900_1000sig','1900_800sig','2200_100sig','2200_800sig','1500_1000sig','1500_1200sig',
              '1600_1100sig','1700_1200sig','1800_1300sig']

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
