import ROOT 

All_files = {
    'DiLepTT' :
        {
        'files': ['TTJets_DiLepton','TTJets_LO_HT'] , 
        'select' : '&& DiLep_Flag == 1',
        'scale' : '1000.0/sumOfWeights2*genWeight*Xsec*1*btagSF*puRatio*lepSF*nISRttweight',
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
        'scale' : '1000.0/sumOfWeights2*genWeight*Xsec*1*btagSF*puRatio*lepSF*nISRttweight',
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
        'scale' : '1000.0/sumOfWeights2*genWeight*Xsec*1*btagSF*puRatio*lepSF',
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
        'scale' : '1000.0/sumOfWeights2*genWeight*Xsec*1*btagSF*puRatio*lepSF',
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
        'scale' : '1000.0/sumOfWeights2*genWeight*Xsec*1*btagSF*puRatio*lepSF',
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
        'scale' : '1000.0/sumOfWeights2*genWeight*Xsec*1*btagSF*puRatio*lepSF',
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
        'scale' : '1000.0/sumOfWeights2*genWeight*Xsec*1*btagSF*puRatio*lepSF',
        "fill": ROOT.TAttFill(ROOT.kGreen-2, 1001),
        "line": ROOT.TAttLine(ROOT.kGreen-2, ROOT.kSolid, 1),
        "marker": None,
        "Label" : "W+jets",
        "Stackable" : True
        },

    'DY' : 
         {
        'files': ['DYJetsToLL'] , 
        'select' : '',
        'scale' : '1000.0/sumOfWeights2*genWeight*Xsec*1*btagSF*puRatio*lepSF',
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
        'select' : '&& mGo == @mGo && mLSP == @mLSP',
        'scale' : '1000.0*genWeight*susyXsec/susyNgen*btagSF*lepSF*nISRweight',
        "fill": None,
        "line": ROOT.TAttLine(ROOT.kBlack, ROOT.kSolid, 2),
        "marker":  None,
        "Label" : "T1t^{4} @mGo/@mLSP",
        "Stackable" : False
        },
        
    'Signal_2' : 
        {
        'files': ['SMS_T1tttt'] , #['SMS_T1tttt'] , 
        'select' : '&& mGo == @mGo && mLSP == @mLSP',
        'scale' : '1000.0*genWeight*susyXsec/susyNgen*btagSF*lepSF*nISRweight',
        "fill": None,
        "line": ROOT.TAttLine(ROOT.kMagenta+1, ROOT.kSolid, 2),
        "marker": None,
        "Label" : "T1t^{4} @mGo/@mLSP",
        "Stackable" : False
        },

    'Signal_3' : 
        {
        'files': ['SMS_T1tttt'] , 
        'select' : '&& mGo == @mGo && mLSP == @mLSP',
        'scale' : '1000.0*genWeight*susyXsec/susyNgen*btagSF*lepSF*nISRweight',
        "fill": None,
        "line": ROOT.TAttLine(ROOT.kBlue, ROOT.kSolid, 2),
        "marker":  None,
        "Label" : "T1t^{4} @mGo/@mLSP",
        "Stackable" : False
        },

    'Signal_4' : 
        {
        'files': ['SMS_T1tttt'] , 
        'select' : '&& mGo == @mGo && mLSP == @mLSP',
        'scale' : '1000.0*genWeight*susyXsec/susyNgen*btagSF*lepSF*nISRweight',
        "fill": None,
        "line": ROOT.TAttLine(ROOT.kGreen+1, ROOT.kDashed, 2),
        "marker":  None,
        "Label" : "T1t^{4} @mGo/@mLSP",
        "Stackable" : False
        },
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
