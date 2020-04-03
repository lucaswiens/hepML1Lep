#!/usr/bin/env python

# works as python combinedatacards.py INDIR1 INDIR2 OUTDIR

import sys
import os
from math import sqrt, log
import shutil


path1 = sys.argv[-2]
path2 = sys.argv[-3]
path3 = sys.argv[-4]

outdire = sys.argv[-1]+"/combinedCards/"

if  os.path.exists(outdire):
    des = raw_input(" this dir is already exist : "+str(outdire)+" do you want to remove it [y/n]: ")
    if ( "y" in des or "Y" in des or "Yes" in des) : 
        shutil.rmtree(str(outdire))
        os.makedirs(str(outdire))
    elif ( "N" in des or  "n" in des or  "No" in des ): print str(outdire) , "will be ovewritten by the job output -- take care"  
    else :
    	raise ValueError( "do not understand your potion")
else : os.makedirs(str(outdire))


list_1 = [f for f in os.listdir(path1+'/combinedCards/') if f.endswith('.txt')]
list_2 = [f for f in os.listdir(path2+'/combinedCards/') if f.endswith('.txt')]
list_3 = [f for f in os.listdir(path3+'/combinedCards/') if f.endswith('.txt')]

for card in list_1 : 
	if (card in list_2 and card in list_3 ) :
		card_1 = path1+'/combinedCards/'+card
		card_2 = path2+'/combinedCards/'+card
		card_3 = path3+'/combinedCards/'+card
		
		cmd = 'combineCards.py ' + card_1 +' '+ card_2 +' '+ card_3 + ' > ' + outdire+"/"+card
		print cmd 
		os.system(cmd)
		
	else : print "card in one dir and not in the other please check : ", card 


