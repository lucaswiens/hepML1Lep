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
 - ```pip install tensorflow==1.14  tensorflow-gpu==1.14 keras==2.2.4 parameter-sherpa```

test the env by opening `python` and check if the python version is `3.6.8` and you can do : 
 - ```import ROOT```
 - ```import keras```
 - ```import tensorflow as tf```
 - ```sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))```

or you can use mine env by doing `export PATH="/nfs/dust/cms/user/amohamed/anaconda3/bin:$PATH" ; source activate hepML;` but keep in mind that you are not able to install or change anything if used but i will work fine as i already installed everything the repo need

- an example to run the training and testing is `run.py` to prepare the data-frames, do training and testing, performance plots and save the model, it can run with: 
```bash 
 # to run the a non-parametrized training you can do 
 ./run.py --indirROOT /path/to/the/rootfiles --indirCSV /path/to/write/the/csvfiles --outdir /path/to/out
```
- There are a number of arguments that can be passed to the `run.py` to control it's behavior: 
    - `--MultiC`, help='do multi-classification training',default=False
    - `--epoch`, help='scale factor alpha',default=1.0
    - `--batchSize`, help='scale factor alpha',default=512
    - `--loadmodel`, help='load a pre-trained model to continue training?'
    - `--pathToModel`, help='is model is loaded, define the path to it',default='./testing_300epc_nj3/model/1Lep_DNN_Multiclass'
    - `--append`, help='add extra text to name of every thing',default=''
    - `--do_parametric`,help='Do the training parametrically or not',default=False
    - `--nSignal_Cla`, help='number of signal classes ',default=1
    - `--multib`, help='multiple b analysis or 0b',default=False
    - `--rm` , help='if randomize the signal mass to the background or do oversampling',default=False
- Once the training is done, you can check the output directory, check the plots and the model files
- `testhyperOpt.py` is also prepared to do hyper parameter optimizations taken mainly from `https://machinelearningmastery.com/grid-search-hyperparameters-deep-learning-models-python-keras/`
- After you are done with the training, you can append the score to the trees for farther analysis by using one of the two scripts `append_DNN_1SigClass.py` and `append_DNN_0b_1SigClass.py`. Both are running interactively or via HTC by executing commands like: 
```bash 
# to interactively append the score you can
./append_DNN_1SigClass.py --infile /path/to/file --model path/to/model --outdir /path/to/out
# to run on HTC 
./append_DNN_1SigClass.py --indir path/to/indir -b --model path/to/model --outdir /path/to/out
# make sure not to add .h5 extension in the model path, it will be autocompleted by the script
```

