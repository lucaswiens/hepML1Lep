varList.append(["1500_1000TTDi","1500_1000TTDi","DNN classifier t#bar{t} ll",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["1500_1000sig","1500_1000sig","DNN classifier T1t^{4}",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['blinded',"0.5 < x < 1.0"]])
varList.append(["1500_1000WJ","1500_1000WJ","DNN classifier W+jets",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["1500_1000TTS","1500_1000TTS","DNN classifier t#bar{t} l",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])

varList.append(["1500_1000sig_10bins","1500_1000sig","DNN classifier T1t^{4}",[10,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['blinded',"0.8 < x < 1.0"]])
varList.append(["1500_1000sig_5bins","1500_1000sig","DNN classifier T1t^{4}",[5,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['blinded',"0.8 < x < 1.0"]])
varList.append(["1500_1000sig_4bins","1500_1000sig","DNN classifier T1t^{4}",[4,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['blinded',"0.8 < x < 1.0"]])

varList.append(["CatTT1Lep","(1500_1000TTS >1500_1000TTDi ) && (1500_1000TTS >1500_1000sig) && (1500_1000TTS >1500_1000WJ)","t#bar{t} l + jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatTT2Lep","(1500_1000TTDi > 1500_1000TTS) && (1500_1000TTDi >1500_1000sig ) && (1500_1000TTDi >1500_1000WJ )","t#bar{t} ll + jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatWJ","(1500_1000WJ >1500_1000TTDi ) && (1500_1000WJ >1500_1000sig) && (1500_1000WJ  > 1500_1000TTS )","W+jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatSig","(1500_1000sig >1500_1000TTDi ) && (1500_1000sig >1500_1000TTS) && (1500_1000sig >1500_1000WJ)","T1t^{4} Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows',['blinded',"1.0 < x < 2.0"]])
