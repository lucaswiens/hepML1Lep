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

    'Others' : 

        {
        'files': ["TBar_tWch","TBar_tch_powheg","T_tWch","T_tWch_ext","T_tch_powheg","VVTo","WWTo","WZTo","ZZTo",'TTW','TTZ',"QCD_","WJetsToLNu_HT","DYJetsToLL"],
        'select' : '',
        'scale' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio*lepSF',
        "fill": ROOT.TAttFill(ROOT.kOrange-3, 1001),
        "line": ROOT.TAttLine(ROOT.kOrange-3, ROOT.kSolid, 1),
        "marker": None,
        "Label" : "Others",
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
        }
}

dPhiCut = '&& ((LT < 350 && fabs(dPhi) > 1.0) || (350 < LT && LT < 600 && fabs(dPhi) > 0.75) || (600 < LT && fabs(dPhi) > 0.5))'
AntidPhiCut = '&& ((LT < 350 && fabs(dPhi) < 1.0) || (350 < LT && LT < 600 && fabs(dPhi) < 0.75) || (600 < LT && fabs(dPhi) < 0.5))'
ntopCut = '&& nTop_Total_Combined >= 2 '
AntintopCut = '&& nTop_Total_Combined < 1'

oldbins = {"LT12HT01": "(LT < 450) && (HT < 1000) "                             , 
           "LT12HT23": "(LT < 450) && (HT > 1000) && (HT < 1500)"               , 
           "LT12HT4i": "(LT < 450) && (HT > 1500) "                             , 
           "LT3HT01" : "(LT > 450) && (LT < 600) && (HT < 1000)"                , 
           "LT3HT23" : "(LT > 450) && (LT < 600) && (HT > 1000) && (HT < 1500)" , 
           "LT3HT4i" : "(LT > 450) && (LT < 600) && (HT > 1500)"                , 
           "LT4HT01" : "(LT > 600) && (LT < 750) && (HT < 1000)"                , 
           "LT4HT23" : "(LT > 600) && (LT < 750) && (HT > 1000) && (HT < 1500)" , 
           "LT4HT4i" : "(LT > 600) && (LT < 750) && (HT > 1500)"                , 
           "LT5iHT0i": "(LT > 750)"                                             }
