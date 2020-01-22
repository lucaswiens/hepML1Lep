#!/bin/bash

eval 'export PATH="/nfs/dust/cms/user/amohamed/anaconda3/bin:$PATH"'

source /nfs/dust/cms/user/amohamed/anaconda3/bin/activate hepML

eval 'cd /nfs/dust/cms/user/amohamed/susy-desy/ML/hepML_1Lep'

echo "$@"

python RoPlotter.py "$@"
