# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 17:02:24 2021

@author: DELL VOSTRO
"""

import Parser
import IndexSimpler
import Weighter

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

#print(indexSimpler.getIndex())

weighter4=Weighter.Weighter4(indexSimpler)
print(weighter4.getWeightsForDoc(200))
print(indexSimpler.getTfsForDoc(200))


#print(weighter1.getWeightsForStem("extract"))
#print(weighter4.getWeightsForQuery("je extract loss suis la comme toujours"))



















