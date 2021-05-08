# -*- coding: utf-8 -*-
"""
Created on Fri May  7 03:22:28 2021

@author: DELL VOSTRO
"""



from Parser import Parser
from IndexSimpler import IndexSimpler
import Weighter
from QueryParser import QueryParser
from IRModel import Vectoriel, ModeleLangue, Okapi
from EvalIRModel import OptimIRModel, EvalIRModel
from EvalMesure import PrecisionModele, RappelModele, FMesure, NDCG, MAP, AvgPrecision, ReciprocalRank


parser=Parser()
parser.buildDocCollectionSimple("data\cisi\cisi.txt")


docs=parser.getListDocs()

#creation des index
indexSimpler=IndexSimpler(parser.getCollection())
indexSimpler.indexation()
indexSimpler.indexation_tf_idf()
indexSimpler.indexationHyperLinks()

#chargement des requetes 
queryParser=QueryParser()
queryCollection=queryParser.buildCollectionQuery("data\cisi\cisi.qry","data\cisi\cisi.rel")

query=queryCollection[1]

fichier=open("resultatsML.txt","w")


#---------------------------------Optimisation des modeles------------------
optimIRModel=OptimIRModel()

trainQ, testQ=optimIRModel.splitTrainTest(queryCollection)

#Grid search pour Okapi--------------------------**********************
params_optim=optimIRModel.gridSearch_Okapi(trainQ, queryCollection, indexSimpler)
print("\n Modele Okapi-BM25 valeur optimale de (K1,B) =",params_optim)
fichier.write("Modele Okapi-BM25 valeur optimale de (K1,B) = "+str(params_optim)+"\n")


K1,B=params_optim
okapi=Okapi(indexSimpler,K1,B)
listes=[] #listes des documents retournés par le modèle pour chaque Query

for q in testQ:
    listes.append(list(okapi.getRanking(queryCollection[q].getText()).keys()))
                
mapMesure=MAP()
score=mapMesure.evalQueries(listes,dict((idq,query) for idq, query in queryCollection.items() if int(idq) in testQ))
print("Score Map pour ces valeurs optimales : ",score)
fichier.write("Score Map pour ces valeurs optimales : "+str(score)+" \n")


#CrossVal pour Okapi----------------------------***************************
score=optimIRModel.crossValidation(Okapi(indexSimpler,K1=params_optim[0],B=params_optim[1]),MAP(),queryCollection,3)
print("Score Avec une cross-val :",score)
fichier.write("Score Avec une cross-val : "+str(score)+" \n")


#Grid search pour Le modele de langue
params_optim=optimIRModel.gridSearch_ModeleLangue(trainQ, queryCollection, indexSimpler)
print("\n Modele de Langue valeur optimal de lambda =",params_optim)
fichier.write("\n Modele de Langue valeur optimal de lambda = "+str(params_optim)+"\n")


#------------------
params_optim=0
lambda_=params_optim

modeleLangue=ModeleLangue(indexSimpler,lambda_)

listes=[] #listes de documents retournés par le modèle pour chaque Query

for q in testQ:
    listes.append(list(modeleLangue.getRanking(queryCollection[q].getText()).keys()))

mapMesure=MAP()
      
score=mapMesure.evalQueries(listes, dict((idq,query) for idq, query in queryCollection.items() if int(idq) in testQ))
print("Score Map pour ces valeurs optimales : ",score)
fichier.write("Score Map pour ces valeurs optimales : "+str(score)+"\n")


#CrossVal pour le Modele de langue-------------------************************
score=optimIRModel.crossValidation(ModeleLangue(indexSimpler,lambda_=params_optim),MAP(),queryCollection,3)
print("Score Avec une cross-val :",score)
fichier.write("Score Avec une cross-val : "+str(score)+"\n")

fichier.close()








