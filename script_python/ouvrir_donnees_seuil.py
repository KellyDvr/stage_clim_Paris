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

import fonctions as fct
import fonctions_tracer as fctt

import time

#%% ouverture et tracer des donnees en un instant, permet de recuperer longitudes et latitudes

seuil = 0 #necessaire pour utiliser la fonction fctt.trace

ybeg,mbeg,dbeg,hbeg,minbeg=2017,7,9,18,0
datefile = datetime.datetime(ybeg,mbeg,dbeg,hbeg,minbeg)
date = datefile.strftime('%Y%m%d%H%M')
print(date)


latitudes, longitudes, values = fct.valeur(date)
print(values)
fctt.trace(date, date , longitudes, latitudes, values, seuil, 'val')

n = len(latitudes) #on recupere la longueur des latitudes (meme que celle des donnees)
#%% on veut garder les latitudes et longitudes des donnees superieures a un seuil pour un instant
#(pour pouvoir les tracer, on pourrait surement garder juste la position dans le tableau longitude/latitude pour optimiser mémoire)
seuil = 40 #en dBZ

latitudes_seuil, longitudes_seuil, values_seuil, compteur = fct.seuil_instant(date, seuil)
        
fctt.trace("201707091800", "201707091800", longitudes, latitudes, values_seuil, seuil, 'val')
fctt.trace("201707091800", "201707091800", longitudes, latitudes, compteur, seuil,'compteur')

#%%on regarde les depassement de seuil sur une periode (quelques heures)
seuil = 40

#periode voulue
datedeb = '201707091500'
datefin = '201707092200'
compteur = fct.seuil_mois(seuil , datedeb, datefin, n)

#tracer de la ou on depasse le seuil avec la valeur
#fctt.trace(datedeb, datefin , lon_seuil, lat_seuil, val_seuil, seuil, 'val')
#tracer du nb de fois ou on depasse le seuil 
fctt.trace(datedeb, datefin, longitudes, latitudes, compteur, seuil, 'compteur')

#%%on regarde les depassement de seuil sur une periode (quelques jours)
seuil = 40

#periode voulue
datedeb = '201707031500'
datefin = '201707302200'
compteur = fct.seuil_mois(seuil , datedeb, datefin, n)

#tracer de la ou on depasse le seuil avec la valeur
#fctt.trace(datedeb, datefin , lon_seuil, lat_seuil, val_seuil, seuil, 'val')
#tracer du nb de fois ou on depasse le seuil 
fctt.trace(datedeb, datefin, longitudes, latitudes, compteur, seuil, 'compteur')

#%%on regarde les depassement de seuil sur une periode (une annee)
tps1 = time.clock()

seuil = 40

compteur_mois = np.zeros((n, 8))

#boucle sur les mois
for i in [4, 5, 6, 7, 8, 9, 10] :
    if i < 10 :
        datedeb = '20170' +  str(i) + '010000'
        datefin = '20170'+ str(i) + '302345'
    else :
        datedeb = '2017' + str(i) + '010000'
        datefin = '2017'+ str(i) + '302345'
    compteur_mois[:,(i-4)] = fct.seuil_mois(seuil , datedeb, datefin, n)
    
tps2 = time.clock()

print('temps execution : ' + tps2-tps1)

compteur = np.sum(compteur_mois, axis = 1)    


#tracer de la ou on depasse le seuil avec la valeur
#fctt.trace(datedeb, datefin , lon_seuil, lat_seuil, val_seuil, seuil, 'val')
#tracer du nb de fois ou on depasse le seuil 
fctt.trace(datedeb, datefin, longitudes, latitudes, compteur, seuil, 'compteur')










