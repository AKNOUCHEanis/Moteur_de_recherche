# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 17:03:15 2021

@author: DELL VOSTRO
"""

import Parser
import IndexSimpler
import Weighter
from IRModel import Vectoriel
from utils.TextRepresenter import PorterStemmer


document1="the new home has been saled on top forecasts"
document2="the home sales rise in july"
document3="there is an increase in home sales in july"
document4="july encounter a new home sales rise"

docs=[document1, document2, document3, document4]
parser=Parser.Parser()

indexSimpler=IndexSimpler.IndexSimpler()
#indexSimpler.buildDocCollectionSimple("data\cisi\cisi.txt")
#docs=indexSimpler.getListDocs()
indexSimpler.indexation(docs)

print(indexSimpler.getIndex()[0])












