# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Arnaud Forster   -   arnaud.forster@meteo.fr
"""


import os
os.environ["USE_PYGEOS"] = "0"
import geopandas
import cartopy.crs as ccrs
from cartopy.feature import NaturalEarthFeature, COLORS
import numpy as np,time,calendar
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import datetime
import matplotlib
import matplotlib.dates as mdates
import sys
import matplotlib.colors as mcolors

import pandas as pd

#il faut surement installer le module metpy (voir sur internet)
import metpy
from metpy import calc
from metpy.units import units


#%%

# personnal libraries
#os.system('cp /home/forstera/fcplr/Codes/LIB_PERSO/fonctions.py .')
import fonctions_zonage as fc
#os.system('rm fonctions.py')
###

#%%

import fonctions as fct
import fonctions_tracer as fctt


#%%
# ------------- Parametres à modifier

# Select Start and End date :                            
ybeg,mbeg,dbeg,hbeg,minbeg=2017,7,9,17,0
yend,mend,dend,hend,minend=2017,7,9,19,0
time_step = 60 #minutes

secteur = 'C'

lat_centre = 48.853
lon_centre = 2.35
zoom=False

#données de vent (U vent zonal et V vent meridien) pour determiner la direction du vent et la direction des secteurs ensuite
ut_final = -0.3
vt_final= 1

# -------------- Start programme

start_date=datetime.datetime(ybeg,mbeg,dbeg,hbeg,minbeg)
end_date=datetime.datetime(yend,mend,dend,hend,minend)
delta = datetime.timedelta(minutes=time_step)

currentdate = start_date
seuil = 0

cumul_total = 0

while currentdate <= end_date:   
    print(currentdate)
    # read txt file
    datefic=currentdate.strftime('%Y%m%d')
    heurefic=currentdate.strftime('%H%M')

    #datefile = datetime.datetime(ybeg,mbeg,dbeg,hbeg,minbeg)
    
    #debfic="./ANTILOPE_PRECIP_"+datefic+"_"+heurefic+"_000100_1675758544166.txt"  # to be modified with you own directory
    """debfic =  datefile.strftime('/cnrm/ville/USERS/doeuvrek/donnees/%Y/%m/%d/%Y%m%d%H%M.text')
    f_data = pd.read_csv(debfic, skiprows = 23, sep =" ", names = ['Latitudes', 'Longitudes', 'Valeurs min', 'Valeurs max']) 
    longitudes = f_data['Longitudes']
    latitudes = f_data['Latitudes']
    values = f_data['Valeurs max']
    values[values==65535]=np.nan   """
    
    latitudes, longitudes, values = fct.valeur(currentdate.strftime('%Y%m%d%H%M'))
        

    
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
    
    '''
    if secteur == 'C':
        indices_secteur = extrait_data_polygone(points_obs, angle_initial-180, angle_initial+180, secteur)
    else:
        indices_secteur = extrait_data_polygone(points_obs, angle_initial-30, angle_initial+30, secteur)   
    '''
    
    #distinction entre cercle et autres secteurs : 
    if secteur == 'C':
        indices_secteur = fc.extract_data_polygon(values, longitudes, latitudes, angle_initial-180, angle_initial+180, secteur, lat_centre, lon_centre)
    else:
        indices_secteur = fc.extract_data_polygon(values, longitudes, latitudes, angle_initial-30, angle_initial+30, secteur, lat_centre, lon_centre)    
    
    #liste_values_levels = []  
    
    values_sector = values[indices_secteur]
    longitudes_sector = longitudes[indices_secteur]
    latitudes_sector = latitudes[indices_secteur]   
    
    #fctt.trace(currentdate.strftime('%Y%m%d%H%M'), currentdate.strftime('%Y%m%d%H%M') , longitudes_sector, latitudes_sector, values_sector, seuil, 'val', 2017, 'av')
    
    #creation d'une carte rapidement pour verifier que les points sont selectionnes dans le bon secteur     
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
    
    departements = geopandas.read_file('/home/doeuvrek/Documents/ouverture_donnees/departements.geojson')
    metropole = geopandas.read_file('/home/doeuvrek/Documents/ouverture_donnees/metropole-version-simplifiee.geojson')

    
    #plt.legend(loc='upper left',fontsize = 14)
    
    ax.add_geometries(departements.geometry, crs = ccrs.PlateCarree(), facecolor='none', edgecolor='black',linewidth=1)
    ax.add_geometries(metropole.geometry, crs = ccrs.PlateCarree(), facecolor='none', edgecolor='black',linewidth=1)
    ax.scatter(list(longitudes_sector), list(latitudes_sector),c=values_sector, cmap='jet', vmin=1, vmax=10, transform=ccrs.PlateCarree(), s = 5) #cordonnes de Paris centre

    
    #plt.savefig('./Test_secteur.png')
    #plt.close()
    sys.exit()
    
    currentdate+=delta
    
    
          
                


