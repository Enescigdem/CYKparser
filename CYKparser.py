
from collections import defaultdict
from random import random
import time
import sys
import numpy as np
from numpy import triu
from itertools import product
import random

class Cell():
    def __init__(self):
        self.cellruleset = []
    
    def addToRules(self,ruleitem):
        for item in ruleitem:
            if not item in self.cellruleset:
                self.cellruleset.append(item)

class CYK():
    def __init__(self,folderpath):
        self.cfgrules = self.rules(folderpath)

    def retrieve_words(self):
        grammaticals = set()
        for vals in self.cfgrules.values():
            for val in vals:
                if val in self.cfgrules.keys() or len(val.split())!=1:
                    grammaticals.add(val)

        grammaticals.update(list(self.cfgrules.keys()))
        grammaticals = list(grammaticals)
        
        words = []
        for vals in self.cfgrules.values():
            for val in vals:
                if not val in self.cfgrules.keys() and len(val.split())==1:
                    words.append(val)

        return words

    def get_left(self,right):
        rightvalue = right
        if isinstance(right,list):
            rightvalue = ""
            for token in right: 
                rightvalue+=token+" "

            rightvalue.rstrip(" ") 
        lv = []
        for k,v in self.cfgrules.items():
            if rightvalue in v:
                lv.append(k)
                for kr,vr in self.cfgrules.items():
                    if k in vr:
                        lv.append(kr)
        return lv
    def create_init_matrix(self,test_sentencelist):
        length_sentence = len(test_sentencelist)
        matrix = []
        for y in range(length_sentence):
            m = [Cell() for l in range(length_sentence)]
            for x in range(length_sentence):   
                if x==y:
                    m[x].addToRules(self.get_left(test_sentencelist[x]))
            matrix.append(m)
        triumatrix = triu(matrix,0)
        return triumatrix
    def production(self,ruleset1,ruleset2):
        lst = product(ruleset1,ruleset2)   
        return lst
    def Union(self,lst1, lst2): 
        final_list = list(lst1) + list(lst2) 
        return list(final_list)
    def CYKParser(self,test_sentence):
        test_sentence = test_sentence.rstrip(".")
        test_sentence = test_sentence.rstrip("?")
        test_sentencelist=test_sentence.split()
        lentest = len(test_sentencelist)
        cykmatrix = self.create_init_matrix(test_sentencelist)
        iu1 = np.triu_indices(lentest)
        suits = []
        for i1,i2 in zip(iu1[0],iu1[1]):
            suits.append((i1,i2))
        for k in range(lentest-1):
            i,j = k,k+1     
            x = self.production(cykmatrix[i][i].cellruleset,cykmatrix[i+1][j].cellruleset)
            for ii in list(x):
                tok = ""
                for ij in ii:
                    tok += ij+" " 
                cykmatrix[i][j].addToRules(self.get_left(tok.rstrip(" ")))
        for n in range(2,lentest):
            for k in range(lentest-n):   
                i,j = k,k+n
                x1 = self.production(cykmatrix[i][i].cellruleset,cykmatrix[i+1][j].cellruleset)
                x2 = self.production(cykmatrix[i][i+1].cellruleset,cykmatrix[i+2][j].cellruleset)       
                uni = self.Union(x1,x2)
                for ii in uni:
                    tok = ""
                    for ij in ii:
                        tok += ij+" "         
                    cykmatrix[i][j].addToRules(self.get_left(tok.rstrip()))

        #Uncomment to see cyk table
        '''
        for i in range(lentest):
            for j in range(lentest):
                if (i,j) in suits:
                    print(i,j,cykmatrix[i][j].cellruleset, end ="\t")
                              
            print("\n\t") 
        '''
        
        if 'S' in cykmatrix[0][lentest-1].cellruleset:
            print("Correct")
        else:
            print("Incorrect")
    def rules(self,folderpath):
        grammarfile = open(grammerfilepath,'r')
        unterminaldict = dict()
        
        for line in grammarfile.readlines():
            line = line.rstrip("\n")
            line = line.rstrip(" ")
            line  = line.split("\t")
            if not "#" in line:
                if len(line)==2:
                    line[0]= line[0].rstrip(" ")
                    try:
                        unterminaldict[line[0]].append(line[1])
                    except KeyError:
                        unterminaldict[line[0]] = [line[1]]
        grammarfile.close()
        return unterminaldict

    def randsentence(self,words,outputfilename):
        randsentences = []
        outfile = open(outputfilename,"w")
        for sentence_count in range(20):
            randomsentence = ""
            for l in range(8):
                sentpart = str(random.choice(words))
                if not sentpart in randomsentence.split():
                    randomsentence+=sentpart+" "

            randomsentence.rstrip(" ")
            randsentences.append(randomsentence)
            outfile.write(randomsentence+"\n\n")
        outfile.close()
        return randsentences

grammerfilepath = "cfg.gr"
#Model should be created by giving path of grammar file to use
cykmodel = CYK(grammerfilepath)

test_sentence = "i like every fine old sandwich"
cykmodel.CYKParser(test_sentence)
'''
#### retrieve_words methos gets the words from rules and given to randsentence() method
terminalwords = cykmodel.retrieve_words()
outputfilename = "output.txt"
cykmodel.randsentence(terminalwords,outputfilename)
'''