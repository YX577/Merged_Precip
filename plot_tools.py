"""
Precip colors and bounds (ticks)

@author: jacobb
"""

# Colors options

# NWS colors
NWS_PRECIP_COLORS = [
                    "#04e9e7",  # 0.01 - 0.10 inches
                    "#019ff4",  # 0.10 - 0.25 inches
                    "#0300f4",  # 0.25 - 0.50 inches
                    "#02fd02",  # 0.50 - 0.75 inches
                    "#01c501",  # 0.75 - 1.00 inches
                    "#008e00",  # 1.00 - 1.50 inches
                    "#fdf802",  # 1.50 - 2.00 inches
                    "#e5bc00",  # 2.00 - 2.50 inches
                    "#fd9500",  # 2.50 - 3.00 inches
                    "#fd0000",  # 3.00 - 4.00 inches
                    "#d40000",  # 4.00 - 5.00 inches
                    "#bc0000",  # 5.00 - 6.00 inches
                    "#f800fd",  # 6.00 - 8.00 inches
                    "#9854c6",  # 8.00 - 10.00 inches
                    "black"     # 10.00+
                    #"#fdfdfd"   # 10.00+
                    ]

# set bounds at specific precip totals for plotting with colors
NWS_BOUNDS = [0.1, 0.5, 1.0, 2.5, 5.0,
          7.5, 10, 15, 20, 25,
          30, 40, 50, 75, 100,
          150]

NWS_COLORS = {"colors" : NWS_PRECIP_COLORS, 
              "bounds" : NWS_BOUNDS}


# Canadian Precipitation Analysis colors
CAPA_PRECIP_COLORS = ['white', 
                    "#98cbfe",  # 0.1
                    "#0098fe",  # 0.5
                    "#002dfe",  # 1.0
                    "#00fe65",  # 2.5
                    "#00cb00",  # 5.0
                    "#009800",  # 7.5
                    "#006500",  # 10.
                    "#fefe32",  # 15.
                    "#fecb00",  # 20.
                    "#fe9800",  # 25
                    "#fe6500",  # 30
                    "#fe0000",  # 40
                    "#fe0098",  # 50
                    "#9832cb",  # 75
                    '#650098',  #100
                    "#989898"    # 150
                    #"#fdfdfd"  # 150
                    ]

CAPA_BOUNDS = [0.0, 0.1, 0.5, 1.0, 2.5, 5.0,
          7.5, 10, 15, 20, 25,
          30, 40, 50, 75, 100,
          150, 250]

CAPA_COLORS = {"colors" : CAPA_PRECIP_COLORS, 
               "bounds" : CAPA_BOUNDS}


def get_colors(colors):
    if colors == 'capa':
        colors = CAPA_COLORS
    elif colors == 'nws':
        colors = NWS_COLORS
    return colors


def get_map_extent(map_extent):

    # extent of plot for Great Lakes
    if map_extent == 'glslr':
        # entire Great Lakes St. Lawrence
        bbox = {'xmin': -93.5, 'xmax': -69, 'ymin': 40, 'ymax': 51}
    elif map_extent == 'erislr':
        # Erie through St. Lawrence
        bbox = {'xmin': -86, 'xmax': -69, 'ymin': 40, 'ymax': 51}
    elif map_extent == 'ontslr':
        # Ontario through St. Lawrence
        bbox = {'xmin': -82, 'xmax': -69, 'ymin': 40, 'ymax': 51} 
    elif map_extent == 'custom':
        bbox = {'xmin': -90, 'xmax': -74, 'ymin': 40, 'ymax': 47} 
    return bbox


def get_cities(map_extent):
    
    
    # depends on map extent 
    if map_extent == 'glslr':
        cities = ['Duluth', 'Thunder Bay', 'Sault Ste. Marie', 
                  'Milwaukee', 'Chicago', 'Detroit', 'Cleveland', 'Buffalo', 
                  'Toronto', 'Rochester', 'Kingston', 
                  'Montreal', 'Ottawa']
    elif map_extent == 'erislr':
        cities = ['Sault Ste. Marie',
                  'Detroit', 'Cleveland', 'Buffalo', 
                  'Toronto', 'Kingston', 
                  'Montreal', 'Ottawa']
    elif map_extent == 'ontslr':
        cities = ['Toronto', 'Buffalo', 'Rochester', 'Kingston', 
                  'Montreal', 'Ottawa']
        
    elif map_extent == 'custom':
        cities = ['Sault Ste. Marie', 
                  'Milwaukee', 'Chicago', 'Detroit', 'Cleveland', 'Buffalo', 
                  'Toronto', 'Rochester', 'Kingston', 
                  'Ottawa']
        
    return cities
    
