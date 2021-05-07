# -*- coding: utf-8 -*-
"""
Created on Thu May  6 13:41:46 2021

@author: DELL VOSTRO
"""

from Parser import Parser
from IndexSimpler import IndexSimpler
import Weighter
from QueryParser import QueryParser
from IRModel import Vectoriel, ModeleLangue, Okapi

parser=Parser()
parser.buildDocCollectionSimple("data\cisi\cisi.txt")


docs=parser.getListDocs()

#creation des index
indexSimpler=IndexSimpler(parser.getCollection())
indexSimpler.indexation()
indexSimpler.indexation_tf_idf()

#-----------------------------test Query----------------------------------
#chargement des requetes 
queryParser=QueryParser()
queryCollection=queryParser.buildCollectionQuery("data\cisi\cisi.qry","data\cisi\cisi.rel")

#test Query
query=queryCollection[1]
"""
print("Query id= ",query.getId())
print("Query text= \n",query.getText())
print("Query relevant ids :\n",query.getRelIds())
"""

#---------------------------------test Weighters----------------------------
#Weighter1
weighter1=Weighter.Weighter1(indexSimpler)
"""
print("Weighter 1:\n")
print("Weights for doc : ID = 1 :\n",weighter1.getWeightsForDoc(1))
print("Weights for stem : stem = present :\n",weighter1.getWeightsForStem("present"))
print("Weights for query : ID=",queryCollection[1].getId()," :\n", weighter1.getWeightsForQuery(queryCollection[1].getText()))
"""

#Weighter2
weighter2=Weighter.Weighter2(indexSimpler)
"""
print("Weighter 2:\n")
print("Weights for doc : ID = 1 :\n",weighter2.getWeightsForDoc(1))
print("Weights for stem : stem = present :\n",weighter2.getWeightsForStem("present"))
print("Weights for query : ID=",queryCollection[1].getId()," :\n", weighter2.getWeightsForQuery(queryCollection[1].getText()))
"""

#Weighter3
weighter3=Weighter.Weighter3(indexSimpler)
"""
print("Weighter 3:\n")
print("Weights for doc : ID = 1 :\n",weighter3.getWeightsForDoc(1))
print("Weights for stem : stem = present :\n",weighter3.getWeightsForStem("present"))
print("Weights for query : ID=",queryCollection[1].getId()," :\n", weighter3.getWeightsForQuery(queryCollection[1].getText()))
"""
      
#Weighter4
weighter4=Weighter.Weighter4(indexSimpler)
"""
print("Weighter 4:\n")
print("Weights for doc : ID = 1 :\n",weighter4.getWeightsForDoc(1))
print("Weights for stem : stem = present :\n",weighter4.getWeightsForStem("present"))
print("Weights for query : ID=",queryCollection[1].getId()," :\n", weighter4.getWeightsForQuery(queryCollection[1].getText()))
"""

#Weighter5
weighter5=Weighter.Weighter5(indexSimpler)
"""
print("Weighter 5:\n")
print("Weights for doc : ID = 1 :\n",weighter5.getWeightsForDoc(1))
print("Weights for stem : stem = present :\n",weighter5.getWeightsForStem("present"))
print("Weights for query : ID=",queryCollection[1].getId()," :\n", weighter5.getWeightsForQuery(queryCollection[1].getText()))
"""


#----------------------------test des modeles RI---------------------------

#test du modèle vectoriel
vectoriel=Vectoriel(indexSimpler,weighter1,normalized=True)
"""
print("Modele vectoriel :\n")
print("Ranking for query id=",query.getId()," :\n",vectoriel.getRanking(query.getText()))
"""

#test de Okapi-BM25
okapi=Okapi(indexSimpler,K1=1.2,B=0.75)
"""
print("Modele Okapi-BM25 :\n")
print("Ranking for query id=",query.getId()," :\n",okapi.getRanking(query.getText()))
"""

#test du Modèle de Langue
modeleLangue=ModeleLangue(indexSimpler,lambda_=0.8)
"""
print("Modele de Langue :\n")
print("Ranking for query id=",query.getId()," :\n",modeleLangue.getRanking(query.getText()))
"""



   
      
      
      
      