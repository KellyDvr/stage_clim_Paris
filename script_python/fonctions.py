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
        retourne la date au format voulu

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
    
    seuil_annee = 2018
    
    if ybeg <seuil_annee :
        filename = datefile.strftime('%Y%m%d%H%M.text')
        date = datefile.strftime('%Y%m%d%H%M')
    else :
        filename = datefile.strftime('%Y%m%d%H%M_DATA.text')
        date = datefile.strftime('%Y%m%d%H%M')
        
    file_path = datadir + filename
    
    if os.path.exists(file_path) :
        if ybeg<seuil_annee :
            data = pd.read_csv(datadir+filename, skiprows = 23, sep =" ", names = ['Latitudes', 'Longitudes', 'Valeurs min', 'Valeurs max'])
            values_min = np.array(data['Valeurs min'])
            values_min[values_min==65535] = 0
            
            values_max = np.array(data['Valeurs max'])
            values_max[values_max==65535] = 0
            values = (values_min + values_max)/2 #moyenne des valeurs min et max
            #values = np.array(data['Valeurs max'])
            #values[values==65535] = 0
            latitudes = np.array(data['Latitudes'])
            longitudes = np.array(data['Longitudes'])
        
        else : 
            data = pd.read_csv(datadir+filename, skiprows = 25, sep =" ", names = ['Latitudes', 'Longitudes', 'Valeurs'])
            values = np.array(data['Valeurs'])
            values[values==-40] = 0
            values[values==-999] = 0
            latitudes = np.array(data['Latitudes'])
            longitudes = np.array(data['Longitudes'])
            
        return(latitudes, longitudes, values)
    
    else :
        print('le fichier voulu n\'existe pas le : ' + date)
        return(0, 0, 0)
    


def seuil_instant (seuil, date, n, mode) :
    """
    Fonction renvoyant les longitudes, latitudes et valeur ou on a depasse le seuil voulu pour une date

    Parameters
    ----------
    date : str (de longueur 12 : AAAAMMDDHHmm)
        date ou l'on veut regarder si les donnees depassent le seuil
        
    seuil : float
        seuil en dBZ
        
    n : int
        taille des donnees
        
    mode : 1 ou 4
        permet de choisir si on recupere juste le compteur ou aussi les valeurs de seuil et position

    Returns
    -------       
    values_seuil : float
        vecteurs des valeurs depassant le seuil 
    
    compteur : int
        vecteur comptant le nombre de depassement par endroit (meme ordre que les longitudes et latitudes des donnees)

    """
    latitudes, longitudes, values = valeur(date)
    
    
    if type(latitudes) == int :
        compteur = np.zeros(n)
        print('erreur : le fichier n\'existe pas pour le :'+ date)
        return(compteur)
    
    else :
        #initialisation
        values_seuil = []
        compteur = np.zeros(len(latitudes)) #compteur du depassement de seuil (sans se soucier de la duree de l'orage)
        
        if mode == 4 :        
            compteur = (values>seuil).astype(int)
            values_seuil = compteur*values
    
            return(values_seuil, compteur)

        else :
            compteur = (values>seuil).astype(int)

            return(compteur)
        

 #datedeb.strftime('%Y%m%d%H%M')
def seuil_periode (seuil, datedeb, datefin, n, mode) :
    """
    Fonction permettant de compter combien de fois on depasse un seuil sur une periode 
    (on suppose que l'on reste sur la meme annee)

    Parameters
    ----------
    datedeb : str (de longueur 12 : AAAAMMDDHHmm)
        date de debut
        
    datefin : str (de longueur 12 : AAAAMMDDHHmm)
        date de fin
        
    seuil : float
        seuil que l'on veut regarder
        
     mode : 1 ou 4
        permet de choisir si on recupere juste le compteur ou aussi les valeurs de seuil et position


    Returns
    -------
    compteur_mois : int
        vecteur du nb de depassement sur la periode voulu, chaque ligne correspond a une localisation (meme ordre que longitudes et latitudes)

    """
    
    #initialisation des sequences
    compteur_mois = np.zeros(n)
    
    datefin = str2date(datefin) 
    date = str2date(datedeb)
    
    while date <= datefin :
        
        date = date.strftime('%Y%m%d%H%M')
        print(date)

        compteur_instant = seuil_instant(seuil, date, n, mode)
       # print(len(compteur_instant))
        compteur_mois += compteur_instant
        #date = str2date(dateint)
        date = str2date(date) + datetime.timedelta(minutes = 15)
    
    return(compteur_mois)



