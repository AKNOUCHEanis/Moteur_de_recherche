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
import copy

class IndexSimpler:
    
    
    
    def normalisation1(self,doc):
        """retourne un dictionnaire de mots et de leurs occurences"""
        words_doc1=doc.lower().split()
        words_stem=[]

        for w in words_doc1:
            words_stem.append(porter.stem(w))
            
        return dict(collections.Counter(words_stem))
    
    def normalisation(self,doc):
        porterStemmer=PorterStemmer()
        return porterStemmer.getTextRepresentation(doc)
    
    def indexation(self,docs):
        """
        Parameters 
        ----------
        docs : TYPE liste de documents 
            DESCRIPTION.

        Clacul l'index tf et l'index inverse tf
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
        self.docs=index.keys()
        self.stems=index_inverse.keys()
        
    def  indexation_tf_idf(self,docs):
        index={}
        index=copy.deepcopy(self.index)
        
        index_inverse={}
        index_inverse=copy.deepcopy(self.index_inverse)
        
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
        try:
            return  copy.deepcopy(self.index[idoc])
        except KeyError:
            print("KeyError: Id du document érroné!")
            

    def getTfIDFsForDoc(self,idoc):
        #idoc id document
        try:
            return copy.deepcopy(self.index_tf_idf[idoc])
        except KeyError:
            print("KeyError: Id du document érroné!")
    
    def getTfsForStem(self,stem):
        try:
            return copy.deepcopy(self.index_inverse[stem])
        except KeyError:
            print("KeyError: Stem introuvable!")
            
    def getTfIDFsForStem(self,stem):
        try:
            return copy.deepcopy(self.index_tf_idf_inverse[stem])
        except KeyError:
            print("KeyError: Stem introuvable!")
    
    def getStrDoc(self,idoc): # Il faut d'abord créer la collection avec buildCollectionSimple
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
        
    def getListDocs(self):
        """retourne une liste de document texte"""
        liste=[]
        keys=self.collection.keys()
        
        for k in keys:
            liste.append(self.collection[k])
                
        return liste
        
    def getIndex(self):
        return copy.deepcopy(self.index)
        
    def getIndexInverse(self):
        return copy.deepcopy(self.index_inverse)
        
    def getIndexTfIdf(self):
        return copy.deepcopy(self.index_tf_idf)
        
    def getIndexTfIdfInverse(self):
        return copy.deepcopy(self.index_tf_idf_inverse)
        
        