# -*- coding: utf-8 -*-
"""
Created on Fri May  7 01:52:39 2021

@author: DELL VOSTRO
"""

from Parser import Parser
from IndexSimpler import IndexSimpler
import Weighter
from QueryParser import QueryParser
from EvalMesure import PrecisionModele, RappelModele, FMesure, NDCG, MAP, AvgPrecision, ReciprocalRank
from IRModel import Vectoriel, ModeleLangue, Okapi
from EvalIRModel import EvalIRModel

parser=Parser()
parser.buildDocCollectionSimple("data\cisi\cisi.txt")


docs=parser.getListDocs()

#creation des index
indexSimpler=IndexSimpler(parser.getCollection())
indexSimpler.indexation()
indexSimpler.indexation_tf_idf()

#chargement des requetes 
queryParser=QueryParser()
queryCollection=queryParser.buildCollectionQuery("data\cisi\cisi.qry","data\cisi\cisi.rel")

query=queryCollection[1]

#-------------------------------- test des mesures d'evaluation-------------
weighter1=Weighter.Weighter1(indexSimpler)

#Les modèles
#Modèle vectoriel
vectoriel=Vectoriel(indexSimpler,weighter1,normalized=True)

#Okapi-BM25
okapi=Okapi(indexSimpler,K1=1.2,B=0.75)

#Modèle de Langue
modeleLangue=ModeleLangue(indexSimpler,lambda_=0.8)


#liste des documents retourné par le modèle vectoriel
listRankingDocs=list(vectoriel.getRanking(query.getText()).keys())

#test de PrecisionModele
precisionModele=PrecisionModele()
print("Precision : ",precisionModele.evalQuery(listRankingDocs[:20], query,k=20 )) #on va se contenter des 20 premiers documents

#testdu RappelModele
rappelModele=RappelModele()
print("Rappel : ",rappelModele.evalQuery(listRankingDocs[:20], query, k=20))

#test FMesure
fmesure=FMesure(beta=1)
print("FMesure : ",fmesure.evalQuery(listRankingDocs[:20], query, k=20))

#test NDCG
ndcg=NDCG()
print("NDCG : ",ndcg.evalQuery(listRankingDocs[:20], query, k=20))

#test MAP
mapMesure=MAP()

listes=[list(vectoriel.getRanking(queryCollection[q].getText()).keys()) for q in list(queryCollection.keys())[:10]]
queries={q:queryCollection[q] for q in list(queryCollection.keys())[:10] }
print("MAP : ",mapMesure.evalQueries(listes, queries))

#test AvgPrecision
avgPrecision=AvgPrecision()
print("AvgPrecision : ",avgPrecision.evalQuery(listRankingDocs[:100], query,k=100))

#test ReciprocalRank
reciprocalRank=ReciprocalRank()
print("Reciprocal Rank :",reciprocalRank.evalQuery(listRankingDocs[:20],query,k=20))

#-----------------------------Evaluation des modèles-----------------------

evalIRModel=EvalIRModel(indexSimpler,weighter1,lambda_=0.8,B=0.75,K1=1.2)
print("Evaluation des Modeles :\n")
evalIRModel.evalModel(queries)


print("Difference significative entre 2 modeles (Vectoriel et Okapi) pour la query id=",query.getId()," :\n",evalIRModel.differenceSignificativeRIModel(vectoriel,okapi, query))


