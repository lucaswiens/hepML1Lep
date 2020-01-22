varList.append(["1500_1200TTDi","1500_1200TTDi","DNN classifier t#bar{t} ll",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["1500_1200sig","1500_1200sig","DNN classifier T1t^{4}",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["1500_1200WJ","1500_1200WJ","DNN classifier W+jets",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["1500_1200TTS","1500_1200TTS","DNN classifier t#bar{t} l",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])

varList.append(["1500_1200sig_10bins","1500_1200sig","DNN classifier T1t^{4}",[10,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["1500_1200sig_5bins","1500_1200sig","DNN classifier T1t^{4}",[5,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["1500_1200sig_4bins","1500_1200sig","DNN classifier T1t^{4}",[4,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["1500_1200sig_3bins","1500_1200sig","DNN classifier T1t^{4}",[3,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['varbin',[0,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.8,1.0],True]])

varList.append(["CatTT1Lep","(1500_1200TTS >1500_1200TTDi ) && (1500_1200TTS >1500_1200sig) && (1500_1200TTS >1500_1200WJ)","t#bar{t} l + jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatTT2Lep","(1500_1200TTDi > 1500_1200TTS) && (1500_1200TTDi >1500_1200sig ) && (1500_1200TTDi >1500_1200WJ )","t#bar{t} ll + jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatWJ","(1500_1200WJ >1500_1200TTDi ) && (1500_1200WJ >1500_1200sig) && (1500_1200WJ  > 1500_1200TTS )","W+jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatSig","(1500_1200sig >1500_1200TTDi ) && (1500_1200sig >1500_1200TTS) && (1500_1200sig >1500_1200WJ)","T1t^{4} Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
