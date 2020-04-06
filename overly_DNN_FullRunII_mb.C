#include "TH1.h"
#include "TH2.h"
#include "TF1.h"
#include "TStyle.h"
#include "TCanvas.h"
#include "TGraph.h"
#include "TLine.h"
#include "TPolyLine.h"
#include "TGraphErrors.h"
#include "TROOT.h"
#include "TApplication.h"
#include "TString.h"
#include "TProfile.h"
#include "TMath.h"
#include "Riostream.h"
#include <iostream>
#include <iomanip>
#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <sstream>
#include <string>
#include <TString.h>
#include "time.h"
#include <ctime>
#include <cstdlib>
#include "TLegend.h"
#include "TTree.h"
#include "TFile.h"
#include "TCut.h"
#include "TString.h"
#include "TLatex.h"
#include "TPaveText.h"



void addText(double x1, double x2, double y1, double y2, TString TEXT, Color_t color, Float_t angle = 0)
{
    TPaveText* T = new TPaveText(x1,y1,x2,y2, "NDC");
    T->SetFillColor(0);
    T->SetFillStyle(0);
    T->SetLineColor(0);
    T->SetTextAlign(22);
    T->SetTextFont(42);
    T->SetTextColor(color);
    TText *text = T->AddText(TEXT);
    text->SetTextAngle(angle);
    text->SetTextAlign(22);
    T->SetTextFont(42);
    T->Draw("same");
    T->SetBorderSize(0);
};


TStyle * createTdrStyle() {
    TStyle * tdrStyle = new TStyle("tdrStyle","Style for P-TDR");

    //// For the canvas:
    tdrStyle->SetCanvasBorderMode(0);
    tdrStyle->SetCanvasColor(kWhite);
    tdrStyle->SetCanvasDefH(600); //Height of canvas
    tdrStyle->SetCanvasDefW(600); //Width of canvas
    tdrStyle->SetCanvasDefX(0);   //POsition on screen
    tdrStyle->SetCanvasDefY(0);

    // For the Pad:
    tdrStyle->SetPadBorderMode(0);
    // tdrStyle->SetPadBorderSize(Width_t size = 1);
    tdrStyle->SetPadColor(kWhite);
    //tdrStyle->SetPadGridX(1);
    //tdrStyle->SetPadGridY(1);
    tdrStyle->SetGridColor(0);
    tdrStyle->SetGridStyle(3);
    tdrStyle->SetGridWidth(1);

    // For the frame:
    tdrStyle->SetFrameBorderMode(0);
    tdrStyle->SetFrameBorderSize(1);
    tdrStyle->SetFrameFillColor(0);
    tdrStyle->SetFrameFillStyle(0);
    tdrStyle->SetFrameLineColor(1);
    tdrStyle->SetFrameLineStyle(1);
    tdrStyle->SetFrameLineWidth(1);

    // For the histo:
    // tdrStyle->SetHistFillColor(1);
    // tdrStyle->SetHistFillStyle(0);
    tdrStyle->SetHistLineColor(1);
    tdrStyle->SetHistLineStyle(0);
    tdrStyle->SetHistLineWidth(1);
    // tdrStyle->SetLegoInnerR(Float_t rad = 0->5);
    // tdrStyle->SetNumberContours(Int_t number = 20);

    tdrStyle->SetEndErrorSize(2);
    //tdrStyle->SetErrorMarker(20);
    tdrStyle->SetErrorX(.5);

    tdrStyle->SetMarkerStyle(20);

    //For the fit/function:
    tdrStyle->SetOptFit(1);
    tdrStyle->SetFitFormat("5.4g");
    tdrStyle->SetFuncColor(2);
    tdrStyle->SetFuncStyle(1);
    tdrStyle->SetFuncWidth(1);

    //For the date:
    tdrStyle->SetOptDate(0);
    // tdrStyle->SetDateX(Float_t x = 0->01);
    // tdrStyle->SetDateY(Float_t y = 0->01);

    // For the statistics box:
    tdrStyle->SetOptFile(0);
    tdrStyle->SetOptStat(0); // To display the mean and RMS:   SetOptStat("mr");
    tdrStyle->SetStatColor(kWhite);
    tdrStyle->SetStatFont(43);
    tdrStyle->SetStatFontSize(0.025);
    tdrStyle->SetStatTextColor(1);
    tdrStyle->SetStatFormat("6.4g");
    tdrStyle->SetStatBorderSize(1);
    tdrStyle->SetStatH(0.1);
    tdrStyle->SetStatW(0.15);


    // Margins:
    tdrStyle->SetPadTopMargin(0.05);
    tdrStyle->SetPadBottomMargin(0.13);
    tdrStyle->SetPadLeftMargin(0.16);
    tdrStyle->SetPadRightMargin(0.05);

    // For the Global title:
    tdrStyle->SetTitleFont(43);
    tdrStyle->SetTitleColor(1);
    tdrStyle->SetTitleTextColor(1);
    tdrStyle->SetTitleFillColor(10);
    tdrStyle->SetTitleFontSize(0.05);

    // For the axis titles:
    tdrStyle->SetTitleFont(42, "XYZ");
    tdrStyle->SetTitleSize(0.05, "XYZ");

    tdrStyle->SetTitleXOffset(0.9);
    tdrStyle->SetTitleYOffset(1.25);

    // For the axis labels:
    tdrStyle->SetLabelColor(1, "XYZ");
    tdrStyle->SetLabelFont(42, "XYZ");
    tdrStyle->SetLabelOffset(0.007, "XYZ");
    tdrStyle->SetLabelSize(0.04, "XYZ");

    // For the axis:
    tdrStyle->SetAxisColor(1, "XYZ");
    tdrStyle->SetStripDecimals(kTRUE);
    tdrStyle->SetTickLength(0.03, "XYZ");
    tdrStyle->SetNdivisions(510, "XYZ");
    tdrStyle->SetPadTickX(1);  // To get tick marks on the opposite side of the frame
    tdrStyle->SetPadTickY(1);

    // Change for log plots:
    tdrStyle->SetOptLogx(0);
    tdrStyle->SetOptLogy(0);
    tdrStyle->SetOptLogz(0);


    tdrStyle->cd();
    return tdrStyle;
}