For the full analysis work-flow, this package is made fully independent of CMSSW but you need it only for limit setting when we use HiggsCombineTools `https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/`

 - For plotting what we need is to identify cuts, plottinggroups you need with styles and the variables to plot here `hepML1Lep/plotClass/plotting/plotGroups.py`
 - You need to check all inside `plotClass` carefully 
 - `RoPlotter.py` is prepared to take over the plotting class and work on what you need to plot with the proper tdrstyle, it runs either interactively or in the batch system (HTC):
 ```bash 
 # interactively 
 ./RoPlotter.py --indir (/path/to/trees) --lumi XX --YmaX 0.0  --YmiN 0.1 --rmax 1.95 --rmin 0.05 --doRatio --year 2016 --showSF --mb --cuts plotClass/parameters_1SigCla/(cuttextfile) --varList plotClass/parameters_1SigCla/baseplots.py --scale_bkgd_toData  --outdir path/to/outdir --Smass (mgo_mlsp) --mvarList plotClass/parameters_1SigCla/Signal/mplots.py
 # the --mb argument is to speicfy that you need to call plot settings for multiple-b analysis, once you remove it it will call 0b settings
 # you need to change all arguments in between ()
 ```
 - To plot on the batch system (HTC) on can use:
 ```bash 
 # multi-b non-parametrized training without alpha/beta/gamma
./plot_onbatch.py --param plotClass/parameters_1SigCla/ --indir tree/input/dir --outdir out/dir --blind --scale --lumi XX.X --showSF
# multi-b non-parametrized training with alpha/beta/gamma
./plot_onbatch.py --param plotClass/parameters_1SigCla/ --indir tree/input/dir --outdir  out/dir --abg path/to/alphabetagamma/alphabetagammaTable.txt --blind --lumi XX.X --showSF
##############################################################
# zero-b non-parametrized training without alpha/beta/gamma
./plot_onbatch.py --param plotClass/parameters_0b_1SigCla/ --indir tree/input/dir --outdir out/dir --blind --scale --lumi XX.X --showSF
# zero-b non-parametrized training with alpha/beta/gamma
./plot_onbatch.py --param plotClass/parameters_0b_1SigCla/ --indir tree/input/dir --outdir out/dir --abg path/to/alphabetagamma/alphabetagammaTable.txt --blind --lumi XX.X --showSF
# use the option --only if you wanted plot one sample/cut only 
```
 - The `plot_onbatch.py` has quite a few arguments, check them!
 - `RoShapes.py` is prepared to make the shapes for the limit calculations, there are few versions of this script the current supported versions are: `RoShapes_1SigCla.py` and `RoShapes_0b_1SigCla.py`. both can run interactively or on the HTC via:
 ```bash 
 # to produce shapes for the background according to the SRs/CRs specified at `hepML1Lep/plotClass/search_regions.py` (-b to activate the batch submission)
 # --doSyst is used to make shape syst as well
 ./RoShapes_1SigCla.py --indir tree/input/dir --outdir out/dir --lumi XX.X -b --doSyst -Y <Year>
 # to produce shapes for the signals according to the SRs specified at `hepML1Lep/plotClass/search_regions.py` (-b to activate the batch submission)
 ./RoShapes_1SigCla.py --indir tree/input/dir --outdir out/dir --lumi XX.X -b --doSyst -Y <Yeas> --scan 
 # to produce shapes for the one signal/backgrpund according to the SRs specified at --cut argument which will be translated from `hepML1Lep/plotClass/search_regions.py` --mass the identify which mass to evaluate with (parametrized DNN)
 ./RoShapes_1SigCla.py --indir tree/input/dir --outdir out/dir --lumi XX.X --doSyst -Y <Year> -g DY -cut CR3
 # this will make shape for DY backgrounds for CR3
 #[CR2,CR3,CR4] <--> [TTsemilep DNN categroy, TTDilep DNN categroy, WJ DNN categroy]
 # you can do the same with RoShapes_0b_1SigCla.py the only difference is #[CR2,CR3] <--> [TTJets DNN categroy, WJ DNN categroy]
 ```
  - After making the shapes one needs to calculate the MC normalization factors,<img src="https://render.githubusercontent.com/render/math?math=\alpha,%20\beta,%20\gamma">, but first you need to `hadd` all the shapes then use the `AlphaBetaGamma_1sigCla.py` and `AlphaBetaGamma_0b_1sigCla.py` as:
  ```bash
  # To calculate the alpha, beta, gamma for nominal shapes
  ./AlphaBetaGamma_1sigCla.py --infile /output/file/from/hadd --outdir out/dir
  # To calculate the alpha, beta, gamma for systematic shapes
  ./AlphaBetaGamma_1sigCla.py --infile /output/file/from/hadd --outdir out/dir --syst <syst_name>
  # the syst_name can be any of Jec_Up,btagSF_b_Up,btagSF_l_Up,ISR_Up,lepSF_Up,PU_Up,TTxsec_Up,TTVxsec_Up,Wpol_Up,Wxsec_Up and also _Down variation
  ```
  - `RoLimits.py` is made to take over the shapes and produce the datacards in addition to calculating the limits. As the other running scripts we have  many versions dedicated for different analysis strategies, the supported once are `RoLimits_1SigCla.py` and `RoLimits_1SigCla_0b.py` and the run as: 
  ```bash 
  # to do the multiple-bin analysis you can use
  ./RoLimits_1SigCla.py --indir shapes/dir --outdir out/dir --sfs alphabetagamma/dir/nom/alphabetagammaTable.txt --Y <YEAR>
  # then you can merge the bins into one data card, this needs to run from CMSSW_BASE for example /nfs/dust/cms/user/amohamed/susy-desy/deepAK8/CMSSW_9_4_11/src/ and not anaconda env, make sure you login from SL6 machine and use CMSSW
  python combinedatacards_base_0.py datacard/path/datacards/
  # if you want to merge cards from the 3-years i.e for full run-II you can also use
  python combinedatacards_base_1.py datacards/pathfor2016/datacards/ datacards/pathfor2017/datacards/ datacards/pathfor2018/datacards/ out/put/datacards/
  ```
  ```bash
  #or if you are planning to run 1-bin analysis
  ./RoLimits_1SigCla.py --indir shapes/dir --outdir out/dir --sfs alphabetagamma/dir/nom/alphabetagammaTable.txt --Y <YEAR> --oneBin
  # if you want to merge cards from the 3-years i.e for full run-II you can also use 
  python combinedatacards_base_1.py datacards/pathfor2016/datacards/ datacards/pathfor2017/datacards/ datacards/pathfor2018/datacards/ out/put/datacards/
  ```
  - once the datacards are ready you can run the limit calculations on the batch system by:
  ```bash
  python limits_only.py PATH/TO/DATACARDS
  ```
  - `plotLimit.py` is made to plot the limit contour it will use the `glu_xsecs_13TeV.txt` for calculating the Xsec limits
  - `overly_DNN_Multi.C` is for comparing to limit contours from different analysis 


