#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fetches and plots bi-national Canada/US "Merged" precipitation product 
available through Midwest Regional Climate Center
https://mrcc.illinois.edu/gismaps/naprecip.htm

The “Merged” dataset is created using both the 
Canadian Precipitation Analysis (CaPA) and the 
Multi-sensor Precipitation Estimate (MPE) datasets.

More information: 
    https://mrcc.illinois.edu/cliwatch/northAmerPcpn/aboutArchive.html#merged

@author: Jacob Bruxer
"""
import sys
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.interpolate import griddata
from datetime import datetime, timedelta
from pathlib import Path
from config import get_colors, get_map_extent, get_cities

colors = 'capa'
#colors = 'nws'

# start and end date.  If equal, then 24 hrs plotted, otherwise cumulative 
print('\n Bi-National Merged Precipitation Map  \n')
print('=' * 50)

def try_parsing_date(text):
    for fmt in ('%Y-%m-%d', '%Y%m%d'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError()


valid = False
while not valid:
    print('''\nEnter start date (YYYY-MM-DD or YYYYMMDD) or 'q' to quit''')
    start_date = input()
    if start_date[0].lower() == 'q':
        sys.exit()
    try:
        start_date = try_parsing_date(start_date)
        valid = True
    except ValueError:
        print('\n Error: not a valid date format \n')
        print('=' * 50)
        valid = False

valid = False
while not valid:
    print('''\nPress enter if same as start date, otherwise''')
    print('''\nEnter end date (YYYY-MM-DD or YYYYMMDD) or 'q' to quit''')
    end_date = input()
    if end_date == '':
        end_date = start_date
        break
    elif end_date[0].lower() == 'q':
        sys.exit()
    try:
        end_date = try_parsing_date(end_date)
        valid = True
    except ValueError:
        print('\n Error: not a valid date format \n')
        print('=' * 50)
        valid = False  

print(start_date)
print(end_date)

valid = False

while not valid:

    print('''\nChoose map extent \n''')
    print('''  1 : Great Lakes - St. Lawrence (glslr)''')
    print('''  2 : Lake Erie - Ontario - St. Lawrence (erislr)''')
    print('''  3 : Lake Ontario - St. Lawrence (ontslr)''')
    print('''  4 : Custom - define in config file (custom)''')

    extent = input('Enter number:')

    if extent == str(1):
        extent = 'glslr'  # entire Great Lakes - St. Lawrence basin
        valid = True
    elif extent == str(2):
        extent = 'erislr'  # Lake Erie through St. Lawrence
        valid = True
    elif extent == str(3):
        extent = 'ontslr'  # Lake Ontario through St. Lawrence
        valid = True
    elif extent == str(4):
        extent = 'custom'
        valid = True
    else:
        valid = False

map_extent = get_map_extent(extent)

# get additional parameters from config file

map_cities = get_cities(extent)
map_colors = get_colors(colors)

# compute # of days and hours
days = (end_date - start_date).days + 1
if days < 1:
    sys.exit()
    
hrs = days*24

def fetch_mrcc_csv(date, dataset='Full Contintent'):
    
    
    # add check that date is within last 30 days, otherwise can't fetch
    # in this way (need to access from archive)
    url = '''http://mrcc.illinois.edu/cliwatch/northAmerPcpn/'''
    
    if dataset == 'Great Lakes':
        url = url + 'greatLakes/mrgGL_{}.csv'.format(date.strftime('%Y%m%d'))

    else:
        # entire continental dataset
        url = url + 'northAmer/mrg_{}.csv'.format(date.strftime('%Y%m%d'))

    try:
        print('Fetching data for {}...'.format(date.strftime('%Y%m%d')))
        print(url)
        # add save csv here also, so it can be recreated later on
        df = pd.read_csv(url,
                     na_values='None', index_col = ['lat', 'lon'])
    except:
        print('Problem fetching data from url: {}'.format(url))
        print('Check dates.  Aborting')
        sys.exit()
        
    return df

# fetch data for first date initially, append other dates after
df = fetch_mrcc_csv(start_date)

# if multiple dates, retrieve additional dates data
if end_date and start_date < end_date: 

    next_date = start_date + timedelta(days=1)
    while next_date <= end_date:
        tempdf = fetch_mrcc_csv(next_date)
        df = df + tempdf
        next_date += timedelta(days=1)

# reset index to use lat lon data for plotting    
df.reset_index(inplace=True)

# data coordinates and values
x = df.lon
y = df.lat
z = df.prcp_mm


xmin = map_extent['xmin']
xmax = map_extent['xmax']
ymin = map_extent['ymin']
ymax = map_extent['ymax']

interval = 0.01  # resolution of plot (smaller = higher res, 0.01 smallest)
xi = np.arange(xmin, xmax, interval)
yi = np.arange(ymin, ymax, interval)

# create mesh grid over lats and lons
xi,yi = np.meshgrid(xi,yi)

# interpolate
zi = griddata((x,y),z,(xi,yi),method='linear')

colors = map_colors['colors']
bounds = map_colors['bounds']

# plot
fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(111)

#  plot on x, y grid and with z contours
p = ax.contourf(xi,yi,zi,
                bounds, 
                colors=colors,
                alpha=1)

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)

cbar = fig.colorbar(p, cax=cax, ticks=bounds)

cbar.ax.set_yticklabels(bounds)
cbar.set_label('Precipitation (mm)', labelpad=10, rotation=270)

local_folder = Path().parent

try:
    # add basin and other GIS/shapefile features for better visualization
    # not included in repository
    
    gis_folder = local_folder / 'gis'
    
    basins=gpd.read_file(gis_folder / '''basin_SLtotal.shp''')
    borders=gpd.read_file(gis_folder / '''politicalborders_GLSL.shp''')
    
    # plot list of specific cities
    cities=gpd.read_file(gis_folder / '''Cities_GL.shp''')
    cities.set_index('Name', inplace=True)
    cities = cities.loc[map_cities]
    cities.reset_index(inplace=True)
    
    basins.plot(ax=ax, 
                alpha=1, 
                facecolor='none', 
                edgecolor='grey')
    
    borders.plot(ax=ax, 
                 facecolor='none', 
                 edgecolor='black', 
                 linestyles='--')
    
    cities.plot(ax=ax, color='black')
    
    # add labels to cities
    n = cities.Name
    
    for i, txt in enumerate(n):
        # adds labels
        # ax.annotate(txt, (cities.Longitude[i], cities.Latitude[i]))
        
        # adds labels with white background
        ax.text(cities.Longitude[i], cities.Latitude[i], txt,
                  size=10,
                  color='black',
                  verticalalignment='bottom',
                  path_effects=[pe.withStroke(linewidth=2, foreground="white")])
        
except:
    print('''Couldn't find and/or add additional GIS data''')

ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

ax.set_title('{}-Hour Accumulated Precipitation : Valid {} 12 UTC'.format(
                str(hrs), end_date.strftime('%Y-%m-%d')))


out_folder = local_folder / 'graphics'

# save figure
fn = 'Precip_MrgCaPA-MPE_{}hr_Accum_{}'.format(str(hrs), 
                                               start_date.strftime('%Y%m%d'))

if start_date != end_date:
    fn = fn + '-{}'
    fn = fn.format(end_date.strftime('%Y%m%d'))
    
plt.savefig(out_folder / fn.format(), dpi=100)
plt.close(fig)
