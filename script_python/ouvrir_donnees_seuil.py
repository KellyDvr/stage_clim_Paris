#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 13:33:34 2023

@author: doeuvrek
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import datetime

import fonctions as fct
import fonctions_tracer as fctt

import time

#%% ouverture et tracer des donnees en un instant, permet de recuperer longitudes et latitudes

seuil = 0 #necessaire pour utiliser la fonction fctt.trace

ybeg,mbeg,dbeg,hbeg,minbeg=2017,7,9,20,0
datefile = datetime.datetime(ybeg,mbeg,dbeg,hbeg,minbeg)
date = datefile.strftime('%Y%m%d%H%M')
print(date)

latitudes, longitudes, values = fct.valeur(date)
print(values)

liste_val = values.tolist()

#fctt.trace(date, date , longitudes, latitudes, values, seuil, 'val', 2017, 'av')

n = 38148 #on recupere la longueur des latitudes (meme que celle des donnees)
#%% on veut garder les latitudes et longitudes des donnees superieures a un seuil pour un instant
#(pour pouvoir les tracer, on pourrait surement garder juste la position dans le tableau longitude/latitude pour optimiser mémoire)
seuil = 40 #en dBZ

values_seuil, compteur = fct.seuil_instant(seuil, date, n, 4)
        
fctt.trace("201707091800", "201707091800", longitudes, latitudes, values_seuil, seuil, 'val', '2017', 'juil')
fctt.trace("201707091800", "201707091800", longitudes, latitudes, compteur, seuil,'compteur', '2017', 'juil')

#%%on regarde les depassements de seuil sur une periode (quelques heures)
seuil = 40

#periode voulue
datedeb = '201707091500'
datefin = '201707092345'
compteur = fct.seuil_periode(seuil , datedeb, datefin, n, 1)

#tracer du nb de fois ou on depasse le seuil 
fctt.trace(datedeb, datefin, longitudes, latitudes, compteur, seuil, 'compteur', '2017', 'avril')


#%%on regarde les depassements de seuil sur une periode (10 jours)
seuil = 40

#periode voulue
datedeb = '201707041500'
datefin = '201707141515'

#tps1 = time.time()
compteur_mois = fct.seuil_periode(seuil , datedeb, datefin, n, 1)
#tps2 = time.time()

print('temps execution : ' + str(round(tps2-tps1, 2))) #attention unite

#tracer du nb de fois ou on depasse le seuil 
fctt.trace(datedeb, datefin, longitudes, latitudes, compteur_mois, seuil, 'compteur', '2017', 'av')

#%%on regarde les depassements de seuil sur une periode (2 mois)

datedeb = '201706010000'
datefin = '201708010000'

seuil = 40
tps1 = time.time()
compteur_mois2 = fct.seuil_periode(seuil , datedeb, datefin, n, 1)
tps2 = time.time()

print('temps execution : ' + str(round(tps2-tps1, 2)) + "s") #attention unite

#attention à l'echelle du nb de depassements dans la fonction
fctt.trace(datedeb, datefin, longitudes, latitudes, compteur_mois2, seuil, 'compteur')

#%%on regarde les depassements de seuil sur une periode (une annee)

datedeb = '201704010000'
datefin = '201711010000'

seuil = 40

tps1 = time.time()
compteur_annee = fct.seuil_periode(seuil , datedeb, datefin, n, 1)
tps2 = time.time()

print('temps execution : ' + str(round(tps2-tps1, 2)) + "s") #attention unite

#attention à l'echelle du nb de depassements dans la fonction
fctt.trace(datedeb, datefin, longitudes, latitudes, compteur_annee, seuil, 'compteur')


#%% moyenne des reflectivites sur JJA 2017

datedeb = '201706010000'
datefin = '201708312345' 

date = fct.str2date(datedeb)
#print(datedeb)

datefin = fct.str2date(datefin)
valeurs = np.zeros(n)
i = 0
n = 38148
while date <= datefin :
    date = date.strftime('%Y%m%d%H%M')
    latitudes, longitudes, values = fct.valeur(date)
    valeurs = valeurs + values 
    i = i + 1
    date = fct.str2date(date) + datetime.timedelta(minutes = 15)
    print(date, i)

