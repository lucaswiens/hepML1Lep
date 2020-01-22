varList.append(["1800_1300TTDi","1800_1300TTDi","DNN classifier t#bar{t} ll",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["1800_1300sig","1800_1300sig","DNN classifier T1t^{4}",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["1800_1300WJ","1800_1300WJ","DNN classifier W+jets",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["1800_1300TTS","1800_1300TTS","DNN classifier t#bar{t} l",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])

varList.append(["1800_1300sig_10bins","1800_1300sig","DNN classifier T1t^{4}",[10,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["1800_1300sig_5bins","1800_1300sig","DNN classifier T1t^{4}",[5,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["1800_1300sig_4bins","1800_1300sig","DNN classifier T1t^{4}",[4,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["1800_1300sig_3bins","1800_1300sig","DNN classifier T1t^{4}",[3,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['varbin',[0,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.8,1.0],True]])


varList.append(["CatTT1Lep","(1800_1300TTS >1800_1300TTDi ) && (1800_1300TTS >1800_1300sig) && (1800_1300TTS >1800_1300WJ)","t#bar{t} l + jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatTT2Lep","(1800_1300TTDi > 1800_1300TTS) && (1800_1300TTDi >1800_1300sig ) && (1800_1300TTDi >1800_1300WJ )","t#bar{t} ll + jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatWJ","(1800_1300WJ >1800_1300TTDi ) && (1800_1300WJ >1800_1300sig) && (1800_1300WJ  > 1800_1300TTS )","W+jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatSig","(1800_1300sig >1800_1300TTDi ) && (1800_1300sig >1800_1300TTS) && (1800_1300sig >1800_1300WJ)","T1t^{4} Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
