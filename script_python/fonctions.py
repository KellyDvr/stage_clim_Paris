#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 11:49:56 2023

@author: doeuvrek
"""

import pandas as pd
import numpy as np


import datetime
import os

import fonctions as fct


def nbjoursmois(m,a):
    """
    Donne le nombre de jours du mois m de l'année a
    
    Parameters
    ----------
    m : int
        numero du mois voulu
        
    a : int
        annee voulue
    """
    nj = (0,31,28,31,30,31,30,31,31,30,31,30,31)[m]
    if m==2 and ((a%4==0 and a%100!=0) or a%400==0): # m=février et a=bissextile?
        return nj + 1
    return nj



def str2date (datestr) :
    """
    Fonction pour basculer d'une chaine de charactere a une date.

    Parameters
    ----------
    datestr : str (de longueur 12 : AAAAMMDDHHmm)
        date a modifier

    Returns
    -------
    date : '%Y%m%d%H%M'
        retourne la date

    """
    annee = int(datestr[0:4])
    mois = int(datestr[4:6])
    jour = int(datestr[6:8])
    heure = int(datestr[8:10])
    minute = int(datestr[10:12])
    
    return datetime.datetime(annee, mois, jour, heure, minute)



def valeur (date) :
    """
    fonction renvoyant les longitudes, latitudes et valeurs pour une date donnee

    Parameters
    ----------
    date : str (de longueur 12 : AAAAMMDDHHmm)
        date ou l'on souahite regarder les donnees

    Returns
    -------
    latitudes : float
        vecteur de latitudes
        
    longitudes : float
        vecteur de longitudes
        
    values : float
        valeur de reflectivite en dBZ pour la date donnee

    """
    ybeg,mbeg,dbeg,hbeg,minbeg=int(date[0:4]), int(date[4:6]), int(date[6:8]), int(date[8:10]), int(date[10:12])
    datefile = datetime.datetime(ybeg,mbeg,dbeg,hbeg,minbeg)
    
    datadir = datefile.strftime('/cnrm/ville/USERS/doeuvrek/donnees/%Y/%m/%d/')
    filename = datefile.strftime('%Y%m%d%H%M.text')
    date = datefile.strftime('%Y%m%d%H%M')
    
    if ybeg <2018 :
        if os.path.exists(datadir+filename) :
            data = pd.read_csv(datadir+filename, skiprows = 23, sep =" ", names = ['Latitudes', 'Longitudes', 'Valeurs min', 'Valeurs max'])
            values_min = np.array(data['Valeurs min'])
            values_min[values_min==65535] = 0
            
            values_max = np.array(data['Valeurs max'])
            values_max[values_max==65535] = 0
            values = (values_min + values_max)/2 #moyenne des valeurs min et max
            latitudes = np.array(data['Latitudes'])
            longitudes = np.array(data['Longitudes'])
            return(latitudes, longitudes, values)
        else :
            print('le fichier voulu n existe pas')
            return('ERROR')
    
    else :
        if os.path.exists(datadir+filename) :
            data = pd.read_csv(datadir+filename, skiprows = 23, sep =" ", names = ['Latitudes', 'Longitudes', 'Valeurs min'])
            values = np.array(data['Valeurs'])
            values[values==65535] = 0
            latitudes = np.array(data['Latitudes'])
            longitudes = np.array(data['Longitudes'])
            return(latitudes, longitudes, values)
        else :
            print('le fichier voulu n existe pas')
            return('ERROR')
    


def seuil_instant (date, seuil) :
    """
    Fonction renvoyant les longitudes, latitudes et valeur ou on a depasse le seuil voulu pour une date

    Parameters
    ----------
    date : str (de longueur 12 : AAAAMMDDHHmm)
        date ou l'on veut regarder si les donnees depassent le seuil
    seuil : float
        seuil en dBZ

    Returns
    -------
    latitudes_seuil : float
        vecteur des latitudes ou on a depasse le seuil
    
    longitudes_seuil : float
        vecteur des longitudes ou on a depasse le seuil
        
    values_seuil : float
        vecteurs des valeurs depassant le seuil 
    
    compteur : int
        vecteur comptant le nombre de depassement par endroit (meme ordre que les longitudes et latitudes des donnees)

    """
    latitudes, longitudes, values = valeur(date)
    
    if latitudes[0]==0 :
        print('erreur : le fichier n existe pas')
        return(0, 0, 0, 0)
    else :
        #initialisation
        latitudes_seuil = []
        longitudes_seuil = []
        values_seuil = []
        compteur = np.zeros(len(latitudes)) #compteur du depassement de seuil (sans se soucier de la duree de l'orage)
        
        for i in range(len(values)) :
            if values[i]>seuil :
                latitudes_seuil.append(latitudes[i])
                longitudes_seuil.append(longitudes[i])
                values_seuil.append(values[i])
                compteur[i] = compteur[i] + 1
            else :
                latitudes_seuil.append(latitudes[i])
                longitudes_seuil.append(longitudes[i])
                values_seuil.append(0)
                
        return(latitudes_seuil, longitudes_seuil, values_seuil, compteur)



def seuil_mois (seuil, datedeb, datefin, n) :
    """
    Fonction permettant de compter combien de fois on est superieur a un seuil en un endroit sur une periode donnee (d'au plus un mois)
    On suppose qu'on ne change pas d'annee et que l'on est sur le meme mois.
    
    Parameters
    ----------
    seuil : float
        seuil en dBZ 
        
    datedeb : str (de longueur 12 : AAAAMMDDHHmm)
        date de debut
        
    datefin : str (de longueur 12 : AAAAMMDDHHmm)
        date de fin
        
    n : int
        longueur du vecteurs des donnees
        
    Returns
    -------
    compteur_mois : int
        vecteur du nb de depassements (l'ordre est celui des longitudes et latitudes)

    """
    
    annee = int(datedeb[0:4])
    
    moisdeb = int(datedeb[4:6])
    #moisfin = int(datefin[4:6])
    jourdeb = int(datedeb[6:8])
    jourfin = int(datefin[6:8])
    
    #liste_mois = np.arange(moisdeb, moisfin+1)
    #print(liste_mois)
    liste_heure = np.arange(1, 24)
    liste_minute = np.arange(0, 60, step = 15)
    
    #print(range(jourdeb, jourfin+1))

    #initialisation des sequences
    compteur_mois = np.zeros(n)
    

    for jour in range(jourdeb, jourfin+1) : #marche si jourdeb<jourfin
        #print('jour : ' + str(jour))
        for heure in liste_heure:
            for minute in liste_minute :
                #print(minute)
                datefile = datetime.datetime(annee, moisdeb, jour, heure, minute)
                print(datefile)
                datefile = datefile.strftime('%Y%m%d%H%M')
                
                latitudes_seuil, longitudes_seuil, values_seuil, compteur = seuil_instant (datefile, seuil) #PROBLEME SI LE FICHIER N'EXISTE PAS

                compteur_mois = compteur + compteur_mois

    return(np.array(compteur_mois))



def seuil_annee (seuil, datedeb, datefin, n) :
    """
    Fonction permettant de compter combien de fois on depasse un seuil sur une periode (une annee max)

    Parameters
    ----------
    datedeb : str (de longueur 12 : AAAAMMDDHHmm)
        date de debut
        
    datefin : str (de longueur 12 : AAAAMMDDHHmm)
    None.
    seuil : float
        seuil que l'on veut regarder

    Returns
    -------
    compteur_mois : int
        vecteur du nb de depassement sur la periode voulu, chaque ligne correspond a une localisation (meme ordre que longitudes et latitudes)

    """

    anneedeb = int(datedeb[0:4])
    anneefin = int(datefin[0:4])
    
    moisdeb = int(datedeb[4:6])
    moisfin = int(datefin[4:6])
    
    jourdeb = int(datedeb[6:8])
    jourfin = int(datefin[6:8])
    
    heuredeb = int(datedeb[8:10])
    heurefin = int(datefin[8:10])
    
    mindeb = int(datedeb[10:12])
    minfin = int(datefin[10:12])
    
    #liste_mois = np.arange(moisdeb, moisfin, step = 1) 
    
    #initialisation des sequences
    compteur_mois = np.zeros(n)
    
    datefin = datetime.datetime(anneefin, moisfin, jourfin, heurefin, minfin)
    date = datetime.datetime(anneedeb, moisdeb, jourdeb, heuredeb, mindeb)
    #print(date, '----', datefin)
    
    while date < datefin :
        dateint = date + datetime.timedelta(days=1)
        #print(dateint)
        
        date = date.strftime('%Y%m%d%H%M')
        #print(date)
        
        
        dateint = dateint.strftime('%Y%m%d%H%M')
        #print(dateint)

        compteur_jour = seuil_mois (seuil, date, dateint, n) 
        compteur_mois = compteur_mois + compteur_jour
        date = str2date(dateint)
    
    return(compteur_mois)






















