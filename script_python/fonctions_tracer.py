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

#on definit les bornes du domaines sur lesquelles seront trace toutes les courbes
bounds = [0.97, 3.7, 47.95, 49.75]

#%%
    
def trace (datedeb, datefin, longitudes, latitudes, values, seuil, mode) :
    """
    Fonction permettant de tracer ou se situe les reflectivite radar superieures a un seuil en un instant donne.
    
    Parameters
    ----------
    datedeb : str (de longueur 12 : AAAAMMDDHHmm)
            date de debut ou on a regarder si on etait superieur au seuil
    
    datefin : str (de longueur 12 : AAAAMMDDHHmm)
            date de debut ou on a regarder si on etait superieur au seuil, peut etre egale a datedeb et dans ce cas on regarde juste en un instant donne
    
    longitudes : float 
            vecteur des longitudes ou on est superieur au seuil
    
    latitudes : float 
            vecteur des latitudesou on est superieur au seuil
    
    values : float 
            vecteur des valeurs de reflectivite en dBZ ou on est superieur au seuil
    
    seuil : float
            valeur du seuil en dBZ que l'on veut regarder (si seuil = 0 on regarde les donnees sans contrainte)
    
    mode : float ('val' ou 'compteur')
            mot clef permettant de specifier si on trace les valeurs ou le nombre de fois ou on a depasse le seuil


    """
    
    if mode != 'val' and mode != 'compteur': 
        print('Syntaxe invalide pour mode !') #message d'erreur si jamais on a mal ecrit le mode
        return()
    
    
    start_date = datetime.datetime(int(datedeb[0:4]), int(datedeb[4:6]), int(datedeb[6:8]), int(datedeb[8:10]), int(datedeb[10:12])) #mise au format UTC de la date
    end_date = datetime.datetime(int(datefin[0:4]), int(datefin[4:6]), int(datefin[6:8]), int(datefin[8:10]), int(datefin[10:12]))
    

    
    if mode == 'val' :
        if seuil==0 : #on trace les donnees brutes en un instant
             print('1')
             levels_reflectivite = [7, 15, 23, 33, 40, 45, 50, 55, 60, 65] #niveaux de reflectivite pour l'echelle de la carte
             title="Reflectivité le \n"+start_date.strftime('%Y-%m-%d - %H:%M UTC')
             img="/cnrm/ville/USERS/doeuvrek/script_python/figures/reflectivite_instant_"+datedeb+".png"  #nom et chemin pour sauvegarder l'image
             unite='dBZ'
        elif seuil!=0 :
            if datedeb == datefin : #on trace les donnees seuillees en un instant
                print('2') 
                levels_reflectivite =  [7, 15, 23, 33, 40, 45, 50, 55, 60, 65] 
                title="Reflectivité >" + str(seuil) + "\n" + start_date.strftime('%Y-%m-%d - %H:%M UTC')
                img="/cnrm/ville/USERS/doeuvrek/script_python/figures/reflectivite_seuil_"+datedeb+".png"  #nom et chemin pour sauvegarder l'image
                unite='dBZ'
                
            elif datedeb != datefin : #on trace les donnees seuillees sur la periode datedeb datefin
                print('3')
                levels_reflectivite =  [7, 15, 23, 33, 40, 45, 50, 55, 60, 65] 
                title="Reflectivité >" + str(seuil) + " de \n" + start_date.strftime('%Y-%m-%d - %H:%M UTC') + ' à ' + end_date.strftime('%Y-%m-%d - %H:%M UTC')
                img="/cnrm/ville/USERS/doeuvrek/script_python/figures/reflectivite_seuil_"+datedeb+".png"  #nom et chemin pour sauvegarder l'image
                unite='dBZ'
        
    elif  mode == 'val' and seuil!=0  and datedeb != datefin : #on trace les donnees seuillees sur la periode datedeb datefin
        levels_reflectivite =  [7, 15, 23, 33, 40, 45, 50, 55, 60, 65] 
        title="Reflectivité >" + str(seuil) + " de \n" + start_date.strftime('%Y-%m-%d - %H:%M UTC') + ' à ' + end_date.strftime('%Y-%m-%d - %H:%M UTC')
        img="/cnrm/ville/USERS/doeuvrek/script_python/figures/reflectivite_seuil_"+datedeb+".png"  #nom et chemin pour sauvegarder l'image
        unite='dBZ'
         
    elif mode == 'compteur' : #on trace combien de fois on a  depassesr le seuil en un instant
        if datedeb!=datefin :
            print('4')
            levels_reflectivite = np.arange(1, 51, 5) #[1, 2., 3., 4., 5., 7., 10., 15., 20., 30.]
            title = "Compteur reflectivité >" + str(seuil) + " de \n"  + start_date.strftime('%Y-%m-%d - %H:%M UTC') + ' à ' + end_date.strftime('%Y-%m-%d - %H:%M UTC')
            img="/cnrm/ville/USERS/doeuvrek/script_python/figures/reflectivite_compteur_seuil_"+str(seuil)+'_periode_deb_'+ start_date.strftime('%Y-%m-%d - %H:%M UTC') + '.png'  #nom et chemin pour sauvegarder l'image
            unite='nb de depassements'
        else :  
            print('5') 
            levels_reflectivite = np.arange(1, 50, 5) 
            title = "Compteur reflectivité >" + str(seuil) + "\n" + start_date.strftime('%Y-%m-%d - %H:%M UTC')
            img="/cnrm/ville/USERS/doeuvrek/script_python/figures/reflectivite_compteur_seuil_"+str(seuil)+'_le_'+ start_date.strftime('%Y-%m-%d - %H:%M UTC') + ".png"  #nom et chemin pour sauvegarder l'image
            unite='nb de depassements'
       
        
    #color_levels = [(0, 0, 255/256), (0, 177/256, 251/256), (0, 255/256, 254/256), (0, 222/256, 212/256), (0, 182/256, 163/256),
                  #(101/256, 163/256, 62/256), (255/256, 255/256, 65/256), (255/256, 215/256, 58/256), (255/256, 163/256, 49/256),
                  #(255/256, 4/256, 34/256)]
                  
    #cmap = mcolors.ListedColormap(color_levels, 'reflectivite')
    cmap = 'jet'
    #norm = mcolors.BoundaryNorm(levels_reflectivite, cmap.N)
    
    #creation de la figure
    fig = plt.figure(figsize=(18., 13.))  
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Mercator())
    ax.set_extent(bounds)
    
    #parametres pour le graphique
    values = values
    levels=levels_reflectivite
    ticks=levels_reflectivite
 
    ax.set_title(title, loc='center', size = 18)
        
    cf = ax.tricontourf(longitudes, latitudes, values, cmap=cmap, levels=levels, transform=ccrs.PlateCarree())
    cb = fig.colorbar(cf, orientation='horizontal', aspect=70, shrink=0.48, pad=0.05,extendrect='False',extend='both',ticks=ticks)
    cb.set_label('('+unite+')', size=15, weight ="bold")
    cb.ax.tick_params(labelsize='medium')
    
    cf.cmap.set_over('brown') #permet de mettre d'une certaine couleur les valeurs depassant la palette de couleur
    
    #ajout des departements et du point de Paris sur la carte
    
    departements = gpd.read_file('/home/doeuvrek/Documents/ouverture_donnees/departements.geojson')
    #metropole = gpd.read_file('/home/doeuvrek/Documents/ouverture_donnees/metropole-version-simplifiee.geojson')    
    ax.add_geometries(departements.geometry, crs = ccrs.PlateCarree(), facecolor='none', edgecolor='black',linewidth=0.8)
    
    ax.add_feature(cfeature.BORDERS.with_scale('10m'))
    ax.add_feature(cfeature.COASTLINE.with_scale('10m'))
    
    # To locate Paris on the map
    ax.scatter(2.35, 48.853, color='black', transform=ccrs.PlateCarree(), linewidths = 1.1) #cordonnes de Paris centre
    ax.text(2.348, 48.859, 'Paris', color='black', transform=ccrs.PlateCarree(), size = 22)
    
    #plt.savefig(img)
    
    
    

 