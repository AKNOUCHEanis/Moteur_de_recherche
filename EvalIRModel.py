# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 03:01:50 2021

@author: DELL VOSTRO
"""
import numpy as np
from EvalMesure import PrecisionModele, RappelModele, FMesure, AvgPrecision, ReciprocalRank, NDCG
from IRModel import Vectoriel, ModeleLangue, Okapi
import scipy.stats as stats

class EvalIRModel:
    
    def __init__(self,index,weighter,lambda_,B,K1):
        self.index=index
        self.weighter=weighter
        self.lambda_=lambda_
        self.B=B
        self.K1=K1
    
    def evalModel(self,queries):
        print("Modele Vectoriel Normalisé :\n")
        vectorielT=Vectoriel(self.index,self.weighter,True)
        listes=[]
        for q in queries:
            listes.append(list(vectorielT.getRanking(q).keys())[20]) #20 documents pertinents
        
        self.evalQueries(listes,queries)
       
        print("Modele Vectoriel Non Normalisé :\n")
        vectorielF=Vectoriel(self.index,self.weighter,False)
        listes=[]
        for q in queries:
            listes.append(list(vectorielF.getRanking(q).keys())[20]) #20 documents pertinents
        
        self.evalQueries(listes,queries)
        
        print("Modele de langue lambda=",self.lambda_," :\n")
        modeleLangue=ModeleLangue(self.index,self.lambda_)
        listes=[]
        for q in queries:
            listes.append(list(modeleLangue.getRanking(q).keys())[20]) #20 documents pertinents
        
        self.evalQueries(listes,queries)
        
        print("Modele Okapi K1=",self.K1," B=",self.B,":\n")
        modeleOkapi=Okapi(self.index,self.K1,self.B)
        listes=[]
        for q in queries:
            listes.append(list(modeleOkapi.getRanking(q).keys())[20]) #20 documents pertinents
        
        self.evalQueries(listes,queries)
        
    
    def evalQueries(self, listes, queries):
        """
        Parameters
        ----------
        queries : List of query
            Contient des queries 
        listes : List of docs Id 
            Contient des ids de documents

        Retourne la moyenne et l'ecart type pour chaque evalution sur toutes les queries
        -------

        """
        precision=PrecisionModele()
        rappel=RappelModele()
        fMesure=FMesure(1)
        avgPrecision=AvgPrecision()
        reciprocalRank=ReciprocalRank()
        ndcg=NDCG()
        
        scorePrecision=[]
        scoreRappel=[]
        scoreFMesure=[]
        scoreAvgPrecision=[]
        scoreReciprocalRank=[]
        scoreNDCG=[]
        
        for i in range(len(queries)):
            
            scorePrecision.append(precision.evalQuery(listes[i], queries[i], len(listes[i])))
            scoreRappel.append(rappel.evalQuery(listes[i], queries[i], len(listes[i])))
            scoreFMesure.append(fMesure.evalQuery(listes[i], queries[i], len(listes[i])))
            scoreAvgPrecision.append(avgPrecision.evalQuery(listes[i], queries[i]))
            scoreReciprocalRank.append(reciprocalRank.evalQuery(listes[i], queries[i]))
            scoreNDCG.append(ndcg.evalQuery(listes[i], queries[i], len(listes[i])))
            
        print("Modele Precision :\n mean: ","%.3f"%np.mean(scorePrecision)," std: ","%.3f"%np.std(scorePrecision))
        print("Modele Rappel :\n mean: ","%.3f"%np.mean(scoreRappel)," std: ","%.3f"%np.std(scoreRappel))
        print("Fmesure :\n mean: ","%.3f"%np.mean(scoreFMesure)," std: ","%.3f"%np.std(scoreFMesure)) 
        print("AvgPrecision :\n mean: ","%.3f"%np.mean(scoreAvgPrecision)," std", "%.3f"%np.std(scoreAvgPrecision))
        print("ReciprocalRank :\n mean: ","%.3f"%np.mean(scoreReciprocalRank)," std: ","%.3f"%np.std(scoreReciprocalRank))
        print("NDCG :\n mean: ","%.3f"%np.mean(scoreNDCG)," std: ","%.3f"%np.std(scoreNDCG))
        
    def differneceSignificative(self,model1,model2,listes,queries):
        """
        Parameters
        ----------
        model1 : modele dérivé de EvalMesure
        model2 : modele dérivé de EvalMesure
        listes : liste de liste de doc id
        queries : Liste de queries

        Returns 
        -------
        bool
            True : si il y a différence significative entre le modele1 et le modele2
            False : Sinon 

        """
        scoreModel1=[]
        scoreModel2=[]
        
        for i in range(len(queries)):
            scoreModel1.append(model1.evalQuery(listes[i],queries[i],len(listes[i])))   
            scoreModel2.append(model2.evalQuery(listes[i],queries[i],len(listes[i])))   
        
        statistic, pvalue=stats.ttest_ind(scoreModel1,scoreModel2)
        
        if pvalue<0.05:
            return True
        else:
            return False
            
        