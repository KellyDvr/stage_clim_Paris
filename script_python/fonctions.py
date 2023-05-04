#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 11:49:56 2023

@author: doeuvrek
"""

import pandas as pd
import numpy as np

import cartopy.crs as ccrs
import datetime

import cartopy.feature as cfeature
import geopandas as gpd

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

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





def seuil (seuil, datedeb, datefin, longitudes, latitudes) :
    """
    Fonction permettant de compter combien de fois on est superieur a un seuil en un endroit sur une periode donnee 

    Parameters
    ----------
    seuil : float
        seuil en dBZ 
        
    datedeb : str (de longueur 12 : AAAAMMDDHHmm)
        date de debut
        
    datefin : str (de longueur 12 : AAAAMMDDHHmm)
        date de fin
        
    longitudes : float 
        vecteur des longitudes
    
    latitudes : float
        vecteur des latitudes
        
    Returns
    -------
    None.

    """
    #initialisation des sequences
    latitudes_seuil = []
    longitudes_seuil = []
    values_seuil = []
    compteur = np.zeros(len(latitudes))
    
    #date de debut et fin au format UTC
    start_date = datetime.datetime(int(datedeb[0:4]), int(datedeb[4:6]), int(datedeb[6:8]), int(datedeb[8:10]), int(datedeb[10:12]))
    end_date = datetime.datetime(int(datefin[0:4]), int(datefin[4:6]), int(datefin[6:8]), int(datefin[8:10]), int(datefin[10:12]))
    
    
    liste_mois = np.arange(int(datedeb[4:6]), int(datefin[4:6]), step = 1)
    
    main_path = "/cnrm/ville/USERS/doeuvrek/donnees/" + str(annee_voulue) + '/'
    


    if int(datedeb[0:4]) < 2018 :
        datadir = datefile.strftime('/cnrm/ville/USERS/doeuvrek/donnees/%Y/%m/%d/')
        filename = datefile.strftime('%Y%m%d%H%M.text')
        data = pd.read_csv(datadir+filename, skiprows = 23, sep =" ", names = ['Latitudes', 'Longitudes', 'Valeurs', 'Valeurs max'])
        values = np.array(data['Valeurs'])
        for i in range(len(values)) :
            if values[i]>seuil :
                latitudes_seuil.append(latitudes[i])
                longitudes_seuil.append(longitudes[i])
                values_seuil.append(values[i])
                compteur[i] =+ 1
            else :
                latitudes_seuil.append(latitudes[i])
                longitudes_seuil.append(longitudes[i])
                values_seuil.append(0)
            
        
    else :
        data = pd.read_csv(datadir+filename, skiprows = 23, sep =" ", names = ['Latitudes', 'Longitudes', 'Valeurs', 'Valeurs max'])
        values = np.array(data['Valeurs'])
        for i in range(len(values)) :
            if values[i]>seuil :
                latitudes_seuil.append(latitudes[i])
                longitudes_seuil.append(longitudes[i])
                values_seuil.append(values[i])
                compteur[i] =+ 1
            else :
                latitudes_seuil.append(latitudes[i])
                longitudes_seuil.append(longitudes[i])
                values_seuil.append(0)
    
    return(latitudes_seuil, longitudes_seuil, compteur, values_seuil)