./RoPlotter.py --indir /nfs/dust/cms/user/amohamed/susy-desy/CMGSamples/UL_FRs_Dec19/2018_FR_ \
    --lumi 59.74 \
    --outdir plots2018_FS/1700_1200 \
    --scale_bkgd_toData \
    #--do_alphabetagamma \
    --doRatio \
    --YmaX 0.0 \
    --YmiN 0.1 \
    --rmax 1.95 \
    --rmin 0.05 \
    --alpha 0.83 \
    --beta 1.03 \
    --gamma 0.73 \
    --cuts plotClass/parameters/inclusive.txt \
    --varList plotClass/parameters/baseplots.py \
    --mvarList plotClass/parameters/1700_1200/mplots_blind.py \
    --mGo1 1700 --mLSP1 1200 \
    -j 5
    
#./RoPlotter.py --indir /nfs/dust/cms/user/amohamed/susy-desy/CMGSamples/UL_FRs_Dec19/2018_FR_ \
#    --lumi 59.74 \
#    --outdir plots2018_FS/1700_1200 \
#    --scale_bkgd_toData \
#    #--do_alphabetagamma \
#    --doRatio \
#    --YmaX 0.0 \
#    --YmiN 0.1 \
#    --rmax 1.95 \
#    --rmin 0.05 \
#    --alpha 0.83 \
#    --beta 1.03 \
#    --gamma 0.73 \
#    --cuts plotClass/parameters/inclusive.txt \
#    --mcuts plotClass/parameters/1700_1200/SB_1.txt \
#    --varList plotClass/parameters/baseplots.py \
#    --mvarList plotClass/parameters/1700_1200/mplots.py \
#    --mGo1 1700 --mLSP1 1200 \
    -j 5
#
#./RoPlotter.py --indir /nfs/dust/cms/user/amohamed/susy-desy/CMGSamples/UL_FRs_Dec19/2018_FR_ \
#    --lumi 59.74 \
#    --outdir plots2018_FS/1700_1200 \
#    --scale_bkgd_toData \
#    #--do_alphabetagamma \
#    --doRatio \
#    --YmaX 0.0 \
#    --YmiN 0.1 \
#    --rmax 1.95 \
#    --rmin 0.05 \
#    --alpha 0.83 \
#    --beta 1.03 \
#    --gamma 0.73 \
#    --cuts plotClass/parameters/inclusive.txt \
#    --mcuts plotClass/parameters/1700_1200/SB_2.txt \
#    --varList plotClass/parameters/baseplots.py \
#    --mvarList plotClass/parameters/1700_1200/mplots.py \
#    --mGo1 1700 --mLSP1 1200 \
    -j 5
#
#./RoPlotter.py --indir /nfs/dust/cms/user/amohamed/susy-desy/CMGSamples/UL_FRs_Dec19/2018_FR_ \
#    --lumi 59.74 \
#    --outdir plots2018_FS/1700_1200 \
#    --scale_bkgd_toData \
#    #--do_alphabetagamma \
#    --doRatio \
#    --YmaX 0.0 \
#    --YmiN 0.1 \
#    --rmax 1.95 \
#    --rmin 0.05 \
#    --alpha 0.83 \
#    --beta 1.03 \
#    --gamma 0.73 \
#    --cuts plotClass/parameters/inclusive.txt \
#    --mcuts plotClass/parameters/1700_1200/SB_3.txt \
#    --varList plotClass/parameters/baseplots.py \
#    --mvarList plotClass/parameters/1700_1200/mplots.py \
#    --mGo1 1700 --mLSP1 1200 \
    -j 5

./RoPlotter.py --indir /nfs/dust/cms/user/amohamed/susy-desy/CMGSamples/UL_FRs_Dec19/2018_FR_ \
    --lumi 59.74 \
    --outdir plots2018_FS/1700_1200 \
    --scale_bkgd_toData \
    #--do_alphabetagamma \
    --doRatio \
    --YmaX 0.0 \
    --YmiN 0.1 \
    --rmax 1.95 \
    --rmin 0.05 \
    --alpha 0.83 \
    --beta 1.03 \
    --gamma 0.73 \
    --blind \
    --cuts plotClass/parameters/inclusive.txt \
    --mcuts plotClass/parameters/1700_1200/Sig.txt \
    --varList plotClass/parameters/baseplots.py \
    --mvarList plotClass/parameters/1700_1200/mplots.py \
    --mGo1 1700 --mLSP1 1200 \
    -j 5
    
