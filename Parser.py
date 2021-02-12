# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 16:50:48 2021

@author: DELL VOSTRO
"""
import Document
import re

class Parser:
    
    
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
                doc=Document.Document()
                doc.setId(key)
                i+=1
                while ".T" not in lignes[i]:
                    i+=1
                i+=1
                while  i<length and "." not in lignes[i] :
                    value+=lignes[i]
                    i+=1
                doc.setTexte(value[:-1])
                collection[key]=doc
            else:
                i+=1
        
        file.close()
    
        return collection
    
   
    def buildDocumentCollectionRegex(self,chemin_doc):
    
        collection={}
        file= open(chemin_doc)
        doc=file.read()
        file.close()
        
        docs=doc.split(".I")
    
        for d in range(1,len(docs)):
            doc=Document.Document()
            
            id=re.search(r'(\d*|$)',docs[d][1:])
            value=re.search(r'\.T(.*?)\.',docs[d], re.DOTALL)
            
            doc.setId(id.group(0))
            
            if value is not None :
                
                doc.setTexte(value.group(1).replace("\n",' '))
            else:
                doc.setTexte("")
                
            collection[id.group(0)]=doc
            
                
        return collection

    
    