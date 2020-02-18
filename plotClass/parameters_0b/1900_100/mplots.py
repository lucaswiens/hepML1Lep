varList.append(["1900_100sig_0b","1900_100sig_0b","DNN classifier T5q^{4}",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["1900_100WJ_0b","1900_100WJ_0b","DNN classifier W+jets",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["1900_100TTJ_0b","1900_100TTJ_0b","DNN classifier t#bar{t} + jets",[20,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])

varList.append(["1900_100sig_0b_10bins","1900_100sig_0b","DNN classifier T5q^{4}",[100,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["1900_100sig_0b_5bins","1900_100sig_0b","DNN classifier T5q^{4}",[5,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["1900_100sig_0b_4bins","1900_100sig_0b","DNN classifier T5q^{4}",[4,0,1],"LogY",["MoreY",1000],'IncludeOverflows'])

varList.append(["1900_100sig_0b_3lastbins","1900_100sig_0b","DNN classifier T5q^{4}",[3,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['varbin',[0.,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.65,0.75,0.85,1.0],True]])
varList.append(["1900_100sig_0b_5lastbins","1900_100sig_0b","DNN classifier T5q^{4}",[3,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['varbin',[0.,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.65,0.75,0.85,0.9,0.92,0.94,0.96,0.98,1.0],True]])
varList.append(["1900_100sig_0b_2lastbins","1900_100sig_0b","DNN classifier T5q^{4}",[3,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['varbin',[0.,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.65,0.75,0.85,0.9,0.95,1.0],True]])
varList.append(["1900_100sig_0b_2lastbins2","1900_100sig_0b","DNN classifier T5q^{4}",[3,0,1],"LogY",["MoreY",1000],'IncludeOverflows',['varbin',[0.,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.93,1.0],True]])

varList.append(["CatTTJ_0b","(1900_100TTJ_0b >1900_100TTDi ) && (1900_100TTJ_0b >1900_100sig_0b) && (1900_100TTJ_0b >1900_100WJ_0b)","t#bar{t} + jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["CatWJ_0b","(1900_100WJ_0b >1900_100TTDi ) && (1900_100WJ_0b >1900_100sig_0b) && (1900_100WJ_0b  > 1900_100TTJ_0b )","W+jets Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
varList.append(["Catsig_0b","(1900_100sig_0b >1900_100TTDi ) && (1900_100sig_0b >1900_100TTJ_0b) && (1900_100sig_0b >1900_100WJ_0b)","T5q^{4} Event Category",[2,0.0,2.0],"LogY",["MoreY",1000],'IncludeOverflows'])
