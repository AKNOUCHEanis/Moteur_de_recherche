# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 16:01:32 2021

@author: DELL VOSTRO
"""
import utils.porter as porter
from utils.TextRepresenter import PorterStemmer
import collections
import numpy as np
import re

class IndexSimpler:
    
    def normalisation(self,doc):
        """retourne un dictionnaire de mots et de leurs occurences"""
        words_doc1=doc.lower().split()
        words_stem=[]

        for w in words_doc1:
            words_stem.append(porter.stem(w))
    
    
        return dict(collections.Counter(words_stem))
    
    def indexation(self,docs):
        """

        Parameters 
        ----------
        docs : TYPE liste de documents 
            DESCRIPTION.

        Clacul l'index et l'index inverse, l'index tf-idf et l'index tf-idf inverse
        -------
        None.

        """
        
        index=dict()
        index_inverse=dict()
        
        for i in range(len(docs)):
            counter=self.normalisation(docs[i])
            index[i]=counter
            
            for k in index[i].keys():
                if not (k in index_inverse) :
                    index_inverse[k]={}
                    index_inverse[k][i]=counter[k]
                else:
                    index_inverse[k][i]=counter[k]
                
                
   
        self.index=index
        self.index_inverse=index_inverse
        
    def  indexation_tf_idf(self,docs):
        index=self.index
        index_inverse=self.index_inverse
        N=len(docs)
        df={}
        idf={}
        for k in index_inverse.keys():
            df[k]=len(index_inverse[k].keys())
            idf[k]=np.log((1+N)/(1+df[k]))
            
        for  doc in index.keys():
             for k in index[doc].keys():
                 index[doc][k]*=idf[k]
                 
        for k in index_inverse.keys():
             for doc in index_inverse[k].keys():
                 index_inverse[k][doc]*=idf[k]
                 
        self.index_tf_idf=index
        self.index_tf_idf_inverse=index_inverse
        
        
    def getTfsForDoc(self,idoc):
        #idoc id document
        return self.index_inverse[idoc]

    def getTfIDFsForDoc(self,idoc):
        #idoc id document
        return self.index_tf_idf[idoc]
    
    def getTfsForStem(self,stem):
        return self.index_inverse[stem]
    
    def getTfIDFsForStem(self,stem):
        return self.index_tf_idf_inverse[stem]
    
    def getStrDoc(self,idoc):
        return self.collection[idoc]
    
    def buildDocCollectionSimple(self,chemin_doc): 
        file=open(chemin_doc,"r")
        lignes=file.readlines()
        length=len(lignes)
        collection={}
        
        i=0
        
        
        while i<length:
            key=""
            value=""
            if ".I" in lignes[i] :
                key=lignes[i][3:-1]
                print(key)
                i+=1
                while ".T" not in lignes[i]:
                    i+=1
                i+=1
                while  i<length and "." not in lignes[i] :
                    value+=lignes[i]
                    i+=1
                collection[key]=value[:-1]
            else:
                i+=1
        
        file.close()
        self.collection= collection
        
        