#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 13:33:34 2023

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

import os

import fonctions_tracer as fctt

#%% ouverture et tracer des donnees en un instant, permet de recuperer longitudes et latitudes
ybeg,mbeg,dbeg,hbeg,minbeg=2017,7,9,18,0
datefile = datetime.datetime(ybeg,mbeg,dbeg,hbeg,minbeg)

datadir = datefile.strftime('/cnrm/ville/USERS/doeuvrek/donnees/%Y/%m/%d/')
filename = datefile.strftime('%Y%m%d%H%M.text')

data = pd.read_csv(datadir+filename, skiprows = 23, sep =" ", names = ['Latitudes', 'Longitudes', 'Valeurs', 'Valeurs max'])

latitudes = np.array(data['Latitudes'])
longitudes = np.array(data['Longitudes'])
values = np.array(data['Valeurs'])
values[values==65535] = 0 #valeur hors du domaine

fctt.trace_instant("201707091800", longitudes, latitudes, values)

#%% on veut garder les latitudes et longitudes des donnees superieures a un seuil pour un instant (pour pouvoir les tracer, on pourrait surement garder juste la position dans le tableau longitude/latitude pour optimiser mémoire)
seuil = 10 #en dBZ

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
        compteur[i] =+ 1
    else :
        latitudes_seuil.append(latitudes[i])
        longitudes_seuil.append(longitudes[i])
        values_seuil.append(0)
        
#fct.trace_instant_seuil("201707091800", longitudes, latitudes, values_seuil, seuil)
fctt.trace_instant("201707091800", longitudes, latitudes, compteur)


#%% on essaie de regarder les occurences de seuil sur le domaine pour une annee si les donnees ne sont pas triees
main_path = "/mnt/nfs/d40/ville/USERS/doeuvrek/donnees/2012"
liste_files = os.listdir(main_path)
os.chdir(main_path)

seuil = 40 #en dBZ
compteur = np.zeros(len(latitudes)) #compteur du depassement de seuil (sans se soucier de la duree de l'orage)
#AJOUTER CONDITION SUR ANNEE
#on suppose qu'on a extrait une fois les longitudes et lattitudes, se mettre dans le dossier ou est le file sinon erreur
for file in liste_files :   
    data = pd.read_csv(file, skiprows = 23, sep =" ", names = ['Latitudes', 'Longitudes', 'Valeurs', 'Valeurs max'])# 'Valeurs max']) attention au nb de colonne qui varie si avant ou apres 2018
    values00h = np.array(data['Valeurs'])
    values00h[values00h==65535]=0 #je devrais mettre une condition en fonction du fichier pour gerer les donnees manquantes car pas le meme formalisme
    for i in range(len(values00h)) :  #pour av et ap 2018, mais apres 2018 il s'agit de -40 ou -999 donc comme on regarde les seuils pas d'impact ici
        if values00h[i]>seuil :
            compteur[i] = compteur[i] + 1

#%% tracer des occurences sur le domaine
levelsRR = [2, 5., 9., 15., 20., 25., 30., 40., 50., 64.]
cmapRR_data = [(0, 0, 255/256), (0, 177/256, 251/256), (0, 255/256, 254/256), (0, 222/256, 212/256), (0, 182/256, 163/256),
              (101/256, 163/256, 62/256), (255/256, 255/256, 65/256), (255/256, 215/256, 58/256), (255/256, 163/256, 49/256),
              (255/256, 4/256, 34/256)]

cmapRR = mcolors.ListedColormap(cmapRR_data, 'reflectivite')
normRR = mcolors.BoundaryNorm(levelsRR, cmapRR.N)

bounds = [0.97, 3.7, 47.95, 49.75]

values = compteur
title = "Occurence sur l'année 2013 pour un seuil de " + str(seuil) +'dBZ' 
cmap = cmapRR
levels = levelsRR
norm = normRR
ticks = levelsRR
unite = 'nb de depassements'

