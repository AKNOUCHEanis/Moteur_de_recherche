# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 03:01:50 2021

@author: DELL VOSTRO
"""
import numpy as np
from EvalMesure import PrecisionModele, RappelModele, FMesure, AvgPrecision, ReciprocalRank, NDCG, MAP
from IRModel import Vectoriel, ModeleLangue, Okapi
import scipy.stats as stats
from Weighter import Weighter1, Weighter2, Weighter3, Weighter4, Weighter5


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
        for q in queries.keys():
            listes.append(list(vectorielT.getRanking(queries[q].getText()).keys())[:20]) #20 documents pertinents
        
        self.evalQueries(listes,queries)
       
        print("Modele Vectoriel Non Normalisé :\n")
        vectorielF=Vectoriel(self.index,self.weighter,False)
        listes=[]
        for q in queries.keys():
            listes.append(list(vectorielF.getRanking(queries[q].getText()).keys())[:20]) #20 documents pertinents
        
        self.evalQueries(listes,queries)
        
        print("Modele de langue lambda=",self.lambda_," :\n")
        modeleLangue=ModeleLangue(self.index,self.lambda_)
        listes=[]
        for q in queries.keys():
            listes.append(list(modeleLangue.getRanking(queries[q].getText()).keys())[:20]) #20 documents pertinents
        
        self.evalQueries(listes,queries)
        
        print("Modele Okapi K1=",self.K1," B=",self.B,":\n")
        modeleOkapi=Okapi(self.index,self.K1,self.B)
        listes=[]
        for q in queries.keys():
            listes.append(list(modeleOkapi.getRanking(queries[q].getText()).keys())[:20]) #20 documents pertinents
        
        self.evalQueries(listes,queries)
        
    
    def evalQueries(self, listes, queries):
        """
        Parameters
        ----------
        queries : Dict of Query
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
        map_=MAP()
        
        scorePrecision=[]
        scoreRappel=[]
        scoreFMesure=[]
        scoreAvgPrecision=[]
        scoreReciprocalRank=[]
        scoreNDCG=[]
        i=0
        
        for q in queries.keys():
            
            scorePrecision.append(precision.evalQuery(listes[i], queries[q], len(listes[i])))
            scoreRappel.append(rappel.evalQuery(listes[i], queries[q], len(listes[i])))
            scoreFMesure.append(fMesure.evalQuery(listes[i], queries[q], len(listes[i])))
            scoreAvgPrecision.append(avgPrecision.evalQuery(listes[i], queries[q]))
            scoreReciprocalRank.append(reciprocalRank.evalQuery(listes[i], queries[q]))
            scoreNDCG.append(ndcg.evalQuery(listes[i], queries[q], len(listes[i])))
            i+=1
        print("Modele Precision :\n mean: ","%.3f"%np.mean(scorePrecision)," std: ","%.3f"%np.std(scorePrecision))
        print("Modele Rappel :\n mean: ","%.3f"%np.mean(scoreRappel)," std: ","%.3f"%np.std(scoreRappel))
        print("Fmesure :\n mean: ","%.3f"%np.mean(scoreFMesure)," std: ","%.3f"%np.std(scoreFMesure)) 
        print("AvgPrecision :\n mean: ","%.3f"%np.mean(scoreAvgPrecision)," std", "%.3f"%np.std(scoreAvgPrecision))
        print("MAP valeur :\n moyenne ",map_.evalQueries(listes,queries))
        print("ReciprocalRank :\n mean: ","%.3f"%np.mean(scoreReciprocalRank)," std: ","%.3f"%np.std(scoreReciprocalRank))
        print("NDCG :\n mean: ","%.3f"%np.mean(scoreNDCG)," std: ","%.3f"%np.std(scoreNDCG))
        
    def differneceSignificativeEvalMesure(self,model1,model2,listes,queries):
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
        i=0
        for q in queries.keys():
            scoreModel1.append(model1.evalQuery(listes[i],queries[q].getText(),len(listes[i])))   
            scoreModel2.append(model2.evalQuery(listes[i],queries[q].getText(),len(listes[i])))   
            i+=1
        statistic, pvalue=stats.ttest_ind(scoreModel1,scoreModel2)
        
        if pvalue<0.05:
            return True
        else:
            return False

    def differenceSignificativeRIModel(self, model1, model2, query):
        """
        Parameters
        ----------
        model1 : Objet IRModel
        model2 : Objet IRModel
        query : Objet Query

        Returns True : si il y a différence significative entre le modele1 et le modele2
            False : Sinon 
        -------
        """
        listeDocs1=list(model1.getRanking(query.getText()).keys())[:100]
        listeDocs2=list(model2.getRanking(query.getText()).keys())[:100]
        
        statistic, pvalue=stats.ttest_ind(listeDocs1,listeDocs2)
        
        if pvalue<0.05:
            return True
        else:
            return False
            

