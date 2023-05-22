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
from PIL import Image

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as mcolors

import fonctions as fct

#on definit les bornes du domaines sur lesquelles seront trace toutes les courbes
bounds = [0.97, 3.7, 47.95, 49.75]

import os
os.system('cd /mnt/nfs/d40/ville/USERS/doeuvrek/stage_clim_Paris/zonage')
import fonctions_zonage as fc
import metpy
from metpy.units import units
import sys

#%%
    
def trace (datedeb, datefin, longitudes, latitudes, values, seuil, mode, annee, mois) :
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
    
    
    start_date =  fct.str2date(datedeb) #datetime.datetime(int(datedeb[0:4]), int(datedeb[4:6]), int(datedeb[6:8]), int(datedeb[8:10]), int(datedeb[10:12])) #mise au format UTC de la date
    end_date = fct.str2date(datefin) #datetime.datetime(int(datefin[0:4]), int(datefin[4:6]), int(datefin[6:8]), int(datefin[8:10]), int(datefin[10:12]))
    

    
    if mode == 'val' :
        if seuil==0 : #on trace les donnees brutes en un instant
             print('1')
             #levels_reflectivite = np.arange(4.3, 6, 0.1) #pour les moyennes
             levels_reflectivite = [8, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 64, 66]#[7, 15, 23, 33, 40, 45, 50, 55, 60, 65] #niveaux de reflectivite pour l'echelle de la carte
             title="Reflectivité le \n"+start_date.strftime('%Y-%m-%d - %H:%M UTC')
             #title='Moyenne des précipitations de \n' + start_date.strftime('%Y-%m-%d - %H:%M UTC') + ' à ' + end_date.strftime('%Y-%m-%d - %H:%M UTC')
             img="/cnrm/ville/USERS/doeuvrek/script_python/figures/reflectivite_instant_"+datedeb+".png"  #nom et chemin pour sauvegarder l'image
             unite='dBZ'
        elif seuil!=0 :
            if datedeb == datefin : #on trace les donnees seuillees en un instant
                print('2') 
                levels_reflectivite =  [7, 15, 23, 33, 40, 45, 50, 55, 60, 65] 
                title="Reflectivité > " + str(seuil) + "dBZ \n" + start_date.strftime('%Y-%m-%d - %H:%M UTC')
                img="/cnrm/ville/USERS/doeuvrek/script_python/figures/reflectivite_seuil_"+datedeb+".png"
                unite='dBZ'
                
            elif datedeb != datefin : #on trace les donnees seuillees sur la periode datedeb datefin
                print('3')
                levels_reflectivite =  [7, 15, 23, 33, 40, 45, 50, 55, 60, 65] 
                title="Reflectivité > " + str(seuil) + "dBZ de \n" + start_date.strftime('%Y-%m-%d - %H:%M UTC') + ' à ' + end_date.strftime('%Y-%m-%d - %H:%M UTC')
                img="/cnrm/ville/USERS/doeuvrek/script_python/figures/reflectivite_seuil_de_"+datedeb+"_a_"+datefin+".png"  
                unite='dBZ'
        
    elif  mode == 'val' and seuil!=0  and datedeb != datefin : #on trace les donnees seuillees sur la periode datedeb datefin
        print('3bis')
        levels_reflectivite =  [7, 15, 23, 33, 40, 45, 50, 55, 60, 65] 
        title="Reflectivité > " + str(seuil) + "dBZ de \n" + start_date.strftime('%Y-%m-%d - %H:%M UTC') + ' à ' + end_date.strftime('%Y-%m-%d - %H:%M UTC')
        img="/cnrm/ville/USERS/doeuvrek/script_python/figures/reflectivite_seuil_de_"+datedeb+"_a_"+datefin+".png"
        unite='dBZ'
         
    elif mode == 'compteur' :
        if datedeb!=datefin : #on trace combien de fois on a depasse le seuil sur la periode datedeb datefin
            print('4')
            levels_reflectivite = np.arange(100,400,20)
            #title = "Compteur de reflectivité > " + str(seuil) + "dBZ de \n"  + start_date.strftime('%Y-%m-%d - %H:%M UTC') + ' à ' + end_date.strftime('%Y-%m-%d - %H:%M UTC')
            title = "Compteur de reflectivité > " + str(seuil) + "dBZ  pour l'année " + annee #+ ' pour ' + mois 
            #title = "Compteur de reflectivité > " + str(seuil) + "dBZ sur " + annee
            #img="/cnrm/ville/USERS/doeuvrek/script_python/figures/reflectivite_compteur_seuil_"+str(seuil)+'_periode_de_'+datedeb+ "_a_"+datefin+".png"   #nom et chemin pour sauvegarder l'image
            img="/cnrm/ville/USERS/doeuvrek/stage_clim_Paris/script_python/figures/compteur_annee/seuil_40/compteur_reflectivite_max_"+str(seuil)+'_'+str(annee)+'_echelle3.png' #_10ans_' + str(mois)+'_zoom.png'#+ mois +'.png'
            unite='nb de depassements'
        else : #on trace combien de fois on a  depassesr le seuil en un instant
            print('5') 
            levels_reflectivite = np.arange(0,25,1) #np.arange(1, 51, 5) 
            title = "Compteur de reflectivité > " + str(seuil) + "dBZ \n" + start_date.strftime('%Y-%m-%d - %H:%M UTC')
            img="/cnrm/ville/USERS/doeuvrek/script_python/figures/reflectivite_compteur_seuil_"+str(seuil)+'_le_'+datedeb+".png"
            unite='nb de depassements'

    cmap = 'jet'#palette de couleur
    
    """zoom = True
    lat_paris = 48.853
    lon_paris = 2.35
        
    if zoom == True:
        #print('T')
        zoom_Paris = 0.3
    else:
        zoom_Paris = 0.5
            
    latmin, latmax = lat_paris-1.7*zoom_Paris, lat_paris+1.7*zoom_Paris   #lat_paris-1.7*zoom_Paris, lat_paris+1.7*zoom_Paris
    lonmin, lonmax = lon_paris-2.15*zoom_Paris, lon_paris+2.15*zoom_Paris #lon_paris-2.15*zoom_Paris, lon_paris+2.15*zoom_Paris
    
    bounds = [lonmin, lonmax, latmin, latmax]
    #print(bounds)"""
        
    #norm = mpl.colors.Normalize(vmin=np.min(values), vmax=np.max(values))    
    
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
    cb = fig.colorbar(cf, orientation='horizontal', aspect=70, shrink=0.48, pad=0.05,extendrect='True',extend='both',ticks=ticks)
    cb.set_label('('+unite+')', size=15, weight ="bold")
    cb.ax.tick_params(labelsize='medium')
    
    #permet de mettre d'une certaine couleur les valeurs depassant la palette de couleur
    cf.cmap.set_over('brown') 
    cf.cmap.set_under('darkblue')
    
    #cf.cmap.set_over('0.25')
    #cf.cmap.set_under('0.75')
    
    #ajout des departements et du point de Paris sur la carte
    departements = gpd.read_file('/home/doeuvrek/Documents/ouverture_donnees/departements.geojson')
    ax.add_geometries(departements.geometry, crs = ccrs.PlateCarree(), facecolor='none', edgecolor='black',linewidth=0.8)
    
    ax.add_feature(cfeature.BORDERS.with_scale('10m'))
    ax.add_feature(cfeature.COASTLINE.with_scale('10m'))
    
    #pour mettre la ville de Paris
    ax.scatter(2.35, 48.853, color='black', transform=ccrs.PlateCarree(), linewidths = 1.1) #cordonnes de Paris centre
    ax.text(2.348, 48.859, 'Paris', color='black', transform=ccrs.PlateCarree(), size = 22)
    
    #plt.savefig(img)
    """
    im = Image.open(img)
    largeur, hauteur = im.size
    im_crop = im.crop((largeur*0.28, hauteur*0.06,0.72*largeur, 0.82*hauteur))
    im_crop.save(img)"""
    
    
    
    