fig = plt.figure(figsize=(18., 13.))  
ax = fig.add_subplot(1, 1, 1, projection=ccrs.Mercator())
ax.set_extent(bounds)

ax.set_title(title, loc='center', size = 18)

cf = ax.tricontourf(longitudes, latitudes, values, cmap=cmap, levels=levels, norm=norm, transform=ccrs.PlateCarree())
cb = fig.colorbar(cf, orientation='horizontal', aspect=70, shrink=0.48, pad=0.05,extendrect='False',extend='both',ticks=ticks)
cb.set_label('('+unite+')', size=15, weight ="bold")
cb.ax.tick_params(labelsize='medium')

departements = gpd.read_file('/home/doeuvrek/Documents/ouverture_donnees/departements.geojson')
metropole = gpd.read_file('/home/doeuvrek/Documents/ouverture_donnees/metropole-version-simplifiee.geojson')    
ax.add_geometries(departements.geometry, crs = ccrs.PlateCarree(), facecolor='none', edgecolor='black',linewidth=0.8)

ax.add_feature(cfeature.BORDERS.with_scale('10m'))
ax.add_feature(cfeature.COASTLINE.with_scale('10m'))

# To locate Paris on the map
ax.scatter(2.35, 48.853, color='black', transform=ccrs.PlateCarree(), linewidths = 1.1) #coordonnes de Paris centre
ax.text(2.348, 48.859, 'Paris', color='black', transform=ccrs.PlateCarree(), size = 22)



#%% fonction pour savoir le nombre de jour d'un mois d'une annee  

def nbjoursmois(m,a):
    """Donne le nombre de jours du mois m de l'année a"""
    nj = (0,31,28,31,30,31,30,31,31,30,31,30,31)[m]
    if m==2 and ((a%4==0 and a%100!=0) or a%400==0): # m=février et a=bissextile?
        return nj + 1
    return nj

#%% on essaie de regarder les occurences de seuil sur le domaine pour une annee si les donnees sont triees (relou bcp de conditions)
annee_voulue = 2012
liste_mois = np.arange(4, 11, step = 1)

main_path = "/cnrm/ville/USERS/doeuvrek/donnees/" + str(annee_voulue) + '/'


seuil = 40 #en dBZ
compteur = np.zeros(len(latitudes)) #compteur du depassement de seuil (sans se soucier de la duree de l'orage)
max_mois = np.zeros(7)
min_mois = np.ones(7)

