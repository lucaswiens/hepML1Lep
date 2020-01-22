#!/usr/bin/env python

import ROOT
import time
import array
import operator
import uproot
import os
os.environ["KERAS_BACKEND"] = "tensorflow"
import keras
from keras.models import model_from_json
import pandas as pd
import argparse


def load_model(pathToModel):
    '''Load a previously saved model (in h5 format)'''
    #print (" Loading the model from ",pathToModel)
    # load json and create model
    json_file = open(pathToModel+'.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load weights into new model
    model.load_weights(pathToModel+'.h5')
    return model


def Predict_Keras(infile,var_list,class_list, mgo = 0.0,mlsp = 0.0,model = None) : 

    model = load_model(model)
    model.compile(loss='sparse_categorical_crossentropy',metrics=['accuracy'],optimizer='adam')


    outbranch = [str(int(mgo))+"_"+str(int(mlsp))+x for x in class_list]
    
    it = uproot.open(infile)["sf/t"]
    file_out = ROOT.TFile.Open(infile, "UPDATE")
    tree_out = file_out.Get("sf/t")
    TT1l_val = array.array('f', [0.])
    TT2l_val = array.array('f', [0.])
    WJet_val = array.array('f', [0.])
    Sign_val = array.array('f', [0.])

    if ((not "T1tttt" in infile)  and (not 'T5qqqq' in infile)) : 
        p_df = it.pandas.df(var_list)
        p_df.loc[:,'mGo'] = mgo
        p_df.loc[:,'mLSP'] = mlsp
    else :
        #masslist = [[1900,100],[2200,100],[2200,800],[1900,800],[1900,1000],[1500,1000],[1500,1200],[1700,1200],[1600,1100],[1800,1300]]
        #TT1l_dict = {} ; TT2l_dict = {} ; WJet_dict = {} ; Sign_dict = {}
        var_list.append('mGo')
        var_list.append('mLSP')
        p_df = it.pandas.df(var_list)
        #for mass in masslist : 
            #mgo = str(mass[0]); mlsp = str(mass[1])
        TT1l_1900_100  = tree_out.Branch('1900_100TTS', TT1l_val, '1900_100TTS/F')
        TT1l_1900_1000 = tree_out.Branch('1900_1000TTS', TT1l_val, '1900_1000TTS/F')
        TT1l_1900_800  = tree_out.Branch('1900_800TTS', TT1l_val, '1900_800TTS/F')
        TT1l_2200_100  = tree_out.Branch('2200_100TTS', TT1l_val, '2200_100TTS/F')
        TT1l_2200_800  = tree_out.Branch('2200_800TTS', TT1l_val, '2200_800TTS/F')
        TT1l_1500_1000 = tree_out.Branch('1500_1000TTS', TT1l_val, '1500_1000TTS/F')
        TT1l_1500_1200 = tree_out.Branch('1500_1200TTS', TT1l_val, '1500_1200TTS/F')
        TT1l_1600_1100 = tree_out.Branch('1600_1100TTS', TT1l_val, '1600_1100TTS/F')
        TT1l_1700_1200 = tree_out.Branch('1700_1200TTS', TT1l_val, '1700_1200TTS/F')
        TT1l_1800_1300 = tree_out.Branch('1800_1300TTS', TT1l_val, '1800_1300TTS/F')

        TT2l_1900_100  = tree_out.Branch('1900_100TTDi', TT2l_val, '1900_100TTDi/F')
        TT2l_1900_1000 = tree_out.Branch('1900_1000TTDi', TT2l_val, '1900_1000TTDi/F')
        TT2l_1900_800  = tree_out.Branch('1900_800TTDi', TT2l_val, '1900_800TTDi/F')
        TT2l_2200_100  = tree_out.Branch('2200_100TTDi', TT2l_val, '2200_100TTDi/F')
        TT2l_2200_800  = tree_out.Branch('2200_800TTDi', TT2l_val, '2200_800TTDi/F')
        TT2l_1500_1000 = tree_out.Branch('1500_1000TTDi', TT2l_val, '1500_1000TTDi/F')
        TT2l_1500_1200 = tree_out.Branch('1500_1200TTDi', TT2l_val, '1500_1200TTDi/F')
        TT2l_1600_1100 = tree_out.Branch('1600_1100TTDi', TT2l_val, '1600_1100TTDi/F')
        TT2l_1700_1200 = tree_out.Branch('1700_1200TTDi', TT2l_val, '1700_1200TTDi/F')
        TT2l_1800_1300 = tree_out.Branch('1800_1300TTDi', TT2l_val, '1800_1300TTDi/F')

        WJet_1900_100  = tree_out.Branch('1900_100WJ', WJet_val, '1900_100WJ/F')
        WJet_1900_1000 = tree_out.Branch('1900_1000WJ', WJet_val, '1900_1000WJ/F')
        WJet_1900_800  = tree_out.Branch('1900_800WJ', WJet_val, '1900_800WJ/F')
        WJet_2200_100  = tree_out.Branch('2200_100WJ', WJet_val, '2200_100WJ/F')
        WJet_2200_800  = tree_out.Branch('2200_800WJ', WJet_val, '2200_800WJ/F')
        WJet_1500_1000 = tree_out.Branch('1500_1000WJ', WJet_val, '1500_1000WJ/F')
        WJet_1500_1200 = tree_out.Branch('1500_1200WJ', WJet_val, '1500_1200WJ/F')
        WJet_1600_1100 = tree_out.Branch('1600_1100WJ', WJet_val, '1600_1100WJ/F')
        WJet_1700_1200 = tree_out.Branch('1700_1200WJ', WJet_val, '1700_1200WJ/F')
        WJet_1800_1300 = tree_out.Branch('1800_1300WJ', WJet_val, '1800_1300WJ/F')

        Sign_1900_100  = tree_out.Branch('1900_100sig', Sign_val, '1900_100sig/F')
        Sign_1900_1000 = tree_out.Branch('1900_1000sig', Sign_val, '1900_1000sig/F')
        Sign_1900_800  = tree_out.Branch('1900_800sig', Sign_val, '1900_800sig/F')
        Sign_2200_100  = tree_out.Branch('2200_100sig', Sign_val, '2200_100sig/F')
        Sign_2200_800  = tree_out.Branch('2200_800sig', Sign_val, '2200_800sig/F')
        Sign_1500_1000 = tree_out.Branch('1500_1000sig', Sign_val, '1500_1000sig/F')
        Sign_1500_1200 = tree_out.Branch('1500_1200sig', Sign_val, '1500_1200sig/F')
        Sign_1600_1100 = tree_out.Branch('1600_1100sig', Sign_val, '1600_1100sig/F')
        Sign_1700_1200 = tree_out.Branch('1700_1200sig', Sign_val, '1700_1200sig/F')
        Sign_1800_1300 = tree_out.Branch('1800_1300sig', Sign_val, '1800_1300sig/F')

    prediction = model.predict_proba(p_df.values)

    #print(prediction)

    TT1l_name = outbranch[0]
    newbranch_TT1l = tree_out.Branch(TT1l_name, TT1l_val, TT1l_name+'/F')
    TT2l_name = outbranch[1]
    newbranch_TT2l = tree_out.Branch(TT2l_name, TT2l_val, TT2l_name+'/F')
    WJet_name = outbranch[2]
    newbranch_WJet =tree_out.Branch(WJet_name, WJet_val, WJet_name+'/F')
    Sign_name = outbranch[3]
    newbranch_Sign = tree_out.Branch(Sign_name, Sign_val, Sign_name+'/F')

    t_start = time.time()

    #print prediction.size
    
    for i_ev in range(tree_out.GetEntries()):
        #print i_ev
        if i_ev % 10000 == 0:
            print ('Event', i_ev)
            t_current = time.time()
            print ('Time', t_current- t_start)
            t_start = t_current

        TT1l_val[0] = prediction[i_ev][0]
        TT2l_val[0] = prediction[i_ev][1]
        WJet_val[0] = prediction[i_ev][2]
        Sign_val[0] = prediction[i_ev][3]

        newbranch_TT1l.Fill()
        newbranch_TT2l.Fill()
        newbranch_WJet.Fill()
        newbranch_Sign.Fill()

        if (("T1tttt" in infile)  or ('T5qqqq' in infile)) : 
            TT1l_1900_100.Fill()
            TT1l_1900_1000.Fill()
            TT1l_1900_800.Fill()
            TT1l_2200_100.Fill()
            TT1l_2200_800.Fill()
            TT1l_1500_1000.Fill()
            TT1l_1500_1200.Fill()
            TT1l_1600_1100.Fill()
            TT1l_1700_1200.Fill()
            TT1l_1800_1300.Fill()
            TT2l_1900_100.Fill()
            TT2l_1900_1000.Fill()
            TT2l_1900_800.Fill()
            TT2l_2200_100.Fill()
            TT2l_2200_800.Fill()
            TT2l_1500_1000.Fill()
            TT2l_1500_1200.Fill()
            TT2l_1600_1100.Fill()
            TT2l_1700_1200.Fill()
            TT2l_1800_1300.Fill()
            WJet_1900_100.Fill()
            WJet_1900_1000.Fill()
            WJet_1900_800.Fill()
            WJet_2200_100.Fill()
            WJet_2200_800.Fill()
            WJet_1500_1000.Fill()
            WJet_1500_1200.Fill()
            WJet_1600_1100.Fill()
            WJet_1700_1200.Fill()
            WJet_1800_1300.Fill()
            Sign_1900_100 .Fill()
            Sign_1900_1000.Fill()
            Sign_1900_800.Fill()
            Sign_2200_100.Fill()
            Sign_2200_800.Fill()
            Sign_1500_1000.Fill()
            Sign_1500_1200.Fill()
            Sign_1600_1100.Fill()
            Sign_1700_1200.Fill()
            Sign_1800_1300.Fill()


    file_out.cd('sf')
    #file_out.Delete("t;1")
    #file_out.Delete("sf/t;1")
    tree_out.Write("t", ROOT.TObject.kOverwrite)
    file_out.Close()

        
def find_all_matching(substring, path):
    result = []
    for root, dirs, files in os.walk(path):
        for thisfile in files:
            if substring in thisfile:
                result.append(os.path.join(root, thisfile ))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evaluate DNN with scikit-learn')
    parser.add_argument('--indir', help='List of datasets to process',default=None, metavar='indir')
    parser.add_argument('--infile', help='infile to process',default=None, metavar='infile')
    parser.add_argument('--exec', help="wight directory", default='./batch/append_exec.sh', metavar='exec')
    parser.add_argument('--batchMode','-b', help='Batch mode.',default=False, action='store_true')
    parser.add_argument('--model', help='model to be used',default=None, metavar='model')


    args = parser.parse_args()

    masslist = [[1900,100],[2200,100],[2200,800],[1900,800],[1900,1000],[1500,1000],[1500,1200],[1700,1200],[1600,1100],[1800,1300]]

    var_list = ['MET', 'MT', 'Jet2_pt','Jet1_pt', 'nLep', 'Lep_pt', 'Selected', 'nVeto', 'LT', 'HT', 'nBCleaned_TOTAL','nTop_Total_Combined', 'nJets30Clean', 'dPhi',"Lep_relIso","Lep_miniIso","iso_pt","iso_MT2"]#,"mGo", "mLSP"]
    
    wdir = os.getcwd()


    if not args.batchMode and args.infile: 
        fout = args.infile
        if ( "T1tttt" in fout or 'T5qqqq' in fout) :
            Predict_Keras(fout,var_list,['TTS','TTDi', 'WJ', 'sig'], mgo = 0.0,mlsp = 0.0,model = args.model)
        else : 
            for mass in masslist : 
                mgo = mass[0] ; mlsp = mass[1]
                Predict_Keras(fout,var_list,['TTS','TTDi', 'WJ', 'sig'], mgo = mgo,mlsp = mlsp,model = args.model)
    else : 
        
        logdir = args.indir+'/Logs' 
        if not os.path.exists(logdir):
            os.makedirs(logdir) 
        import htcondor    
        schedd = htcondor.Schedd()  

        Filenamelist = find_all_matching(".root",args.indir) 
        print (Filenamelist)
        for fc in Filenamelist : 
            ##Condor configuration
            submit_parameters = { 
                "executable"                : args.exec,
                "arguments"                 : " ".join([fc,wdir,args.model]),
                "universe"                  : "vanilla",
                "should_transfer_files"     : "YES",
                "log"                       : "{}/job_$(Cluster)_$(Process).log".format(logdir),
                "output"                    : "{}/job_$(Cluster)_$(Process).out".format(logdir),
                "error"                     : "{}/job_$(Cluster)_$(Process).err".format(logdir),
                "when_to_transfer_output"   : "ON_EXIT",
                'Requirements'              : 'OpSysAndVer == "CentOS7"',

             }
            job = htcondor.Submit(submit_parameters)
            with schedd.transaction() as txn:
                    job.queue(txn)
                    print ("Submit job for file {}".format(fc))

