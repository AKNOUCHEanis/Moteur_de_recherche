# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 01:14:05 2021

@author: DELL VOSTRO
"""

class IRModel:
    
    def __init__(self,index):
        self.index=index
        
        
    def getScoresQuery(self,query):
        """Retourne le score des documents pour une requete"""
        pass
    
    def getRanking(self,query):
        """Retourne une liste de couple(document-score) ordonnés par score décroissant"""
        pass
    
