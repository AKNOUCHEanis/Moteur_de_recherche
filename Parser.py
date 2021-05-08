# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 16:50:48 2021

@author: DELL VOSTRO
"""
import Document 
import re
import copy

class Parser:
    
    def __init__(self):
        self.documents = dict()
    
    def buildDocCollectionSimple(self,fichier):

         
        resultat = dict()
        f = open(fichier, 'r')
        lignes = f.readlines()
        l = lignes[0]
        idDoc = int(l[3:])
        title=""
        date=""
        author=""
        keywords=""
        txt=""
        link=""
        N = len(lignes)
        
        
        for i in range(1,N):  

            
            if lignes[i].startswith('.I'):
                d =Document.Document(idDoc,title,date,author,keywords,txt,link)
                self.documents[idDoc]=d
                idDoc = int(lignes[i][3:])
                title=""
                date=""
                author=""
                keywords=""
                txt=""
                link=""


            elif lignes[i].startswith(".T") :
                i+=1
                title = lignes[i].strip()
                
            elif lignes[i].startswith(".B") :
                i+=1
                date = lignes[i].strip()
                
            elif lignes[i].startswith(".A") :
                author = lignes[i+1].strip()
                i+=2
                while(i < N and lignes[i].startswith('.') == False):
                    author += ', '+lignes[i].strip()
                    i+=1
                i-=1
                
            elif lignes[i].startswith(".K") :
                keywords = lignes[i+1].strip()
                i+=2
                while(i < N and lignes[i].startswith('.') == False):
                    keywords += ' '+lignes[i].strip()
                    i+=1
                i-=1
                
            elif lignes[i].startswith(".W") :
                txt = lignes[i+1].strip()
                i+=2
                while(i < N and lignes[i].startswith('.') == False):
                    txt += ' '+lignes[i].strip()
                    i+=1
                i-=1
                
            elif lignes[i].startswith(".X") :
                link=[]
                if len(lignes[i+1].split())!=0:
                    link.append(lignes[i+1].split()[0])
                i+=2
                while(i < N and lignes[i].startswith('.') == False):
                    #link += ' '+lignes[i].split(' ')[0]
                    if len(lignes[i].split())!=0:
                        link.append(lignes[i].split()[0])
                    i+=1
                i-=1
                
        d = Document.Document(idDoc,title,date,author,keywords,txt,link)
        self.documents[idDoc]=d
        f.close()
    
    
    def buildDocCollectionSimple2(self,chemin_doc): 
        
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
                doc=Document.Document()
                doc.setId(key)
                i+=1
                while ".T" not in lignes[i]:
                    i+=1
                i+=1
                while  i<length and "." not in lignes[i] :
                    value+=lignes[i]
                    i+=1
                doc.setTexte(value[:-1])
                collection[key]=doc
            else:
                i+=1
        
        file.close()
    
        return collection
    
   
    def buildDocumentCollectionRegex(self,chemin_doc):
    
        collection={}
        file= open(chemin_doc)
        doc=file.read()
        file.close()
        
        docs=doc.split(".I")
    
        for d in range(1,len(docs)):
            doc=Document.Document()
            
            id=re.search(r'(\d*|$)',docs[d][1:])
            value=re.search(r'\.W(.*?)\.',docs[d], re.DOTALL)
            
            doc.setId(id.group(0))
            
            if value is not None :
                
                doc.setTexte(value.group(1).replace("\n",' '))
            else:
                doc.setTexte("")
                
            collection[id.group(0)]=doc
            
                
        return collection
    
    def getListDocs(self):
        """retourne une liste de document texte"""
        liste=[]
        keys=self.documents.keys()
        
        for k in keys:
            liste.append(self.documents[k])
                
        return liste
    
    def getCollection(self):
        
        return copy.deepcopy(self.documents)

            
    