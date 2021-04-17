# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 13:46:30 2021

@author: DELL VOSTRO
"""

import random

class PageRank():
    
    def __init__(self,model,weighter,n=5,k=3,d=0.85):
        self.n=n
        self.k=k
        self.d=d
        self.model=model
        self.weighter=weighter
    
    def get_scores(self,query, max_iter=100):
        """
        Parameters
        ---------- 
        query : un objet Query

        Returns
        -------
        resultats : une liste de documents avec leur score
        
        """
        scores_docs=self.model.getRanking(query)
        seeds=list(scores_docs.keys())
        graphe=self.initialisationGraphe(seeds[:self.n])
        nbPage=len(graphe.keys())
        
        scores={ idDoc : (1-self.d)/(nbPage) for idDoc in graphe.keys()}
        
        for i in range(max_iter):
            
            for page in graphe.keys():
                
                sum=0
                pageFrom=[]
                for p in graphe.keys():
                    if page in graphe[p]:
                        pageFrom.append(p)
                
                for p in pageFrom:
                    nbOut=len(graphe[p])
                    sum+= scores[p]/nbOut
                
                scores[page]= (1-self.d)/nbPage + self.d*sum
         
        return sorted(scores.items(), key=lambda x: x[1],reverse=True) 
        
        
        
        

    def initialisationGraphe(self, seeds):
        """Initialisation du graphe avec les document contenus dans seeds """
        graphe={}
        
        for page in seeds:
            if page not in graphe.keys():
                graphe[page]=[]
                
            for idDocFrom in self.weighter.index.getHyperLinksFrom(page):
                graphe[page].append(idDocFrom)
                graphe[idDocFrom]=graphe.get(idDocFrom,[])
            
            hyperLinksTo=self.weighter.index.getHyperLinksTo(page)
            
            if  hyperLinksTo != None:
                idDocsTo=self.weighter.index.getHyperLinksTo(page).keys()
                
                for idDoc in random.sample(idDocsTo, min(len(idDocsTo),self.k)):
                    graphe[idDoc]=graphe.get(idDoc,[page])
                
        return graphe
            
        
    
    