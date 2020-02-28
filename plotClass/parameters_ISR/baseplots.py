varList.append(["ISR_HT", "HT", "ISR H_{T} [GeV]", [30, 0, 800], "LogY", ["MoreY", 500],['YmiN',10], ['varbin', [0,50,100,150,200,300,400,600,800],False],"IncludeOverflows"])
varList.append(["ISR_N", "nJets30Clean", "ISR jet multiplicity", [7, 0, 7] , "LogY",["MoreY",500],'IncludeOverflows'])
varList.append(["ISR_pT", "Jet_pt", "ISR p_{T} [GeV]", [30, 0, 800], "LogY",["MoreY",500],['YmiN',10],['varbin', [0,50,100,150,200,300,400,600,800],False],"IncludeOverflows"])

varList.append(["ISR_HT_", "HT", "ISR H_{T} [GeV]", [30, 0, 800], "LogY", ["MoreY", 500],['YmiN',10],"IncludeOverflows"])
varList.append(["ISR_N_", "nJets30Clean", "ISR jet multiplicity", [7, 0, 7],['YmiN',10], "LogY",["MoreY",500],'IncludeOverflows'])
varList.append(["ISR_pT_", "Jet_pt", "ISR p_{T} [GeV]", [30, 0, 800], "LogY",['YmiN',10],["MoreY",500],"IncludeOverflows"])

varList.append(["ISR_pT_1", "Jet_pt_arr[0]", "ISR.1 p_{T} [GeV]", [30, 0, 800],['YmiN',10],"LogY",["MoreY",500], ['varbin', [0,50,100,150,200,300,400,600,800],False],['AddCut','nJets30Clean >=1'],"IncludeOverflows"])
varList.append(["ISR_pT_2", "Jet_pt_arr[1]", "ISR.2 p_{T} [GeV]", [30, 0, 800],['YmiN',10],"LogY",["MoreY",500], ['varbin', [0,50,100,150,200,300,400,600,800],False],['AddCut','nJets30Clean >=2'],"IncludeOverflows"])
varList.append(["ISR_pT_3", "Jet_pt_arr[2]", "ISR.3 p_{T} [GeV]", [30, 0, 800],['YmiN',10],"LogY",["MoreY",500], ['varbin', [0,50,100,150,200,300,400,600,800],False],['AddCut','nJets30Clean >=3'],"IncludeOverflows"])
varList.append(["ISR_pT_4", "Jet_pt_arr[3]", "ISR.4 p_{T} [GeV]", [30, 0, 800],['YmiN',10],"LogY",["MoreY",500], ['varbin', [0,50,100,150,200,300,400,600,800],False],['AddCut','nJets30Clean >=4'],"IncludeOverflows"])