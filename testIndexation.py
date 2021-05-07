# -*- coding: utf-8 -*-
"""
Created on Thu May  6 00:15:39 2021

@author: DELL VOSTRO
"""

from Parser import Parser
from IndexSimpler import IndexSimpler


parser=Parser()
parser.buildDocCollectionSimple("data\cisi\cisi.txt")


docs=parser.getListDocs() #liste des documents parsés

#------------------------------------------test Class Document
"""
document=docs[0]
print("Document ID :",document.getId())
print("Document Text :",document.getText())
"""

#----------------------------------------tests pour les index
indexSimpler=IndexSimpler(parser.getCollection()) 

indexSimpler.indexation() #creation de l'index et l'index inverse
#test indexation tf
"""
print("Tfs For Doc : id = 1:\n",indexSimpler.getTfsForDoc(1))
print("Tfs For stem : stem = present:\n",indexSimpler.getTfsForStem("present"))
"""

indexSimpler.indexation_tf_idf()  #creation de l'index tf-idf et de son index inverse
#test indexation tf-idf
"""
print("Tfs Idf For DOc : id = 1:\n",indexSimpler.getTfIDFsForDoc(1))
print("Tfs Idf For stem : stem = present :\n",indexSimpler.getTfIDFsForStem("present"))
"""

indexSimpler.indexationHyperLinks() #creation de l'index des hyperliens
#test indexation hyperLinks
"""
print("Hyperlinks from doc: id =1 :\n",indexSimpler.getHyperLinksFrom(1))
print("Hyperlinks to doc : id = 1:\n",indexSimpler.getHyperLinksTo(1))
"""



