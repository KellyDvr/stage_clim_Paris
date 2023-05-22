#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 15:03:28 2023

@author: doeuvrek
"""

import xarray as xr
import numpy as np
import pandas as pd

datadir = '/mnt/nfs/d40/ville/USERS/doeuvrek/donnees/2017/07/09/201707091500.text'
df = pd.read_csv(datadir, skiprows = 23, sep =" ", names = ['Latitudes', 'Longitudes', 'Valeurs min', 'Valeurs max'])

xr = df.to_xarray()

