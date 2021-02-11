# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 10:03:08 2021

@author: DELL VOSTRO
"""
import utils.porter as porter
from utils.TextRepresenter import PorterStemmer
import collections
import numpy as np
import re


mots_vides=["the","a", "an", "on", "behind", "under", "there", "in", "on"]

document1="the new home has been saled on top forecasts"
document2="the home sales rise in july"
document3="there is an increase in home sales in july"
document4="july encounter a new home sales rise"

N=4 # nombre de documents

def normalisation(doc):
        """retourne un dictionnaire de mots et de leurs occurences"""
        words_doc1=doc.lower().split()
        words_stem=[]

        for w in words_doc1:
            words_stem.append(porter.stem(w))
    
    
        return dict(collections.Counter(words_stem))
    
    
#counter=normalisation(document1) 
#print(counter)

#tp=PorterStemmer()
#text=tp.getTextRepresentation(document1)  #on peut l'utiliser à la place de normalisation() 


def indexes(docs):
    
    index=dict()
    index_inverse=dict()
    
    for i in range(len(docs)):
        counter=normalisation(docs[i])
        index[i]=counter
        
        for k in index[i].keys():
            if not (k in index_inverse) :
                index_inverse[k]={}
                index_inverse[k][i]=counter[k]
            else:
                index_inverse[k][i]=counter[k]
                
                
    return index,index_inverse
    
        
        
index,index_inverse=indexes([document1,document2,document3,document4])


def update_indexes_tf_idf(index,index_inverse):
    df={}
    idf={}
    for k in index_inverse.keys():
        df[k]=len(index_inverse[k].keys())
        idf[k]=np.log((1+N)/(1+df[k]))
        
    for  doc in index.keys():
         for k in index[doc].keys():
             index[doc][k]*=idf[k]
             
    for k in index_inverse.keys():
         for doc in index_inverse[k].keys():
             index_inverse[k][doc]*=idf[k]
             
    return index, index_inverse
    
    
        
        
indx,indx_inverse=update_indexes_tf_idf(index,index_inverse)

#print(index)
#print(index_inverse)


def buildDocCollectionSimple(chemin_doc): 
    file=open(chemin_doc,"r")
    lignes=file.readlines()
    length=len(lignes)
    collection={}
    
    i=0
    
    
    while i<length:
        key=""
        value=""
        if ".I" in lignes[i] :
            key=lignes[i][3:-1]
            print(key)
            i+=1
            while ".T" not in lignes[i]:
                i+=1
            i+=1
            while  i<length and "." not in lignes[i] :
                value+=lignes[i]
                i+=1
            collection[key]=value[:-1]
        else:
            i+=1
    
    file.close()
    
    return collection

#print(buildDocCollectionSimple("cacmShort-good.txt"))

def buildDocumentCollectionRegex(chemin_doc):
    
    collection={}
    file= open(chemin_doc)
    doc=file.read()
    file.close()
    
    docs=doc.split(".I")
    
    for d in range(1,len(docs)):
        
        id=re.search(r'(\d*|$)',docs[d][1:])
        value=re.search(r'\.T(.*?)\.',docs[d], re.DOTALL)
        
        if value is not None :
            collection[id.group(0)]=value.group(1).replace("\n",' ')
        else:
            collection[id.group(0)]=""
            
    return collection
    
    

collection=buildDocumentCollectionRegex("cacmShort-good.txt")
print(collection)

            

                
            

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
