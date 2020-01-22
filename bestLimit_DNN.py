#!/usr/bin/env python

# works as python combinedatacards.py INDIR1 INDIR2 INDIR3 OUTDIR
import sys
import os
from math import sqrt, log
import shutil
from ROOT import TH2F,TCanvas,TFile,gStyle

path1 = sys.argv[-3]+'/datacards/limitOutput/'
path2 = sys.argv[-2]+'/datacards/limitOutput/'
#path3 = sys.argv[-2]+'/limitOutput/'

print (path1 , path2)
def find_all_matching(substring, path):
    result = []
    for root, dirs, files in os.walk(path):
        for thisfile in files:
            if substring in thisfile:
                result.append(os.path.join(root, thisfile ))
    return result

items1 = find_all_matching('.root',str(path1))
items2 = find_all_matching('.root',str(path2))

items_1_root = [x.split("/")[-1] for x in items1]
items_2_root = [x.split("/")[-1] for x in items2]

intersect = [value for value in items_1_root if value in items_2_root] 
items_1_not2 = [value for value in items_1_root if  value not in items_2_root] 
items_2_not1 = [value for value in items_2_root if  value not in items_1_root] 

#print "intersect == " , intersect
#print "items_1_not2 == " , items_1_not2
#print "items_2_not1 == " , items_2_not1

print (2*len(intersect)+len(items_1_not2)+len(items_2_not1) - len(items_1_root)- len(items_2_root))

outdire = sys.argv[-1]

if  os.path.exists(outdire):
    des = input(" this dir is already exist : "+str(outdire)+" do you want to remove it [y/n]: ")
    if ( "y" in des or "Y" in des or "Yes" in des) : 
        shutil.rmtree(str(outdire))
        os.makedirs(str(outdire))
    elif ( "N" in des or  "n" in des or  "No" in des ): print (str(outdire)) , "will be ovewritten by the job output -- take care"  
    else :
    	raise ValueError( "do not understand your potion")
else : os.makedirs(str(outdire))
os.makedirs(str(outdire)+'/datacards/limitOutput/')
# 2016 ranges 
#grid = TH2F('grid','grid', 101,-12.5,2512.5,73,-12.5,1812.5)
# 2017 ranges 
grid = TH2F('grid','grid', 113,-12.5,2812.5,73,-12.5,1812.5)

c = TCanvas("c","c",1000,1000)
# copy what are not in the overlap between both pathes 

for i_1 in items_1_not2 :
    shutil.copy(path1+'/'+i_1, str(outdire)+'/datacards/limitOutput/')
    mGo = i_1.split("mGo")[-1].split('_mLSP')[0]
    mLSP = i_1.split("_mLSP")[-1].split('.Asymptotic.')[0]
    grid.Fill(mGo,mLSP,1)
for i_2 in items_2_not1 : 
    shutil.copy(path2+'/'+i_2, str(outdire)+'/datacards/limitOutput/')
    mGo = i_2.split("mGo")[-1].split('_mLSP')[0]
    mLSP = i_2.split("_mLSP")[-1].split('.Asymptotic.')[0]
    grid.Fill(mGo,mLSP,2)
for item in intersect : 

    if not item.startswith("higgsCombineT1tttt_Scan"): continue
    masspoint1 = path1+'/'+item
    masspoint2 = path2+'/'+item
    #print masspoint1
    masspoint = str(outdire)+'/datacards/limitOutput/'+item
    
    for mGo in range(600, 2800, 25):
        for mLSP in range(0,1600,25):
            Min = 9999.9999 
            best = ''
            bestClass = 0
            if (masspoint1 and masspoint2 ).endswith('higgsCombineT1tttt_Scan_mGo'+str(mGo)+'_mLSP'+str(mLSP)+'.Asymptotic.mH120.root') :
                f1 = TFile.Open(masspoint1, 'read')
                f2 = TFile.Open(masspoint2, 'read')
                t1 = f1.Get('limit')
                t2 = f2.Get('limit')
                for entry in t1:
                    q = entry.quantileExpected
                    if q == 0.5:
                        r1 = entry.limit
                        if r1 < Min :
                            Min = r1
                            best = masspoint1
                            bestClass = 1 
                for entry in t2:
                    q = entry.quantileExpected
                    if q == 0.5:
                        r2 = entry.limit
                        if r2 < Min :
                            Min = r2
                            best = masspoint2
                            bestClass = 2
                if bestClass == 0 : continue 
                print (str(mGo)," " * 3 ,str(mLSP) , " " * 3 , 'DNN_'+str(bestClass))
                shutil.copy(best, masspoint)
                #print masspoint
                #print r1 ,' from  ',masspoint1 ,' and ', r2, ' from  ',masspoint2,' and ', r3, ' from ',masspoint3,' The Min is : ' , Min , ' from ', best
                
                grid.Fill(mGo,mLSP,bestClass) 
                
c.cd()
gStyle.SetOptStat(0)
grid.GetXaxis().SetTitle("m_{g} [GeV]")
grid.GetYaxis().SetTitle("m_{LSP} [GeV]")
grid.GetYaxis().SetTitleOffset(1.5)
grid.Draw('COL text goff')
c.SaveAs(outdire+"/grid.pdf")
