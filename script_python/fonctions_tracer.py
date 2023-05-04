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

def trace_instant (date, longitudes, latitudes, values) :
    """
    Fonction permettant de tracer les reflectivite radar en un instant donne.
    
    Parameters
    ----------
    date : str (de longueur 12 : AAAAMMDDHHmm)
            date de l'instant 
            
    longitudes : float 
        vecteur des longitudes
    
    latitudes : float
        vecteur des latitudes
        
    values : float 
        vecteur des valeurs de reflectivite en dBZ


    """
    start_date=datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]), int(date[8:10]), int(date[10:12])) #mise au format UTC de la date
    
    levels_reflectivite = [1, 3., 5., 7., 10., 15., 20., 30., 50., 70.] #niveaux de reflectivite pour l'echelle de la carte
    color_levels = [(0, 0, 255/256), (0, 177/256, 251/256), (0, 255/256, 254/256), (0, 222/256, 212/256), (0, 182/256, 163/256),
                  (101/256, 163/256, 62/256), (255/256, 255/256, 65/256), (255/256, 215/256, 58/256), (255/256, 163/256, 49/256),
                  (255/256, 4/256, 34/256)]
                  
    cmap = mcolors.ListedColormap(color_levels, 'reflectivite')
    norm = mcolors.BoundaryNorm(levels_reflectivite, cmap.N)
    
    #creation de la figure
    fig = plt.figure(figsize=(18., 13.))  
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Mercator())
    ax.set_extent(bounds)
    
    #parametres pour le graphique
    values = values
    title="Reflectivité \n"+start_date.strftime('%Y-%m-%d - %H:%M UTC')
    levels=levels_reflectivite
    ticks=levels_reflectivite
    unite='dBZ'
    #nom et chemin pour sauvegarder l'image
    img="/cnrm/ville/USERS/doeuvrek/script_python/figures/reflectivite_instant"+date+".png"
    
    ax.set_title(title, loc='center', size = 18)
    
    cf = ax.tricontourf(longitudes, latitudes, values, cmap=cmap, levels=levels, norm=norm, transform=ccrs.PlateCarree())
    cb = fig.colorbar(cf, orientation='horizontal', aspect=70, shrink=0.48, pad=0.05,extendrect='False',extend='both',ticks=ticks)
    cb.set_label('('+unite+')', size=15, weight ="bold")
    cb.ax.tick_params(labelsize='medium')
    
    #ajout des departements et du point de Paris sur la carte
    
    departements = gpd.read_file('/home/doeuvrek/Documents/ouverture_donnees/departements.geojson')
    metropole = gpd.read_file('/home/doeuvrek/Documents/ouverture_donnees/metropole-version-simplifiee.geojson')    
    ax.add_geometries(departements.geometry, crs = ccrs.PlateCarree(), facecolor='none', edgecolor='black',linewidth=0.8)
    
    ax.add_feature(cfeature.BORDERS.with_scale('10m'))
    ax.add_feature(cfeature.COASTLINE.with_scale('10m'))
    
    # To locate Paris on the map
    ax.scatter(2.35, 48.853, color='black', transform=ccrs.PlateCarree(), linewidths = 1.1) #cordonnes de Paris centre
    ax.text(2.348, 48.859, 'Paris', color='black', transform=ccrs.PlateCarree(), size = 22)
    
    #plt.savefig(img)
    
    
    
    
    
def trace_instant_seuil (date, longitudes, latitudes, values, seuil) :
    """
    Fonction permettant de tracer ou se situe les reflectivite radar superieures a un seuil en un instant donne.
    
    Parameters
    ----------
    date : str (de longueur 12 : AAAAMMDDHHmm)
            date de l'instant (de longueur 12) ou on a regarder si on etait superieur au seuil
    longitudes : float 
            vecteur des longitudes ou on est superieur au seuil
    latitudes : float 
            vecteur des latitudesou on est superieur au seuil
    values : float 
            vecteur des valeurs de reflectivite en dBZ ou on est superieur au seuil
    seuil : float
            valeur du seuil en dBZ que l'on veut regarder'


    """
    start_date=datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]), int(date[8:10]), int(date[10:12])) #mise au format UTC de la date
    
    levels_reflectivite = [1, 3., 5., 7., 10., 15., 20., 30., 50., 70.] #niveaux de reflectivite pour l'echelle de la carte, comme la fonction précédente pour comparer les cartes
    color_levels = [(0, 0, 255/256), (0, 177/256, 251/256), (0, 255/256, 254/256), (0, 222/256, 212/256), (0, 182/256, 163/256),
                  (101/256, 163/256, 62/256), (255/256, 255/256, 65/256), (255/256, 215/256, 58/256), (255/256, 163/256, 49/256),
                  (255/256, 4/256, 34/256)]
                  
    cmap = mcolors.ListedColormap(color_levels, 'reflectivite')
    norm = mcolors.BoundaryNorm(levels_reflectivite, cmap.N)
    
    #creation de la figure
    fig = plt.figure(figsize=(18., 13.))  
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Mercator())
    ax.set_extent(bounds)
    
    #parametres pour le graphique
    values = values
    title = "Reflectivité >" + str(seuil) + "\n" + start_date.strftime('%Y-%m-%d - %H:%M UTC')
    levels=levels_reflectivite
    ticks=levels_reflectivite
    unite='dBZ'
    #nom et chemin pour sauvegarder l'image
    img="/cnrm/ville/USERS/doeuvrek/script_python/figures/reflectivite_instant_seuil_"+str(seuil)+"_"+date+".png"
    
    ax.set_title(title, loc='center', size = 18)
    
    cf = ax.tricontourf(longitudes, latitudes, values, cmap=cmap, levels=levels, norm=norm, transform=ccrs.PlateCarree())
    cb = fig.colorbar(cf, orientation='horizontal', aspect=70, shrink=0.48, pad=0.05,extendrect='False',extend='both',ticks=ticks)
    cb.set_label('('+unite+')', size=15, weight ="bold")
    cb.ax.tick_params(labelsize='medium')
    
    #ajout des departements et du point de Paris sur la carte
    
    departements = gpd.read_file('/home/doeuvrek/Documents/ouverture_donnees/departements.geojson')
    metropole = gpd.read_file('/home/doeuvrek/Documents/ouverture_donnees/metropole-version-simplifiee.geojson')    
    ax.add_geometries(departements.geometry, crs = ccrs.PlateCarree(), facecolor='none', edgecolor='black',linewidth=0.8)
    
    ax.add_feature(cfeature.BORDERS.with_scale('10m'))
    ax.add_feature(cfeature.COASTLINE.with_scale('10m'))
    
    # To locate Paris on the map
    ax.scatter(2.35, 48.853, color='black', transform=ccrs.PlateCarree(), linewidths = 1.1) #cordonnes de Paris centre
    ax.text(2.348, 48.859, 'Paris', color='black', transform=ccrs.PlateCarree(), size = 22)
    
    plt.savefig(img)
    
    
    

    
