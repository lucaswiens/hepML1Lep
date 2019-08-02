#!/bin/bash

eval 'export PATH="/nfs/dust/cms/user/amohamed/anaconda3/bin:$PATH"'

source /nfs/dust/cms/user/amohamed/anaconda3/bin/activate hepML

cd $1

/nfs/dust/cms/user/amohamed/anaconda3/envs/hepML/bin/python RoShapes.py --indir $2 --outdir $3 --lumi $4 --group $5 --cutdict $6 --mass $7 $8
