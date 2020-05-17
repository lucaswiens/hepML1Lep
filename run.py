#!/usr/bin/env python
from preperData.splitDFs import splitDFs
from preperData.PrepData import PrepData
from MLClass.score import score
from sklearn.preprocessing import label_binarize
from sklearn.metrics import confusion_matrix

## copied from A.Elwood https://github.com/aelwood/hepML/blob/master/MlFunctions/DnnFunctions.py
from MlFunctions.DnnFunctions import significanceLoss,significanceLossInvert,significanceLoss2Invert,significanceLossInvertSqrt,significanceFull,asimovSignificanceLoss,asimovSignificanceLossInvert,asimovSignificanceFull,truePositive,falsePositive

import os

import argparse
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Runs a NAF batch system for nanoAOD', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--indirROOT', help='List of datasets to process',default='/nfs/dust/cms/user/amohamed/susy-desy/CMGSamples/2017-18/', metavar='indirROOT')
    parser.add_argument('--indirCSV', help='List of datasets to process',default='/nfs/dust/cms/user/amohamed/susy-desy/CMGSamples/2017-18/csvs', metavar='indirCSV')
    parser.add_argument('--outdir', help='output directory',default=None,metavar='outdir')
    parser.add_argument('--MultiClass','--MultiC', help='do multiclassification training',default=False, action='store_true')
    parser.add_argument('--epoch', help='scale factor alpha',default=1.0, metavar='epoch')
    parser.add_argument('--batchSize', help='scale factor alpha',default=512, metavar='batchSize')
    parser.add_argument('--loadmodel','--loadmodel', help='load a pretrained model to continue training?',default=False, action='store_true')
    parser.add_argument('--pathToModel', help='is model is loaded, define the path to it',default='./testing_300epc_nj3/model/1Lep_DNN_Multiclass', metavar='pathToModel')
    parser.add_argument('--append', help='add extra text to name of every thing',default='',metavar='append')
    parser.add_argument('--do_parametric',help='Do the training parametrically or not',default=False,action='store_true')
    parser.add_argument('--nSignal_Cla', help='number of signal classes ',default=1 , metavar='nSignal_Cla')
    parser.add_argument('--multib','--mb', help='multiple b analysis or 0b',default=False, action='store_true')
    parser.add_argument('--rm','--ranodom', help='if randomize the signal mass to the backgorund or do oversampeling',default=False, action='store_true')


    args = parser.parse_args()

    # if you want to use a pretrained model activate it and give the model path wthout any extension
    loadmodel = args.loadmodel
    pathToModel = args.pathToModel
    append= args.append
    ##########################
    if not os.path.exists(args.indirCSV): os.makedirs(args.indirCSV)
    # multiclass or binary 
    MultiClass = args.MultiClass

    if MultiClass : 
        if args.multib : 
            class_names = ['TTSemiLep','TTDiLep','WJets','signal']#_LDM','signal_HDM']
        else :  class_names = ['TTJets','WJets','signal']
    else : 
        class_names = ['signal','background']
    ##########################
    
    if args.multib : 
        # variables to be used in the training 
        var_list = ['MET', 'MT', 'Jet2_pt','Jet1_pt', 'nLep', 'Lep_pt', 'Selected', 'nVeto', 'LT', 'HT', 'nBCleaned_TOTAL','nTop_Total_Combined', 'nJets30Clean', 'dPhi',"Lep_relIso","Lep_miniIso","iso_pt","iso_MT2","mGo", "mLSP"]
        # variables to be used in while transfere DFs
        VARS = ["MET","MT","Jet2_pt","Jet1_pt","nLep","Lep_pt","Selected","nVeto","LT","HT",
                "nBCleaned_TOTAL","nBJet","nTop_Total_Combined","nJets30Clean","dPhi","met_caloPt",
                "lheHTIncoming","genTau_grandmotherId","genTau_motherId","genLep_grandmotherId",
                "genLep_motherId","DiLep_Flag","semiLep_Flag","genWeight","sumOfWeights","btagSF",
                "puRatio","lepSF","nISRttweight","GenMET","Lep_relIso","Lep_miniIso","iso_pt","iso_MT2"]
    else :  
        # variables to be used in the training 
        var_list = ['MET', 'MT', 'Jet2_pt','Jet1_pt', 'Lep_pt', 'LT', 'HT','nTop_Total_Combined', 'nJets30Clean', 'dPhi',"Lep_relIso","Lep_miniIso","iso_pt","iso_MT2","nWLoose","nWMedium","nWTight","mGo", "mLSP"]
        # variables to be used in while transfere DFs
        VARS = ["MET","MT","Jet2_pt","Jet1_pt","nLep","Lep_pt","Selected","nVeto","LT","HT","W_fromHadTop_dRb","W_fromHadTop_dRb_2","W_fromHadTop_dRb_3","W_fromHadTop_dRb_4",
                "nBCleaned_TOTAL","nBJet","nTop_Total_Combined","nJets30Clean","dPhi","met_caloPt","nWLoose","nWMedium","nWTight","nWVeryTight",
                "lheHTIncoming","genTau_grandmotherId","genTau_motherId","genLep_grandmotherId",
                "genLep_motherId","DiLep_Flag","semiLep_Flag","genWeight","sumOfWeights","btagSF",
                "puRatio","lepSF","nISRttweight","GenMET","Lep_relIso","Lep_miniIso","iso_pt","iso_MT2"]
    ## remove the mgo and mlsp if not going to train parametrically
    if not args.do_parametric : 
        var_list = var_list[:-2]

    ##########################
    # start preparing the data if it's not in place
    Data = PrepData(args.indirROOT,args.indirCSV,VARS,skipexisting = False,multib = args.multib)
    Data.saveCSV()
    # preper the data and split them into testing sample + training sample
    splitted = splitDFs(Data.df_all['sig'],Data.df_all['bkg'],do_multiClass = MultiClass,ranomMass = args.rm,nSignal_Cla = int(args.nSignal_Cla),do_parametric = args.do_parametric,split_Sign_training = False,multib = args.multib)
    splitted.prepare()
    splitted.split(splitted.df_all['all_sig'],splitted.df_all['all_bkg'],train_size=0.8, test_size=0.2)
    ##########################
    print(splitted.test_DF.groupby(['isSignal']).size())
    print(splitted.train_DF.groupby(['isSignal']).size())
    print(splitted.train_DF.isnull().any() )
    # init the modele 
    scoreing = score('DNN',args.outdir,splitted.train_DF,splitted.test_DF,splitted.class_weights,var_list=var_list,do_multiClass = MultiClass,nSignal_Cla = int(args.nSignal_Cla),do_parametric = args.do_parametric,class_names=class_names)
    # if continue pretrained model
    if loadmodel : 
        append='_2nd'
        scoreing.load_model(pathToModel, loss='sparse_categorical_crossentropy') # mode will be save automatically
    else : 
        # nClass will be ignored in binary classification tasks anywayes
        # loss = None will use the normal cross entropy change it if you want to whatever defined in MlFunctions/DnnFunctions.py
        scoreing.do_train(nclass =len(class_names),epochs=int(args.epoch),batch_size=int(args.batchSize),loss=None)
        #scoreing.load_model()
        scoreing.save_model(scoreing.model) # here we need to enforce saving it
    ##########################
    # start the performance plottng 
    # 1- the DNN score plots
    from plotClass.pandasplot import pandasplot
    import pandas as pd
    train_s_df = pd.DataFrame(scoreing.dnn_score_train)
    test_s_df = pd.DataFrame(scoreing.dnn_score_test)
    full_test = pd.concat([scoreing.testDF,test_s_df],axis=1)
    full_train = pd.concat([scoreing.trainDF,train_s_df],axis=1)
    plott = pandasplot(os.path.join(args.outdir,'./testing_300epc_nj3/'),var_list)
    plott.classifierPlot(full_test,full_train,norm=False,logY=True,append='',multiclass=MultiClass)
    #plott.var_plot(full_test,full_train,norm=False,logY=True,append='',multiclass=MultiClass,class_names=class_names)

    # 2- the DNN loss and acc plotters 
    scoreing.performance_plot(scoreing.history,scoreing.dnn_score_test,scoreing.dnn_score_train,append=append)

    # 3- the DNN ROC plotters 
    if MultiClass : 
        scoreing.rocCurve_multi(scoreing.dnn_score_test,label_binarize(splitted.test_DF['isSignal'], classes=[x for x in range(len(class_names))]),append='MultiClass_Test'+append,n_classes=len(class_names))
        scoreing.rocCurve_multi(scoreing.dnn_score_train,label_binarize(splitted.train_DF['isSignal'], classes=[x for x in range(len(class_names))]),append='MultiClass_Train'+append,n_classes=len(class_names))
    else:
        scoreing.rocCurve(scoreing.dnn_score_test,label_binarize(splitted.test_DF['isSignal'], classes=[0,1]),append='Binary_Test')
        scoreing.rocCurve(scoreing.dnn_score_train,label_binarize(splitted.train_DF['isSignal'], classes=[0,1]),append='Binary_Train')
    
    # 4- the DNN confusion matrix plotters 
    test_cm = confusion_matrix(splitted.test_DF["isSignal"],scoreing.dnn_score_test.argmax(axis=1))
    train_cm = confusion_matrix(splitted.train_DF["isSignal"],scoreing.dnn_score_train.argmax(axis=1))
    
    scoreing.plot_confusion_matrix(test_cm, classes=class_names, normalize=True,
                          title='Normalized confusion matrix',append="test"+append)
    scoreing.plot_confusion_matrix(train_cm, classes=class_names, normalize=True,
                                   title='Normalized confusion matrix', append="train"+append)
    
    # 5- the DNN correlation matrix plotters 
    scoreing.heatMap(splitted.test_DF, append=append)
    ##########################
