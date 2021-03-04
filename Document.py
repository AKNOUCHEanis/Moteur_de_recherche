# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 16:33:42 2021

@author: AKNOUCHE Anis
"""

class Document():
    """ La classe Document sert à stocker les infos pertinentes d'un document (Id,Texte, ...)
    """
    
    def __init__(self,id,title="",date="",author="",keywords="",txt="",link=""):

        self.id = id 
        self.title= title
        self.date= date
        self.author= author
        self.keywords= keywords
        self.txt = txt
        self.links= link
        
        
    def getId(self):
        return self.id

    def getText(self):
        return self.txt
     
    def getLinks(self):
        return {i:self.links.count(i) for i in self.links }
        
        
    
        