#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 17 09:21:06 2023

@author: Arnaud Forster -   arnaud.forster@meteo.fr

"""

from __future__ import unicode_literals


import numpy as np
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from shapely.geometry import Polygon
import geopandas
import datetime
import sys
import rtree

    
def calcul_demi_cercle(angles,lat_centre,lon_centre, distance):
   '''Fonction permettant de calculer les latitudes et longitudes situées à une distance "distance" du point central lat_centre, lon_centre
      en prenant en compte un certains nombres d'angles (le Nord est défini comme degré 0).
      http://www.movable-type.co.uk/scripts/latlong.html (à la fin de la page)
      le forum s'inspire des equations du site ci-dessus https://stackoverflow.com/questions/7222382/get-lat-long-given-current-point-distance-and-bearing'''
   
   R_terre = 6378.1 #Rayon de la Terre
   
   lat1 = np.radians(lat_centre) #on converti en radian
   lon1 = np.radians(lon_centre) #on converti en radian

   lats = np.arcsin( np.sin(lat1)*np.cos(distance/R_terre) + np.cos(lat1)*np.sin(distance/R_terre)*np.cos(angles))

   lons = lon1 + np.arctan2(np.sin(angles)*np.sin(distance/R_terre)*np.cos(lat1),np.cos(distance/R_terre)-np.sin(lat1)*np.sin(lats))

   lats = np.degrees(lats)  #on reconverti en degré
   lons = np.degrees(lons)  #on reconverti en degré
   
   return lats, lons 
 
    
def extract_data_polygon(points_liste, longitudes_liste, latitudes_liste, angle_moins, angle_plus, secteur, lat_centre, lon_centre):
    ''' Fonction qui permet de selectionner les points qui sont situés dans le secteur selectionne (C,D,DL,DR,U,UL,UR) autour d'un 
    point central de coordonnees (lon_centre,lat_centre). L'ouverture du demi-cercle est determinee par angle_moins et angle_plus.
    La distance des demi-cercle au centre du cercle est codee en dur dans le programme mais peut etre modifie facilement.
    Ce programme renvoit les indices des points_liste situes dans le secteur voulu'''

    # Creation de la liste des angles du demi-cercle en fonction de angle_moins et angle_plus
    arr_angles = np.arange(angle_moins,angle_plus+1,1)
    arr_angles_radian = np.radians(arr_angles)
    
    #distinction entre le secteur cercle et les autres secteurs :

    if secteur == 'C':
       #on cree le cercle :
       lats_up,lons_up = calcul_demi_cercle(arr_angles_radian,lat_centre,lon_centre, 20)  
       lats_down,lons_down = calcul_demi_cercle(arr_angles_radian,lat_centre,lon_centre, 0.001) 

    else:
       # on cree deux demi-cercles. Un pour le grand demi-cercle et l'autre pour le petit afin de former ensuite le polygone :
       lats_up,lons_up = calcul_demi_cercle(arr_angles_radian,lat_centre,lon_centre, 60)  #60
       lats_down,lons_down = calcul_demi_cercle(arr_angles_radian,lat_centre,lon_centre, 20) #20
       
    #on forme un polygone avec les données de lats et lons obtenues :
    lats_polygon = np.concatenate((lats_down[::-1], lats_up), axis=0)
    lons_polygon = np.concatenate((lons_down[::-1], lons_up), axis=0)

    polygon_geom = Polygon(zip(lons_polygon, lats_polygon))
    polygon_secteur = geopandas.GeoDataFrame(index=[0], crs='epsg:4326',geometry=[polygon_geom])
       
    #on cree un tableau avec les points et leurs coordonnees (lon,lat) :
    points_avec_coord = np.vstack([longitudes_liste,latitudes_liste,points_liste]).T
    
    #transformation des coordonnees des points en polygone :    
    points_polygon = geopandas.GeoDataFrame(points_avec_coord, geometry=geopandas.points_from_xy(longitudes_liste, latitudes_liste))
    points_polygon = points_polygon.set_crs(epsg=4326)
    
    #on recupere les points qui se trouvent dans la zone voulue :
    points_secteur = geopandas.tools.sjoin(points_polygon,polygon_secteur, how="inner")
    
    data_secteur = points_secteur[2] 
    
    indices_points_dans_secteur = data_secteur.index
    
    return indices_points_dans_secteur
    
    

