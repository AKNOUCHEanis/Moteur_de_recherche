# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 15:58:13 2021

@author: DELL VOSTRO
"""
import utils.porter as porter

class Weighter:
    
    
    def __init__(self,index):
        self.index=index
          
          
    def getIndex(self):
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
    
    
        
    