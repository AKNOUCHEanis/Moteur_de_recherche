# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 00:40:26 2021

@author: DELL VOSTRO
"""
import numpy as np

class EvalMesure():
    
    def __init__(self):
        pass
    
    def evalQuery(self,liste,query,k=None):
        pass
    
class PrecisionModele(EvalMesure):
    
    def evalQuery(self,liste,query,k):
        
        tp=0  #TruePositif    docs pertinents sélectionnés
        fp=0  #FalsePositif   docs Non pertinents sélectionnés
        tp=len([ id  for id in liste[:k] if id in query.getRelIds() ])
        fp=len([id for id in liste[:k] if id not in query.getRelIds()])
        
        return tp/(tp+fp)
    
class RappelModele(EvalMesure):
    
    def evalQuery(self,liste,query,k):
        
        if len(query.getRelIds())!=0:
            tp=0  #TruePositif    docs pertinents sélectionnés
            fn=0  #FalseNegative  docs pertinents Non sélectionnés
            tp=len([ id  for id in liste[:k] if id in query.getRelIds() ])
            fn=len([ id  for id in query.getRelIds() if id not in liste[:k] ])
            
            return tp/(tp+fn)
        else:
            return 0
    
    
class FMesure(EvalMesure):
    
    def __init__(self,beta):
        super()
        self.beta=beta
    
    def evalQuery(self,liste,query,k):
        #Retourne la F-Mesure
        precision=PrecisionModele()
        p=precision.evalQuery(liste, query,k)
        
        rappel=RappelModele()
        r=rappel.evalQuery(liste, query,k)
        
        if r!=0 and p!=0:
            return (1 + self.beta**2)*( p * r )/( (self.beta**2)*p + r )
        else:
            return 0
        
        
        
class AvgPrecision(EvalMesure):
    
    
    def evalQuery(self,liste,query,k=None):
        N=len(liste) #nombre de documents
        n=0          #nombre de documents pertinents
        score=0
        precision=PrecisionModele()
        
        for k in range(N):
            relevant=0
            if k in query.getRelIds():
                relevant=1
                n+=1
            
            score+=relevant*precision.evalQuery(liste,query,k+1)
        
        if n==0:
            return 0
        else:
            return score/n 
    
class ReciprocalRank(EvalMesure):
      
    
    def evalQuery(self,liste,query,k=None):
        N=len(liste)
        i=0
        bool_=False
      
        while (not bool_ )and (i<N):
            if liste[i] in query.getRelIds():
                bool_=True
            i+=1
            
        return 1/(i)
                
            
class NDCG(EvalMesure):
    
    def evalQuery1(self,liste,query,k):
        
        if len(query.getRelIds())!=0 and len(liste)!=0:
            liste_rel=[ 1 if d in query.getRelIds() else 0 for d in liste[:k]]
            
            dcgk=liste_rel[0]+ np.sum([ x/np.log2(liste_rel.index(x)+1) for x in liste_rel[1:k]])
            
            n_rel=np.sum(liste_rel)
            idcgk=0
        
            for i in range(2,n_rel+1):
                idcgk+=1/np.log2(i)
                
            print("\n 1- ",dcgk/(idcgk+1))    
            return dcgk/(idcgk+1)
        else:
            print("\n 2- 0")
            return 0
        
    def evalQuery(self, liste, query,k):

        pertinent = query.getRelIds()
        
        if liste[0] in pertinent:
            dcg=1 
        else :
            dcg=0  
        idcg=0

        for i in range(1,len(liste)):
            if liste[i] in pertinent: 
                dcg+=1/np.log2(i+1)
            idcg+=1/np.log2(i+1)

        return dcg/(idcg+1)    
        
        
        
        
        