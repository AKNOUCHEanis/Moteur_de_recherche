# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 00:40:26 2021

@author: DELL VOSTRO
"""

class EvalMesure():
    
    def __init__(self):
        pass
    
    def evalQuery(self,liste,query):
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
        
        tp=0  #TruePositif    docs pertinents sélectionnés
        fn=0  #FalseNegative  docs pertinents Non sélectionnés
        tp=len([ id  for id in liste[:k] if id in query.getRelIds() ])
        fn=len([ id  for id in query.getRelIds() if id not in liste[:k] ])
        
        return tp/(tp+fn)
    
    
class FMesure(EvalMesure):
    
    def __init__(self,beta):
        super(FMesure,self).__init__()
        self.beta=beta
    
    def evalQuery(self,liste,query,k):
        #Retourne la F-Mesure
        precision=PrecisionModele()
        p=precision.evalQuery(liste, query,k)
        
        rappel=RappelModele()
        r=rappel.evalQuery(liste, query,k)
        
        return (1 + self.beta**2)*( p * r )/( (self.beta**2)*p + r )
        
        
        
      
        
        
        
        
        
        
        
        
        
        