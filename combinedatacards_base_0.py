#!/usr/bin/env python

# works as python combinedatacards.py INDIR1 INDIR2 OUTDIR

import sys
import os
from math import sqrt, log
import shutil

import glob

path = sys.argv[-1]
outdire = path+"/combinedCards/"

if  not os.path.exists(outdire):
    os.makedirs(str(outdire))

dirlist = [x for x in os.listdir(path) if "mLSP" in x]

for dir in dirlist : 
	#file_list = glob.glob(os.path.join(path,dir+'/*.txt'))
	cmd = 'combineCards.py '+path+'/'+dir+'/*.txt > ' + outdire+"/"+dir+'.txt'
	print cmd 
	os.system(cmd)
		
