varList.append(["TTDi","TTDi[0]","DNN classifier t#bar{t} ll",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["sig","sig[0]","DNN classifier T1t^{4}",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["WJ","WJ[0]","DNN classifier W+jets",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["TTS","TTS[0]","DNN classifier t#bar{t} l",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])

varList.append(["sig_100bins","sig[0]","DNN classifier T1t^{4}",[100,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['Ymin',1.0]])
varList.append(["sig_10bins","sig[0]","DNN classifier T1t^{4}",[10,0,1],"LogY",["MoreY",1000],'IncludeOverflows'],['Ymin',1.0])
varList.append(["sig_5bins","sig[0]","DNN classifier T1t^{4}",[5,0,1],"LogY",["MoreY",1000],'IncludeOverflows'],['Ymin',1.0])
varList.append(["sig_4bins","sig[0]","DNN classifier T1t^{4}",[4,0,1],"LogY",["MoreY",1000],'IncludeOverflows'],['Ymin',1.0])

varList.append(["sig_3bins","sig[0]","DNN classifier T1t^{4}",[3,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['varbin', [0.,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.65,0.75,0.85,1.0],False],['Ymin',1.0]])
varList.append(["sig_5lastbins","sig[0]","DNN classifier T1t^{4}",[3,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['varbin',[0.,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.65,0.75,0.85,0.9,0.92,0.94,0.96,0.98,1.0],False],['Ymin',1.0]])
varList.append(["sig_2lastbins","sig[0]","DNN classifier T1t^{4}",[3,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['varbin',[0.,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.65,0.75,0.85,0.9,0.95,1.0],False],['Ymin',1.0]])
varList.append(["sig_2lastbins2","sig[0]","DNN classifier T1t^{4}",[3,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['varbin',[0.,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.93,1.0],False],['Ymin',1.0]])

varList.append(["CatTT1Lep","(TTS[0] >TTDi[0] ) && (TTS[0] >sig[0]) && (TTS[0] >WJ[0])","t#bar{t} l + jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatTT2Lep","(TTDi[0] > TTS[0]) && (TTDi[0] >sig[0] ) && (TTDi[0] >WJ[0] )","t#bar{t} ll + jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatWJ","(WJ[0] >TTDi[0] ) && (WJ[0] >sig[0]) && (WJ[0]  > TTS[0] )","W+jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatSig","(sig[0] >TTDi[0] ) && (sig[0] >TTS[0]) && (sig[0] >WJ[0])","T1t^{4} Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