#on suppose qu'on a extrait une fois les longitudes et lattitudes
if annee_voulue<2018 :
    for mois in liste_mois :
        if mois<10 :
            for jour in range(1,nbjoursmois(mois,annee_voulue)+1) :
                if jour<10 :
                    path = main_path + '0' + str(mois) + '/' + '0' + str(jour)
                    for file in os.listdir(path)[0:2] :
                        data = pd.read_csv(path + '/' + file, skiprows = 23, sep =" ", names = ['Latitudes', 'Longitudes', 'Valeurs', 'Valeurs max'])
                        values00h = np.array(data['Valeurs'])
                        values00h[values00h==65535]=0#je devrais mettre une condition en fonction du fichier pour gerer les donnees manquantes car pas le meme formalisme
                        for i in range(len(values00h)) :  #pour av et ap 2018, mais apres 2018 il s'agit de -40 ou -999 donc comme on regarde les seuils pas d'impact ici
                            if values00h[i]>seuil :
                                compteur[i] = compteur[i] + 1
                            if values00h[i]!=0 and min_mois[mois - 4] > np.min(values00h) :
                                min_mois[mois - 4] = np.min(values00h)
                        
                else :
                    path = main_path + '0' + str(mois) + '/' + str(jour)
                    for file in os.listdir(path)[0:2] :
                        data = pd.read_csv(path + '/' + file, skiprows = 23, sep =" ", names = ['Latitudes', 'Longitudes', 'Valeurs', 'Valeurs max'])
                        values00h = np.array(data['Valeurs'])
                        values00h[values00h==65535]=0 #je devrais mettre une condition en fonction du fichier pour gerer les donnees manquantes car pas le meme formalisme
                        for i in range(len(values00h)) :  #pour av et ap 2018, mais apres 2018 il s'agit de -40 ou -999 donc comme on regarde les seuils pas d'impact ici
                            if values00h[i]>seuil :
                                compteur[i] = compteur[i] + 1
                            if values00h[i]!=0 and min_mois[mois - 4] > np.min(values00h) :
                                min_mois[mois - 4] = np.min(values00h)
                                
                if max_mois[mois - 4] < np.max(values00h) :
                    max_mois[mois - 4] = np.max(values00h)
                
        else :
            for jour in range(1,nbjoursmois(mois,annee_voulue)+1) :
                if jour<10 :
                    path = main_path + str(mois) + '/' + '0' + str(jour)
                    for file in os.listdir(path)[0:2] :
                        data = pd.read_csv(path + '/' + file, skiprows = 23, sep =" ", names = ['Latitudes', 'Longitudes', 'Valeurs', 'Valeurs max'])
                        values00h = np.array(data['Valeurs'])
                        values00h[values00h==65535]=0 #je devrais mettre une condition en fonction du fichier pour gerer les donnees manquantes car pas le meme formalisme
                        for i in range(len(values00h)) :  #pour av et ap 2018, mais apres 2018 il s'agit de -40 ou -999 donc comme on regarde les seuils pas d'impact ici
                            if values00h[i]>seuil :
                                compteur[i] = compteur[i] + 1
                            if values00h[i]!=0 and min_mois[mois - 4] > np.min(values00h) :
                                min_mois[mois - 4] = np.min(values00h)
                else :
                    path = main_path + str(mois) + '/' + str(jour)
                    for file in os.listdir(path)[0:2] :
                        data = pd.read_csv(path + '/' + file, skiprows = 23, sep =" ", names = ['Latitudes', 'Longitudes', 'Valeurs', 'Valeurs max'])
                        values00h = np.array(data['Valeurs'])
                        values00h[values00h==65535]=0 #je devrais mettre une condition en fonction du fichier pour gerer les donnees manquantes car pas le meme formalisme
                        for i in range(len(values00h)) :  #pour av et ap 2018, mais apres 2018 il s'agit de -40 ou -999 donc comme on regarde les seuils pas d'impact ici
                            if values00h[i]>seuil :
                                compteur[i] = compteur[i] + 1
                                
                    if max_mois[mois - 4] < np.max(values00h) :
                        max_mois[mois - 4] = np.max(values00h)
                        
