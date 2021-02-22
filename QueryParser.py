# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 22:14:48 2021

@author: DELL VOSTRO
"""

from Query import Query
import re

class QueryParser():
    
    def __init__(self):
        pass
        
    def buildCollectionQuery(self,chemin_query,chemin_pertinence):
        """
        

        Parameters
        ----------
        chemin_query : chemin vers le fichier contenant les queries
        chemin_pertinence : chemin vers le fichier contenant les pertinences

        Returns
        -------
        collectionQuery : un dictionnaire (id: query)

        """
        fQuery=open(chemin_query,'r')
        lignes=fQuery.readlines()
        
        N=len(lignes)
        text=""
        id=0
        collectionQuery={}
        
        for i in range(N):
            
            if lignes[i].startswith('.I'):
                id=int(lignes[i][3:])
            
            elif lignes[i].startswith('.W'):
                text = lignes[i+1].strip()
                i+=2
                while(i<N and lignes[i].startswith('.')==False):
                    text +=' '+lignes[i].strip()
                    i+=1
                i-=1
            
            collectionQuery[id]=Query(id,text,[])
        fQuery.close()   
        
        fRel=open(chemin_pertinence,'r')
        lignes=fRel.readlines()
        N=len(lignes)
        
        for i in range(N):
            x=re.findall(r'(\d+)',lignes[i])
            idQuery=int(x[0])
            idRel=int(x[1])
            
            collectionQuery[idQuery].addRelId(idRel)
        
        fRel.close()
        
        return collectionQuery
                
            
                