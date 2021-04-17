# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 13:46:30 2021

@author: DELL VOSTRO
"""

class PageRank():
    
    def __init__(self,n,k):
        self.n=n
        self.k=k
    
    def get_docs(self,model,query):
        """
        Parameters
        ----------
        model : un objet IRModel 
        query : un objet Query

        Returns
        -------
        resultats : une liste de n documents pertinents

        """
        scores_docs=model.getRanking(query)
        docs=scores_docs.getkeys()
        if len(docs)<self.n:
            return docs
        else:    
            return docs[:self.n]
        
    
    