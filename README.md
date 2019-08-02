# hepML1Lep
The package is to train and evaluate (binary or multiclass) neural network and/or xgb BDT,... within the context of susy single lepton analysis
The workflow will be 
 - prepare the training set of root trees into pandas dataframe (dfs) and split them into training/testing df
 - train and neural network with a specific/multiple signal model with/without doing parametric training i.e. give the physical identity of the model as a parameter in the training step, for this we use oversampling method to assign the parameter to the background
 - during the training and testing, we do some performance plots 
 - we use independent datasets for evaluation and farther analysis steps, to avoid any potential bias 

this package will take root files and append a DNN score and the very end to the root files

the setup is based on Anaconda 2019.03 for Linux Installer (https://www.anaconda.com/distribution/) for python3 

on DESY NAF El7 WGS one can install it by using 
 - ```bash /nfs/dust/cms/user/amohamed/Anaconda3-2019.03-Linux-x86_64.sh```
 - ```export PATH="path/to/anaconda3/bin:$PATH```
 - I keep everything as default but the installation dir i change it to a place where I have enough space
 - ```conda create -n hepML -c conda-forge root=6.16 root_numpy  pandas seaborn scikit-learn matplotlib root_pandas uproot python=3.6.8```
 - ```conda activate hepML``` or ```source activate hepML``` based on conda version
 - if you got any error related to "libstdc" and "libcrypto" when opening root I do : 
     - ```ln -s  path/to/anaconda3/envs/hepML/lib/libstdc++.so.6.0.26 path/to/anaconda3/envs/hepML/lib/libstdc++.so```
     - ```ln -s  path/to/anaconda3/envs/hepML/lib/libstdc++.so.6.0.26 path/to/anaconda3/envs/hepML/lib/libstdc++.so.6```
     - same for 'libcrypto'
 - if you have GPU and you want to use, you need to install tensorflow, tensorflow-gpu and keras but from `pip` as conda tensorflow is not doing the correct setup for `GPU`
 - ```pip install tensorflow tensorflow-gpu keras parameter-sherpa```

test the env by opening `python` and check if the python version is `3.6.8` and you can do : 
 - ```import ROOT```
 - ```import keras```
 - ```import tensorflow as tf```
 - ```sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))```

or you can use mine env by doing `export PATH="/nfs/dust/cms/user/amohamed/anaconda3/bin:$PATH" ; source activate hepML;` but keep in mind that you are not able to install or change anything if used but i will work fine as i already installed everything the repo need

- an example to run the training and testing is `run.py` to prepare the dataframes, do training and testing, performance plots and save the model
- `evaluate.py` is prepared to evaluate the model on any of the independent samples we use for farther analysis
- `evaluate_onbatch.py` will wrap `evaluate.py` to run an independent batch system job for each sample, it will produce either `.root` or `.csv` based on the input file extension and it can also save the score only or save the entire sample based on what you need. Finally, it can run with parametric evaluation i.e. evaluate an indepenedet score for each signal hypothis  
- `testhyperOpt.py` is also prepared to do hyper parameter optimizations taken mainly from `https://machinelearningmastery.com/grid-search-hyperparameters-deep-learning-models-python-keras/`


For the full analysis work-flow, this package is made fully independent of CMSSW but you need it only for limit setting when we use HiggsCombineTools `https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/`

 - for plotting what we need is to indentify cuts, plottinggroups you need with styles and the variables to plot here `hepML1Lep/plotClass/plotting/plotGroups.py`
 - `RoPlotter.py` is prepared to take over the plotting class and work on what you need to plot with the proper tdrstyle 
 - the first few lines are made to contol how the `plotter` should work `https://github.com/ashrafkasem/hepML1Lep/blob/master/RoPlotter.py#L28-L48`
 - `RoShapes.py` is prepared to make the shapes for the limits (still simplifed version i.e without the prpoer systematics) `development are upcoming`
 ```bash 
 # to produce shapes for the background according to the SRs/CRs specified at `hepML1Lep/plotClass/search_regions.py` (-b to activate the batch submission)
 ./RoShapes.py --indir root_FRs_w_score/ --outdir shapes --lumi 35.9 -b
 # to produce shapes for the signals according to the SRs specified at `hepML1Lep/plotClass/search_regions.py` (-b to activate the batch submission)
 ./RoShapes.py --indir root_FRs_w_score/ --outdir shapes --lumi 35.9 -b --scan
 # to produce shapes for the one signal/backgrpund according to the SRs specified at --cut argument which will be translated from `hepML1Lep/plotClass/search_regions.py` --mass the identify which mass to evaluate with (parametrized DNN)
 ./RoShapes.py --indir root_FRs_w_score/ --outdir shapes --lumi 35.9 --scan -cut 'SR' --mass 1700_800
 ```

  - `RoLimits.py` is made to take over the shapes and produce the datacards in addition to calculating the limits still working on getting all the systematics into the game
  - `/nfs/dust/cms/user/amohamed/susy-desy/deepAK8/CMSSW_9_4_11/src/` will be used by default as I've already prepared the combine tool but feel free to change it to whatever you have
  ```bash
  # -L is to calculate the limit on HTC otherwise only the datacards will be produced
  ./RoLimits.py --indir shapes_16_DNN_31_July19v2 --outdir testLimits -L
  ```
  - `plotLimit.py` is made to plot the limit contour it will use the `glu_xsecs_13TeV.txt` for calculating the Xsec limits
  - `overly_DNN_Multi.C` is for comparing to limit contours 


