# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 01:14:05 2021

@author: DELL VOSTRO
"""

import utils.porter as porter
import numpy as np

class IRModel:
    
    def __init__(self,index):
        self.index=index
        
        
    def getScores(self,query):
        """Retourne le score des documents pour une requete"""
        pass
    
    def getRanking(self,query):
        """Retourne une liste de couple(document-score) ordonnés par score décroissant"""
        score_doc=self.getScores(query)
        return dict(sorted(score_doc.items(), key=lambda x: x[1],reverse=True))
    
    

class Vectoriel(IRModel):
    
    def __init__(self, index, weighter, normalized):
        super().__init__(index)
        self.weighter=weighter
        self.normalized=normalized
     
    def getWeighter(self):
        return self.weighter
    
    def getScores(self, query):
        weighter=self.getWeighter()
        words=query.lower().split()
        
        self.norm_doc={} #Les normes des documents
        
        words_stem=[]
        
        for w in words:
            words_stem.append(porter.stem(w))
            
            
        if(self.normalized): #Methode Cosinus
            docs=weighter.getWeightsForQuery(query)
            keysDocs=docs.keys()
            
            docsScores={}
            for k in keysDocs:
                score=0
                weighterDoc=weighter.getWeightsForDoc(k)
                for stem in words_stem:
                    if stem in docs[k].keys():
                        score+=docs[k][stem]*weighterDoc[stem]
                        
                norm_vect1=np.linalg.norm(np.array(list(docs[k].values())),ord=2)
                if k in self.norm_doc.keys():
                    norm_vect2=self.norm_doc[k]
                else:
                    norm_vect2=np.linalg.norm(np.array(list(weighterDoc.values())),ord=2)
                    self.norm_doc[k]=norm_vect2
                
                docsScores[k]=score/(norm_vect1+norm_vect2)
            
            
            
        else: #Produit scalaire
            docs=weighter.getWeightsForQuery(query)
            keysDocs=docs.keys()
            
            docsScores={}
            for k in keysDocs:
                score=0
                weighterDoc=weighter.getWeightsForDoc(k)
                for stem in words_stem:
                    if stem in docs[k].keys():
                        score+=docs[k][stem]*weighterDoc[stem]
                
                docsScores[k]=score
                
        return docsScores
   

class ModeleLangue(IRModel):
    
    def __init__(self, index, lambda_):
        super().__init__(index)
        self.lambda_=lambda_
        

    def getScores(self, query):
        """

        Parameters
        ----------
        query : String
        
        Returns Les scores des documents sous forme de couple (Doc , Score) dans un dict
                Calcul du score basé sur Le lissage Jelineck-Mercer
        -------
        """
        
        words=query.lower().split()
        words_stem=[]
        
        for w in words:
            words_stem.append(porter.stem(w))
            
        index=self.index.getIndex()
        docs=index.keys()
        docsScores={}
        
        probaCollection={}
        sizeOfCollection=self.index.getCollectionSize()
        
        for t in words_stem:
            probaCollection[t]=sum([doc.get(t,0) for doc in index.values()])/sizeOfCollection
        
        
        for d in docs:
            score=1
            for t in words_stem:
                score*=(1-self.lambda_)*index[d].get(t,0) + self.lambda_*probaCollection[t]
                
            docsScores[d]=score
            
        return docsScores
                
            
class Okapi(IRModel):
    
    def __init__(self,index,K1, B):
        self.index=index
        self.K1=K1
        self.B=B
        
    def getScores(self,query,pertinence=None):
        """ Calcul du score basé sur Okapi-BM25
        """
        
        words=query.lower().split()
        words_stem=[]
        
        
        for w in words:
            words_stem.append(porter.stem(w))
            
        index=self.index.getIndex()
        index_inverse=self.index.getIndexInverse()
        
        idf={t:self.getIdf(t,index,index_inverse,pertinence) for t in words_stem}
        length_docs={doc:sum([int(tf) for tf in index[doc].values()]) for doc in index.keys() }
        
        mean_length_docs=np.mean([int(val) for val in length_docs.values()])
        docs=index.keys()
        
        docsScores={}
        
        for d in docs:
            score=0
            for t in words_stem:
                score+=idf[t]*index[d].get(t,0)/(index[d].get(t,0) +self.K1*(1-self.B+self.B*(length_docs[d]/mean_length_docs)))
                
            docsScores[d]=score     
            
        return docsScores
            
            
            
            
    def getIdf(self,term,index,index_inverse,pertinence=None):
        
        N=len(index.keys())
        if term in index_inverse.keys():
            n=len(index_inverse[term].keys())
        else:
            n=0
        
        if pertinence is None and n!=0 :
            return np.log(N/n)
        elif n==0 :
            return 0
        else:
            r,R=pertinence
            return np.log((r+0.5)*(N-n-R+r+0.5)/((R-r+0.5)*(n-r+0.5)))
        
                          
    def getRanking(self,query,pertinence=None):
        """Retourne une liste de couple(document-score) ordonnés par score décroissant"""
        score_doc=self.getScores(query,pertinence)
        return dict(sorted(score_doc.items(), key=lambda x: x[1],reverse=True))
        
                
            
                      
    
