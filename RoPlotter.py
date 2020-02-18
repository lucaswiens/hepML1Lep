#!/usr/bin/env python
from array import array

import sys
sys.argv.append( '-b-' )
import ROOT
from ROOT import std
ROOT.gROOT.SetBatch(True)
sys.argv.remove( '-b-' )

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

from plotClass.rootplot  import rootplot

from plotClass.plotting import tdrstyle,CMS_lumi

import os 
import datetime

from math import hypot, sqrt, ceil

currentDT = datetime.datetime.now()
import shutil 
#from plotClass.plotting.SplitCanv import * 


'''def findItem(theList, item):
   return [(ind, theList[ind].index(item)) for ind in range(len(theList)) if item in theList[ind]]'''
def findItem(theList, item):
    for ind in range(len(theList)):
        if item in theList[ind]:
            return ind, theList[ind].index(item)
        else: pass

def make1D(var,style,name,bins = []):
    '''  A functon to make a 1D histogram and set it's style '''
    # check if var binwidth is requested 
    if len(bins) == 0 :
        hist = ROOT.TH1F(name,name,var[3][0],var[3][1],var[3][2])
    else : 
        hist = ROOT.TH1F(name,name,len(bins)-1 ,array('d',bins))
    #hist.Draw('goff')
    if style["fill"]:
        style["fill"].Copy(hist)
    if style["line"]:
        style["line"].Copy(hist)
    if style["marker"]:
        style["marker"].Copy(hist)
    hist.GetYaxis().SetTitle('Events')
    hist.GetYaxis().SetTitleSize(0.07)
    hist.GetYaxis().SetTitleFont(42)
    hist.GetYaxis().SetTitleOffset(1.2)
    hist.GetXaxis().SetTitle(var[2])
    hist.GetXaxis().SetLabelFont(42)
    hist.GetYaxis().SetLabelSize(0.05)
    hist.GetXaxis().SetTitleOffset(1.1)
    hist.SetTitle(style["Label"])
    return hist

def make1D_bins(binlist,style,name):
    '''  A functon to make a 1D histogram from bins and set it's style '''
    # check if var binwidth is requested 
    if len(binlist) == 0 : 
        print('you requested to make 1D histogram from bins while the bin list is empy, will not do it, please check')
        pass
    else : 
        hist = ROOT.TH1F(name,name,len(binlist),0,len(binlist))
    #hist.Draw('goff')
    if style["fill"]:
        style["fill"].Copy(hist)
    if style["line"]:
        style["line"].Copy(hist)
    if style["marker"]:
        style["marker"].Copy(hist)
    hist.GetYaxis().SetTitle('Events')
    hist.GetYaxis().SetTitleSize(0.07)
    hist.GetYaxis().SetTitleFont(42)
    hist.GetYaxis().SetTitleOffset(1.2)
    hist.GetXaxis().SetTitle('')
    hist.GetXaxis().SetLabelFont(42)
    hist.GetYaxis().SetLabelSize(0.05)
    hist.GetXaxis().SetTitleOffset(1.1)
    hist.SetTitle(style["Label"])
    for i , binname in enumerate(binlist) : 
        hist.GetXaxis().SetBinLabel(i+1,binname)
    return hist


def doScaleBkgNormData(datalist,bkglist,bkgsum,Apply = False):
    if len(datalist) == 0 : return -1.0
    if len(bkglist)  == 0 : return -1.0
    data = datalist[0]
    bkg  = bkgsum
    int = 0
    for l in bkglist : 
       int+= l.Integral()
    rm = bkg.Integral() - int
    sf = (data.Integral() - rm) / int
    bkgs = bkglist
    if Apply : 
        for h in bkgs:
            h.Scale(sf)
    return sf

def sorttinglist(Hlist) : 
    #print "Hlist has : " ,Hlist
    sortedHList = sorted(Hlist,key = lambda l : l.Integral())#,reverse=True)
    #print "sotred List : " , sortedHList
    return sortedHList

