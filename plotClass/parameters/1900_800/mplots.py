varList.append(["1900_800TTDi","1900_800TTDi","DNN classifier t#bar{t} ll",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["1900_800sig","1900_800sig","DNN classifier T1t^{4}",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["1900_800WJ","1900_800WJ","DNN classifier W+jets",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["1900_800TTS","1900_800TTS","DNN classifier t#bar{t} l",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])

varList.append(["1900_800sig_10bins","1900_800sig","DNN classifier T1t^{4}",[10,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["1900_800sig_5bins","1900_800sig","DNN classifier T1t^{4}",[5,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["1900_800sig_4bins","1900_800sig","DNN classifier T1t^{4}",[4,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["1900_800sig_3bins","1900_800sig","DNN classifier T1t^{4}",[3,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['varbin',[0,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.9,1.0],True]])

varList.append(["CatTT1Lep","(1900_800TTS >1900_800TTDi ) && (1900_800TTS >1900_800sig) && (1900_800TTS >1900_800WJ)","t#bar{t} l + jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatTT2Lep","(1900_800TTDi > 1900_800TTS) && (1900_800TTDi >1900_800sig ) && (1900_800TTDi >1900_800WJ )","t#bar{t} ll + jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatWJ","(1900_800WJ >1900_800TTDi ) && (1900_800WJ >1900_800sig) && (1900_800WJ  > 1900_800TTS )","W+jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatSig","(1900_800sig >1900_800TTDi ) && (1900_800sig >1900_800TTS) && (1900_800sig >1900_800WJ)","T1t^{4} Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
