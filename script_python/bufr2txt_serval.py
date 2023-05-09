#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  4 12:06:26 2023

@author: doeuvrek
"""

import os
import datetime

# Extraction des lames d'eau 5 minutes avec la commande :
# ./lunerad -id  CMF.PAN -d1 201904010600 -d2 201905010600

#on converti les dates de debut et de fin de fichiers desarchive
datebegin = datetime.datetime.strptime('201805091930', '%Y%m%d%H%M')
dateend = datetime.datetime.strptime('201805140700', '%Y%m%d%H%M')

os.system('cd doeuvrek@sotrtm33-sidev:/home/mrmu/doeuvrek/lunairs')

date = datebegin
while date <= dateend :
    d1 = date.strftime('%Y%m%d%H%M') 
    d2 = (date + datetime.timedelta(days=1)).strftime('%Y%m%d%H%M') 
    os.system('./bufr2txt_serval -w -f txt -id CMF.SREF -d1 d1 -d2 d2 -pdt 15 -unit U_DBZ -latmin 47.95 -latmax 49.75 -lonmin 0.97 -lonmax 3.7')
    #print('./bufr2txt_serval -w -f txt -id CMF.SREF -d1 ' + str(date.strftime('%Y%m%d%H%M')) +' -d2 ' + str((date + datetime.timedelta(days=1)).strftime('%Y%m%d%H%M')) + ' -pdt 15 -unit U_DBZ -latmin 47.95 -latmax 49.75 -lonmin 0.97 -lonmax 3.7')
    date = date + datetime.timedelta(days=1)

os.system('scp doeuvrek@sotrtm33-sidev:/home/mrmu/doeuvrek/lunairs/RESULT/RADAR/COMPOSIT_ELLIPSO/REFLECTIVITE/*.text /cnrm/ville/USERS/doeuvrek/donnees/2018' )