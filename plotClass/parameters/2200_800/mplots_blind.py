varList.append(["2200_800TTDi","2200_800TTDi","DNN classifier t#bar{t} ll",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["2200_800sig","2200_800sig","DNN classifier T1t^{4}",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['blinded',"0.5 < x < 1.0"]])
varList.append(["2200_800WJ","2200_800WJ","DNN classifier W+jets",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["2200_800TTS","2200_800TTS","DNN classifier t#bar{t} l",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])

varList.append(["2200_800sig_10bins","2200_800sig","DNN classifier T1t^{4}",[10,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['blinded',"0.8 < x < 1.0"]])
varList.append(["2200_800sig_5bins","2200_800sig","DNN classifier T1t^{4}",[5,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['blinded',"0.8 < x < 1.0"]])
varList.append(["2200_800sig_4bins","2200_800sig","DNN classifier T1t^{4}",[4,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['blinded',"0.8 < x < 1.0"]])

varList.append(["CatTT1Lep","(2200_800TTS >2200_800TTDi ) && (2200_800TTS >2200_800sig) && (2200_800TTS >2200_800WJ)","t#bar{t} l + jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatTT2Lep","(2200_800TTDi > 2200_800TTS) && (2200_800TTDi >2200_800sig ) && (2200_800TTDi >2200_800WJ )","t#bar{t} ll + jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatWJ","(2200_800WJ >2200_800TTDi ) && (2200_800WJ >2200_800sig) && (2200_800WJ  > 2200_800TTS )","W+jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatSig","(2200_800sig >2200_800TTDi ) && (2200_800sig >2200_800TTS) && (2200_800sig >2200_800WJ)","T1t^{4} Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows',['blinded',"1.0 < x < 2.0"]])
