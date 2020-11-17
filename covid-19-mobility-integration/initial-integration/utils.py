from logging import error
import pandas as pd
import sys
import datetime
import os
import numpy as np
import pycountry
import logging

# a list of countries
list_regions = [c.name.lower() for c in list(pycountry.countries)]


def country_alpha2_from_name(df, list_regions):
    """Lambda function to generate country alpha2 code from country name

    The given dataframe was required to have the two columns: 'country_region_code'
    'and country_region'.

    https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#

    Args:
        df (pandas.DataFrame): input
        list_regions (list(str)): a list of country
    """

    if 'country_region_code' not in df.index:
        raise ValueError(
            '{} not in the dataframe.'.format('country_region_code'))

    if 'country_region' not in df.index:
        raise ValueError('{} not in the dataframe.'.format('country_region'))

    country_region_code = df['country_region_code']
    region_name = df['country_region'].lower()

    # special case:
    if region_name == 'us':
        return 'us'
    if region_name == 'mainland china':
        return 'cn'
    if region_name == 'south korea' or region_name == 'korea, south':
        return 'kr'
    if region_name == 'macau':
        return 'mo'

    # if region_name does not exist in the list_regions, try fuzzy search
    if region_name not in list_regions:
        # find a possible matched country
        try:
            fuzzy_search_result = pycountry.countries.search_fuzzy(region_name)
            return fuzzy_search_result[0].alpha_2
        # does not find a matched area, return NaN
        except:
            logging.warning(
                '{} was not found to a matched area'.format(region_name))
            return np.nan

    # generate country_region_code from region_name
    if pd.isna(country_region_code):
        return pycountry.countries.get(name=region_name).alpha_2
    # if country_region_code exists, no need to generate from region_name
    else:
        return country_region_code


def parse_coronavirus_data(data_path, input_date):
    """ Parse the JHU daily report data (left table)

    Args:
        data_path (str): path to the data file
        input_date (str): report date
    
    Returns:
        pandas.DataFrame: parsed df
    """
    df = pd.read_csv(data_path, sep=',', header=0, encoding='utf-8')

    # 1. add a column date to be the integration date
    logging.info('add a date column... ')

    date_object = datetime.datetime.strptime(input_date, "%m-%d-%Y")
    input_date = date_object.strftime("%Y-%m-%d")
    df.loc[:, 'date'] = input_date

    # 2. rename the join column
    logging.info('rename columns... ')
    
    rename_dict = {
        'Province/State': 'sub_region_1',
        'Country/Region': 'country_region',
    }
    df.rename(rename_dict, axis='columns', inplace=True)

    # add sub_region_2 columns it not exist
    if 'sub_region_2' not in df.columns:
        df['sub_region_2'] = ''

    # dictionary of state full name and abbreviation
    states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
    }

    # sub_region_1 is organized in county, state format
    # extract the state name and store in sub_region_1
    # extract the county name and store in sub_region_2
    for i, row in df.iterrows():
       cur_state = df.loc[i, 'sub_region_1']
       position = str(cur_state).find(',')
       if (position > 0):
            state = cur_state[position+1:]
            county = cur_state[: position]
            state=str(state).strip()
            state=str(state).upper()
            if state in states:
                df.loc[i, 'sub_region_1']=states[state].lower()
            df.loc[i, 'sub_region_2']=county.lower()    

    # 3. remove leading and trailing blank
    logging.info('remove leading and trailing blank... ')

    df['country_region']=df['country_region'].str.strip('*')
    df['sub_region_1']=df['sub_region_1'].str.strip()
    df['sub_region_2']=df['sub_region_2'].str.strip()

    # 4. fix missing country_region_code
    logging.info('fix missing country region code... ')
    # create country_region_code column if it does not exist
    if 'country_region_code' not in df.columns:
        df['country_region_code'] = np.nan
    df['country_region_code'] = df.apply(country_alpha2_from_name, list_regions=list_regions, axis=1)

    # 5. to lowercase
    logging.info('convert string to lower case... ')

    df['sub_region_1']=df['sub_region_1'].str.lower()
    df['date']=df['date'].str.strip()
    df['country_region']=df['country_region'].str.lower()
    df['sub_region_2']=df['sub_region_2'].str.lower()
    df['country_region_code'] = df['country_region_code'].str.lower()

    return df

def parse_mobility_data(data_path):
    """Parse the Google Mobility Data (right table)

    Args: 
        data_path (str): path to the google mobility data

    Returns:
        pandas.DataFrame: parsed df
    """
    df = pd.read_csv(data_path, sep=',', header=0, encoding='utf-8', low_memory=False)

    # 1.  to lowercase
    logging.info('convert string to lowercase (another table)... ') 

    df['sub_region_1']=df['sub_region_1'].str.lower()
    df['sub_region_2']=df['sub_region_2'].str.lower()
    df['country_region_code']=df['country_region_code'].str.lower()

    # 2. fix missing country alpha_2 code
    logging.info('fix missing country region code... (another table)')

    # filter the rows whose country_region_code is missing
    to_fix_index = pd.isna(df['country_region_code'])
    to_fix_df = df[to_fix_index]
    df.loc[to_fix_index, 'country_region_code'] = to_fix_df.apply(country_alpha2_from_name, list_regions=list_regions, axis=1)

    # 3. remove 'county', 'city' string from sub_region_2
    remove_dict = {
        'county': '',
        'city': ''
    }
    df['sub_region_2'] = df['sub_region_2'].replace(remove_dict, regex=True)

    # 4. remove leading and trailing blank
    logging.info('remove leading and trailing blank... (another table)')
    
    df['country_region_code']=df['country_region_code'].str.strip()
    df['sub_region_1']=df['sub_region_1'].str.strip()
    df['sub_region_2']=df['sub_region_2'].str.strip()
    df['date']=df['date'].str.strip()
 
    return df

def download_file():
    if (os.path.isdir('ground-truth')):
        logging.info('Data exists. No need to download again.')
    else:
        # Download data file
        os.system('gdown https://drive.google.com/uc?id=1UOS5MgOYUwZ2dL_MEljmP-KBJI-lv1le')
        os.system('unzip -q covid-19-data.zip')
        os.system('rm covid-19-data.zip')

def verify_data():
    if os.path.isfile('source-datasets/Global_Mobility_Report.csv') and \
            os.path.isfile('source-datasets/time_series_covid19_confirmed_US.csv') and \
            os.path.isfile('source-datasets/us-counties-nyt.csv') and \
            os.path.isdir('ground-truth'):
        logging.info('Data files verification complete.')
    else:
        erro_msg = 'Data files are missing. Please goto '\
        'https://drive.google.com/file/d/1UOS5MgOYUwZ2dL_MEljmP-KBJI-lv1le/view?usp=sharing ' \
        'and manually download the covid-19-data.zip file and extract the content to ' \
        'the current folder.'
        raise logging.ERROR(erro_msg)

def library_check():
    try:
        import pandas
    except:
        raise logging.ERROR('pandas missing, please use pip to install it.')

    try:
        import pycountry
    except:
        raise logging.ERROR('pycountry missing, please use pip to install it.')

    try:
        import numpy
    except:
        raise logging.ERROR('numpy missing, please use pip to install it.')
    
    try:
        import gdown
    except:
        raise logging.ERROR('gdown missing, please use pip to install it.')