def compteur_seuil_annee (seuil, anneedeb, anneefin, n) :
    """
    Fonction permettant de calculer les depassements de seuil sur chaque annee pour toutes la periode des donnees (avril à octobre)

    Parameters
    ----------
    seuil : float
        seuil de depassement souahité en dBZ
        
    anneedeb : str (de longueur 4)
        annee de debut de la periode souhaite
        
    anneefin : str (de longeur 4)
        annee de fin de la periode souhaite
        
    n : int
        longueur des donnees

    Returns
    -------
    compteur_annee : int
        matrice d'entier comptant les depassement sur les annees voulues (1 colonne = 1 annee)

    """

    liste_annee = np.arange(anneedeb, anneefin+1, 1)

    compteur_annee = np.zeros(n)#,len(liste_annee)))
    
    for annee in liste_annee : 
        #print('------'+str(annee)+'------')
        datedeb = str(annee)+'04010000'
        datefin = str(annee)+'11010000' 
        
        compteur_annee[:] = seuil_periode(seuil , datedeb, datefin, n, 1) #on choisit 1 comme mode par defaut

    return(compteur_annee)

#compteur_annee[:,annee-anneedeb]

def compteur_seuil_mois (seuil, mois, anneedeb, anneefin, n) :
    """
    Fonction comptant le nb de depassement de seuil sur un mois donne complet sur les annees anneedeb/anneefin

    Parameters
    ----------
    seuil : float
                seuil de depassement souahité en dBZ

    mois : int
        entre 4 et 11, mois ou l'on souhaite regarder les depassements
        
    anneedeb : int
        entre 2010 et 2022, annee de depart ou l'on regarde les depassements
        
    anneefin : int
         entre 2010 et 2022 et tel que anneefin>anneedeb, annee de depart ou l'on regarde les depassements
         
    n : int
        taille des donnees

    Returns
    -------
    compteur_mois : int
        vecteur ou chaque entree correspond au nombre de fois ou on a depasse le seuil en une localisation (meme ordre que longitudes/latitudes)

    """
    liste_annee = np.arange(anneedeb, anneefin+1, 1) #+1 pour inclure l'annee de fin dans le compteur 
    
    compteur_mois = np.zeros(n)
    
    for annee in liste_annee :
        if mois < 10 :
            mois_str = '0'+str(mois)
        else:
            mois_str = str(mois)

        nb_jours_mois = nbjoursmois(mois, annee)
        datedeb = str(annee)+mois_str+'010000'
        datefin = str(annee)+mois_str+str(nb_jours_mois) +'2345'
            
        compteur_temp = seuil_periode(seuil , datedeb, datefin, n, 1)

        compteur_mois += compteur_temp

    return(compteur_mois)


def compteur_zone (compteur, indice) :
    """
    La fonction permet de compteur le nombre de fois ou on a depasser un seuil à partir d'un vecteur 

    Parameters
    ----------
    compteur : int
        compteur des depassements sur le domaine entier pour une duree donnee et un seuil fixe
    indice : float
        vecteur des indices de position dans le sous domaine que l'on veut etudier

    Returns
    -------
    compteur_zone : int
        nombre de depassements totals sur la sous zone etudiee sans distinction geographique

    """
    
    compteur_zone = np.sum(compteur[indice, :])
    
    return (compteur_zone)



def compteur_2h(seuil, datedeb, datefin, n):
    """
    Fonction renvoyant le nombre de depassements du seuil voulu par tranche de 2h sur la période datedeb-datefin

    Parameters
    ----------
    seuil : int
        seuil de depassements voulu
        
    datedeb : str
        date de debut de période
        
    datefin : str
        date de fin de periode
        
    n : int
        taille des donnees

    Returns
    -------
    compteur_temp : int
        matrice du nombre de depassements sur une période donne chaque colonne correspond a une periode de deux heures (00:00-01:45 coonne 1 puis 02:00-03:45 colonne 2, etc)

    """
    
    compteur_temp = np.zeros((n,12))

    delta = datetime.timedelta(minutes = 105)
    
    datetemp1 = str2date(datedeb)

    i=0
    while datetemp1 < str2date(datefin) :
        #print('temp1')
        #print(datetemp1)
        datetemp2 = datetemp1 + delta
        #print('temp2') 
        #print(datetemp2)
        
        datetemp1str = datetemp1.strftime('%Y%m%d%H%M')
        datetemp2str = datetemp2.strftime('%Y%m%d%H%M')
    
        compteur_temp[:,int(int(datetemp1.strftime('%H'))/2)] += seuil_periode(seuil , datetemp1str, datetemp2str, n, 1)
        
        datetemp1 = datetemp2 + datetime.timedelta(minutes = 15)
        datetemp2 = datetemp1 + delta
        i+=1
    
    return(compteur_temp)#, i)






