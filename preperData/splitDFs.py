import numpy as np
import pandas as pd
# fix random seed for reproducibility
seed = 7
np.random.seed(seed)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils import class_weight
import os
Mass_points = [[1900,100],[2200,100],[2200,800],[1900,800],[1900,1000],[1500,1000],[1500,1200],[1700,1200],[1600,1100],[1800,1300]]
signal_Cla = [[[1600,1100],[1800,1300],[1500,1000],[1500,1200],[1700,1200]],[[1900,100],[2200,100],[2200,800],[1900,800],[1900,1000]]]
to_drop = ['lheHTIncoming', 'genTau_grandmotherId', 'genTau_motherId', 'genLep_grandmotherId',
               'genLep_motherId', 'DiLep_Flag', 'semiLep_Flag', 'GenMET',  'filename']

class splitDFs(object):
    def __init__(self,signalDF, bkgDF,do_multiClass = True,nSignal_Cla = 1,do_parametric = True,ranomMass = False,split_Sign_training = False,multib = False):
        self.signalDF = signalDF
        self.bkgDF = bkgDF
        #self.do_binary_first = do_binary_first
        self.do_multiClass = do_multiClass
        self.nSignal_Cla =nSignal_Cla
        self.do_parametric = do_parametric
        self.split_Sign_training = split_Sign_training
        self.multib = multib
        self.ranomMass = ranomMass
    # function to get the index of each class of background
    def classidxs(self):
        """
        function to find idex for each  bkg class for multiclass training
        """
        if self.multib : 
            self.class_0   = self.bkgDF[self.bkgDF['filename'].str.contains('TTJets_SingleLeptonFrom')].index
            self.class_1   = self.bkgDF[self.bkgDF['filename'].str.contains('TTJets_DiLepton')].index
            #QCD_index        = self.bkgDF[self.bkgDF['filename'].str.contains('QCD')].index
            self.class_2   = self.bkgDF[~ self.bkgDF['filename'].str.contains('TTJets')].index
        else : 
            self.class_0   = self.bkgDF[~(self.bkgDF['filename'].str.contains('WJetsToLNu_'))].index#self.bkgDF[(self.bkgDF['filename'].str.contains('TTJets_SingleLeptonFrom') | self.bkgDF['filename'].str.contains('TTJets_DiLepton'))].index
            self.class_1   = self.bkgDF[self.bkgDF['filename'].str.contains('WJetsToLNu_')].index
            self.class_2   = np.array([]) #self.bkgDF[~ (self.bkgDF['filename'].str.contains('TTJets_')|self.bkgDF['filename'].str.contains('WJetsToLNu_'))].index            # #self.bkgDF[~ (self.bkgDF['filename'].str.contains('TTJets_SingleLeptonFrom')|self.bkgDF['filename'].str.contains('WJetsToLNu_'))].index            
        print (self.signalDF.groupby(['mGo','mLSP']).size())
        ## this is very usful when you need to sample specific class to match with other class (overSample Signal to backgound for example)        
    from sklearn.utils import shuffle
    def _overbalance(self,train_s,train_bkg):
        """
        Return Oversampled dataset
        """
        count_s = len(train_s.index)
        count_bkg = len(train_bkg.index)
        # Divide by class
        df_class_0 = train_bkg
        df_class_1 = train_s
        df_class_1_over = df_class_1.sample(count_bkg, replace=True)
        df_class_1_over = shuffle(df_class_1_over)
        return df_class_1_over

    ## this is very usful when you need to sample background class to preper it for the parametric training
    def _overbalance_bkg(self,signals_df_list,bkg_df):
        """
        Return Oversampled dataset for parametric training
        """
        new_bkg_train = pd.DataFrame()
        bkg_df = bkg_df.copy()
        for ns in signals_df_list : 
            bkg_df.loc[:,'mGo'] = np.random.choice(list(ns['mGo']), len(bkg_df))
            bkg_df.loc[:,'mLSP'] = np.random.choice(list(ns['mLSP']), len(bkg_df))
            new_bkg_train = pd.concat([new_bkg_train, bkg_df], ignore_index=True)
        return new_bkg_train

    def _fit_sign_mass(self,signals_df,bkg_df):
        """
        Return Oversampled dataset for parametric training
        """
        bkg_df = bkg_df.copy()
        bkg_df.loc[:,'mGo'] = np.random.choice(list(signals_df['mGo']), len(bkg_df))
        bkg_df.loc[:,'mLSP'] = np.random.choice(list(signals_df['mLSP']), len(bkg_df))
        return bkg_df
        
    def sigidxs(self):
        '''
         Function to find the indexes of each signal mass point from the big signal DF
        '''
        self.list_of_mass_idxs = []
        self.signal_list_names = [] 
        for massP in Mass_points:
            print ('mass chosen is [mGo,mLSP] == : ', massP)
            vars()['Sig_index_mGo_'+str(massP[0])+'_mLSP_'+str(massP[1])] = self.signalDF.index[(self.signalDF['mGo'] == massP[0]) & (self.signalDF['mLSP'] == massP[1])]
            self.list_of_mass_idxs.append(vars()['Sig_index_mGo_'+str(massP[0])+'_mLSP_'+str(massP[1])])
            self.signal_list_names.append('Sig_'+str(massP[0])+'_'+str(massP[1]))

    def prepare(self):
        self.classidxs()
        self.sigidxs()
        self.df_all = {}
        self.df_all['all_sig'] = pd.DataFrame()

        if self.nSignal_Cla > 1 and self.do_multiClass: 
            print('signal will be splitted into ',self.nSignal_Cla, 'classes')
            self.bkgDF.loc[self.class_0,'isSignal'] = 0 #pd.Series(np.zeros(self.bkgDF.shape[0]), index=self.bkgDF.index)
            self.bkgDF.loc[self.class_1,'isSignal'] = 1
            if self.class_2.size != 0 : self.bkgDF.loc[self.class_2,'isSignal'] = 2
            for num ,idxs in enumerate(self.list_of_mass_idxs) : 
                    self.df_all[self.signal_list_names[num]] = self.signalDF.loc[idxs ,:]
                    for j ,i in  enumerate(signal_Cla[0]) : 
                        if str(i[0]) in self.signal_list_names[num] and str(i[1]) in self.signal_list_names[num] : 
                            print (i , j ,self.signal_list_names[num])
                            if self.class_2.size != 0 : self.signalDF.loc[idxs,'isSignal'] = 3
                            else : self.signalDF.loc[idxs,'isSignal'] = 2
                    for j ,i in  enumerate(signal_Cla[1]) : 
                        if str(i[0]) in self.signal_list_names[num] and str(i[1]) in self.signal_list_names[num] : 
                            print (i , j ,self.signal_list_names[num])
                            if self.class_2.size != 0 : self.signalDF.loc[idxs,'isSignal'] = 4
                            else : self.signalDF.loc[idxs,'isSignal'] = 3
            self.df_all['all_sig'] = self.signalDF.copy()
            self.df_all['all_sig'] = self.df_all['all_sig'].dropna()
            if self.do_parametric : 
                signal_list_dfs = [] 
                for name in  self.signal_list_names : 
                    signal_list_dfs.append(self.df_all[name])
                    #print signal_list_dfs
                if not self.ranomMass : 
                    print(" you choosed parametric training and the signal mass will be oversampling the background")
                    self.df_all['all_bkg'] = self._overbalance_bkg(signal_list_dfs,self.bkgDF)
                    self.df_all['all_sig'] = self.df_all['all_sig'].sample(10*len(self.df_all['all_sig'].index), replace=True)
                else : 
                    print(" you choosed parametric training and the signal mass will be randomized to the background")
                    self.df_all['all_bkg'] = self._fit_sign_mass(self.df_all['all_sig'],self.bkgDF)
            else : self.df_all['all_bkg'] = self.bkgDF.copy()
            ## free up the memeory from all other dfs 
            bkgdf =  self.df_all['all_bkg'].copy()
            sigdf =  self.df_all['all_sig'].copy()
            del self.df_all
            self.df_all = {}
            self.df_all['all_bkg'] = bkgdf.copy()
            self.df_all['all_sig'] = sigdf.copy()
            del bkgdf
            del sigdf
    
        elif self.do_multiClass and not self.split_Sign_training : 
            print('signal will be taken as ',self.nSignal_Cla, 'class')
            self.bkgDF.loc[self.class_0,'isSignal'] = 0 #pd.Series(np.zeros(self.bkgDF.shape[0]), index=self.bkgDF.index)
            self.bkgDF.loc[self.class_1,'isSignal'] = 1
            if self.class_2.size != 0 : self.bkgDF.loc[self.class_2,'isSignal'] = 2
            
            for num ,idxs in enumerate(self.list_of_mass_idxs) :
                self.df_all[self.signal_list_names[num]] = self.signalDF.loc[idxs ,:]
                if self.class_2.size != 0 : self.df_all[self.signal_list_names[num]].loc[:,'isSignal'] = 3
                else :self.df_all[self.signal_list_names[num]].loc[:,'isSignal'] = 2
                ## for the last training over all the samples (the multiClass trainig)
                self.df_all['all_sig'] = pd.concat([self.df_all['all_sig'],self.df_all[self.signal_list_names[num]]])
                #del self.df_all[self.signal_list_names[num]]
            if self.do_parametric : 
                signal_list_dfs = [] 
                for name in  self.signal_list_names : 
                    signal_list_dfs.append(self.df_all[name])
                #print signal_list_dfs
                if not self.ranomMass : 
                    print(" you choosed parametric training and the signal mass will be oversampling the background")
                    self.df_all['all_bkg'] = self._overbalance_bkg(signal_list_dfs,self.bkgDF)
                    self.df_all['all_sig'] = self.df_all['all_sig'].sample(
                        10*len(self.df_all['all_sig'].index), replace=True)
                else : 
                    print(" you choosed parametric training and the signal mass will be randomized to the background")
                    self.df_all['all_bkg'] = self._fit_sign_mass(self.df_all['all_sig'],self.bkgDF)

            else : self.df_all['all_bkg'] = self.bkgDF.copy()
            ## free up the memeory from all other dfs 
            bkgdf =  self.df_all['all_bkg'].copy()
            sigdf =  self.df_all['all_sig'].copy()
            del self.df_all
            self.df_all = {}
            self.df_all['all_bkg'] = bkgdf.copy()
            self.df_all['all_sig'] = sigdf.copy()
            del bkgdf
            del sigdf
    
        elif self.split_Sign_training and self.do_multiClass: 
            print("you choosed to train twice, once per signal class, make sure your configuration does what you need ")
            self.bkgDF.loc[self.class_0,'isSignal'] = 0 #pd.Series(np.zeros(self.bkgDF.shape[0]), index=self.bkgDF.index)
            self.bkgDF.loc[self.class_1,'isSignal'] = 1
            if self.class_2.size != 0 : self.bkgDF.loc[self.class_2,'isSignal'] = 2
            self.df_all['sig_1'] = self.signalDF.copy()
            self.df_all['sig_2'] = self.signalDF.copy()
            for num ,idxs in enumerate(self.list_of_mass_idxs) : 
                    self.df_all[self.signal_list_names[num]] = self.signalDF.loc[idxs ,:]
                    for j ,i in  enumerate(signal_Cla[0]) : 
                        if str(i[0]) in self.signal_list_names[num] and str(i[1]) in self.signal_list_names[num] : 
                            print (i , j ,self.signal_list_names[num])
                            if self.class_2.size != 0 : self.df_all['sig_1'].loc[idxs,'isSignal'] = 3
                            else : self.df_all['sig_1'].loc[idxs,'isSignal'] = 2
                    for j ,i in  enumerate(signal_Cla[1]) : 
                        if str(i[0]) in self.signal_list_names[num] and str(i[1]) in self.signal_list_names[num] : 
                            print (i , j ,self.signal_list_names[num])
                            if self.class_2.size != 0 : self.df_all['sig_2'].loc[idxs,'isSignal'] = 3
                            else : self.df_all['sig_2'].loc[idxs,'isSignal'] = 2
            self.df_all['all_sig_1'] = self.df_all['sig_1'].copy()
            self.df_all['all_sig_2'] = self.df_all['sig_2'].copy()
            self.df_all['all_sig_1'] = self.df_all['all_sig_1'].dropna()
            self.df_all['all_sig_2'] = self.df_all['all_sig_2'].dropna()
            if self.do_parametric : 
                signal_list_dfs_1 = [] 
                signal_list_dfs_2 = [] 
                for name in  self.signal_list_names :
                    print (signal_Cla[0])
                    for scla in signal_Cla[0] :
                        if name == 'Sig_'+str(scla[0])+'_'+str(scla[1]) : 
                                signal_list_dfs_1.append(self.df_all[name])
                    print (signal_Cla[1])
                    for scla in signal_Cla[1] :
                        if name == 'Sig_'+str(scla[0])+'_'+str(scla[1]) : 
                                signal_list_dfs_2.append(self.df_all[name])
                if not self.ranomMass : 
                    print(" you choosed parametric training and the signal mass will be oversampling the background")
                    self.df_all['all_bkg_1'] = self._overbalance_bkg(signal_list_dfs_1,self.bkgDF)
                    self.df_all['all_bkg_2'] = self._overbalance_bkg(signal_list_dfs_2,self.bkgDF)
                    self.df_all['all_sig_1'] = self.df_all['all_sig_1'].sample(10*len(self.df_all['all_sig_1'].index), replace=True)
                    self.df_all['all_sig_2'] = self.df_all['all_sig_2'].sample(10*len(self.df_all['all_sig_2'].index), replace=True)
                else : 
                    print(" you choosed parametric training and the signal mass will be randomized to the background")
                    self.df_all['all_bkg_1'] = self._fit_sign_mass(signal_list_dfs_1,self.bkgDF)
                    self.df_all['all_bkg_2'] = self._fit_sign_mass(signal_list_dfs_2,self.bkgDF)

            else : self.df_all['all_bkg'] = self.bkgDF.copy()

        elif not self.do_multiClass : 
            print("binary classification mode activated, make sure your configuration does what you need ")
            #self.df_all['all_bkg'] = pd.DataFrame()
            for num ,idxs in enumerate(self.list_of_mass_idxs) : 
                self.df_all[self.signal_list_names[num]] = self.signalDF.loc[idxs ,:]
                self.df_all[self.signal_list_names[num]].loc[:,'isSignal'] = 1
                ## for the last training over all the samples (the multiClass trainig)
                self.df_all['all_sig'] = pd.concat([self.df_all['all_sig'],self.df_all[self.signal_list_names[num]]])
                #del self.df_all[self.signal_list_names[num]]
            # if doing binary classification then overwrite the bkgclass numbers by 0 and signal to 1 
            self.df_all['all_sig'] = self.df_all['all_sig'].reset_index()    
            self.bkgDF.loc[self.class_0,'isSignal'] = 0 #pd.Series(np.zeros(self.bkgDF.shape[0]), index=self.bkgDF.index)
            self.bkgDF.loc[self.class_1,'isSignal'] = 0
            if self.class_2.size != 0 : self.bkgDF.loc[self.class_2,'isSignal'] = 0
            if self.do_parametric : 
                signal_list_dfs = [] 
                for name in  self.signal_list_names : 
                    signal_list_dfs.append(self.df_all[name])
                #print signal_list_dfs
                if not self.ranomMass : 
                    print(" you choosed parametric training and the signal mass will be oversampling the background")
                    self.df_all['all_bkg'] = self._overbalance_bkg(signal_list_dfs,self.bkgDF)
                    self.df_all['all_sig'] = self.df_all['all_sig'].sample(10*len(self.df_all['all_sig'].index), replace=True)
                else :
                    print(" you choosed parametric training and the signal mass will be randomized to the background")
                    self.df_all['all_bkg'] = self._fit_sign_mass(signal_list_dfs,self.bkgDF)

            else : self.df_all['all_bkg'] = self.bkgDF.copy()
            del self.bkgDF
            ## free up the memeory from all other dfs 
            bkgdf =  self.df_all['all_bkg'].copy()
            sigdf =  self.df_all['all_sig'].copy()
            del self.df_all
            self.df_all = {}
            self.df_all['all_bkg'] = bkgdf.copy()
            self.df_all['all_sig'] = sigdf.copy()
            del bkgdf
            del sigdf

    def split(self,sigdfnew,bkgdfnew,train_size=0.6, test_size=0.4, shuffle=True, random_state=0) :
        "Function to split the DFs into testing and training supsets "
        print ('now splitting the samples with the options : ','train_size = ', train_size, 'test_size = ',test_size, 'shuffle = ',shuffle, 'random_state = ',random_state)
        _df_all = pd.concat([sigdfnew,bkgdfnew])
        del sigdfnew, bkgdfnew
        _df_all_tr = _df_all.drop(to_drop,axis=1)
        self.train_DF, self.test_DF = train_test_split(_df_all_tr, train_size=train_size, test_size=test_size, shuffle=shuffle, random_state=random_state)
        del _df_all_tr
        print('Done splitting, going to next step')
        self.train_DF = self.train_DF.reset_index(drop=True)
        self.test_DF  = self.test_DF.reset_index(drop=True)
        classes_ = np.unique(self.train_DF['isSignal'])
        print('Done reindexing, going to next step')
        #if self.multib : 
        #self.train_DF = self.train_DF.dropna()
        #self.test_DF = self.test_DF.dropna()
        self.class_weights = class_weight.compute_class_weight('balanced',
                                                                classes_,
                                                                self.train_DF['isSignal'])
        #else :
        #    self.class_weights = class_weight.compute_sample_weight('balanced',
        #                                                            self.train_DF['isSignal'])
