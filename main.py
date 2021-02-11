# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 17:02:24 2021

@author: DELL VOSTRO
"""

import Parser

parser=Parser.Parser()

#collection=parser.buildDocCollectionSimple("data\cacm\cacm.txt")
#print(collection)

collection=parser.buildDocumentCollectionRegex("data\cacm\cacm.txt")
print(collection["1"].getTexte())




