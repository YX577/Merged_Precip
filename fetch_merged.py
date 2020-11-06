import sys
import pandas as pd
from datetime import datetime, timedelta

def fetch_mrcc_csv(date, dataset='Full Contintent'):
    
    if date < datetime.today() - timedelta(days=30):
        raise Exception("Date must be within past 30 days")
        
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
        print('URL: ', url)
        # add save csv here also, so it can be recreated later on
        df = pd.read_csv(url,
                     na_values='None', index_col = ['lat', 'lon'])
    except:
        raise RuntimeError('Problem fetching data from url: {}'.format(url))
        
    return df