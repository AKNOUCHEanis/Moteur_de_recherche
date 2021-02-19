# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 15:58:13 2021

@author: DELL VOSTRO
"""
import utils.porter as porter
import collections
import numpy as np

class Weighter:
    
    
    def __init__(self,index):
        """Initialisation, on lui passe un indexSimpler"""
        self.index=index
          
          
    def getIndex(self):
        """Retourn l'index pris en entré"""
        return self.index
        
    def getWeightsForDoc(self,idDoc) :
        """ Retourne les poids des termes pour un document
              dont l’identifiant est idDoc
          """
        pass
      
        
    def getWeightsForStem(self,stem):
        """ Retourne les poids du terme stem pour tous les
              documents qui le contiennent.
        """
        pass
      
        
    def getWeightsForQuery(self,query):
        """ Retourne les poids des termes de la requˆete
        """
        pass
      
      
class Weighter1(Weighter):
    
        
    def getWeightsForDoc(self, idDoc):
        return self.index.getTfsForDoc(idDoc)
    
    def getWeightsForStem(self,stem):
        return self.index.getTfsForStem(stem)
    
    def getWeightsForQuery(self, query):
        indexTf=self.index.getIndex()
        words=query.lower().split()
        
        words_stem=[]
        
        for w in words:
            words_stem.append(porter.stem(w))
            
        resultat=dict()
        terms=[]
        docs=[]
        docs=indexTf.keys()
        for d in docs:
            doc=dict()
            terms=indexTf[d].keys()
            for t in terms:
                if t in words_stem:
                    doc[t]=1
                else:
                    doc[t]=0
            resultat[d]=doc
        return resultat 
    
   
class Weighter2(Weighter):
    
    def getWeightsForDoc(self, idDoc):
        return self.index.getTfsForDoc(idDoc)
    
    def getWeightsForStem(self,stem):
        return self.index.getTfsForStem(stem)
    
    def getWeightsForQuery(self, query):
        
        words=query.lower().split()
        words_stem=[]

        for w in words:
            words_stem.append(porter.stem(w))
            
        counter=dict(collections.Counter(words_stem))
        resultat=dict()
        terms=[]
        
        indexTf=self.index.getIndex()
        docs=[]
        docs=indexTf.keys()
        for d in docs:
            doc=dict()
            terms=indexTf[d].keys()
            for t in terms:
                if t in words_stem:
                    doc[t]=counter[t]
                else:
                    doc[t]=0
            resultat[d]=doc
        return resultat
    

class Weighter3(Weighter):
    
    def getWeightsForDoc(self, idDoc):
        return self.index.getTfsForDoc(idDoc)
    
    def getWeightsForStem(self,stem):
        return self.index.getTfsForStem(stem)
    
    def getWeightsForQuery(self, query):
        indexTf=self.index.getIndex()
        words=query.lower().split()
        
        words_stem=[]
        
        for w in words:
            words_stem.append(porter.stem(w))
            
        resultat=dict()
        terms=[]
        docs=[]
        docs=indexTf.keys()
        
        for d in docs:
            doc=dict()
            terms=indexTf[d].keys()
            for t in terms:
                if t in words_stem:
                    doc[t]=np.log((1+len(docs)/(1+len(self.index.getTfsForStem(t).keys()))))
                else:
                    doc[t]=0
            resultat[d]=doc
        return resultat
        
        
 
class Weighter4(Weighter):
    
    def getWeightsForDoc(self, idDoc):
        weights= self.index.getTfsForDoc(idDoc)
        keys=weights.keys()
        for k in keys:
            weights[k]=1+np.log(weights[k])
            
        return weights
    
    def getWeightsForStem(self,stem):
        weights= self.index.getTfsForStem(stem)
        keys=weights.keys()
        for k in keys:
            weights[k]=1+np.log(weights[k])
            
        return weights
    
    def getWeightsForQuery(self, query):
        indexTf=self.index.getIndex()
        words=query.lower().split()
        
        words_stem=[]
        
        for w in words:
            words_stem.append(porter.stem(w))
            
        resultat=dict()
        terms=[]
        docs=[]
        docs=indexTf.keys()
        
        for d in docs:
            doc=dict()
            terms=indexTf[d].keys()
            for t in terms:
                if t in words_stem:
                    doc[t]=np.log((1+len(docs)/(1+len(self.index.getTfsForStem(t).keys()))))
                else:
                    doc[t]=0
            resultat[d]=doc
        return resultat
        
class Weighter5(Weighter):
    
    def getWeightsForDoc(self, idDoc):
        weights= self.index.getTfsForDoc(idDoc)
        keys=weights.keys()
        
        index=self.index.getIndex()
        indexInverse=self.index.getIndexInverse()
        N=len(index.keys())
        
        resultat={}
        for k in keys:
            resultat[k]=(1+np.log(weights[k]))*np.log((1+N)/(1+len(indexInverse[k].keys())))
            
        return resultat
    
    def getWeightsForStem(self,stem):
        weights= self.index.getTfsForStem(stem)
        keys=weights.keys()
        
        index=self.index.getIndex()
        indexInverse=self.index.getIndexInverse()
        N=len(index.keys())
        
        resultat={}
        for k in keys:
            resultat[k]=(1+np.log(weights[k]))*np.log((1+N)/(1+len(indexInverse[stem].keys())))
            
        return resultat
    
    def getWeightsForQuery(self, query):
        indexTf=self.index.getIndex()
        words=query.lower().split()
        
        words_stem=[]
        
        for w in words:
            words_stem.append(porter.stem(w))
            
        resultat=dict()
        terms=[]
        docs=[]
        docs=indexTf.keys()
        
        for d in docs:
            doc=dict()
            terms=indexTf[d].keys()
            for t in terms:
                if t in words_stem:
                    doc[t]=(1+np.log(indexTf[d][t]))*np.log((1+len(docs)/(1+len(self.index.getTfsForStem(t).keys()))))
                else:
                    doc[t]=0
            resultat[d]=doc
        return resultat
    