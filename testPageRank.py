# -*- coding: utf-8 -*-
"""
Created on Fri May  7 03:10:04 2021

@author: DELL VOSTRO
"""

from Parser import Parser
from IndexSimpler import IndexSimpler
import Weighter
from QueryParser import QueryParser
from IRModel import Vectoriel, ModeleLangue, Okapi
from PageRank import PageRank

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


weighter1=Weighter.Weighter1(indexSimpler)

vectoriel=Vectoriel(indexSimpler,weighter1,normalized=True)


#------------------------------------test du Page Rank---------------------

pageRank=PageRank(vectoriel,weighter1,n=5,k=3,d=0.85)
listDocs=pageRank.get_scores(query.getText(),max_iter=100)
print("Page rank: liste des documents avec leur score : ",listDocs[:20])





