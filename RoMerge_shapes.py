#!/usr/bin/env python

import sys
sys.argv.append( '-b-' )
import ROOT
from ROOT import std
ROOT.gROOT.SetBatch(True)
sys.argv.remove( '-b-' )

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

import os ,glob
import datetime

from math import hypot, sqrt, ceil

currentDT = datetime.datetime.now()

import argparse

import htcondor


def getSFs(sffile,mass='1900_100',which='alpha') : 
    token = open(sffile,'r')
    linestoken=token.readlines()
    if which == 'alpha' :  tokens_column_number = 1
    if which == 'alphaE' :  tokens_column_number = 2
    if which == 'beta' :  tokens_column_number = 3
    if which == 'betaE' :  tokens_column_number = 4
    if which == 'gamma' :  tokens_column_number = 5
    if which == 'gammaE' :  tokens_column_number = 6
    resulttoken=[]
    masstoken=[]
    for x in linestoken:
        resulttoken.append(x.split()[tokens_column_number])
        masstoken.append(x.split()[0])
    token.close()
    idx = masstoken.index(mass)
    return resulttoken[idx]


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Runs a NAF batch system merging the shapes', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--indir', help='List of process', metavar='indir')
    #prser.add_argument('--indirB', help='List of BKGs to process', metavar='indirB')
    parser.add_argument('--sfs', help="the text file that has alpha beta gamma",default=None ,metavar='sfs')
    parser.add_argument('--outfile', help="output file name",default=None ,metavar='outfile')

    
    binned = False
    args = parser.parse_args()
    indirB = args.indir+'/grid'
    sfs = args.sfs
    outfile = args.outfile
    
    background_List = os.listdir(indirB)
    for bkg in background_List : 
        bkg_files_SR = glob.glob(os.path.join(indirB,bkg+'/*SR.root'))
        #print (bkg_files_SR)
        outdir = bkg_files_SR[0].replace(bkg_files_SR[0].split("/")[-1],"")
        totabkgroot = ROOT.TFile(outdir+"background.root",'recreate')
        temp = ROOT.TFile.Open(bkg_files_SR[0], "read")
        hist = temp.Get(bkg_files_SR[0].split('/')[-1].split('_')[1]+'/'+bkg+'/'+bkg+'sig_SR').Clone()
        othershist = temp.Get(bkg_files_SR[0].split('/')[-1].split('_')[1]+'/'+bkg+'/'+bkg+'sig_SR').Clone()
        hist.Reset()
        othershist.Reset()
        for i,bkgf in enumerate(bkg_files_SR) :
            print(bkgf)
            bkg_name = bkgf.split('/')[-1].split('_')[1]
            if bkg_name == 'Data' : continue 
            bf = ROOT.TFile.Open(bkgf, "read")
            #print(bkg_name+'/'+bkg+'/'+bkg_name+bkg+'sig_SR_nominal')
            bhist = bf.Get(bkg_name+'/'+bkg+'/'+bkg+'sig_SR')
            #print(bhist.Integral())
            which = ''
            scalefactor = 1.0
            if bkg_name == 'DiLepTT' : which = 'beta'
            elif bkg_name == 'SemiLepTT' :which = 'alpha'
            elif bkg_name != 'Data' : which = 'gamma'
            scalefactor = float(getSFs(sfs,mass=bkg,which=which))
            bhist.Scale(scalefactor)
            if (bkg_name != 'DiLepTT' and bkg_name != 'SemiLepTT' and bkg_name != 'Data') : 
                othershist.Add(bhist)
            hist.Add(bhist)
            print(bkg_name,bhist.Integral())
        print(othershist.Integral(),hist.Integral())

        background_dir = totabkgroot.mkdir("background")
        background_dir.cd()
        background_dir_  = background_dir.mkdir(bkg)
        background_dir_.cd()
        hist.SetName("background")
        hist.SetTitle("background")
        hist.Write()

        Others_dir = totabkgroot.mkdir("Others")
        Others_dir.cd()
        Others_dir_  = Others_dir.mkdir(bkg)
        Others_dir_.cd()
        othershist.SetName("Others")
        othershist.SetTitle("Others")
        othershist.Write()

        totabkgroot.Close()
    os.system("hadd -f "+outfile+" "+args.indir+"/*/*/*.root")