def zonage (secteur,ut_final,  vt_final) :

    lat_centre = 48.853
    lon_centre = 2.35
    zoom=False
    
    #données de vent (U vent zonal et V vent meridien) pour determiner la direction du vent et la direction des secteurs ensuite
    #ut_final = -0.3
    #vt_final= 1
    
    ybeg,mbeg,dbeg,hbeg,minbeg=2017,7,9,17,0
    start_date=datetime.datetime(ybeg,mbeg,dbeg,hbeg,minbeg)
    
    currentdate = start_date
    
    #on défini la liste des angles pour former notre demi-cercle en fonction du secteur voulu (upwind ou downwind)
    
    if secteur == 'D':
        angle_initial = metpy.calc.wind_direction(ut_final*units('m/s'), vt_final*units('m/s'), convention='to').magnitude
    elif secteur == 'DL':
        angle_initial = metpy.calc.wind_direction(ut_final*units('m/s'), vt_final*units('m/s'), convention='to').magnitude - 60
    elif secteur == 'DR':
        angle_initial = metpy.calc.wind_direction(ut_final*units('m/s'), vt_final*units('m/s'), convention='to').magnitude + 60
    elif secteur == 'U':
        angle_initial = metpy.calc.wind_direction(ut_final*units('m/s'), vt_final*units('m/s'), convention='to').magnitude + 180.
    elif secteur == 'UL':
        angle_initial = metpy.calc.wind_direction(ut_final*units('m/s'), vt_final*units('m/s'), convention='to').magnitude + 180. + 60
    elif secteur == 'UR':
        angle_initial = metpy.calc.wind_direction(ut_final*units('m/s'), vt_final*units('m/s'), convention='to').magnitude + 180. - 60
    elif secteur == 'C':
        angle_initial = 0
   
    latitudes, longitudes, values = fct.valeur(currentdate.strftime('%Y%m%d%H%M'))
    
    #distinction entre cercle et autres secteurs : 
    if secteur == 'C':
        indices_secteur = fc.extract_data_polygon(values, longitudes, latitudes, angle_initial-180, angle_initial+180, secteur, lat_centre, lon_centre)
    else:
        indices_secteur = fc.extract_data_polygon(values, longitudes, latitudes, angle_initial-30, angle_initial+30, secteur, lat_centre, lon_centre)    
   
    
    values_sector = values[indices_secteur]
    longitudes_sector = longitudes[indices_secteur]
    latitudes_sector = latitudes[indices_secteur]
    
    print('tracer cartes')
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Mercator())
    
    
    
    if zoom == False:
       zoom_Paris = 0.8
    else:
       zoom_Paris = 0.5 #0.5
    
    
    lat_min, lat_max = lat_centre-1.7*zoom_Paris, lat_centre+1.7*zoom_Paris   #lat_paris-1.7*zoom_Paris, lat_paris+1.7*zoom_Paris
    lon_min, lon_max = lon_centre-2.15*zoom_Paris, lon_centre+2.15*zoom_Paris #lon_paris-2.15*zoom_Paris, lon_paris+2.15*zoom_Paris
    bounds = [lon_min, lon_max, lat_min, lat_max]
    
    ax.set_extent(bounds)
    
    
    titre = 'Variable in sector '+ secteur + '\n'
    plt.title(titre, loc='center', size = 19)
    
    departements = gpd.read_file('/home/doeuvrek/Documents/ouverture_donnees/departements.geojson')
    metropole = gpd.read_file('/home/doeuvrek/Documents/ouverture_donnees/metropole-version-simplifiee.geojson')

    
    #plt.legend(loc='upper left',fontsize = 14)
    
    ax.add_geometries(departements.geometry, crs = ccrs.PlateCarree(), facecolor='none', edgecolor='black',linewidth=1)
    ax.add_geometries(metropole.geometry, crs = ccrs.PlateCarree(), facecolor='none', edgecolor='black',linewidth=1)
    ax.scatter(list(longitudes_sector), list(latitudes_sector),c=values_sector, cmap='jet', vmin=1, vmax=10, transform=ccrs.PlateCarree(), s = 5) #cordonnes de Paris centre
    
    return (indices_secteur)













    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     