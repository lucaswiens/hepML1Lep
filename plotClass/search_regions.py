#!/usr/bin/env python
from plotClass.plotting.plotGroups import All_files,varList
# this is for limit setting
categories = ['sig','TTS','TTDi','WJ']
massList = ["1900_100","1600_1100","1900_800","1500_1200","1800_1300","2200_800","1700_1200","2200_100","1500_1000","1900_1000"]
selected_var = []
for mass in massList : 
    small_list = []
    for cat in categories : 
        small_list.append(mass+cat)
    selected_var.append(small_list)


cut_strings = ""
cut_strings +='(nLep == 1 && Lep_pt > 25)'
cut_strings +='&& (Selected == 1)'
cut_strings +='&& (nVeto == 0 )'
cut_strings +='&& (!isData || (HLT_EleOR || HLT_MuOR || HLT_MetOR))'
cut_strings +='&& (!isData || ( (PD_SingleEle && HLT_EleOR) || (PD_SingleMu && (HLT_MuOR) && !(HLT_EleOR) ) || (PD_MET && (HLT_MetOR) && !(HLT_EleOR) && !(HLT_MuOR) )  ))'
#cut_strings +='&& (!isData || fabs(dPhi) < 0.75 )'
cut_strings +='&& (!isData || METfilters == 1)'
cut_strings +='&& (!iso_Veto)'
cut_strings +='&& (MET/met_caloPt <= 5)'
cut_strings +='&& (RA2_muJetFilter == 1)'
cut_strings +='&& (Flag_fastSimCorridorJetCleaning)'
cut_strings +='&& (nJets30Clean >= 5)'
cut_strings +='&& (Jet2_pt > 80)'
cut_strings +='&& (HT > 500)'
cut_strings +='&& (LT > 250)'
cut_strings +='&& (nBJet >= 1)'


SRs_cut_strings = {}
CRs_1_cut_strings = {}
CRs_2_cut_strings = {}
CRs_3_cut_strings = {}
CRs_4_cut_strings = {}

dPhiCut = '&& ((LT < 350 && fabs(dPhi) > 1.0) || (350 < LT && LT < 600 && fabs(dPhi) > 0.75) || (600 < LT && fabs(dPhi) > 0.5))'
AntidPhiCut = '&& ((LT < 350 && fabs(dPhi) < 1.0) || (350 < LT && LT < 600 && fabs(dPhi) < 0.75) || (600 < LT && fabs(dPhi) < 0.5))'
for i,m in enumerate(selected_var) : 
    SRs_cut_strings[massList[i]]   = cut_strings+"&&(("+m[0]+">"+m[1]+" ) && ("+m[0]+">"+m[2]+") && ("+m[0]+" >"+m[3]+"))" + dPhiCut #&& ("+m[0]+" > 0.8)"
    CRs_1_cut_strings[massList[i]] = cut_strings+"&&(("+m[0]+">"+m[1]+" ) && ("+m[0]+">"+m[2]+") && ("+m[0]+" >"+m[3]+"))" + AntidPhiCut #&& ("+m[0]+" <= 0.8)"
    CRs_2_cut_strings[massList[i]] = cut_strings+"&&(("+m[1]+">"+m[0]+" ) && ("+m[1]+">"+m[2]+") && ("+m[1]+" >"+m[3]+"))"
    CRs_3_cut_strings[massList[i]] = cut_strings+"&&(("+m[2]+">"+m[0]+" ) && ("+m[2]+">"+m[1]+") && ("+m[2]+" >"+m[3]+"))"
    CRs_4_cut_strings[massList[i]] = cut_strings+"&&(("+m[3]+">"+m[0]+" ) && ("+m[3]+">"+m[1]+") && ("+m[3]+" >"+m[2]+"))"

