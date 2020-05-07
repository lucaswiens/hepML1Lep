#!/bin/bash

eval 'export PATH="/nfs/dust/cms/user/amohamed/anaconda3/bin:$PATH"'

source /nfs/dust/cms/user/amohamed/anaconda3/bin/activate hepML

cd $2

/nfs/dust/cms/user/amohamed/anaconda3/envs/hepML/bin/python skimmer.py --infile $1 --outdir $3 --tree $4 --tdir $5 --cuts "($6)"