./RoPlotter.py --indir /nfs/dust/cms/user/amohamed/susy-desy/CMGSamples/UL_FRs_Dec19/2018_FR_ \
    --lumi 59.74 \
    --outdir plots2018_FS/1700_1200 \
    --scale_bkgd_toData \
    #--do_alphabetagamma \
    --doRatio \
    --YmaX 0.0 \
    --YmiN 0.1 \
    --rmax 1.95 \
    --rmin 0.05 \
    --alpha 0.83 \
    --beta 1.03 \
    --gamma 0.73 \
    --cuts plotClass/parameters/inclusive.txt \
    --mcuts plotClass/parameters/1700_1200/AntiSig.txt \
    --varList plotClass/parameters/baseplots.py \
    --mvarList plotClass/parameters/1700_1200/mplots.py \
    --mGo1 1700 --mLSP1 1200 \
    -j 5

./RoPlotter.py --indir /nfs/dust/cms/user/amohamed/susy-desy/CMGSamples/UL_FRs_Dec19/2018_FR_ \
    --lumi 59.74 \
    --outdir plots2018_FS/1700_1200 \
    --scale_bkgd_toData \
    #--do_alphabetagamma \
    --doRatio \
    --YmaX 0.0 \
    --YmiN 0.1 \
    --rmax 1.95 \
    --rmin 0.05 \
    --alpha 0.83 \
    --beta 1.03 \
    --gamma 0.73 \
    --cuts plotClass/parameters/inclusive.txt \
    --mcuts plotClass/parameters/1700_1200/Sig_Antilastbin.txt \
    --varList plotClass/parameters/baseplots.py \
    --mvarList plotClass/parameters/1700_1200/mplots.py \
    --mGo1 1700 --mLSP1 1200 \
    -j 5

./RoPlotter.py --indir /nfs/dust/cms/user/amohamed/susy-desy/CMGSamples/UL_FRs_Dec19/2018_FR_ \
    --lumi 59.74 \
    --outdir plots2018_FS/1700_1200 \
    --scale_bkgd_toData \
    #--do_alphabetagamma \
    --doRatio \
    --YmaX 0.0 \
    --YmiN 0.1 \
    --rmax 1.95 \
    --rmin 0.05 \
    --alpha 0.83 \
    --beta 1.03 \
    --gamma 0.73 \
    --cuts plotClass/parameters/inclusive.txt \
    --mcuts plotClass/parameters/1700_1200/TTL.txt \
    --varList plotClass/parameters/baseplots.py \
    --mvarList plotClass/parameters/1700_1200/mplots.py \
    --mGo1 1700 --mLSP1 1200 \
    -j 5
   
./RoPlotter.py --indir /nfs/dust/cms/user/amohamed/susy-desy/CMGSamples/UL_FRs_Dec19/2018_FR_ \
    --lumi 59.74 \
    --outdir plots2018_FS/1700_1200 \
    --scale_bkgd_toData \
    #--do_alphabetagamma \
    --doRatio \
    --YmaX 0.0 \
    --YmiN 0.1 \
    --rmax 1.95 \
    --rmin 0.05 \
    --alpha 0.83 \
    --beta 1.03 \
    --gamma 0.73 \
    --cuts plotClass/parameters/inclusive.txt \
    --mcuts plotClass/parameters/1700_1200/TTLL.txt \
    --varList plotClass/parameters/baseplots.py \
    --mvarList plotClass/parameters/1700_1200/mplots.py \
    --mGo1 1700 --mLSP1 1200 \
    -j 5

