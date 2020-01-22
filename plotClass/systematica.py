import ROOT
import os

class do_syst(object) : 
    def __init__(self,systList = None) : 
        self.input      = input  
        self.systList  = systList

    def append_syst(self,All_files = {},isSignal = False) : 
        ''' This function is to append systematics'''
        for obj in All_files : 
            

