#!/usr/bin/env python
import argparse
import os

def appendW(infile,outdir) : 

    file_in = ROOT.TFile(infile, "READ")
    tree_in = file_in.Get("sf/t")
    file_out = ROOT.TFile(os.path.join(outdir,infile.split("/")[-1]), "RECREATE")
    file_out.mkdir('sf')
    file_out.cd('sf')
    #tree_out = file_out.Get("sf/t")
    ISREWK_val = array.array('f', [0])
    ISREWKDY_val = array.array('f', [0])

    tree_out = tree_in.CopyTree("")

    ISREWK  = tree_out.Branch('EWK_ISR', ISREWK_val, 'EWK_ISR/F')
    ISREWK_DY  = tree_out.Branch('EWKDY_ISR', ISREWKDY_val, 'EWKDY_ISR/F')
    
    t_start = time.time()

    #print prediction.size
    ISRweights_DY  = {0: 1, 1: 0.988, 2: 1.0, 3: 1.117, 4: 1.379, 5: 1.5, 6: 2.262}
    ISRweights = { 0: 1, 1 : 0.988, 2 : 0.999, 3 : 1.103, 4 : 1.293, 5 : 1.339, 6 : 1.603}
    for i_ev in range(tree_out.GetEntries()):
        #print i_ev
        if i_ev % 10000 == 0:
            print ('Event', i_ev,"/",tree_out.GetEntries())
            t_current = time.time()
            print ('Time', t_current - t_start)
            t_start = t_current
        #tree_out.GetEntry(i_ev)
        tree_out.GetEntry(i_ev)
        nISR = tree_out.nJets30Clean
        nISRforWeights = int(nISR)
        if nISR > 6:
            nISRforWeights = 6
        C_ISR = 1.001
        C_ISRDY =0.9997
        ISREWK_val[0] = C_ISR * ISRweights[nISRforWeights]
        ISREWK.Fill()
        ISREWKDY_val[0] = C_ISRDY * ISRweights_DY[nISRforWeights]
        ISREWK_DY.Fill()
    file_in.Close()
    #file_out.mkdir('sf')
    #file_out.cd('sf')
    #file_out.Delete("t;1")
    #file_out.Delete("sf/t;1")
    tree_out.Write("t",ROOT.TObject.kOverwrite)
    file_out.Close()

        
def find_all_matching(substring, path):
    result = []
    for root, dirs, files in os.walk(path):
        for thisfile in files:
            if substring in thisfile:
                result.append(os.path.join(root, thisfile ))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evaluate DNN with scikit-learn')
    parser.add_argument('--indir', help='List of datasets to process',default=None, metavar='indir')
    parser.add_argument('--outdir', help='output directory',default=None, metavar='outdir')
    parser.add_argument('--infile', help='infile to process',default=None, metavar='infile')
    parser.add_argument('--exec', help="wight directory", default='./batch/appendW_exec.sh', metavar='exec')
    parser.add_argument('--batchMode','-b', help='Batch mode.',default=False, action='store_true')

    args = parser.parse_args()    
    wdir = os.getcwd()
    
    if not args.batchMode and args.infile: 
        import ROOT
        import time
        import array
        import operator
        
        outdir = args.outdir
        if not os.path.exists(outdir):
            os.makedirs(outdir) 
        
        appendW(args.infile,outdir)

    else : 
        outdir = os.path.join(args.outdir,os.path.basename(os.path.normpath(args.indir)))
        if not os.path.exists(outdir):
            os.makedirs(outdir) 

        logdir = outdir+'/Logs' 
        if not os.path.exists(logdir):
            os.makedirs(logdir) 
        import htcondor    
        schedd = htcondor.Schedd()  
        sub = htcondor.Submit("")

        Filenamelist = find_all_matching(".root",args.indir) 
        #print (Filenamelist)

        sub["executable"]               = args.exec
        sub["universe"]                 = "vanilla"
        sub["should_transfer_files"]    = "YES"
        sub["log"]                      = "{}/job_$(Cluster)_$(Process).log".format(logdir)
        sub["output"]                   = "{}/job_$(Cluster)_$(Process).out".format(logdir)
        sub["error"]                    = "{}/job_$(Cluster)_$(Process).err".format(logdir)
        sub["when_to_transfer_output"]  = "ON_EXIT"

        while(True):
            try: 
                with schedd.transaction() as txn:
                    for fc in Filenamelist : 
                        print(fc)
                        sub["arguments"] = " ".join([fc,wdir,outdir])
                        sub.queue(txn)
                    print ("Submit jobs for the batch system")
                break
            except: 
                pass



        
