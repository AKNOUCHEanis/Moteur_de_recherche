# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 21:47:37 2021

@author: DELL VOSTRO
"""

class Query():
    
    def __init__(self,id,text,listIds):
        self.id=id
        self.text=text
        self.listIds=listIds  #id des documents pertinents pour cette requete
        
    def getText(self):
        return self.text
    
    def getId(self):
        return self.id
    
    def getRelIds(self):
        return self.listIds
    
    def addRelId(self,id):
        #Add relevant id document
        self.listIds.append(id)