else :
    for mois in liste_mois :
        if mois<10 :
            for jour in range(1,nbjoursmois(mois,annee_voulue)+1) :
                if jour<10 :
                    path = main_path + '0' + str(mois) + '/' + '0' + str(jour)
                    for file in os.listdir(path)[0:2] :
                        data = pd.read_csv(path + '/' + file, skiprows = 23, sep =" ", names = ['Latitudes', 'Longitudes', 'Valeurs'])
                        values00h = np.array(data['Valeurs'])
                        values00h[values00h==65535]=0 #je devrais mettre une condition en fonction du fichier pour gerer les donnees manquantes car pas le meme formalisme
                        for i in range(len(values00h)) :  #pour av et ap 2018, mais apres 2018 il s'agit de -40 ou -999 donc comme on regarde les seuils pas d'impact ici
                            if values00h[i]>seuil :
                                compteur[i] = compteur[i] + 1
                            if values00h[i]!=0 and min_mois[mois - 4] > np.min(values00h) :
                                min_mois[mois - 4] = np.min(values00h)
                else :
                    path = main_path + '0' + str(mois) + '/' + str(jour)
                    for file in os.listdir(path)[0:2] :
                        data = pd.read_csv(path + '/' + file, skiprows = 23, sep =" ", names = ['Latitudes', 'Longitudes', 'Valeurs'])
                        values00h = np.array(data['Valeurs'])
                        values00h[values00h==65535]=0 #je devrais mettre une condition en fonction du fichier pour gerer les donnees manquantes car pas le meme formalisme
                        for i in range(len(values00h)) :  #pour av et ap 2018, mais apres 2018 il s'agit de -40 ou -999 donc comme on regarde les seuils pas d'impact ici
                            if values00h[i]>seuil :
                                compteur[i] = compteur[i] + 1
                            if values00h[i]!=0 and min_mois[mois - 4] > np.min(values00h) :
                                min_mois[mois - 4] = np.min(values00h)
                                
                if max_mois[mois - 4] < np.max(values00h) :
                    max_mois[mois - 4] = np.max(values00h)
                    
                    
        else :
            for jour in range(1,nbjoursmois(mois,annee_voulue)+1) :
                if jour<10 :
                    path = main_path + str(mois) + '/' + '0' + str(jour)
                    for file in os.listdir(path)[0:2] :
                        data = pd.read_csv(path + '/' + file, skiprows = 23, sep =" ", names = ['Latitudes', 'Longitudes', 'Valeurs'])
                        values00h = np.array(data['Valeurs'])
                        values00h[values00h==65535]=0 #je devrais mettre une condition en fonction du fichier pour gerer les donnees manquantes car pas le meme formalisme
                        for i in range(len(values00h)) :  #pour av et ap 2018, mais apres 2018 il s'agit de -40 ou -999 donc comme on regarde les seuils pas d'impact ici
                            if values00h[i]>seuil :
                                compteur[i] = compteur[i] + 1
                            if values00h[i]!=0 and min_mois[mois - 4] > np.min(values00h) :
                                min_mois[mois - 4] = np.min(values00h)
                else :
                    path = main_path + str(mois) + '/' + str(jour)
                    for file in os.listdir(path)[0:2] :
                        data = pd.read_csv(path + '/' + file, skiprows = 23, sep =" ", names = ['Latitudes', 'Longitudes', 'Valeurs'])
                        values00h = np.array(data['Valeurs'])
                        values00h[values00h==65535]=0 #je devrais mettre une condition en fonction du fichier pour gerer les donnees manquantes car pas le meme formalisme
                        for i in range(len(values00h)) :  #pour av et ap 2018, mais apres 2018 il s'agit de -40 ou -999 donc comme on regarde les seuils pas d'impact ici
                            if values00h[i]>seuil :
                                compteur[i] = compteur[i] + 1
                            if values00h[i]!=0 and min_mois[mois - 4] > np.min(values00h) :
                                min_mois[mois - 4] = np.min(values00h)
                                
                if max_mois[mois - 4] < np.max(values00h) :
                    max_mois[mois - 4] = np.max(values00h)

      

#%% tracer des occurences sur le domaine
levelsRR = [2, 5., 9., 15., 20., 25., 30., 40., 50., 64.]
cmapRR_data = [(0, 0, 255/256), (0, 177/256, 251/256), (0, 255/256, 254/256), (0, 222/256, 212/256), (0, 182/256, 163/256),
              (101/256, 163/256, 62/256), (255/256, 255/256, 65/256), (255/256, 215/256, 58/256), (255/256, 163/256, 49/256),
              (255/256, 4/256, 34/256)]

cmapRR = mcolors.ListedColormap(cmapRR_data, 'reflectivite')
normRR = mcolors.BoundaryNorm(levelsRR, cmapRR.N)

bounds = [0.97, 3.7, 47.95, 49.75]

values = compteur
title = "Occurence sur l'année" + str(annee_voulue) + 'pour un seuil de' + str(seuil) +'dBZ' 
cmap = cmapRR
levels = levelsRR
norm = normRR
ticks = levelsRR
unite = 'nb de depassements'

fig = plt.figure(figsize=(18., 13.))  
ax = fig.add_subplot(1, 1, 1, projection=ccrs.Mercator())
ax.set_extent(bounds)