void applyStyleToGraph(TGraph * h_g1){
    h_g1->SetLineWidth(4);
    h_g1->SetMarkerStyle(20);
    h_g1->SetLineStyle(1);
    h_g1->SetMarkerSize(0.8);
    h_g1->SetMarkerColor(2);
    h_g1->SetLineColor(2);
}



void overly_DNN_FullRunII_mb()
{


      TFile *f1 = TFile::Open("datacards_161718_syst_1bin/datacards/limit_scan.root");//testLimits_alpha_nT/datacards/limit_scan.root");
      TGraph *Gr_Exp_NTOP1 =(TGraph*)f1->Get("T1ttttExpectedLimit");
    
      TFile *f2 = TFile::Open("datacards_161718_syst_6bins/datacards/limit_scan.root");//testLimits_alpha_nT/datacards/limit_scan.root");
      TGraph *Gr_Exp_NTOP2 =(TGraph*)f2->Get("T1ttttExpectedLimit");
    
      TFile *f3 = TFile::Open("datacards_161718_syst_1SigCla_1bin/datacards/limit_scan.root");//testLimits_alpha_nT/datacards/limit_scan.root");
      TGraph *Gr_Exp_NTOP3 =(TGraph*)f3->Get("T1ttttExpectedLimit");

      TFile *f4 = TFile::Open("datacards_161718_syst_1SigCla_6bins/datacards/limit_scan.root");//testLimits_alpha_nT/datacards/limit_scan.root");
      TGraph *Gr_Exp_NTOP4 =(TGraph*)f4->Get("T1ttttExpectedLimit");


      Gr_Exp_NTOP2->SetLineColor(6);
      Gr_Exp_NTOP3->SetLineColor(1);
      Gr_Exp_NTOP4->SetLineColor(3);

      TStyle * TDR = createTdrStyle();
      TDR->cd();

      TCanvas *c11=new TCanvas("c11","c11",10,10,1100,1100);

      TMultiGraph *mg= new TMultiGraph();



      mg->Add(Gr_Exp_NTOP1,"l");
      mg->Add(Gr_Exp_NTOP2,"l");
      mg->Add(Gr_Exp_NTOP3,"l");
      mg->Add(Gr_Exp_NTOP4,"l");



      mg->SetTitle("; m_{#tildeg} [GeV]; m_{#tilde#chi_{1}^{0}} [GeV]");
      mg->Draw("ap sames");

      c11->SetLeftMargin(0.15);
      c11->Update();

      TLegend *leg = new TLegend(0.25,0.25,0.85,0.6);
      leg->SetFillStyle(0);
      leg->SetBorderSize(0);
      leg->SetHeader("T1tttt NLO+NLL exclusion");
      leg->AddEntry(Gr_Exp_NTOP1, "expected limit param. 1 bin from 0.997", "l");
      leg->AddEntry(Gr_Exp_NTOP2, "expected limit param. 6 bin from 0.9", "l");
      leg->AddEntry(Gr_Exp_NTOP3, "expected limit non-param 1 bin from 0.999 ", "l");
      leg->AddEntry(Gr_Exp_NTOP4, "expected limit non-param 6 bins from 0.9", "l");

      leg->Draw();
      
      addText(0.8-0.15,0.995-0.15,0.95,0.996,"137.54 fb^{-1} (13 TeV)",kBlack);
      addText(0.19,0.39,0.86,0.916,"#bf{CMS} #it{Preliminary}",kBlack);

      c11->SaveAs("Limit_param_vs_nonparam_mb.png");

}