def doLegend(signalHists, BKGHists, DataHists, textSize=0.035, columns=1,showSF=True,uncertHist = None ):
    sigEntries = signalHists
    bgEntries = BKGHists
    dataEntry = DataHists
    legWidth= 0.36 if columns > 1 else 0.18
    nentries = len(sigEntries) if sigEntries else 0 + len(bgEntries) if bgEntries else 0 + 1 if dataEntry else 0 + 1 if uncertHist else 0 
    height = (.20 + textSize*max(nentries-3, 0))
    if columns > 1:
    	height = 0.9*height/columns#1.3*
    (x1, y1, x2, y2) = (0.9 - 1.3*legWidth , .88 - 2.5*height, .9, .92)
    
    leg = ROOT.TLegend(x1, y1, x2, y2)
    leg.SetHeader("")
    leg.SetFillColor(0)
    leg.SetShadowColor(0)
    leg.SetLineColor(0)
    leg.SetTextFont(42)
    leg.SetTextSize(textSize)
    leg.SetNColumns(columns)
    entries = []
    if dataEntry:
    	entries.append((DataHists,'', 'LPE'))
    if signalHists : 
        for sigplot in signalHists:
            entries.append((sigplot,'', 'LE'))
    if bgEntries : 
        for bplot in bgEntries:
            entries.append((bplot,'', 'F'))
    #if totalError:
    #    entries.append((totalError, "Total unc.", "F"))
    nrows = int(ceil(len(entries)/float(columns)))
    for r in range(nrows):
        for c in range(columns):
            i = r+c*nrows
            if i >= len(entries):
                break
            #print(entries[i])   
            leg.AddEntry(*entries[i])
    if showSF:
        leg.AddEntry('SF', 'SF: {0}'.format(round(sf, 2)), '')
    #if options.showSF: leg.AddEntry('SF', 'SF: {0}'.format(round(1.19,2)), '')
    if uncertHist : 
        leg.AddEntry(uncertHist,"Total unc.")
    leg.Draw()
    ## assign it to a global variable so it's not deleted
    global legend_
    legend_ = leg
    return leg


def doalphabetagamma(histlist,alpha,beta,gamma):
    scaled_List = []
    for h in histlist : 
        hname = h.GetName()
        if 'DiLepTT' in hname : 
            h.Scale(beta)
        elif 'SemiLepTT' in hname : 
            h.Scale(alpha)
        else : 
            h.Scale(gamma)
        scaled_List.append(h)
    return scaled_List

def doShadedUncertainty(h):
    xaxis = h.GetXaxis()
    points = []; errors = []
    for i in range(h.GetNbinsX()):
        N = h.GetBinContent(i+1); dN = h.GetBinError(i+1);
        if N == 0 and dN == 0: continue
        x = xaxis.GetBinCenter(i+1);
        points.append( (x,N) )
        EYlow, EYhigh  = dN, min(dN,N);
        EXhigh, EXlow = (xaxis.GetBinUpEdge(i+1)-x, x-xaxis.GetBinLowEdge(i+1))
        errors.append( (EXlow,EXhigh,EYlow,EYhigh) )
    ret = ROOT.TGraphAsymmErrors(len(points))
    ret.SetName(h.GetName()+"_errors")
    for i,((x,y),(EXlow,EXhigh,EYlow,EYhigh)) in enumerate(zip(points,errors)):
        ret.SetPoint(i, x, y)
        ret.SetPointError(i, EXlow,EXhigh,EYlow,EYhigh)
    ret.SetFillStyle(3244);
    ret.SetFillColor(ROOT.kGray+2)
    ret.SetMarkerStyle(0)
    #ret.Draw("PE2 SAME")
    return ret

def makeStack(histList):
    '''  A functon to make a THStack for background and set it's style '''
    s = ROOT.THStack("s","")
    for bkghist in histList :
        s.Add(bkghist)
    s.SetTitle('THStack')
    return s 

def hadd1ds(histList,alphabetagamma=False):
    '''  A functon to hadd background and set it's style '''
    sumbkg = ROOT.TH1F(histList[0].Clone())
    sumbkg.Reset()
    for bkghist in histList :
        h = ROOT.TH1F(bkghist.Clone())
        if alphabetagamma : 
            hname = h.GetName()
            if 'DiLepTT' in hname : h.Scale(beta)
            elif 'SemiLepTT' in hname : h.Scale(alpha)
            else : h.Scale(gamma)
        sumbkg.Add(h)
    #sumbkg.Draw('goff')
    sumbkg.SetTitle('Total BKG')
    sumbkg.SetName('sumbkg')
    return sumbkg

#lumi = #'59.74'#'41.9'#

