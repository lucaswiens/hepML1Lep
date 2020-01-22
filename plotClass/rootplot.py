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
            for f in self.All_files[g]['files']:
                    for rf in self.rootList:
                        if f in rf : 
                            textsample.write("{:<20}{:<20}".format(" ",rf)+"\n")
                            self.group.setdefault(g,[]).append(rf)
        

    def makeChain (self, filesList = [],Tname = "sf/t") : 
        ''' This function takes a group of files and add then to one Tchain
            to get one chain for each background kind'''
        chain = ROOT.TChain(Tname)
        for f in filesList : 
            chain.Add(f)
        return chain
    def makecutflow(self,Tree = None,cutstring = [], extraCuts=[]) :
        ''' This Function is to apply selection on specific tree'''
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


