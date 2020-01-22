

./RoPlotter.py --indir /nfs/dust/cms/user/amohamed/susy-desy/ML/hepML_1Lep/16_score_Xmas \
    --lumi 35.9 \
    --outdir plots2016_Xmas_2SigCla \
    --scale_bkgd_toData \
    --doRatio \
    --YmaX 0.0 \
    --YmiN 0.1 \
    --rmax 1.95 \
    --rmin 0.05 \
    --blind \
    --cuts plotClass/parameters_2SigCla/inclusive.txt \
    --mcuts plotClass/parameters_2SigCla/Signal/Sig_HDMnj6.txt \
    --varList plotClass/parameters_2SigCla/baseplots.py \
    --mvarList plotClass/parameters_2SigCla/Signal/mplots.py \
    --mGo1 1500 --mLSP1 1000 \
    --mGo2 1900 --mLSP2 100 
