# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 17:02:24 2021

@author: DELL VOSTRO
"""

import Parser
import IndexSimpler
import Weighter
from IRModel import Vectoriel

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

#collection=parser.buildDocumentCollectionRegex("data\cacm\cacm.txt")
#print(collection["1"].getTexte())


indexSimpler=IndexSimpler.IndexSimpler()
indexSimpler.buildDocCollectionSimple("data\cacm\cacm.txt")
docs=indexSimpler.getListDocs()
indexSimpler.indexation(docs)

weighter1=Weighter.Weighter1(indexSimpler)
tf=indexSimpler.getTfsForDoc(0)
#print("tf \n",tf)

indexSimpler.indexation_tf_idf(docs)
tfIdf=indexSimpler.getTfIDFsForDoc(0)
#print("\n tfIdf \n",tfIdf)

#print(indexSimpler.getIndex())

#print("\n 3 \n",weighter5.getWeightsForStem("report-intern"))

#print("tfidf \n",tfIdf,"\n tf \n",tf,"\n resultat \n")

#print(indexSimpler.getTfsForDoc(200))

#print(weighter1.getWeightsForStem("extract"))
#print(weighter5.getWeightsForQuery("je extract science loss regim suis la comme toujours"))


vectorielModel=Vectoriel(indexSimpler, weighter1,True)
print(vectorielModel.getScores("je extract science loss regim suis la comme toujours"))


