def trace_compteur_seuil (datedeb, datefin, longitudes, latitudes, compteur, seuil) :
    """
    Fonction permettant de tracer ou se situe les reflectivite radar superieures a un seuil en un instant donne.
    
    Parameters
    ----------
    datedeb : str (de longueur 12 : AAAAMMDDHHmm)
            date de debut (de longueur 12) ou on a regarder si on etait superieur au seuil
            
    datefin : str (de longueur 12 : AAAAMMDDHHmm)
            date de fin (de longueur 12) ou on a regarder si on etait superieur au seuil
            
    longitudes : float 
            vecteur des longitudes ou on est superieur au seuil
            
    latitudes : float
            vecteur des latitudesou on est superieur au seuil
            
    compteur : float
            vecteur des valeurs de reflectivite en dBZ ou on est superieur au seuil sur la periode de temps regarder
    
    seuil : float
            valeur du seuil en dBZ que l'on veut regarder'

    """
    start_date = datetime.datetime(int(datedeb[0:4]), int(datedeb[4:6]), int(datedeb[6:8]), int(datedeb[8:10]), int(datedeb[10:12])) #mise au format UTC de la date
    end_date = datetime.datetime(int(datefin[0:4]), int(datefin[4:6]), int(datefin[6:8]), int(datefin[8:10]), int(datefin[10:12]))
    
    levels_reflectivite = [1, 3., 5., 7., 10., 15., 20., 30., 50., 70.] #niveaux de reflectivite pour l'echelle de la carte, comme la fonction précédente pour comparer les cartes
    color_levels = [(0, 0, 255/256), (0, 177/256, 251/256), (0, 255/256, 254/256), (0, 222/256, 212/256), (0, 182/256, 163/256),
                  (101/256, 163/256, 62/256), (255/256, 255/256, 65/256), (255/256, 215/256, 58/256), (255/256, 163/256, 49/256),
                  (255/256, 4/256, 34/256)]
                  
    cmap = mcolors.ListedColormap(color_levels, 'reflectivite')
    norm = mcolors.BoundaryNorm(levels_reflectivite, cmap.N)
    
    #creation de la figure
    fig = plt.figure(figsize=(18., 13.))  
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Mercator())
    ax.set_extent(bounds)
    
    #parametres pour le graphique
    values = compteur
    title = "Reflectivité >" + str(seuil) + "\n"  + 'de '+ start_date.strftime('%Y-%m-%d - %H:%M UTC') + ' à ' + end_date.strftime('%Y-%m-%d - %H:%M UTC')
    levels=levels_reflectivite
    ticks=levels_reflectivite
    unite='dBZ'
    #nom et chemin pour sauvegarder l'image
    img="/cnrm/ville/USERS/doeuvrek/script_python/figures/reflectivite_compteur_seuil_"+str(seuil)+".png"
    
    ax.set_title(title, loc='center', size = 18)
    
    cf = ax.tricontourf(longitudes, latitudes, values, cmap=cmap, levels=levels, norm=norm, transform=ccrs.PlateCarree())
    cb = fig.colorbar(cf, orientation='horizontal', aspect=70, shrink=0.48, pad=0.05,extendrect='False',extend='both',ticks=ticks)
    cb.set_label('('+unite+')', size=15, weight ="bold")
    cb.ax.tick_params(labelsize='medium')
    
    #ajout des departements et du point de Paris sur la carte
    
    departements = gpd.read_file('/home/doeuvrek/Documents/ouverture_donnees/departements.geojson')
    metropole = gpd.read_file('/home/doeuvrek/Documents/ouverture_donnees/metropole-version-simplifiee.geojson')    
    ax.add_geometries(departements.geometry, crs = ccrs.PlateCarree(), facecolor='none', edgecolor='black',linewidth=0.8)
    
    ax.add_feature(cfeature.BORDERS.with_scale('10m'))
    ax.add_feature(cfeature.COASTLINE.with_scale('10m'))
    
    # To locate Paris on the map
    ax.scatter(2.35, 48.853, color='black', transform=ccrs.PlateCarree(), linewidths = 1.1) #cordonnes de Paris centre
    ax.text(2.348, 48.859, 'Paris', color='black', transform=ccrs.PlateCarree(), size = 22)
    
    plt.savefig(img)