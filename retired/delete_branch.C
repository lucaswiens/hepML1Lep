TFile *input =TFile::Open("evVarFriend_ZZTo4L.root");
TTree *inputtree;
input->GetObject("sf/t",inputtree);
TFile *output = TFile::Open("output.root","RECREATE");
inputtree->SetBranchStatus("1900_100sig",0);
inputtree->SetBranchStatus("1900_100TTDi",0);
inputtree->SetBranchStatus("1900_100TTS",0);
inputtree->SetBranchStatus("1900_100WJ",0);

inputtree->SetBranchStatus("1900_1000sig",0);
inputtree->SetBranchStatus("1900_1000TTDi",0);
inputtree->SetBranchStatus("1900_1000TTS",0);
inputtree->SetBranchStatus("1900_1000WJ",0);

inputtree->SetBranchStatus("2200_100sig",0);
inputtree->SetBranchStatus("2200_100TTDi",0);
inputtree->SetBranchStatus("2200_100TTS",0);
inputtree->SetBranchStatus("2200_100WJ",0);

inputtree->SetBranchStatus("2200_800sig",0);
inputtree->SetBranchStatus("2200_800TTDi",0);
inputtree->SetBranchStatus("2200_800TTS",0);
inputtree->SetBranchStatus("2200_800WJ",0);

inputtree->SetBranchStatus("1500_1000sig",0);
inputtree->SetBranchStatus("1500_1000TTDi",0);
inputtree->SetBranchStatus("1500_1000TTS",0);
inputtree->SetBranchStatus("1500_1000WJ",0);

inputtree->SetBranchStatus("1600_1100sig",0);
inputtree->SetBranchStatus("1600_1100TTDi",0);
inputtree->SetBranchStatus("1600_1100TTS",0);
inputtree->SetBranchStatus("1600_1100WJ",0);

inputtree->SetBranchStatus("1700_1200sig",0);
inputtree->SetBranchStatus("1700_1200TTDi",0);
inputtree->SetBranchStatus("1700_1200TTS",0);
inputtree->SetBranchStatus("1700_1200WJ",0);

inputtree->SetBranchStatus("1800_1300sig",0);
inputtree->SetBranchStatus("1800_1300TTDi",0);
inputtree->SetBranchStatus("1800_1300TTS",0);
inputtree->SetBranchStatus("1800_1300WJ",0);

inputtree->SetBranchStatus("1900_800sig",0);
inputtree->SetBranchStatus("1900_800TTDi",0);
inputtree->SetBranchStatus("1900_800TTS",0);
inputtree->SetBranchStatus("1900_800WJ",0);

inputtree->SetBranchStatus("1500_1200sig",0);
inputtree->SetBranchStatus("1500_1200TTDi",0);
inputtree->SetBranchStatus("1500_1200TTS",0);
inputtree->SetBranchStatus("1500_1200WJ",0);
inputtree->SetBranchStatus("TTS",0);
inputtree->SetBranchStatus("WJ",0);
inputtree->SetBranchStatus("TTDi",0);
inputtree->SetBranchStatus("sig",0);

output->mkdir("sf");
output->cd("sf");
TTree *outputtree = inputtree->CloneTree(-1,"fast");
output->Write("t", TObject::kOverwrite);
delete input; delete output;