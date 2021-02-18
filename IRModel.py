# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 01:14:05 2021

@author: DELL VOSTRO
"""
import copy
import utils.porter as porter
import numpy as np

class IRModel:
    
    def __init__(self,index):
        self.index=index
        
        
    def getScores(self,query):
        """Retourne le score des documents pour une requete"""
        pass
    
    def getRanking(self,query):
        """Retourne une liste de couple(document-score) ordonnés par score décroissant"""
        score_doc=self.getScores(query)
        return sorted(score_doc.items(), key=lambda x: x[1],reverse=True)
    
    def getWeighter(self):
        pass

class Vectoriel(IRModel):
    
    def __init__(self, Index, Weighter, normalized):
        super().__init__(Index)
        self.Weighter=Weighter
        self.normalized=normalized
     
    def getWeighter(self):
        return self.Weighter
    
    def getScores(self, query):
        weighter=self.getWeighter()
        words=query.lower().split()
        
        self.norm_doc={} #Les normes des documents
        
        words_stem=[]
        
        for w in words:
            words_stem.append(porter.stem(w))
            
            
        if(self.normalized): #Methode Cosinus
            docs=weighter.getWeightsForQuery(query)
            keysDocs=docs.keys()
            
            docsScores={}
            for k in keysDocs:
                score=0
                weighterDoc=weighter.getWeightsForDoc(k)
                for stem in words_stem:
                    if stem in docs[k].keys():
                        score+=docs[k][stem]*weighterDoc[stem]
                        
                norm_vect1=np.linalg.norm(np.array(list(docs[k].values())),ord=2)
                if k in self.norm_doc.keys():
                    norm_vect2=self.norm_doc[k]
                else:
                    norm_vect2=np.linalg.norm(np.array(list(weighterDoc.values())),ord=2)
                    self.norm_doc[k]=norm_vect2
                
                docsScores[k]=score/(norm_vect1+norm_vect2)
            
            
            
        else: #Produit scalaire
            docs=weighter.getWeightsForQuery(query)
            keysDocs=docs.keys()
            
            docsScores={}
            for k in keysDocs:
                score=0
                weighterDoc=weighter.getWeightsForDoc(k)
                for stem in words_stem:
                    if stem in docs[k].keys():
                        score+=docs[k][stem]*weighterDoc[stem]
                
                docsScores[k]=score
                
        return docsScores
   

           
                
            
                      
    
