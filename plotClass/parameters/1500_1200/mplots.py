varList.append(["TTDi","TTDi[1]","DNN classifier t#bar{t} ll",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["sig","sig[1]","DNN classifier T1t^{4}",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["WJ","WJ[1]","DNN classifier W+jets",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["TTS","TTS[1]","DNN classifier t#bar{t} l",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])

varList.append(["sig_100bins","sig[1]","DNN classifier T1t^{4}",[100,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["sig_10bins","sig[1]","DNN classifier T1t^{4}",[10,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["sig_5bins","sig[1]","DNN classifier T1t^{4}",[5,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["sig_4bins","sig[1]","DNN classifier T1t^{4}",[4,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])

varList.append(["sig_3bins","sig[1]","DNN classifier T1t^{4}",[3,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['varbin', [0.,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.65,0.75,0.85,1.0],True]])
varList.append(["sig_5lastbins","sig[1]","DNN classifier T1t^{4}",[3,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['varbin',[0.,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.65,0.75,0.85,0.9,0.92,0.94,0.96,0.98,1.0],True]])
varList.append(["sig_2lastbins","sig[1]","DNN classifier T1t^{4}",[3,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['varbin',[0.,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.65,0.75,0.85,0.9,0.95,1.0],True]])
varList.append(["sig_2lastbins2","sig[1]","DNN classifier T1t^{4}",[3,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['varbin',[0.,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.93,1.0],True]])

varList.append(["CatTT1Lep","(TTS[1] >TTDi[1] ) && (TTS[1] >sig[1]) && (TTS[1] >WJ[1])","t#bar{t} l + jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatTT2Lep","(TTDi[1] > TTS[1]) && (TTDi[1] >sig[1] ) && (TTDi[1] >WJ[1] )","t#bar{t} ll + jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatWJ","(WJ[1] >TTDi[1] ) && (WJ[1] >sig[1]) && (WJ[1]  > TTS[1] )","W+jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatSig","(sig[1] >TTDi[1] ) && (sig[1] >TTS[1]) && (sig[1] >WJ[1])","T1t^{4} Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
