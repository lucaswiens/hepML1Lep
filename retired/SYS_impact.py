#!/usr/bin/env python
import sys
sys.argv.append( '-b-' )
import ROOT
from ROOT import std
ROOT.gROOT.SetBatch(True)
sys.argv.remove( '-b-' )

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

import os 
import datetime

import shutil 

infile = ROOT.TFile.Open(sys.argv[0])
outdir = sys.argv[1]

if not os.path.exists(outdir) :  os.makedirs(outdir)

mass = '1500_1000'

bkgs = ["DiLepTT","SemiLepTT","DY","QCD","SingleT","TTV","VV","WJ"]

for bkg in bkgs :
    print(bkg)
    dir = infile.GetDirectory(bkg+"/"+mass)
    histList = dir.GetListOfKeys()
    print([x.GetName() for x in histList])

"""

Dilep = infile.Get("DilepTT/"+mass+"/"+mass+"sig_SR_nom")
Silep = infile.Get("SemiLepTT/1500_1000/1500_1000sig_SR_nom")
DY = infile.Get("DY/1500_1000/1500_1000sig_SR_nom")
QCD = infile.Get("QCD/1500_1000/1500_1000sig_SR_nom")
STop = infile.Get("SingleT/1500_1000/1500_1000sig_SR_nom")
TTV = infile.Get("TTV/1500_1000/1500_1000sig_SR_nom")
VV = infile.Get("TTV/1500_1000/1500_1000sig_SR_nom")
WJ = infile.Get("WJ/1500_1000/1500_1000sig_SR_nom")

Dilep = _file0->Get("DilepTT/1500_1000/1500_1000sig_SR_nom")
Silep = _file0->Get("SemiLepTT/1500_1000/1500_1000sig_SR_nom")
DY = _file0->Get("DY/1500_1000/1500_1000sig_SR_nom")
QCD = _file0->Get("DY/1500_1000/1500_1000sig_SR_nom")
STop = _file0->Get("SingleT/1500_1000/1500_1000sig_SR_nom")
TTV = _file0->Get("TTV/1500_1000/1500_1000sig_SR_nom")
VV = _file0->Get("TTV/1500_1000/1500_1000sig_SR_nom")
WJ = _file0->Get("WJ/1500_1000/1500_1000sig_SR_nom")
"""