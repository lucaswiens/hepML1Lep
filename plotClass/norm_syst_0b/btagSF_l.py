
btagSF_l = {
    'DiLepTT' :
        {
        'scale_up' : '1000.0/sumOfWeights2*genWeight*Xsec*1*btagSF_l_up*puRatio*lepSF*nISRttweight',
        'scale_dn' : '1000.0/sumOfWeights2*genWeight*Xsec*1*btagSF_l_down*puRatio*lepSF*nISRttweight',
        },

    'SemiLepTT' : 
        {
        'scale_up' : '1000.0/sumOfWeights2*genWeight*Xsec*1*btagSF_l_up*puRatio*lepSF*nISRttweight',
        'scale_dn' : '1000.0/sumOfWeights2*genWeight*Xsec*1*btagSF_l_down*puRatio*lepSF*nISRttweight',
        },

    'SingleT' : 

        {
        'scale_up' : '1000.0/sumOfWeights2*genWeight*Xsec*1*btagSF_l_up*puRatio*lepSF',
        'scale_dn' : '1000.0/sumOfWeights2*genWeight*Xsec*1*btagSF_l_down*puRatio*lepSF',
        },

    'VV' : 
         {
        'scale_up' : '1000.0/sumOfWeights2*genWeight*Xsec*1*btagSF_l_up*puRatio*lepSF',
        'scale_dn' : '1000.0/sumOfWeights2*genWeight*Xsec*1*btagSF_l_down*puRatio*lepSF',
        },

    'TTV' : 
         {
        'scale_up' : '1000.0/sumOfWeights2*genWeight*Xsec*1*btagSF_l_up*puRatio*lepSF',
        'scale_dn' : '1000.0/sumOfWeights2*genWeight*Xsec*1*btagSF_l_down*puRatio*lepSF',
        },

    'QCD' : 
         {
        'scale_up' : '1000.0/sumOfWeights2*genWeight*Xsec*1*btagSF_l_up*puRatio*lepSF',
        'scale_dn' : '1000.0/sumOfWeights2*genWeight*Xsec*1*btagSF_l_down*puRatio*lepSF',
        },
        
    'WJ' : 
        {
        'scale_up' : '1000.0/sumOfWeights2*genWeight*Xsec*1*btagSF_l_up*puRatio*lepSF',
        'scale_dn' : '1000.0/sumOfWeights2*genWeight*Xsec*1*btagSF_l_down*puRatio*lepSF',
        },

    'DY' : 
         {
        'scale_up' : '1000.0/sumOfWeights2*genWeight*Xsec*1*btagSF_l_up*puRatio*lepSF',
        'scale_dn' : '1000.0/sumOfWeights2*genWeight*Xsec*1*btagSF_l_down*puRatio*lepSF',
        },
    'Signal_1' : 
        {
        'scale_up' : '1000.0*genWeight*susyXsec/susyNgen*btagSF_l_up*lepSF',
        'scale_dn' : '1000.0*genWeight*susyXsec/susyNgen*btagSF_l_down*lepSF',
        },
}
