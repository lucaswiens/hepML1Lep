#!/usr/bin/env python
from ROOT import TFile, TTree, TList
from array import array
import argparse
import os 

def find_all_matching(substring, path):
    result = []
    for root, dirs, files in os.walk(path):
        for thisfile in files:
            if substring in thisfile:
                result.append(os.path.join(root, thisfile))
    return result

#Run on its own for testing
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runs a NAF batch system for nanoAOD', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--indir', help='List of datasets to process',default=None, metavar='indir')
    parser.add_argument('--infile', help='infile to process',default=None, metavar='infile')
    parser.add_argument('--scores', help='path to score dir where you have one dir for each mass score with name mGo_mLSP',default=None, metavar='scores')
    parser.add_argument('--outdir', help='output directory', metavar='outdir')
    parser.add_argument('--exec', help="wight directory", default='./batch/merger_exec.sh', metavar='exec')
    parser.add_argument('--batchMode','-b', help='Batch mode.',default=False, action='store_true')

    args = parser.parse_args()
    dirname = args.indir
    outdir = args.outdir
    execu = args.exec
    logdir = outdir+'/Logs' 
    batch = args.batchMode
    infile = args.infile
    scores = os.listdir(args.scores)
    scores = [os.path.join(args.scores,x) for x in scores if not x.startswith('.')]
    #ana = args.ana
    wdir = os.getcwd()
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if not os.path.exists(logdir):
        os.makedirs(logdir) 

    if ((batch) and (dirname is not None)): 
        import htcondor
        schedd = htcondor.Schedd()  

        Filenamelist = find_all_matching(".root",dirname) 
        print (Filenamelist)
        for fc in Filenamelist : 
            ##Condor configuration
            submit_parameters = { 
                "executable"                : execu,
                "arguments"                 : " ".join([fc,outdir,wdir,args.scores]),
                "universe"                  : "vanilla",
                "should_transfer_files"     : "YES",
                "log"                       : "{}/job_$(Cluster)_$(Process).log".format(logdir),
                "output"                    : "{}/job_$(Cluster)_$(Process).out".format(logdir),
                "error"                     : "{}/job_$(Cluster)_$(Process).err".format(logdir),
                "when_to_transfer_output"   : "ON_EXIT",
                'Requirements'              : 'OpSysAndVer == "CentOS7"',

             }
            job = htcondor.Submit(submit_parameters)
            with schedd.transaction() as txn:
                    job.queue(txn)
                    print ("Submit job for file {}".format(fc))
    if not batch : 
        source_file = TFile.Open(infile)
        source_tree = source_file.Get("sf/t")
        second_file_list = [str(x)+"/"+str(infile).split("/")[-1] for x in scores ]
        for sco in second_file_list:
            if 'Logs' in sco : continue 
            print(sco)
            if '1500_1000' in sco :
                second_file1500_1000 = TFile.Open(sco)
                second_tree1500_1000 = second_file1500_1000.Get("sf/t")             
            if '1500_1200' in sco :
                second_file1500_1200 = TFile.Open(sco)
                second_tree1500_1200 = second_file1500_1200.Get("sf/t") 
            if '1600_1100' in sco :
                second_file1600_1100 = TFile.Open(sco)
                second_tree1600_1100 = second_file1600_1100.Get("sf/t") 
            if '1700_1200' in sco :
                second_file1700_1200 = TFile.Open(sco)
                second_tree1700_1200 = second_file1700_1200.Get("sf/t") 
            if '1800_1300' in sco :
                second_file1800_1300 = TFile.Open(sco)
                second_tree1800_1300 = second_file1800_1300.Get("sf/t") 
            if '1900_100' in sco :
                second_file1900_100  = TFile.Open(sco)
                second_tree1900_100  = second_file1900_100.Get("sf/t") 
            if '1900_1000' in sco :
                second_file1900_1000 = TFile.Open(sco)
                second_tree1900_1000 = second_file1900_1000.Get("sf/t") 
            if '1900_800' in sco:
                second_file1900_800  = TFile.Open(sco)
                second_tree1900_800  = second_file1900_800.Get("sf/t")
            if '2200_100' in sco:
                second_file2200_100  = TFile.Open(sco)
                second_tree2200_100  = second_file2200_100.Get("sf/t")
            if '2200_800' in sco:
                second_file2200_800  = TFile.Open(sco)
                second_tree2200_800  = second_file2200_800.Get("sf/t")

        target_file = TFile(outdir+"/"+str(infile).split("/")[-1],"recreate")
        
        source_tree.SetBranchStatus("*", 1)

        target_dire = target_file.mkdir("sf")
        target_dire.cd()

        target_tree =  source_tree.CloneTree(0)

        #&& (1500_1200sig >1500_1200TTDi ) && (1500_1200sig >1500_1200TTS) && (1500_1200sig >1500_1200WJ)

        v1500_1000sig  = array( 'd', [ -999 ] )
        v1500_1000TTS  = array( 'd', [ -999 ] )
        v1500_1000TTDi = array( 'd', [ -999 ] )
        v1500_1000WJ   = array( 'd', [ -999 ] )
        b1500_1000sig  = target_tree.Branch( "1500_1000sig"  , v1500_1000sig   ,"1500_1000sig/D" )
        b1500_1000TTS  = target_tree.Branch( "1500_1000TTS"  , v1500_1000TTS   ,"1500_1000TTS/D" )
        b1500_1000TTDi = target_tree.Branch( "1500_1000TTDi" , v1500_1000TTDi  ,"1500_1000TTDi/D")
        b1500_1000WJ   = target_tree.Branch( "1500_1000WJ"   , v1500_1000WJ    , "1500_1000WJ/D" )

        v1500_1200sig  = array( 'd', [ -999 ] )
        v1500_1200TTS  = array( 'd', [ -999 ] )
        v1500_1200TTDi = array( 'd', [ -999 ] )
        v1500_1200WJ   = array( 'd', [ -999 ] )
        b1500_1200sig  = target_tree.Branch( "1500_1200sig"  , v1500_1200sig   ,"1500_1200sig/D" )
        b1500_1200TTS  = target_tree.Branch( "1500_1200TTS"  , v1500_1200TTS   ,"1500_1200TTS/D" )
        b1500_1200TTDi = target_tree.Branch( "1500_1200TTDi" , v1500_1200TTDi  ,"1500_1200TTDi/D")
        b1500_1200WJ   = target_tree.Branch( "1500_1200WJ"   , v1500_1200WJ    , "1500_1200WJ/D" )

        v1600_1100sig  = array( 'd', [ -999 ] )
        v1600_1100TTS  = array( 'd', [ -999 ] )
        v1600_1100TTDi = array( 'd', [ -999 ] )
        v1600_1100WJ   = array( 'd', [ -999 ] )
        b1600_1100sig  = target_tree.Branch( "1600_1100sig"  , v1600_1100sig   ,"1600_1100sig/D" )
        b1600_1100TTS  = target_tree.Branch( "1600_1100TTS"  , v1600_1100TTS   ,"1600_1100TTS/D" )
        b1600_1100TTDi = target_tree.Branch( "1600_1100TTDi" , v1600_1100TTDi  ,"1600_1100TTDi/D")
        b1600_1100WJ   = target_tree.Branch( "1600_1100WJ"   , v1600_1100WJ    , "1600_1100WJ/D" )
        
        v1700_1200sig  = array( 'd', [ -999 ] )
        v1700_1200TTS  = array( 'd', [ -999 ] )
        v1700_1200TTDi = array( 'd', [ -999 ] )
        v1700_1200WJ   = array( 'd', [ -999 ] )
        b1700_1200sig  = target_tree.Branch( "1700_1200sig"  , v1700_1200sig   ,"1700_1200sig/D" )
        b1700_1200TTS  = target_tree.Branch( "1700_1200TTS"  , v1700_1200TTS   ,"1700_1200TTS/D" )
        b1700_1200TTDi = target_tree.Branch( "1700_1200TTDi" , v1700_1200TTDi  ,"1700_1200TTDi/D")
        b1700_1200WJ   = target_tree.Branch( "1700_1200WJ"   , v1700_1200WJ    , "1700_1200WJ/D" )

        
        v1800_1300sig  = array( 'd', [ -999 ] )
        v1800_1300TTS  = array( 'd', [ -999 ] )
        v1800_1300TTDi = array( 'd', [ -999 ] )
        v1800_1300WJ   = array( 'd', [ -999 ] )
        b1800_1300sig  = target_tree.Branch( "1800_1300sig"  , v1800_1300sig   ,"1800_1300sig/D" )
        b1800_1300TTS  = target_tree.Branch( "1800_1300TTS"  , v1800_1300TTS   ,"1800_1300TTS/D" )
        b1800_1300TTDi = target_tree.Branch( "1800_1300TTDi" , v1800_1300TTDi  ,"1800_1300TTDi/D")
        b1800_1300WJ   = target_tree.Branch( "1800_1300WJ"   , v1800_1300WJ    , "1800_1300WJ/D" )
        
        v1900_100sig  = array( 'd', [ -999 ] )
        v1900_100TTS  = array( 'd', [ -999 ] )
        v1900_100TTDi = array( 'd', [ -999 ] )
        v1900_100WJ   = array( 'd', [ -999 ] )
        b1900_100sig  = target_tree.Branch( "1900_100sig"  , v1900_100sig   ,"1900_100sig/D" )
        b1900_100TTS  = target_tree.Branch( "1900_100TTS"  , v1900_100TTS   ,"1900_100TTS/D" )
        b1900_100TTDi = target_tree.Branch( "1900_100TTDi" , v1900_100TTDi  ,"1900_100TTDi/D")
        b1900_100WJ   = target_tree.Branch( "1900_100WJ"   , v1900_100WJ    , "1900_100WJ/D" )

        v1900_1000sig  = array( 'd', [ -999 ] )
        v1900_1000TTS  = array( 'd', [ -999 ] )
        v1900_1000TTDi = array( 'd', [ -999 ] )
        v1900_1000WJ   = array( 'd', [ -999 ] )
        b1900_1000sig  = target_tree.Branch( "1900_1000sig"  , v1900_1000sig   ,"1900_1000sig/D" )
        b1900_1000TTS  = target_tree.Branch( "1900_1000TTS"  , v1900_1000TTS   ,"1900_1000TTS/D" )
        b1900_1000TTDi = target_tree.Branch( "1900_1000TTDi" , v1900_1000TTDi  ,"1900_1000TTDi/D")
        b1900_1000WJ   = target_tree.Branch( "1900_1000WJ"   , v1900_1000WJ    , "1900_1000WJ/D" )

        
        v1900_800sig  = array( 'd', [ -999 ] )
        v1900_800TTS  = array( 'd', [ -999 ] )
        v1900_800TTDi = array( 'd', [ -999 ] )
        v1900_800WJ   = array( 'd', [ -999 ] )
        b1900_800sig  = target_tree.Branch( "1900_800sig"  , v1900_800sig   ,"1900_800sig/D" )
        b1900_800TTS  = target_tree.Branch( "1900_800TTS"  , v1900_800TTS   ,"1900_800TTS/D" )
        b1900_800TTDi = target_tree.Branch( "1900_800TTDi" , v1900_800TTDi  ,"1900_800TTDi/D")
        b1900_800WJ   = target_tree.Branch( "1900_800WJ"   , v1900_800WJ    , "1900_800WJ/D" )

        v2200_100sig  = array( 'd', [ -999 ] )
        v2200_100TTS  = array( 'd', [ -999 ] )
        v2200_100TTDi = array( 'd', [ -999 ] )
        v2200_100WJ   = array( 'd', [ -999 ] )
        b2200_100sig  = target_tree.Branch( "2200_100sig"  , v2200_100sig   ,"2200_100sig/D" )
        b2200_100TTS  = target_tree.Branch( "2200_100TTS"  , v2200_100TTS   ,"2200_100TTS/D" )
        b2200_100TTDi = target_tree.Branch( "2200_100TTDi" , v2200_100TTDi  ,"2200_100TTDi/D")
        b2200_100WJ   = target_tree.Branch( "2200_100WJ"   , v2200_100WJ    , "2200_100WJ/D" )

        v2200_800sig  = array( 'd', [ -999 ] )
        v2200_800TTS  = array( 'd', [ -999 ] )
        v2200_800TTDi = array( 'd', [ -999 ] )
        v2200_800WJ   = array( 'd', [ -999 ] )
        b2200_800sig  = target_tree.Branch( "2200_800sig"  , v2200_800sig   ,"2200_800sig/D" )
        b2200_800TTS  = target_tree.Branch( "2200_800TTS"  , v2200_800TTS   ,"2200_800TTS/D" )
        b2200_800TTDi = target_tree.Branch( "2200_800TTDi" , v2200_800TTDi  ,"2200_800TTDi/D")
        b2200_800WJ   = target_tree.Branch( "2200_800WJ"   , v2200_800WJ    , "2200_800WJ/D" )

        for i in range(source_tree.GetEntries()):
            source_tree.GetEntry(i)
            for j in range(second_tree1500_1000.GetEntries()):
                second_tree1500_1000.GetEntry(j) ; second_tree1500_1200.GetEntry(j); second_tree1600_1100.GetEntry(j)
                second_tree1700_1200.GetEntry(j) ; second_tree1800_1300.GetEntry(j); second_tree1900_100.GetEntry(j)
                second_tree1900_1000.GetEntry(j) ; second_tree1900_800.GetEntry(j); second_tree2200_100.GetEntry(j)
                second_tree2200_800.GetEntry(j) ;

                if (source_tree.Run == second_tree1500_1000.Run and  source_tree.Event == second_tree1500_1000.Event and  source_tree.Lumi == second_tree1500_1000.Lumi) : 
                
                    v1500_1000sig[0] = second_tree1500_1000.signal
                    v1500_1000TTS[0] = second_tree1500_1000.TTSemiLep
                    v1500_1000TTDi[0] = second_tree1500_1000.TTDiLep
                    v1500_1000WJ[0] = second_tree1500_1000.WJets

                    b1500_1000sig.Fill()
                    b1500_1000TTS.Fill()
                    b1500_1000TTDi.Fill()
                    b1500_1000WJ.Fill()

                    v1500_1200sig[0] = second_tree1500_1200.signal
                    v1500_1200TTS[0] = second_tree1500_1200.TTSemiLep
                    v1500_1200TTDi[0] = second_tree1500_1200.TTDiLep
                    v1500_1200WJ[0] = second_tree1500_1200.WJets

                    b1500_1200sig.Fill()
                    b1500_1200TTS.Fill()
                    b1500_1200TTDi.Fill()
                    b1500_1200WJ.Fill()

                    v1600_1100sig[0] = second_tree1600_1100.signal
                    v1600_1100TTS[0] = second_tree1600_1100.TTSemiLep
                    v1600_1100TTDi[0] = second_tree1600_1100.TTDiLep
                    v1600_1100WJ[0] = second_tree1600_1100.WJets

                    b1600_1100sig.Fill()
                    b1600_1100TTS.Fill()
                    b1600_1100TTDi.Fill()
                    b1600_1100WJ.Fill()

                    v1700_1200sig[0] = second_tree1700_1200.signal
                    v1700_1200TTS[0] = second_tree1700_1200.TTSemiLep
                    v1700_1200TTDi[0] = second_tree1700_1200.TTDiLep
                    v1700_1200WJ[0] = second_tree1700_1200.WJets

                    b1700_1200sig.Fill()
                    b1700_1200TTS.Fill()
                    b1700_1200TTDi.Fill()
                    b1700_1200WJ.Fill()

                    v1800_1300sig[0] = second_tree1800_1300.signal
                    v1800_1300TTS[0] = second_tree1800_1300.TTSemiLep
                    v1800_1300TTDi[0] = second_tree1800_1300.TTDiLep
                    v1800_1300WJ[0] = second_tree1800_1300.WJets

                    b1800_1300sig.Fill()
                    b1800_1300TTS.Fill()
                    b1800_1300TTDi.Fill()
                    b1800_1300WJ.Fill()

                    v1900_100sig[0] = second_tree1900_100.signal
                    v1900_100TTS[0] = second_tree1900_100.TTSemiLep
                    v1900_100TTDi[0] = second_tree1900_100.TTDiLep
                    v1900_100WJ[0] = second_tree1900_100.WJets

                    b1900_100sig.Fill()
                    b1900_100TTS.Fill()
                    b1900_100TTDi.Fill()
                    b1900_100WJ.Fill()
                    
                    v1900_1000sig[0] = second_tree1900_1000.signal
                    v1900_1000TTS[0] = second_tree1900_1000.TTSemiLep
                    v1900_1000TTDi[0] = second_tree1900_1000.TTDiLep
                    v1900_1000WJ[0] = second_tree1900_1000.WJets

                    b1900_1000sig.Fill()
                    b1900_1000TTS.Fill()
                    b1900_1000TTDi.Fill()
                    b1900_1000WJ.Fill()

                    v1900_800sig[0] = second_tree1900_800.signal
                    v1900_800TTS[0] = second_tree1900_800.TTSemiLep
                    v1900_800TTDi[0] = second_tree1900_800.TTDiLep
                    v1900_800WJ[0] = second_tree1900_800.WJets

                    b1900_800sig.Fill()
                    b1900_800TTS.Fill()
                    b1900_800TTDi.Fill()
                    b1900_800WJ.Fill()

                    v2200_100sig[0] = second_tree2200_100.signal
                    v2200_100TTS[0] = second_tree2200_100.TTSemiLep
                    v2200_100TTDi[0] = second_tree2200_100.TTDiLep
                    v2200_100WJ[0] = second_tree2200_100.WJets

                    b2200_100sig.Fill()
                    b2200_100TTS.Fill()
                    b2200_100TTDi.Fill()
                    b2200_100WJ.Fill()

                    v2200_800sig[0] = second_tree2200_800.signal
                    v2200_800TTS[0] = second_tree2200_800.TTSemiLep
                    v2200_800TTDi[0] = second_tree2200_800.TTDiLep
                    v2200_800WJ[0] = second_tree2200_800.WJets

                    b2200_800sig.Fill()
                    b2200_800TTS.Fill()
                    b2200_800TTDi.Fill()
                    b2200_800WJ.Fill()
                    
                    target_tree.Fill()
                    break
                
        #target_tree.AutoSave()
        target_file.Write()
        target_file.Close()
