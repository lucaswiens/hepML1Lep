
PU = {
    'DiLepTT' :
        {
        'scale_up' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio_up*lepSF*nISRttweight',
        'scale_dn' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio_down*lepSF*nISRttweight',
        },

    'SemiLepTT' : 
        {
        'scale_up' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio_up*lepSF*nISRttweight',
        'scale_dn' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio_down*lepSF*nISRttweight',
        },

    'SingleT' : 

        {
        'scale_up' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio_up*lepSF',
        'scale_dn' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio_down*lepSF',
        },

    'VV' : 
         {
        'scale_up' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio_up*lepSF',
        'scale_dn' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio_down*lepSF',
        },

    'TTV' : 
         {
        'scale_up' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio_up*lepSF',
        'scale_dn' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio_down*lepSF',
        },

    'QCD' : 
         {
        'scale_up' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio_up*lepSF',
        'scale_dn' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio_down*lepSF',
        },
        
    'WJ' : 
        {
        'scale_up' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio_up*lepSF',
        'scale_dn' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio_down*lepSF',
        },

    'DY' : 
         {
        'scale_up' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio_up*lepSF',
        'scale_dn' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio_down*lepSF',
        },
    'Signal_1' : 
        {
        'scale_up' : '1000.0*genWeight*susyXsec/susyNgen*btagSF*lepSF*nISRweight',
        'scale_dn' : '1000.0*genWeight*susyXsec/susyNgen*btagSF*lepSF*nISRweight',
        },
}
