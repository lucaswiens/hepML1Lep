
lepSF = {
    'DiLepTT' :
        {
        'scale_up' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio*(lepSF+lepSFerr)*nISRttweight',
        'scale_dn' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio*(lepSF-lepSFerr)*nISRttweight',
        },

    'SemiLepTT' : 
        {
        'scale_up' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio*(lepSF+lepSFerr)*nISRttweight',
        'scale_dn' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio*(lepSF-lepSFerr)*nISRttweight',
        },

    'SingleT' : 

        {
        'scale_up' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio*(lepSF+lepSFerr)',
        'scale_dn' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio*(lepSF-lepSFerr)',
        },

    'VV' : 
         {
        'scale_up' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio*(lepSF+lepSFerr)',
        'scale_dn' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio*(lepSF-lepSFerr)',
        },

    'TTV' : 
         {
        'scale_up' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio*(lepSF+lepSFerr)',
        'scale_dn' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio*(lepSF-lepSFerr)',
        },

    'QCD' : 
         {
        'scale_up' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio*(lepSF+lepSFerr)',
        'scale_dn' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio*(lepSF-lepSFerr)',
        },
        
    'WJ' : 
        {
        'scale_up' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio*(lepSF+lepSFerr)',
        'scale_dn' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio*(lepSF-lepSFerr)',
        },

    'DY' : 
         {
        'scale_up' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio*(lepSF+lepSFerr)',
        'scale_dn' : '1000.0/sumOfWeights*genWeight*Xsec*1*btagSF*puRatio*(lepSF-lepSFerr)',
        },
    'Signal_1' : 
        {
        'scale_up' : '1000.0*genWeight*susyXsec/susyNgen*btagSF*(lepSF+lepSFerr)',
        'scale_dn' : '1000.0*genWeight*susyXsec/susyNgen*btagSF*(lepSF-lepSFerr)',
        },
}
