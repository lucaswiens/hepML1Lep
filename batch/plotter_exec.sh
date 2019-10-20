#!/bin/bash

eval 'export PATH="/nfs/dust/cms/user/amohamed/anaconda3/bin:$PATH"'

source /nfs/dust/cms/user/amohamed/anaconda3/bin/activate hepML

cd $2

./$1
