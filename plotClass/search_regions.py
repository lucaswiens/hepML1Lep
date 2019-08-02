#!/usr/bin/env python
from plotClass.plotting.plotGroups import All_files,cut_strings,varList
# this is for limit setting
categories = ['sig','TTS','TTDi','WJ']
massList = ["1900_100","1600_1100","1900_800","1500_1200","1800_1300","2200_800","1700_1200","2200_100","1500_1000","1900_1000"]
selected_var = []
for mass in massList : 
    small_list = []
    for cat in categories : 
        small_list.append(mass+cat)
    selected_var.append(small_list)

SRs_cut_strings = {}
CRs_1_cut_strings = {}
CRs_2_cut_strings = {}
CRs_3_cut_strings = {}
CRs_4_cut_strings = {}

for i,m in enumerate(selected_var) : 
    SRs_cut_strings[massList[i]]   = cut_strings+"&&(("+m[0]+">"+m[1]+" ) && ("+m[0]+">"+m[2]+") && ("+m[0]+" >"+m[3]+")) && ("+m[0]+" > 0.8)"
    CRs_1_cut_strings[massList[i]] = cut_strings+"&&(("+m[0]+">"+m[1]+" ) && ("+m[0]+">"+m[2]+") && ("+m[0]+" >"+m[3]+")) && ("+m[0]+" <= 0.8)"
    CRs_2_cut_strings[massList[i]] = cut_strings+"&&(("+m[1]+">"+m[0]+" ) && ("+m[1]+">"+m[2]+") && ("+m[1]+" >"+m[3]+"))"
    CRs_3_cut_strings[massList[i]] = cut_strings+"&&(("+m[2]+">"+m[0]+" ) && ("+m[2]+">"+m[1]+") && ("+m[2]+" >"+m[3]+"))"
    CRs_4_cut_strings[massList[i]] = cut_strings+"&&(("+m[3]+">"+m[0]+" ) && ("+m[3]+">"+m[1]+") && ("+m[0]+" >"+m[2]+"))"

