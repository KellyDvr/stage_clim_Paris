#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 09:01:07 2023

@author: doeuvrek
"""

import os
import numpy as np


#%% fonction pour savoir le nombre de jour d'un mois d'une annee  

def nbjoursmois(m,a):
    """Donne le nombre de jours du mois m de l'année a"""
    nj = (0,31,28,31,30,31,30,31,31,30,31,30,31)[m]
    if m==2 and ((a%4==0 and a%100!=0) or a%400==0): # m=février et a=bissextile?
        return nj + 1
    return nj

#%% creation des dossiers mois et jours

#on defini les dates de debut et de fin de l'étude
ybeg,mbeg,dbeg,hbeg,minbeg=2011,4,1,0,0
yend,mend,dend,hend,minend=2021,11,1,0,0

#chemin ou on veut stocker les donnees
main_path = '/mnt/nfs/d40/ville/USERS/doeuvrek/donnees'

liste_annees = np.arange(ybeg, yend+1, step = 1)
liste_mois = np.arange(mbeg, mend+1, step = 1)

#%% suite section precedente
for annee in liste_annees :
    annee = str(annee)
    
    for mois in liste_mois :
        if mois<10 :
            mois = str(mois)
            print(mois)
            os.system('mkdir '+ main_path + '/' + annee + '/' + '0' + mois)
            chemin_mois = main_path + '/' + annee + '/' + '0' + mois + '/'
            jour_mois = nbjoursmois(int(mois), int(annee))
        
            for jour in range(1,jour_mois+1):
                if jour<10:
                    jour = str(jour)
                    os.system('mkdir '+ chemin_mois + '0' + jour)
                else :
                    jour = str(jour)
                    os.system('mkdir '+ chemin_mois + jour)
        else :
            
             mois = str(mois)
             print(mois)
             os.system('mkdir '+ main_path + '/' + annee + '/' + mois)
             chemin_mois = main_path + '/' + annee + '/' + mois + '/'
             jour_mois = nbjoursmois(int(mois), int(annee))
        
             for jour in range(1,jour_mois+1):
                if jour<10:
                    jour = str(jour)
                    os.system('mkdir '+ chemin_mois + '0' + jour)
                else :
                    jour = str(jour)
                    os.system('mkdir '+ chemin_mois + jour)

#%% ranger les donnees par mois et jour
chemin = '/cnrm/ville/USERS/doeuvrek/donnees/'
annee_voulue = '2019'
liste_fichiers = os.listdir(chemin+annee_voulue) #attention les mois sont dedans aussi 04, 05...

for fichier in liste_fichiers :
    #print(fichier)
    annee = str(fichier[0:4]) 
    mois = str(fichier[4:6])
    jour = str(fichier [6:8])
    os.system('mv '+ chemin + annee +'/' + fichier+ ' ' + chemin + annee +'/' + mois + '/' + jour)
    
#%% on veut verifier s'il y a des donnees manquantes (combien et ou)
chemin = '/cnrm/ville/USERS/doeuvrek/donnees/'
annee = '2019' #on choisit l'annee que l'on veut regarder


for mois in liste_mois :
    jour_mois = nbjoursmois(int(mois), int(annee))
    if mois<10 :
        mois = str('0' + str(mois))
        for jour in range(1,jour_mois) :
            #print(jour, type(jour))
            if jour<10 :
                jour = str('0' + str(jour))
                nb_fichier = len(os.listdir(chemin+annee+'/' + mois + '/' + jour))
                if nb_fichier == 96 :
                    print('Pas de donnees manquantes pour le mois :' + str(mois) + ' et le jour :' + jour, '-- on a ' + str(nb_fichier) + ' fichiers')
                else :
                    nb_donnee_manquante = 96 - nb_fichier
                    print('Il manque '+ str(nb_donnee_manquante) + ' fichiers pour le mois :' + str(mois) + '  et le jour :' + str(jour), '-- on a ' + str(nb_fichier) + 'fichiers')
            else :
                jour = str(jour)
                nb_fichier = len(os.listdir(chemin+annee+'/' + mois + '/' + jour))
                if nb_fichier == 96 :
                    print('Pas de donnees manquantes pour le mois :' + mois + ' et le jour :' + jour, '-- on a ' + str(nb_fichier) + ' fichiers')
                else :
                    nb_donnee_manquante = 96 - nb_fichier
                    print('Il manque '+ str(nb_donnee_manquante) + ' fichiers pour le mois :' + str(mois) + ' et le jour :' + str(jour), '-- on a ' + str(nb_fichier) + ' fichiers')
    else :
        if mois == 11 :
            print('Mois de novembre une donnee seulement')
        else :
            mois = str(mois)
            for jour in range(1,jour_mois) :
                if jour<10 :
                    jour = str('0' + str(jour))
                    nb_fichier = len(os.listdir(chemin+annee+'/' + mois + '/' + jour))
                    if nb_fichier == 96 :
                        print('Pas de donnees manquantes pour le mois :' + str(mois) + ' et le jour :' + str(jour), '-- on a ' + str(nb_fichier) + 'fichiers')
                    else :
                        nb_donnee_manquante = 96 - nb_fichier
                        print('Il manque '+ str(nb_donnee_manquante) + ' fichiers pour le mois :' + str(mois) + ' et le jour :'+str(jour), '-- on a ' + str(nb_fichier) + ' fichiers')
                else :
                    jour = str(jour)
                    nb_fichier = len(os.listdir(chemin+annee+'/' + mois + '/' + jour))
                    if nb_fichier == 96 :
                        print('Pas de donnees manquantes pour le mois :' + str(mois) + ' et le jour :' + str(jour), '-- on a ' + str(nb_fichier) + ' fichiers')
                    else :
                        nb_donnee_manquante = 96 - nb_fichier
                        print('Il manque '+ str(nb_donnee_manquante) + ' fichiers pour le mois :' + str(mois) + ' et le jour :' + str(jour), '-- on a ' + str(nb_fichier) + ' fichiers')
    
print(annee)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        