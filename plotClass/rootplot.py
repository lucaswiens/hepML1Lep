import ROOT
import os

def find_all_matching(substring, path):
    result = []
    for root, dirs, files in os.walk(path):
        for thisfile in files:
            if substring in thisfile:
                result.append(os.path.join(root, thisfile ))
    return result

class rootplot(object) : 
    def __init__(self,input,outdir,All_files = {}) : 
        self.input      = input  
        self.outdir     = outdir 
        self.rootList   = find_all_matching('.root',self.input)
        self.group      = {}
        self.All_files  = All_files
        if not os.path.exists(self.outdir) : os.makedirs(self.outdir)

        textsample = open(self.outdir+"/sample.txt", "w+")

        for g in self.All_files :
            textsample.write(g+" : "+"\n") 
            textsample.write("{:<20}{:<20}".format(" ",self.All_files[g]['scale'])+"\n")
            for f in self.All_files[g]['files']:
                    for rf in self.rootList:
                        if f in rf : 
                            textsample.write("{:<20}{:<20}".format(" ",rf)+"\n")
                            self.group.setdefault(g,[]).append(rf)
        
    
    def makeChain (self, filesList = [],Tname = "sf/t") : 
        ''' This function takes a group of files and add then to one Tchain
            to get one chain for each background kind'''
        chain = ROOT.TChain(Tname)
        '''# create a list of all the extended samples
        extlist = [e for e in filesList if e.find("_ext") != -1]
        # create a list of all the nominal samples
        nomlist = [e.replace(e[e.find("_ext"):],'.root') for e in extlist if e.replace(e[e.find("_ext"):],'.root') in filesList]
        # drop any redundentcy
        nomlist = list(dict.fromkeys(nomlist))
        # make a list of list of nom + ext samples
        unifiedlist = []
        for x in nomlist : 
            unifiedlist.append([x]+[y for y in extlist if x.replace(".root","_ext") in y ])
        # merge the weights for nom + ext 
        if len(unifiedlist) != 0 : 
            for list_ in unifiedlist : 
                new_sumW = 0
                old_weight = 0
                for file_ in list_ : 
                    f = ROOT.TFile.Open(file_)
                    tree = f.Get('sf/t')
                    tree.GetEntry(0)
                    w = tree.sumOfWeights
                    if not w == old_weight : 
                        new_sumW += w
                    old_weight = w '''
        for f in filesList : 
            chain.Add(f)
        return chain
    def makecutflow(self,Tree = None,cutstring = [], extraCuts=[]) :
        ''' This Function is to apply selection on specific tree''' ## Don't use, not yet ready
        from ROOT import TCut
        
        CUTtext = open(self.outdir+"/cuts.txt", "w+")
        CUTtext.write(str(cutstring)+str(extraCuts)+'\n')
        cutstring = [TCut(x) for x in cutstring or x in extraCuts]
        cut = [cutstring[x].GetTitle() for x in range(len(cutstring))]

        if Tree ==None : 
            print ('no Tree founded please cheack')
            pass  
        else : 
            tt_out = Tree.CopyTree("")
            for i in cut:
                tt_out = tt_out.CopyTree(i)
                print(i,tt_out.GetEntries())
                #del tt_out
            #return tt_out
        pass
    def makecuts(self,Tree = None,cutstring = "",extraCuts = "" ) :
        ''' This Function is to apply selection on specific tree'''
        from ROOT import TCut
        
        CUTtext = open(self.outdir+"/cuts.txt", "w+")
        CUTtext.write(cutstring+extraCuts+'\n')

        cutstring = TCut(cutstring+extraCuts)
        cut = cutstring.GetTitle()

        if Tree ==None : 
            print ('no Tree founded please cheack')
            pass  
        else : 
            tt_out = Tree.CopyTree(cut)
            return tt_out
        pass
    def chain_and_cut (self,filesList,Tname,cutstring ,extraCuts): 
        '''This function is to make TChain and apply selections at the same time'''
        chain = self.makeChain(filesList ,Tname)
        chain = self.makecuts(chain,cutstring,extraCuts)
        return chain
        
    def chain_and_cutflow (self,filesList,Tname,cutstring ,extraCuts): 
        '''This function is to make TChain and apply selections at the same time'''
        chain = self.makeChain(filesList ,Tname)
        chain = self.makecuts(chain,cutstring,extraCuts)
        return chain