ax.set_title(title, loc='center', size = 18)

cf = ax.tricontourf(longitudes, latitudes, values, cmap=cmap, levels=levels, norm=norm, transform=ccrs.PlateCarree())
cb = fig.colorbar(cf, orientation='horizontal', aspect=70, shrink=0.48, pad=0.05,extendrect='False',extend='both',ticks=ticks)
cb.set_label('('+unite+')', size=15, weight ="bold")
cb.ax.tick_params(labelsize='medium')

departements = gpd.read_file('/home/doeuvrek/Documents/ouverture_donnees/departements.geojson')
metropole = gpd.read_file('/home/doeuvrek/Documents/ouverture_donnees/metropole-version-simplifiee.geojson')    
ax.add_geometries(departements.geometry, crs = ccrs.PlateCarree(), facecolor='none', edgecolor='black',linewidth=0.8)

ax.add_feature(cfeature.BORDERS.with_scale('10m'))
ax.add_feature(cfeature.COASTLINE.with_scale('10m'))

# To locate Paris on the map
ax.scatter(2.35, 48.853, color='black', transform=ccrs.PlateCarree(), linewidths = 1.1) #coordonnes de Paris centre
ax.text(2.348, 48.859, 'Paris', color='black', transform=ccrs.PlateCarree(), size = 22)

#%% max, min ... par mois par annee
mois_lettre = ['avril', 'mai', 'juin', 'juillet', 'aout', 'septembre', 'octobre']
plt.plot(mois_lettre ,max_mois, label = "max par mois")
plt.title('Maximum par mois pour annee ' + str(annee_voulue))
plt.legend()


#%% on regarde les occurences de seuil sur toutes les annees de donnees triees sans se soucier de la duree de l'orage
annee_voulue = 2013
liste_mois = np.arange(4, 11, step = 1)
liste_annee = np.arange(2011, 2018, step = 1)

seuil = 40 #en dBZ
compteur = np.zeros((len(latitudes), len(liste_annee)) )#compteur du depassement de seuil (sans se soucier de la duree de l'orage)