class OptimIRModel():
    
    
    def splitTrainTest(self, queries):
        list_keys=list(queries.keys())
        n=len(list_keys)
        trainQ=list_keys[:int(0.8*n)]
        testQ=list_keys[int(0.8*n):]
        
        return trainQ, testQ
    
    def gridSearch_Okapi(self,trainQ,queries,index):
        """
        Parameters
        ----------
        trainQ : List of trainning query keys 
        queries : Dict of query
        index : IndexSimpler

        Returns
        -------
        TYPE (K1, B) parametres optimaux pour Okapi-BM25

        """
        mesure=MAP()
        listes=[]
        scores=[]
        params=[]
        j=0
        for K1 in [i/10 for i in range(10)]:
            for B in [i/10 for i in range(10)]:
                okapi=Okapi(index,K1,B)
                listes=[]
                for q in trainQ:
                    listes.append(list(okapi.getRanking(queries[q].getText()).keys())[:100])
                
                
             
                scores.append(mesure.evalQueries(listes, dict((idq,query) for idq, query in queries.items() if int(idq) in trainQ)))
                params.append((K1,B))
                print("score= ",scores[j]," params= ", params[j])
                j+=1
                
        
        return params[np.argmax(scores)]
        
    def gridSearch_ModeleLangue(self, trainQ, queries, index):
        """
        Parameters
        ----------
        trainQ : List of trainning query keys 
        queries : Dict of query
        index : IndexSimpler

        Returns
        -------
        TYPE (lambda_) parametre optimal pour le modele de langue lissage jelinek-mercer

        """
        
        mesure=MAP()
        listes=[]
        scores=[]
        params=[]
        j=0 
        for lambda_ in [i/10 for i in range(10) ]:
            
            modeleLangue=ModeleLangue(index,lambda_)
            for q in trainQ:
                listes.append(list(modeleLangue.getRanking(queries[q].getText()).keys())[:100])
            
            scores.append(mesure.evalQueries(listes, dict((idq,query) for idq, query in queries.items() if int(idq) in trainQ)))
            params.append(lambda_)
            print("score= ",scores[j]," params= ",params[j])
            j+=1
            
        return params[np.argmax(scores)]
    
    
    def crossValidation(self,model,mesure,queries,folds):
        scores=[]
        query_keys=list(queries.keys())
        l=len(query_keys)
        testQ=[]
        trainQ=[]
        listes=[]
        
        for i in range(folds):
            if i==0:
               testQ=query_keys[:int((i+1)*l/folds)]
               trainQ=query_keys[int((i+1)*l/folds):]
            elif i==(folds-1):
                 testQ=query_keys[int(i*l/folds):]
                 trainQ=query_keys[:int(i*l/folds)]
            else:
                 testQ=query_keys[int(i*l/folds):int((i+1)*l/folds)]
                 trainQ=query_keys[:int(i*l/folds)]
                 trainQ.extend(query_keys[int(i*l/folds):])
                
            listes=[]
            for q in trainQ:
                listes.append(list(model.getRanking(queries[q].getText()).keys())[:100])
            
            scores.append(mesure.evalQueries(listes, dict((idq,query) for idq, query in queries.items() if int(idq) in testQ)))
                
        
        return sum(scores)/folds
        
        
     
        