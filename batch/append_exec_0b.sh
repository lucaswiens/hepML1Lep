#!/bin/bash

eval 'export PATH="/nfs/dust/cms/user/amohamed/anaconda3/bin:$PATH"'

eval 'export KERAS_BACKEND=tensorflow'

source /nfs/dust/cms/user/amohamed/anaconda3/bin/activate hepML

cd $2

/nfs/dust/cms/user/amohamed/anaconda3/envs/hepML/bin/python append_DNN_0b2.py --infile $1  --model $3 --outdir $4 --indir $5