#on suppose qu'on a extrait une fois les longitudes et lattitudes
for annee in liste_annee :
    main_path = "/cnrm/ville/USERS/doeuvrek/donnees/" + str(annee) + '/'
    if annee<2018 :
        for mois in liste_mois :
            if mois<10 :
                for jour in range(1,nbjoursmois(mois,annee)+1) :
                    if jour<10 :
                        path = main_path + '0' + str(mois) + '/' + '0' + str(jour)
                        for file in os.listdir(path)[0:2] :
                            data = pd.read_csv(path + '/' + file, skiprows = 23, sep =" ", names = ['Latitudes', 'Longitudes', 'Valeurs', 'Valeurs max'])
                            values00h = np.array(data['Valeurs'])
                            values00h[values00h==65535]=0 #je devrais mettre une condition en fonction du fichier pour gerer les donnees manquantes car pas le meme formalisme
                            for i in range(len(values00h)) :  #pour av et ap 2018, mais apres 2018 il s'agit de -40 ou -999 donc comme on regarde les seuils pas d'impact ici
                                if values00h[i]>seuil :
                                    compteur[i,annee-2011] = compteur[i, annee-2011] + 1 #annee - 2011 : pour avoir le bon indice de l'annee
                    else :
                        path = main_path + '0' + str(mois) + '/' + str(jour)
                        for file in os.listdir(path)[0:2] :
                            data = pd.read_csv(path + '/' + file, skiprows = 23, sep =" ", names = ['Latitudes', 'Longitudes', 'Valeurs', 'Valeurs max'])
                            values00h = np.array(data['Valeurs'])
                            values00h[values00h==65535]=0 #je devrais mettre une condition en fonction du fichier pour gerer les donnees manquantes car pas le meme formalisme
                            for i in range(len(values00h)) :  #pour av et ap 2018, mais apres 2018 il s'agit de -40 ou -999 donc comme on regarde les seuils pas d'impact ici
                                if values00h[i]>seuil :
                                    compteur[i,annee-2011] = compteur[i, annee-2011] + 1
            else :
                for jour in range(1,nbjoursmois(mois,annee_voulue)+1) :
                    if jour<10 :
                        path = main_path + str(mois) + '/' + '0' + str(jour)
                        for file in os.listdir(path)[0:2] :
                            data = pd.read_csv(path + '/' + file, skiprows = 23, sep =" ", names = ['Latitudes', 'Longitudes', 'Valeurs', 'Valeurs max'])
                            values00h = np.array(data['Valeurs'])
                            values00h[values00h==65535]=0 #je devrais mettre une condition en fonction du fichier pour gerer les donnees manquantes car pas le meme formalisme
                            for i in range(len(values00h)) :  #pour av et ap 2018, mais apres 2018 il s'agit de -40 ou -999 donc comme on regarde les seuils pas d'impact ici
                                if values00h[i]>seuil :
                                    compteur[i,annee-2011] = compteur[i, annee-2011] + 1
                    else :
                        path = main_path + str(mois) + '/' + str(jour)
                        for file in os.listdir(path)[0:2] :
                            data = pd.read_csv(path + '/' + file, skiprows = 23, sep =" ", names = ['Latitudes', 'Longitudes', 'Valeurs', 'Valeurs max'])
                            values00h = np.array(data['Valeurs'])
                            values00h[values00h==65535]=0 #je devrais mettre une condition en fonction du fichier pour gerer les donnees manquantes car pas le meme formalisme
                            for i in range(len(values00h)) :  #pour av et ap 2018, mais apres 2018 il s'agit de -40 ou -999 donc comme on regarde les seuils pas d'impact ici
                                if values00h[i]>seuil :
                                    compteur[i,annee-2011] = compteur[i, annee-2011] + 1
                            
    else :
        for mois in liste_mois :
            if mois<10 :
                for jour in range(1,nbjoursmois(mois,annee_voulue)+1) :
                    if jour<10 :
                        path = main_path + '0' + str(mois) + '/' + '0' + str(jour)
                        for file in os.listdir(path)[0:2] :
                            data = pd.read_csv(path + '/' + file, skiprows = 23, sep =" ", names = ['Latitudes', 'Longitudes', 'Valeurs'])
                            values00h = np.array(data['Valeurs'])
                            values00h[values00h==65535]=0 #je devrais mettre une condition en fonction du fichier pour gerer les donnees manquantes car pas le meme formalisme
                            for i in range(len(values00h)) :  #pour av et ap 2018, mais apres 2018 il s'agit de -40 ou -999 donc comme on regarde les seuils pas d'impact ici
                                if values00h[i]>seuil :
                                    compteur[i,annee-2011] = compteur[i, annee-2011] + 1
                    else :
                        path = main_path + '0' + str(mois) + '/' + str(jour)
                        for file in os.listdir(path)[0:2] :
                            data = pd.read_csv(path + '/' + file, skiprows = 23, sep =" ", names = ['Latitudes', 'Longitudes', 'Valeurs'])
                            values00h = np.array(data['Valeurs'])
                            values00h[values00h==65535]=0 #je devrais mettre une condition en fonction du fichier pour gerer les donnees manquantes car pas le meme formalisme
                            for i in range(len(values00h)) :  #pour av et ap 2018, mais apres 2018 il s'agit de -40 ou -999 donc comme on regarde les seuils pas d'impact ici
                                if values00h[i]>seuil :
                                    compteur[i,annee-2011] = compteur[i, annee-2011] + 1
            else :
                for jour in range(1,nbjoursmois(mois,annee_voulue)+1) :
                    if jour<10 :
                        path = main_path + str(mois) + '/' + '0' + str(jour)
                        for file in os.listdir(path)[0:2] :
                            data = pd.read_csv(path + '/' + file, skiprows = 23, sep =" ", names = ['Latitudes', 'Longitudes', 'Valeurs'])
                            values00h = np.array(data['Valeurs'])
                            values00h[values00h==65535]=0 #je devrais mettre une condition en fonction du fichier pour gerer les donnees manquantes car pas le meme formalisme
                            for i in range(len(values00h)) :  #pour av et ap 2018, mais apres 2018 il s'agit de -40 ou -999 donc comme on regarde les seuils pas d'impact ici
                                if values00h[i]>seuil :
                                    compteur[i,annee-2011] = compteur[i, annee-2011] + 1
                    else :
                        path = main_path + str(mois) + '/' + str(jour)
                        for file in os.listdir(path)[0:2] :
                            data = pd.read_csv(path + '/' + file, skiprows = 23, sep =" ", names = ['Latitudes', 'Longitudes', 'Valeurs'])
                            values00h = np.array(data['Valeurs'])
                            values00h[values00h==65535]=0 #je devrais mettre une condition en fonction du fichier pour gerer les donnees manquantes car pas le meme formalisme
                            for i in range(len(values00h)) :  #pour av et ap 2018, mais apres 2018 il s'agit de -40 ou -999 donc comme on regarde les seuils pas d'impact ici
                                if values00h[i]>seuil :
                                    compteur[i,annee-2011] = compteur[i, annee-2011] + 1
        

