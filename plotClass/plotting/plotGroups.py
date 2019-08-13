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
        "Label" : "t#bar{t}",
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

    'Signal_2' : 
        {
        'files': ['SMS_T1tttt'] , 
        'select' : '&& mGo == 1900 && mLSP == 1000',
        'scale' : '1000.0*genWeight*susyXsec/susyNgen*btagSF*lepSF*nISRweight',
        "fill": None,
        "line": ROOT.TAttLine(ROOT.kMagenta+1, ROOT.kSolid, 2),
        "marker": None,
        "Label" : "T1t^{4} 1.9/1.0",
        "Stackable" : False
        },

    'Signal_3' : 
        {
        'files': ['SMS_T1tttt'] , 
        'select' : '&& mGo == 1900 && mLSP == 800',
        'scale' : '1000.0*genWeight*susyXsec/susyNgen*btagSF*lepSF*nISRweight',
        "fill": None,
        "line": ROOT.TAttLine(ROOT.kBlack, ROOT.kSolid, 2),
        "marker":  None,
        "Label" : "T1t^{4} 1.9/0.8",
        "Stackable" : False
        },

    'Signal_4' : 
        {
        'files': ['SMS_T1tttt'] , 
        'select' : '&& mGo == 1500 && mLSP == 1000',
        'scale' : '1000.0*genWeight*susyXsec/susyNgen*btagSF*lepSF*nISRweight',
        "fill": None,
        "line": ROOT.TAttLine(ROOT.kMagenta+1, ROOT.kDashed, 2),
        "marker":  None,
        "Label" : "T1t^{4} 1.50/1.0",
        "Stackable" : False
        },
}

dPhiCut = '&& ((LT < 350 && fabs(dPhi) > 1.0) || (350 < LT && LT < 600 && fabs(dPhi) > 0.75) || (600 < LT && fabs(dPhi) > 0.5))'
AntidPhiCut = '&& ((LT < 350 && fabs(dPhi) < 1.0) || (350 < LT && LT < 600 && fabs(dPhi) < 0.75) || (600 < LT && fabs(dPhi) < 0.5))'
ntopCut = '&& nTop_Total_Combined >= 1 '
AntintopCut = '&& nTop_Total_Combined < 1'

CatTT1Lep = '&& (1900_100TTS >1900_100TTDi ) && (1900_100TTS >1900_100sig) && (1900_100TTS >1900_100WJ)'
CatTT2Lep = '&& (1900_100TTDi > 1900_100TTS) && (1900_100TTDi >1900_100sig ) && (1900_100TTDi >1900_100WJ )'
CatWJ     = '&& (1900_100WJ >1900_100TTDi ) && (1900_100WJ >1900_100sig) && (1900_100WJ  > 1900_100TTS )'
CatSig   = '&& (1900_100sig >1900_100TTDi ) && (1900_100sig >1900_100TTS) && (1900_100sig >1900_100WJ)'
# cut to produce control plots 
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
#cut_strings += CatSig + dPhiCut + ntopCut

# for Dilep CR 
'''cut_strings += '(!isData || (HLT_EleOR || HLT_MuOR || HLT_MetOR))'
cut_strings += '&& (!isData || ( (PD_SingleEle && HLT_EleOR) || (PD_SingleMu && (HLT_MuOR) && !(HLT_EleOR) ) || (PD_MET && (HLT_MetOR) && !(HLT_EleOR) && !(HLT_MuOR) )  ))'
cut_strings += '&& (!isData || METfilters == 1)'
cut_strings += '&& ( nLep == 2 && Selected == 1 && nVeto == 0)'
cut_strings += '&& ( DLMS_nJets30Clean_0 >=3)'
cut_strings += '&& (Jet2_pt > 80 ) '
cut_strings += '&& (DLMS_HT_0>500)'
cut_strings += '&& ( DLMS_ST_0>250 )'
cut_strings += '&& (nBJet == 0)'
cut_strings += CatSig'''

# variables to plot
varList = [] #[ name of tree branch, name of pdf file, name of variable, number of bins, min bin, max bin]
varList.append(["HT", "HT", "H_{T} [GeV]", [30, 0, 3000], "LogY",["MoreY",1000]])
varList.append(["LT", "LT", "L_{T} [GeV]", [15, 0, 1500] , "LogY",["MoreY",1000]])
varList.append(["MET", "MET", "MET [GeV]", [15, 0, 1500] , "LogY",["MoreY",1000]])
varList.append(["Lep_pt", "Lep_pt", "Lep p_{T} [GeV]", [32, 0, 800], "LogY",["MoreY",1000]])
varList.append(["nJets30Clean", "nJets30Clean", "jet multiplicity", [10, 0, 15] , "LogY",["MoreY",1000]])
#varList.append(["BDT","BDT","BDT Response" , 60,-0.5,1 , "Logy"]) 
varList.append(["dPhi", "fabs(dPhi)", "#Delta #varphi (lep,W)" ,[30, 0, 3.142],"LogY",["MoreY",1000]])
varList.append(["nBJet","nBJet","b-jet multiplicity (Med)",[8, 0, 8], "LogY",["MoreY",1000]])

varList.append(["1900_100TTDi","1900_100TTDi","DNN classifier t#bar{t} ll",[20,0,1],"LogY",["MoreY",1000]])
varList.append(["1900_100sig","1900_100sig","DNN classifier T1t^{4}",[20,0,1],"LogY",["MoreY",1000]]) #,['blinded',"0.8 < x < 1.0"]])

varList.append(["1900_100WJ","1900_100WJ","DNN classifier W+jets",[20,0,1],"LogY",["MoreY",1000]])
varList.append(["1900_100TTS","1900_100TTS","DNN classifier t#bar{t} l",[20,0,1],"LogY",["MoreY",1000]])

varList.append(["CatTT1Lep","(1900_100TTS >1900_100TTDi ) && (1900_100TTS >1900_100sig) && (1900_100TTS >1900_100WJ)","t#bar{t} l + jets Event Category",[2,0,1.1],"LogY",["MoreY",1000]])
varList.append(["CatTT2Lep","(1900_100TTDi > 1900_100TTS) && (1900_100TTDi >1900_100sig ) && (1900_100TTDi >1900_100WJ )","t#bar{t} ll + jets Event Category",[2,0,1.1],"LogY",["MoreY",1000]])
varList.append(["CatWJ","(1900_100WJ >1900_100TTDi ) && (1900_100WJ >1900_100sig) && (1900_100WJ  > 1900_100TTS )","W+jets Event Category",[2,0,1.1],"LogY",["MoreY",1000]])
varList.append(["CatSig","(1900_100sig >1900_100TTDi ) && (1900_100sig >1900_100TTS) && (1900_100sig >1900_100WJ)","T1t^{4} Event Category",[2,0,1.1],"LogY",["MoreY",1000]])

