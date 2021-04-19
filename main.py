# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 17:02:24 2021

@author: DELL VOSTRO
"""

from Parser import Parser
import IndexSimpler
import Weighter
from IRModel import Vectoriel, ModeleLangue, Okapi
from QueryParser import QueryParser
from EvalMesure import PrecisionModele, RappelModele, FMesure, NDCG
from QueryParser import QueryParser
from EvalIRModel import EvalIRModel
from PageRank import PageRank

"""
document1="the new home has been saled on top forecasts"
document2="the home sales rise in july"
document3="there is an increase in home sales in july"
document4="july encounter a new home sales rise"

docs=[document1, document2, document3, document4]
parser=Parser.Parser()

collection=parser.buildDocCollectionSimple("data\cacm\cacm.txt")
print(collection["1"].getTexte())
"""


parser=Parser()
parser.buildDocCollectionSimple("data\cisi\cisi.txt")
docs=parser.getListDocs()

#Test PageRank

indexSimpler=IndexSimpler.IndexSimpler(parser.getCollection())
indexSimpler.indexationHyperLinks()
indexSimpler.indexation()
indexSimpler.indexation_tf_idf()

queryParser=QueryParser()
queryCollection=queryParser.buildCollectionQuery("data\cisi\cisi.qry","data\cisi\cisi.rel")

weighter=Weighter.Weighter1(indexSimpler)

"""
model=Vectoriel(indexSimpler,weighter,True)

pageRank=PageRank(model,weighter,n=3,k=1)
scores=pageRank.get_scores(queryCollection[1].getText(),max_iter=10)
print(scores)
"""





#Test EvalIRModel
queryParser=QueryParser()
queryCollection=queryParser.buildCollectionQuery("data\cisi\cisi.qry","data\cisi\cisi.rel")
#print(type(queryCollection))
evalIRModel=EvalIRModel(indexSimpler,weighter,lambda_=0.8,K1=1.2,B=0.75)
evalIRModel.evalModel(queryCollection)






"""
indexSimpler=IndexSimpler.IndexSimpler(parser.getCollection())
indexSimpler.indexationHyperLinks()

print(docs[0].getLinks())
print(indexSimpler.getHyperLinksFrom(1558))
print(indexSimpler.getHyperLinksTo(1))
"""
#indexSimpler.indexation()
#indexSimpler.indexation_tf_idf()

#print(indexSimpler.getTfsForStem("system"))
#print(indexSimpler.getTfsForDoc(126))


#weighter=Weighter.Weighter2(indexSimpler)
#print("Test getWeightsFOrStem\n",weighter.getWeightsForStem("grow"))
#print("\n Test getWeightsForDoc \n",weighter.getWeightsForDoc(28))
#print("\n Test getWeightsForQuery \n",weighter.getWeightsForQuery("grow sale for house")[28])


#vectorielModel=Vectoriel(indexSimpler, weighter,True)
#print(vectorielModel.getRanking("sales")[:10])
#print(indexSimpler.getTfsForStem("sale"))

#modeleLangue=ModeleLangue(indexSimpler,0.8)
#print("First Docs retournés par le modele de langue \n",modeleLangue.getRanking("sales")[:10])
#print(indexSimpler.getTfsForStem("sale"))

#okapi=Okapi(indexSimpler,1.2,0.75)
#print("\n First Docs retournés par le modele Okapi BM25 \n",okapi.getRanking("sales")[:10])


#queryParser=QueryParser()
#collectionQuery=queryParser.buildCollectionQuery("data\cisi\cisi.qry", "data\cisi\cisi.rel")
#print(collectionQuery[1].getRelIds())





#modele=FMesure(1)
#print(modele.evalQuery(collectionQuery[1].getRelIds(), collectionQuery[1],30))


























