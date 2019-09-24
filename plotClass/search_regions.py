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
cut_strings +='&& (nJets30Clean >= 3)'
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
ntopCut = '&& nTop_Total_Combined >= 1 '
AntintopCut = '&& nTop_Total_Combined < 1'

for i,m in enumerate(selected_var) : 
    SRs_cut_strings[massList[i]]   = cut_strings+"&&(("+m[0]+">"+m[1]+" ) && ("+m[0]+">"+m[2]+") && ("+m[0]+" >"+m[3]+"))" #+ dPhiCut + ntopCut #&& ("+m[0]+" > 0.8)"
    CRs_1_cut_strings[massList[i]] = cut_strings+"&&(("+m[0]+">"+m[1]+" ) && ("+m[0]+">"+m[2]+") && ("+m[0]+" >"+m[3]+"))" + AntidPhiCut #&& ("+m[0]+" <= 0.8)"
    CRs_2_cut_strings[massList[i]] = cut_strings+"&&(("+m[1]+">"+m[0]+" ) && ("+m[1]+">"+m[2]+") && ("+m[1]+" >"+m[3]+"))"
    CRs_3_cut_strings[massList[i]] = cut_strings+"&&(("+m[2]+">"+m[0]+" ) && ("+m[2]+">"+m[1]+") && ("+m[2]+" >"+m[3]+"))"
    CRs_4_cut_strings[massList[i]] = cut_strings+"&&(("+m[3]+">"+m[0]+" ) && ("+m[3]+">"+m[1]+") && ("+m[3]+" >"+m[2]+"))"

import ROOT 

All_files = {
    'DiLepTT' :
        {
        'files': ['TTJets_DiLepton','TTJets_LO_HT'] , 
        'select' : '&& DiLep_Flag == 1',
        'scale' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio*lepSF*nISRttweight',
        "fill": ROOT.TAttFill(ROOT.kRed, 1001),
        "line": ROOT.TAttLine(ROOT.kRed, ROOT.kSolid, 1),
        "marker": None,
        "Label" : "t#bar{t} ll + jets",
        "Stackable" : True
        },

    'SemiLepTT' : 
        {
        'files': ['TTJets_SingleLeptonFrom','TTJets_LO_HT'] , 
        'select' : '&& semiLep_Flag == 1',
        'scale' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio*lepSF*nISRttweight',
        "fill": ROOT.TAttFill(ROOT.kBlue-7, 1001),
        "line": ROOT.TAttLine(ROOT.kBlue-7, ROOT.kSolid, 1),
        "marker": None,
        "Label" : "t#bar{t} l + jets",
        "Stackable" : True
        },

    'SingleT' : 

        {
        'files': ["TBar_tWch","TBar_tch_powheg","T_tWch","T_tWch_ext","T_tch_powheg"] , #"TToLeptons_sch","TBar_tWch_noFullyHad_ext","T_tWch_noFullyHad_ext",
        'select' : '',
        'scale' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio*lepSF',
        "fill": ROOT.TAttFill(ROOT.kViolet+5, 1001),
        "line": ROOT.TAttLine(ROOT.kViolet+5, ROOT.kSolid, 1),
        "marker": None,
        "Label" : "t/#bar{t}",
        "Stackable" : True
        },

    'VV' : 
         {
        'files': ["VVTo","WWTo","WZTo","ZZTo"] , 
        'select' :'',
        'scale' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio*lepSF',
        "fill": ROOT.TAttFill(ROOT.kRed+3, 1001),
        "line": ROOT.TAttLine(ROOT.kRed+3, ROOT.kSolid, 1),
        "marker": None,
        "Label" : "VV(W/Z/H)",
        "Stackable" : True
        },

    'TTV' : 
         {
        'files': ['TTW','TTZ'] , 
        'select' : '',
        'scale' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio*lepSF',
        "fill": ROOT.TAttFill(ROOT.kOrange-3, 1001),
        "line": ROOT.TAttLine(ROOT.kOrange-3, ROOT.kSolid, 1),
        "marker": None,
        "Label" : "ttV(W/Z/H)",
        "Stackable" : True
        },

    'QCD' : 
         {
        'files': ['QCD_'] , 
        'select' :'',
        'scale' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio*lepSF',
        "fill": ROOT.TAttFill(ROOT.kCyan-6, 1001),
        "line": ROOT.TAttLine(ROOT.kCyan-6, ROOT.kSolid, 1),
        "marker": None,
        "Label" : "QCD",
        "Stackable" : True
        },
        
       
    'WJ' : 
        {
        'files': ['WJetsToLNu_HT'] , 
        'select' : '',
        'scale' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio*lepSF',
        "fill": ROOT.TAttFill(ROOT.kGreen-2, 1001),
        "line": ROOT.TAttLine(ROOT.kGreen-2, ROOT.kSolid, 1),
        "marker": None,
        "Label" : "W+jets",
        "Stackable" : True
        },

    'DY' : 
         {
        'files': ['DYJetsToLL_M50_HT'] , 
        'select' : '',
        'scale' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio*lepSF',
        "fill": ROOT.TAttFill(ROOT.kRed-6, 1001),
        "line": ROOT.TAttLine(ROOT.kRed-6, ROOT.kSolid, 1),
        "marker": None,
        "Label" :"DY+jets",
        "Stackable" : True
        },

    'Data' :
        {
        'files': ['SingleElectron','SingleMuon','MET_Run'] , 
        'select' : '',
        'scale' : '1',
        "fill": None,
        "line": None,
        "marker":  ROOT.TAttMarker(ROOT.kBlack, ROOT.kFullCircle, 0.7),
        "Label" : "Data",
        "Stackable" : False
        },

    'Signal_1' : 
        {
        'files': ['SMS_T1tttt'] , 
        'select' : '&& mGo == 1900 && mLSP == 100',
        'scale' : '1000.0*genWeight*susyXsec/susyNgen*btagSF*lepSF*nISRweight',
        "fill": None,
        "line": ROOT.TAttLine(ROOT.kRed+1, ROOT.kSolid, 2),
        "marker":  None,
        "Label" : "T1t^{4} 1.9/0.1",
        "Stackable" : False
        },

}