import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Runs a NAF batch system for nanoAOD', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--indir', help='List of datasets to process',default=None, metavar='indir')
    parser.add_argument('--lumi', help='integrated luminosity',default='35.9', metavar='lumi')
    parser.add_argument('--outdir', help='output directory',default=None,metavar='outdir')
    parser.add_argument('--scale_bkgd_toData','--sbtd', help="scale the over all bkg to data",default=False, action='store_true')
    parser.add_argument('--do_alphabetagamma','--apg', help='use alpha/beta/gamma scale',default=False, action='store_true')
    parser.add_argument('--blind',help='blind data',default=False, action='store_true')
    parser.add_argument('--doRatio','--ratio', help='do data/MC ration plot',default=False, action='store_true')
    parser.add_argument('--YmaX', help='Yaxis maximum',default='0.0', metavar='YmaX')
    parser.add_argument('--YmiN', help='Yaxis minimum',default='0.1', metavar='YmiN')
    parser.add_argument('--rmax', help='ratio Yaxis maximum',default='1.95', metavar='YmaX')
    parser.add_argument('--rmin', help='ratio Yaxis minimum',default='0.05', metavar='YmiN')
    parser.add_argument('--cuts','--c',help='a text file that has a cutlist',default='plotClass/Cutstring.txt', metavar='cuts')
    parser.add_argument('--mcuts','--mc',help='a text file that has additional cutlist',default=None, metavar='mcuts')
    parser.add_argument('--varList','--vars',help='variables to plot',default=None, metavar='varList')
    parser.add_argument('--mvarList','--mvars',help='more variables to plot',default=None, metavar='mvarList')
    parser.add_argument('--alpha', help='scale factor alpha',default='0.0', metavar='alpha')
    parser.add_argument('--beta', help='scale factor alpha',default='0.0', metavar='beta')
    parser.add_argument('--gamma', help='scale factor alpha',default='0.0', metavar='gamma')
    parser.add_argument('--mGo1', help='Signal 1 mGo',default=None, metavar='mGo1')
    parser.add_argument('--mGo2', help='Signal 2 mGo',default=None, metavar='mGo2')
    parser.add_argument('--mLSP1', help='Signal 1 mLSP',default=None, metavar='mLSP1')
    parser.add_argument('--mLSP2', help='Signal 2 mLSP',default=None, metavar='mLSP2')
    parser.add_argument("-j", "--jobs", default=0, help="Use N threads",metavar='jobs')
    parser.add_argument("-Y", "--year", default=2016, help="which ear to run on 2016/17/18",metavar='year')
    parser.add_argument("--mb", "--multib", default=False, help="multple b or zero b analysis",action='store_true')
    



    args = parser.parse_args()

    if args.mb : 
        from plotClass.plotting.plotGroups import All_files
    else : 
        from plotClass.plotting.plotGroups_0b import All_files

    subdir = args.cuts.split("/")[-1].replace('.txt',"") if args.mcuts == None else args.mcuts.split("/")[-1].replace('.txt',"")
    lumi = args.lumi ; indir = args.indir ; outdire = os.path.join(args.outdir,subdir)
    if not os.path.exists(outdire) : os.makedirs(outdire) ; shutil.copy('batch/index.php',outdire)
    
    textdire = os.path.join(outdire,'txt')
    if not os.path.exists(textdire) : os.makedirs(textdire)
    pngdire = os.path.join(outdire,'png')
    if not os.path.exists(pngdire): os.makedirs(pngdire)
    pdfdire = os.path.join(outdire,'pdf')
    if not os.path.exists(pdfdire) : os.makedirs(pdfdire)
    epsdire = os.path.join(outdire,'eps')
    if not os.path.exists(epsdire) : os.makedirs(epsdire)

    scale_bkgd_toData = args.scale_bkgd_toData
    do_alphabetagamma = args.do_alphabetagamma
    doRatio = args.doRatio
    YmaX = float(args.YmaX) ; YmiN = float(args.YmiN)
    rmax = float(args.rmax) ; rmin = float(args.rmin)
    mGo1 = args.mGo1 ; mGo2 = args.mGo2 
    mLSP1 = args.mLSP1 ; mLSP2 = args.mLSP2 

    if 'Signal_1' in All_files.keys() or 'Signal_2' in All_files.keys() : 
        if mGo1 == None : 
            del All_files['Signal_1']
        else : 
            All_files['Signal_1']['select'] = All_files['Signal_1']['select'].replace('@mGo',str(mGo1)).replace('@mLSP',str(mLSP1))
            All_files['Signal_1']['Label'] = All_files['Signal_1']['Label'].replace('@mGo',str(float(mGo1)/1000.0)).replace('@mLSP',str(float(mLSP1)/1000))
        if mGo2 == None : 
            del All_files['Signal_2']
        else : 
            All_files['Signal_2']['select'] = All_files['Signal_2']['select'].replace('@mGo',str(mGo2)).replace('@mLSP',str(mLSP2))
            All_files['Signal_2']['Label'] = All_files['Signal_2']['Label'].replace('@mGo',str(float(mGo2)/1000.0)).replace('@mLSP',str(float(mLSP2)/1000))

    cut_strings = ''
    cf = open(args.cuts, 'r')
    for cutline in cf : 
        if cutline.startswith("#") : continue
        cutline = str(cutline).strip()
        cut_strings+= cutline 
    
    if args.mcuts != None : 
        mcf = open(args.mcuts, 'r')
        for cutline in mcf : 
            if cutline.startswith("#") : continue
            cutline = str(cutline).strip()
            cut_strings+= cutline 

    if args.blind : 
        del All_files['Data']
        doRatio = False
    varList = [] 
    exec(open(args.varList).read())
    if args.mvarList != None : 
        exec(open(args.mvarList).read())
 
    alpha,beta,gamma =  float(args.alpha),float(args.beta),float(args.gamma)#0.83 ,1.01 , 0.74


    tdrstyle.setTDRStyle()

    showRatioErorr = True
    ShowMCerror = True
    CMS_lumi.writeExtraText = 1

    CMS_lumi.lumi_13TeV = "%s fb^{-1}" % lumi
    CMS_lumi.extraText  = 'Preliminary'
    CMS_lumi.lumi_sqrtS = '13 TeV'
    CMS_lumi.lumiTextSize     = 0.6 if doRatio else 0.52
    CMS_lumi.cmsTextSize      = 0.75 if doRatio else 0.62
    CMS_lumi.extraOverCmsTextSize  = 0.76 if doRatio else 0.62 

    # get the plotter class instant 
    instPlot = rootplot(indir,outdire,All_files=All_files)
    if int(args.jobs) == 0 : 
        for g in instPlot.group:
            # fill the dictionary with all the files founded under the indir under each category 
            All_files[g]['files'] = instPlot.group[g]
            # make chain with each background seperatly 
            chain = instPlot.chain_and_cut(All_files[g]['files'],"sf/t",cut_strings,All_files[g]['select'])
            # add the chain to each category
            All_files[g]['chain']  = chain
            # init empty list of histogram tio be filled in the next loop
            All_files[g]['hist'] = []
            All_files[g]['hist_bins'] = []
    else : 
        from multiprocessing import Pool
        pool = Pool(int(args.jobs))
        myargs = []
        # make tuple of aruments to be passed to the chain maker
        for g in instPlot.group:
            # fill the dictionary with all the files founded under the indir under each category 
            All_files[g]['files'] = instPlot.group[g]
            All_files[g]['hist'] = []
            All_files[g]['hist_bins'] = []
            myargs.append((All_files[g]['files'],"sf/t",cut_strings,All_files[g]['select']))
        #print(myargs[0])
        # make chain with each background seperatly 
        retlist = [pool.apply_async(instPlot.chain_and_cut,args = argo) for argo in myargs]
        #print(retlist)
        for i , g in enumerate(instPlot.group):
            All_files[g]['chain']  = retlist[i].get() 
    # create the output root file
    outroot = ROOT.TFile(outdire+"/plots_{0}_{1}_{2}".format(currentDT.year,currentDT.month,currentDT.day)+".root","recreate")
    
    for i,var in enumerate(varList) :

        outtext = open(textdire+"/"+var[0]+".txt", "w+")
        print (var[0])
        # make Tdir for each Varable to plot
        tDirectory= outroot.mkdir(var[0])
        # move the the TDir
        tDirectory.cd()
        # list to be filled with bkg to be stacked
        stackableHists = []
        SignalHists = []
        error = ROOT.Double(0.)
        for key in All_files :
            # make the hist 
            if any('varbin' in e for e in var) : 
                index0,_ = findItem(var , 'varbin')
                bins = var[index0][1]
                hist = make1D(var,All_files[key],key+var[0],bins = bins)
            else : 
                hist = make1D(var,All_files[key],key+var[0])
            # draw the variable to the hist created 
            if 'Data' in key : lum = '1.0' 
            else  : lum = lumi
            if int(args.year) != 2016 : All_files[key]['scale']  = All_files[key]['scale'].replace('*nISRweight','').replace("*nISRttweight","")
            All_files[key]['chain'].Draw(var[1] +' >> '+key+var[0], All_files[key]['scale']+'*'+lum+'*(1)',"goff")
            #print (hist)
            ROOT.gROOT.ForceStyle()
            All_files[key]['hist'].append(hist) 
            if All_files[key]['Stackable'] : stackableHists.append(hist)
            if 'Sig' in key : SignalHists.append(hist)
            if (hist.GetSumw2N() == 0) : hist.Sumw2(ROOT.kTRUE)
            # check the overflow bins 
            if any('IncludeOverflows' in e for e in var) :
                n = hist.GetNbinsX()
                hist.SetBinContent(1,hist.GetBinContent(0)+hist.GetBinContent(1))
                hist.SetBinContent(n,hist.GetBinContent(n+1)+hist.GetBinContent(n))
                hist.SetBinError(1,hypot(hist.GetBinError(0),hist.GetBinError(1)))
                hist.SetBinError(n,hypot(hist.GetBinError(n+1),hist.GetBinError(n)))
                hist.SetBinContent(0,0)
                hist.SetBinContent(n+1,0)
                hist.SetBinContent(0,0)
                hist.SetBinContent(n+1,0)
            # per binwidth normalization
            if any('varbin' in e for e in var) : 
                normBinW = var[index0][2]
                bins = var[index0][1]
                if normBinW == True:
                    nbins = hist.GetNbinsX()
                    #for bin in range(0,nbins+1):
                    #    hist.SetBinContent(bin,hist.GetBinContent(bin)/hist.GetXaxis().GetBinWidth(bin))
                    hist.Scale(0.1,"width");
            # write the hist
            outtext.write("{:<20}{:<20}{:<20}".format(hist.GetTitle(),round(hist.IntegralAndError(0,hist.GetNbinsX()+1,error),2),round(error,2))+"\n")
            hist.Write()
        # make the total BKG hist to be used for ratio calculation
        total = hadd1ds(stackableHists,do_alphabetagamma)
        outtext.write("{:<20}{:<20}{:<20}".format('total bkg unscaled ',round(total.IntegralAndError(0,total.GetNbinsX()+1,error),2),round(error,2))+"\n")
        total.SetName("totalBKG")
        total.Write()
        stackableHists = sorttinglist(stackableHists)
        # scale the individual background to data
        apply = False
        if do_alphabetagamma : 
            stackableHists_ = doalphabetagamma(stackableHists,alpha,beta,gamma)
            if ('Data' in All_files.keys() and scale_bkgd_toData ) : 
                apply = False
                sf = doScaleBkgNormData(All_files['Data']['hist'],stackableHists_,total,Apply = apply)
            else : sf = 1.0
        elif ('Data' in All_files.keys() and scale_bkgd_toData and not do_alphabetagamma) :
            apply = True 
            sf = doScaleBkgNormData(All_files['Data']['hist'],stackableHists,total,Apply=apply)
        else : sf = 1.0
        # scale the total backgrounds to data
        total.Scale(sf if apply == True else 1.0 )
        total.SetName("totalBKG_scaled")
        # make stack of the background (sorted)
        stack = makeStack(stackableHists)
        # write them 
        stack.Write()
        total.Write()
        outtext.write("{:<20}{:<20}{:<20}".format('total bkg scaled ',round(total.IntegralAndError(0,total.GetNbinsX()+1,error),2),round(error,2))+"\n")
        # make canvas to draw 
        plotformat = (600,600)
        sf_ = 20./plotformat[0]

        height = plotformat[1]+150 if (doRatio  and 'Data' in All_files.keys()) else plotformat[1]
        ROOT.gStyle.SetPadLeftMargin(600.*0.18/plotformat[0])

        if (doRatio and 'Data' in All_files.keys()) : ROOT.gStyle.SetPaperSize(20.,sf_*(plotformat[1]+150))
        else:       ROOT.gStyle.SetPaperSize(20.,sf_*plotformat[1])
        
        # create canvas
        canv = ROOT.TCanvas(var[0],var[0],plotformat[0]+150, height)
        ROOT.SetOwnership(canv, False)
        canv.SetTopMargin(canv.GetTopMargin()*1.2)
        topsize = 0.12*600./height if doRatio else 0.06*600./height
        canv.SetTopMargin(topsize)
        canv.cd()
        if (doRatio  and 'Data' in All_files.keys()) : 
            stackPad = ROOT.TPad("mainpad"+var[0], "mainpad"+var[0], 0, 0.30, 1, 1)
            ROOT.SetOwnership(stackPad, False)
            stackPad.SetBottomMargin(0.025)
            stackPad.SetTicks(1, 1)
            stackPad.Draw()
            ratioPad = ROOT.TPad("ratiodpad"+var[0], "ratiopad"+var[0],0,0,1,0.30)
            ROOT.SetOwnership(ratioPad, False)
            ratioPad.SetTopMargin(0.001)
            ratioPad.SetBottomMargin(0.35)
            ratioPad.SetTicks(1,1)
            ratioPad.Draw()
            stackPad.cd()
        # Draw the stack first
        stack.Draw('hist')
        if any('MoreY' in e for e in var) : 
            index1,_ = findItem(var , 'MoreY')
            stack.SetMaximum(var[index1][1]*stack.GetMaximum())
        if any('YmiN' in e for e in var) : 
            index1,_ = findItem(var , 'YmiN')
            YmiN = var[index1][1]
        if any('YmiN' in e for e in var) : 
            index1,_ = findItem(var , 'YmiN')
            YmiN = var[index1][1]

        stack.SetMinimum(YmiN)
        stack.GetXaxis().SetTitleOffset(1.1)
        stack.GetXaxis().SetLabelOffset(0.007)
        if  (doRatio and 'Data' in All_files.keys()): 
            stack.GetXaxis().SetLabelOffset(999) ## send them away
            stack.GetXaxis().SetTitleOffset(999) ## in outer space
        stack.GetXaxis().SetTitleFont(42)
        stack.GetXaxis().SetTitleSize(0.05)
        stack.GetXaxis().SetLabelFont(42)
        stack.GetXaxis().SetLabelSize(0.04)
        stack.GetYaxis().SetTitleFont(42)
        stack.GetYaxis().SetTitleSize(0.05)
        stack.GetYaxis().SetTitleOffset(1.2)
        stack.GetYaxis().SetLabelFont(42)
        stack.GetYaxis().SetLabelSize(0.05)
        stack.GetYaxis().SetLabelOffset(0.007)
        stack.GetYaxis().SetTitle('Events')
        stack.GetXaxis().SetTitle(var[2])
        stack.GetXaxis().SetNdivisions(510)

        if ShowMCerror : 
            totaluncert = doShadedUncertainty(total.Clone())
            totaluncert.Draw("PE2 SAME")
        # for blinding a specific histogram
        xblind = [9e99, -9e99]
        if any('blinded' in e for e in var) and  'Data' in All_files.keys() : 
            index2,_ = findItem(var , 'blinded')
            blind = var[index2][1]
            import re
            if re.match(r'(bin|x)\s*([<>]?)\s*(\+|-)?\d+(\.\d+)?|(\+|-)?\d+(\.\d+)?\s*<\s*(bin|x)\s*<\s*(\+|-)?\d+(\.\d+)?', blind):
                xfunc = (lambda h, b: b) if 'bin' in blind else (lambda h, b: h.GetXaxis().GetBinCenter(b))
                test = eval("lambda bin : "+blind) if 'bin' in blind else eval("lambda x : "+blind)
                All_files['Data']['hist'][i]
                for b in range(1, All_files['Data']['hist'][i].GetNbinsX()+1):
                    if test(xfunc(All_files['Data']['hist'][i], b)):
                    #print "blinding bin %d, x = [%s, %s]" % (b, hdata.GetXaxis().GetBinLowEdge(b), hdata.GetXaxis().GetBinUpEdge(b))
                        All_files['Data']['hist'][i].SetBinContent(b, 0)
                        All_files['Data']['hist'][i].SetBinError(b, 0)
                        xblind[0] = min(xblind[0], All_files['Data']['hist'][i].GetXaxis().GetBinLowEdge(b))
                        xblind[1] = max(xblind[1], All_files['Data']['hist'][i].GetXaxis().GetBinUpEdge(b))

        # draw and write the data histo if there any 
        if 'Data' in All_files.keys() : 
            All_files['Data']['hist'][i].Write()
            All_files['Data']['hist'][i].Draw('EP same')
            All_files['Data']['hist'][i].SetMarkerStyle(20)
            All_files['Data']['hist'][i].SetMarkerSize(1.6)
            All_files['Data']['hist'][i].SetLineColor(1)
            All_files['Data']['hist'][i].SetMarkerColor(ROOT.kBlack)
            #All_files['Data']['hist'][i].SetLineWidth(2)
            All_files['Data']['hist'][i].Sumw2()
        
        # draw the blind 
        if xblind[0] < xblind[1]:
                blindbox = ROOT.TBox(xblind[0],total.GetYaxis().GetXmin(),xblind[1],total.GetMaximum())
                blindbox.SetFillColor(ROOT.kBlue+3)
                blindbox.SetFillStyle(3944)
                blindbox.Draw()
                xblind.append(blindbox) # so it doesn't get deleted
        
        # same for signals 
        if SignalHists : 
            for sHist in SignalHists : 
                sHist.Write()
                sHist.Draw('histsame')

        if (doRatio and 'Data' in All_files.keys()): 
            ratioPad.cd()
            sumbkgscaled = ROOT.TH1F(total.Clone())
            pull = ROOT.TH1F(All_files['Data']['hist'][i].Clone())
            
            pull.Divide(sumbkgscaled)
            pull.SetMarkerStyle(20)
            pull.GetYaxis().SetTitle('Data/Pred.')
            #pull.GetXaxis().SetTitle(key)
            pull.GetYaxis().SetRangeUser(rmin,rmax)
            pull.GetYaxis().SetDecimals(True)
            pull.SetLabelSize(0.14, "XY")
            pull.GetXaxis().SetTitleSize(.1)
            pull.GetYaxis().SetTitleSize(.11)
            pull.GetYaxis().SetLabelSize(0.11)
            pull.GetXaxis().SetLabelSize(0.11)
            pull.GetYaxis().SetTitleOffset(0.6)
            pull.GetYaxis().SetNdivisions(505)
            
            pull.Draw("EP")
            # Draw Line at ration == 1 
            line = ROOT.TLine(pull.GetXaxis().GetXmin(),1,pull.GetXaxis().GetXmax(),1)
            line.SetLineWidth(2);
            line.SetLineColor(58);
            line.Draw()
            
            if showRatioErorr : 
                sumMCErrors = total.Clone()
                sumMCErrors.SetFillColorAlpha(ROOT.kGray, 0.0)
                sumMCErrors.SetMarkerSize(0)
                for j in range(All_files['Data']['hist'][i].GetNbinsX()+2):
                    sumMCErrors.SetBinError(j, sumMCErrors.GetBinError(j)/max(sumMCErrors.GetBinContent(j), 1))
                    sumMCErrors.SetBinContent(j, 1.)
                sumMCErrors.Draw("PE2 same")
                sumMCErrors.SetFillStyle(3001);
                sumMCErrors.SetFillColor(ROOT.kGray);
                sumMCErrors.SetMarkerStyle(1);
                sumMCErrors.SetMarkerColor(ROOT.kGray);
            
            stackPad.cd()

        CMS_lumi.CMS_lumi(ROOT.gPad, 4, 0, 0.05 if doRatio else 0.09)

        doLegend(SignalHists if SignalHists else None, stackableHists if stackableHists else None,
                 All_files['Data']['hist'][i] if 'Data' in All_files.keys() else None, textSize=0.040, columns=2, uncertHist=totaluncert if ShowMCerror else None)
        if any('LogY' in e for e in var) :
            ROOT.gPad.SetLogy()
                    
        canv.SaveAs(pngdire+'/'+var[0]+'.png')
        canv.SaveAs(pdfdire+'/'+var[0]+'.pdf')
        canv.SaveAs(epsdire+'/'+var[0]+'.eps')
        
        tDirectory.WriteObject(canv,"TheCanvas")
        #del canv
        outroot.cd('')
    outroot.Close()
