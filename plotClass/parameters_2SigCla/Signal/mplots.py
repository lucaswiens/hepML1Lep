varList.append(["TTDiLep","TTDiLep","DNN classifier t#bar{t} ll",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["signal_LDM","signal_LDM","DNN classifier T1t^{4}",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["signal_HDM","signal_HDM","DNN classifier T1t^{4}",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["WJets","WJets","DNN classifier W+jets",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["TTSemiLep","TTSemiLep","DNN classifier t#bar{t} l",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])

varList.append(["signal_LDM_10bins","signal_LDM","DNN classifier T1t^{4}",[10,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["signal_LDM_5bins","signal_LDM","DNN classifier T1t^{4}",[5,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["signal_LDM_4bins","signal_LDM","DNN classifier T1t^{4}",[4,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])


varList.append(["signal_HDM_10bins","signal_HDM","DNN classifier T1t^{4}",[10,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["signal_HDM_5bins","signal_HDM","DNN classifier T1t^{4}",[5,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["signal_HDM_4bins","signal_HDM","DNN classifier T1t^{4}",[4,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])


varList.append(["CatTT1Lep","(TTSemiLep >TTDiLep ) && (TTSemiLep >signal_LDM)&& (TTSemiLep >signal_HDM) && (TTSemiLep >WJets)","t#bar{t} l + jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatTT2Lep","(TTDiLep > TTSemiLep) && (TTDiLep >signal_LDM )&& (TTDiLep >signal_HDM ) && (TTDiLep >WJets )","t#bar{t} ll + jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatWJ","(WJets >TTDiLep ) && (WJets >signal_LDM)&& (WJets >signal_HDM) && (WJets  > TTSemiLep )","W+jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatSigLDM","(signal_LDM >TTDiLep ) && (signal_LDM >signal_HDM) && (signal_LDM >TTSemiLep) && (signal_LDM >WJets)","T1t^{4} Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatSigHDM","(signal_HDM >TTDiLep ) && (signal_HDM >signal_LDM) && (signal_HDM >TTSemiLep) && (signal_HDM >WJets)","T1t^{4} Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