datefin = '201708312345' 

val_moy = valeurs/i #on divise par le nombre d'iterations

fctt.trace(datedeb, datefin, longitudes, latitudes, val_moy, 0, 'val')


#%% compteur depassements par annee
seuil = 45 #45 40
n = 38148 

compteur_annee_45_max = fct.compteur_seuil_annee(seuil, 2021, 2021, n)
#compteur_annee_45 = fct.compteur_seuil_annee(seuil, 2011, 2021, n)
#compteur_annee_50 = fct.compteur_seuil_annee(seuil, 2011, 2021, n)

#compteuranne40 = pd.DataFrame(compteur_annee_40, columns = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018','2019', '2020'])

#%%plot depassement seuil sur une annee
for i in np.arange(0,4,1):
    fctt.trace(datedeb, datefin, longitudes, latitudes, compteur_annee_40_max[:,i], seuil, 'compteur', str(2011+i),' ')


#%% plot des depassements par annee pour le seuil voulu 
#attention à l'echelle du nb de depassements dans la fonction
datedeb = '201706010000'
datefin = '201708312345' 
seuil = 40

for i in np.arange(0,1, 1) :
    fctt.trace(datedeb, datefin, longitudes, latitudes, compteur_annee21_40, seuil, 'compteur', str(2022),' ')

#%%
compteur_10ans = np.sum(compteur_annee_40, axis = 1) #on somme sur les colonnes
fctt.trace(datedeb, datefin, longitudes, latitudes, compteur_10ans, seuil, 'compteur', "10 ans")


#%% compteur depassement sur un mois pour 10 ans
#liste_annee = np.arange(2010, 2022, 1)

liste_mois = np.arange(4, 12, step = 1)
#seuil = 50 A DEFINIR UNE SEULE FOIS DANS LA CONSOLE POUR NE PAS SE MELANGER LES PINCEAUX ENTRE LES DIFFERENTES CONSOLES

anneedeb = 2017
anneefin = 2018

compteur_mois_40_10ans3 = np.zeros((n,8))

for mois in liste_mois[3:4] :
    
    compteur_mois_40_10ans3[:,mois-4] = fct.compteur_seuil_mois (seuil, mois, anneedeb, anneefin, n)

#compteurmois40 = pd.DataFrame(compteur_mois_10, columns = ['avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre'])

#%% on trace le compteur par mois
liste_mois_nom = ['avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre']
#seuil = 40
for i in np.arange(0, 8, 1) :
    fctt.trace(datedeb, datefin, longitudes, latitudes, compteur_mois_40_10ans3[:, i], seuil, 'compteur', "10 ans", liste_mois_nom[i])
    #fctt.trace(datedeb, datefin, longitudes, latitudes, compteur_mois_45_10ans[:, i], seuil, 'compteur', "10 ans", liste_mois_nom[i])
    #fctt.trace(datedeb, datefin, longitudes, latitudes, compteur_mois_50_10ans3[:, i], seuil, 'compteur', "10 ans", liste_mois_nom[i])

#%% moyenne depassement par mois
liste_mois_nom = ['avril', 'mai', 'juin', 'juil', 'août', 'sep', 'oct', 'nov']
moy_mois40 = np.mean(compteur_mois_40_10ans, axis = 0)
moy_mois45 = np.mean(compteur_mois_45_10ans, axis = 0)
moy_mois50 = np.mean(compteur_mois_50_10ans, axis = 0)

plt.bar(liste_mois_nom[:-1], moy_mois40[:-1], label = '40dBZ')
plt.bar(liste_mois_nom[:-1], moy_mois45[:-1], label = '45dBZ')
plt.bar(liste_mois_nom[:-1], moy_mois50[:-1], label = '50dBZ')
plt.title('Moyenne du nb de dépassements de par mois sur 10ans')
plt.ylabel('nb de dépassements')
plt.legend()

#%% 













