./RoPlotter.py --indir /nfs/dust/cms/user/amohamed/susy-desy/CMGSamples/UL_FRs_Dec19/2018_FR_ \
    --lumi 59.74 \
    --outdir plots2018_FS/1700_1200 \
    --scale_bkgd_toData \
    #--do_alphabetagamma \
    --doRatio \
    --YmaX 0.0 \
    --YmiN 0.1 \
    --rmax 1.95 \
    --rmin 0.05 \
    --alpha 0.83 \
    --beta 1.03 \
    --gamma 0.73 \
    --cuts plotClass/parameters/inclusive.txt \
    --mcuts plotClass/parameters/1700_1200/WJ.txt \
    --varList plotClass/parameters/baseplots.py \
    --mvarList plotClass/parameters/1700_1200/mplots.py \
    --mGo1 1700 --mLSP1 1200 \
    -j 5
     
./RoPlotter.py --indir /nfs/dust/cms/user/amohamed/susy-desy/CMGSamples/UL_FRs_Dec19/2018_FR_ \
    --lumi 59.74 \
    --outdir plots2018_FS/1700_1200 \
    --scale_bkgd_toData \
    #--do_alphabetagamma \
    --doRatio \
    --YmaX 0.0 \
    --YmiN 0.1 \
    --rmax 1.95 \
    --rmin 0.05 \
    --alpha 0.83 \
    --beta 1.03 \
    --gamma 0.73 \
    --cuts plotClass/parameters/0bCS.txt \
    --varList plotClass/parameters/baseplots.py \
    --mvarList plotClass/parameters/1700_1200/mplots.py \
    --mGo1 1700 --mLSP1 1200 \
    -j 5

./RoPlotter.py --indir /nfs/dust/cms/user/amohamed/susy-desy/CMGSamples/UL_FRs_Dec19/2018_FR_ \
    --lumi 59.74 \
    --outdir plots2018_FS/1700_1200 \
    --scale_bkgd_toData \
    #--do_alphabetagamma \
    --doRatio \
    --YmaX 0.0 \
    --YmiN 0.1 \
    --rmax 1.95 \
    --rmin 0.05 \
    --alpha 0.83 \
    --beta 1.03 \
    --gamma 0.73 \
    --cuts plotClass/parameters/2LCS.txt \
    --varList plotClass/parameters/baseplots.py \
    --mvarList plotClass/parameters/1700_1200/mplots.py \
    --mGo1 1700 --mLSP1 1200 \
    -j 5

./RoPlotter.py --indir /nfs/dust/cms/user/amohamed/susy-desy/CMGSamples/UL_FRs_Dec19/2018_FR_ \
    --lumi 59.74 \
    --outdir plots2018_FS/1700_1200 \
    --scale_bkgd_toData \
    #--do_alphabetagamma \
    --doRatio \
    --YmaX 0.0 \
    --YmiN 0.1 \
    --rmax 1.95 \
    --rmin 0.05 \
    --alpha 0.83 \
    --beta 1.03 \
    --gamma 0.73 \
    --cuts plotClass/parameters/inclusive.txt \
    --mcuts plotClass/parameters/1700_1200/Sig_nj6.txt \
    --varList plotClass/parameters/baseplots.py \
    --mvarList plotClass/parameters/1700_1200/mplots.py \
    --mGo1 1700 --mLSP1 1200 \
    -j 5

./RoPlotter.py --indir /nfs/dust/cms/user/amohamed/susy-desy/CMGSamples/UL_FRs_Dec19/2018_FR_ \
    --lumi 59.74 \
    --outdir plots2018_FS/1700_1200 \
    --scale_bkgd_toData \
    #--do_alphabetagamma \
    --doRatio \
    --YmaX 0.0 \
    --YmiN 0.1 \
    --rmax 1.95 \
    --rmin 0.05 \
    --alpha 0.83 \
    --beta 1.03 \
    --gamma 0.73 \
    --cuts plotClass/parameters/inclusive.txt \
    --mcuts plotClass/parameters/1700_1200/Sig_nj7.txt \
    --varList plotClass/parameters/baseplots.py \
    --mvarList plotClass/parameters/1700_1200/mplots.py \
    --mGo1 1700 --mLSP1 1200 \
    -j 5