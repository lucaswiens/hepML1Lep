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

void overly_DNN_Multi()
{

      //TFile *f1=TFile::Open("/nfs/dust/cms/user/amohamed/susy-desy/CMSSW_8_0_28_patch1/src/CMGTools/TTHAnalysis/python/plotter/susy-1lep/RcsDevel/datacards_BaseLine_Cards/limit_scan.root");
      TFile *f1 = TFile::Open("datacards_16_BaseLine/limit_scan.root");
      TGraph *Gr_Exp_NTOP1 =(TGraph*)f1->Get("T1ttttExpectedLimit");
      TH2D *Xsec_hist=(TH2D*)f1->Get("T1ttttObservedExcludedXsec");

      Gr_Exp_NTOP1->GetHistogram()->GetXaxis()->SetTitle("m_{#tilde g} [GeV]");
      Gr_Exp_NTOP1->GetHistogram()->GetYaxis()->SetTitle("m_{#{chi}_{1}^{0}}");
      Gr_Exp_NTOP1->GetHistogram()->GetYaxis()->SetTitleOffset(0.1);

      TFile *f2 = TFile::Open("datacards_16_DNNcorr_MultiClass_param_June3/limit_scan.root");
      TGraph *Gr_Exp_NTOP2 =(TGraph*)f2->Get("T1ttttExpectedLimit");


      Gr_Exp_NTOP2->GetHistogram()->GetXaxis()->SetTitle("m_{g} [GeV]");
      Gr_Exp_NTOP2->GetHistogram()->GetYaxis()->SetTitle("m_{#{chi}_{1}^{0}}");
      Gr_Exp_NTOP2->GetHistogram()->GetYaxis()->SetTitleOffset(0.5);


      Gr_Exp_NTOP2->SetLineColor(6);

      TFile *f3 = TFile::Open("datacards_combined_baseline/limit_scan.root");
      TGraph *Gr_Exp_NTOP3 =(TGraph*)f3->Get("T1ttttExpectedLimit");


      Gr_Exp_NTOP3->GetHistogram()->GetXaxis()->SetTitle("m_{g} [GeV]");
      Gr_Exp_NTOP3->GetHistogram()->GetYaxis()->SetTitle("m_{#{chi}_{1}^{0}}");
      Gr_Exp_NTOP3->GetHistogram()->GetYaxis()->SetTitleOffset(0.5);


      Gr_Exp_NTOP3->SetLineColor(4);
      
      /*TFile *f4 = TFile::Open("datacards_16_DNN_MultiClass_10signalClasses_1234567/limit_scan.root");
      TGraph *Gr_Exp_NTOP4 =(TGraph*)f4->Get("T1ttttExpectedLimit");


      Gr_Exp_NTOP4->GetHistogram()->GetXaxis()->SetTitle("m_{g} [GeV]");
      Gr_Exp_NTOP4->GetHistogram()->GetYaxis()->SetTitle("m_{#{chi}_{1}^{0}}");
      Gr_Exp_NTOP4->GetHistogram()->GetYaxis()->SetTitleOffset(0.5);


      Gr_Exp_NTOP4->SetLineColor(4);


      
      TFile *f5=TFile::Open("datacards_16_BaseLine_nT/limit_scan.root");
      TGraph *Gr_Exp_NTOP5 =(TGraph*)f5->Get("T1ttttExpectedLimit");


      Gr_Exp_NTOP5->GetHistogram()->GetXaxis()->SetTitle("m_{g} [GeV]");
      Gr_Exp_NTOP5->GetHistogram()->GetYaxis()->SetTitle("m_{#{chi}_{1}^{0}}");
      Gr_Exp_NTOP5->GetHistogram()->GetYaxis()->SetTitleOffset(0.5);


      Gr_Exp_NTOP5->SetLineColor(1);

      TFile *f6 = TFile::Open("datacards_16_DNN_19bins_0p9_nT/limit_scan.root");
      TGraph *Gr_Exp_NTOP6 = (TGraph *)f6->Get("T1ttttExpectedLimit");

      Gr_Exp_NTOP6->GetHistogram()->GetXaxis()->SetTitle("m_{g} [GeV]");
      Gr_Exp_NTOP6->GetHistogram()->GetYaxis()->SetTitle("m_{#{chi}_{1}^{0}}");
      Gr_Exp_NTOP6->GetHistogram()->GetYaxis()->SetTitleOffset(0.5);

      Gr_Exp_NTOP6->SetLineColor(9);*/

      TCanvas *c11=new TCanvas("c11","c11",10,10,1100,1100);



      TMultiGraph *mg= new TMultiGraph();



      mg->Add(Gr_Exp_NTOP1,"l");
      mg->Add(Gr_Exp_NTOP2,"l");
      //mg->Add(Gr_Exp_NTOP3,"l");
      //mg->Add(Gr_Exp_NTOP4,"l");
      //mg->Add(Gr_Exp_NTOP5,"l");
      //mg->Add(Gr_Exp_NTOP6,"l");

      mg->SetTitle("; m_{#tildeg} [GeV]; m_{#tilde#chi_{1}^{0}} [GeV]");
      //mg->GetYaxis()->SetTitleOffset(1.5);

//      Xsec_hist->Draw("colz sames");
//      c11->Update();
      mg->Draw("ap sames");

///////      mg->GetXaxis()->SetRangeUser(1000,2500);
      //mg->GetXaxis()->SetLimits(1000,2000);
      //mg->GetYaxis()->SetRangeUser(0,1270);
      //mg->Draw("ap sames");
      c11->SetLeftMargin(0.15);
      c11->Update();

      TLegend *leg = new TLegend(0.15,0.25,0.55,0.4);
      leg->SetHeader("Supersymmetric Gluino ");
      leg->AddEntry(Gr_Exp_NTOP1, "Traditional Cut-and-Count analysis", "l");
      leg->AddEntry(Gr_Exp_NTOP2, "Deep Neural Network", "l");
      //leg->AddEntry(Gr_Exp_NTOP3, "Boosted Decision Trees", "l");
      //leg->AddEntry(Gr_Exp_NTOP4, "DNN MultiClass 7 Sig Classes", "l");
      //leg->AddEntry(Gr_Exp_NTOP5, "Baseline with nTop #geq 1", "l");
      //leg->AddEntry(Gr_Exp_NTOP6, "DNN 19 bins with nTop #geq 1", "l");

      leg->Draw();
      c11->SaveAs("Limit_combdPhiMTout_DNN_multiClass_BDT.pdf");

}
