# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 16:33:42 2021

@author: AKNOUCHE Anis
"""

class Document:
    """ La classe Document sert à stocker les infos pertinentes d'un document (Id,Texte, ...)
    """
    
    def __init__(self):
        self.identifiant=0
        self.texte=""
        
    def setId(self,id):
        self.identifiant=id
        
    def getId(self):
        return self.identifiant
    
    def setTexte(self,texte):
        self.texte=texte
    
    def getTexte(self):
        return self.texte
    
        