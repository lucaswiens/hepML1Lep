varList.append(["1900_100TTDi","1900_100TTDi","DNN classifier t#bar{t} ll",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["1900_100sig","1900_100sig","DNN classifier T1t^{4}",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['blinded',"0.5 < x < 1.0"]])
varList.append(["1900_100WJ","1900_100WJ","DNN classifier W+jets",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["1900_100TTS","1900_100TTS","DNN classifier t#bar{t} l",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])

varList.append(["1900_100sig_10bins","1900_100sig","DNN classifier T1t^{4}",[10,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['blinded',"0.8 < x < 1.0"]])
varList.append(["1900_100sig_5bins","1900_100sig","DNN classifier T1t^{4}",[5,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['blinded',"0.8 < x < 1.0"]])
varList.append(["1900_100sig_4bins","1900_100sig","DNN classifier T1t^{4}",[4,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['blinded',"0.8 < x < 1.0"]])

varList.append(["CatTT1Lep","(1900_100TTS >1900_100TTDi ) && (1900_100TTS >1900_100sig) && (1900_100TTS >1900_100WJ)","t#bar{t} l + jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatTT2Lep","(1900_100TTDi > 1900_100TTS) && (1900_100TTDi >1900_100sig ) && (1900_100TTDi >1900_100WJ )","t#bar{t} ll + jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatWJ","(1900_100WJ >1900_100TTDi ) && (1900_100WJ >1900_100sig) && (1900_100WJ  > 1900_100TTS )","W+jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatSig","(1900_100sig >1900_100TTDi ) && (1900_100sig >1900_100TTS) && (1900_100sig >1900_100WJ)","T1t^{4} Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows',['blinded',"1.0 < x < 2.0"]])