#%%
levelsRR = [0, 1., 2., 3., 4., 5., 6., 7., 10., 44.]
cmapRR_data = [(0, 0, 255/256), (0, 177/256, 251/256), (0, 255/256, 254/256), (0, 222/256, 212/256), (0, 182/256, 163/256),
              (101/256, 163/256, 62/256), (255/256, 255/256, 65/256), (255/256, 215/256, 58/256), (255/256, 163/256, 49/256),
              (255/256, 4/256, 34/256)]

cmapRR = mcolors.ListedColormap(cmapRR_data, 'reflectivite')
normRR = mcolors.BoundaryNorm(levelsRR, cmapRR.N)

bounds = [0.97, 3.7, 47.95, 49.75]

for i in np.arange(7) :
    values = compteur[:,i]
    title = 'Occurence sur annee 201' + str(i+1) + ' pour un seuil de' + str(seuil) +'dBZ' 
    cmap = cmapRR
    levels = levelsRR
    norm = normRR
    ticks = levelsRR
    unite = 'nb de depassements'
    
    fig = plt.figure(figsize=(18., 13.))  
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Mercator())
    ax.set_extent(bounds)
    
    ax.set_title(title, loc='center', size = 18)
    
    cf = ax.tricontourf(longitudes, latitudes, values, cmap=cmap, levels=levels, norm=norm, transform=ccrs.PlateCarree())
    cb = fig.colorbar(cf, orientation='horizontal', aspect=70, shrink=0.48, pad=0.05,extendrect='False',extend='both',ticks=ticks)
    cb.set_label('('+unite+')', size=15, weight ="bold")
    cb.ax.tick_params(labelsize='medium')
    
    departements = gpd.read_file('/home/doeuvrek/Documents/ouverture_donnees/departements.geojson')
    metropole = gpd.read_file('/home/doeuvrek/Documents/ouverture_donnees/metropole-version-simplifiee.geojson')    
    ax.add_geometries(departements.geometry, crs = ccrs.PlateCarree(), facecolor='none', edgecolor='black',linewidth=0.8)
    
    ax.add_feature(cfeature.BORDERS.with_scale('10m'))
    ax.add_feature(cfeature.COASTLINE.with_scale('10m'))
    
    # To locate Paris on the map
    ax.scatter(2.35, 48.853, color='black', transform=ccrs.PlateCarree(), linewidths = 1.1) #coordonnes de Paris centre
    ax.text(2.348, 48.859, 'Paris', color='black', transform=ccrs.PlateCarree(), size = 22)
    plt.show()

#%%
plt.plot(1,1)
















