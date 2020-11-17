import pandas as pd
import sys
import datetime
import os

#Province/State  Country/Region      Last Update  Confirmed  Deaths  Recovered
def parse_coronavirus_data(data_path, input_date):
    df = pd.read_csv(data_path, sep=',', header=0, encoding='utf-8')
    print(df)

    #1. add a column date to be the integration date
    print("add a date column")
    print(input_date)
    date_object =datetime.datetime.strptime(input_date, "%m-%d-%Y")
    print(date_object)
    input_date=date_object.strftime("%Y-%m-%d")        
    df.loc[:, 'date']=input_date
    print(df)

    #2. rename the join column
    print("rename columns")
    df.rename({'Province/State':'sub_region_1', 'Country/Region':'country_region_code'}, axis='columns', inplace=True)
    print(df)


    #3. to lowercase
    print("to lower case")
    df['sub_region_1']=df['sub_region_1'].str.lower()
    df['sub_region_1']=df['sub_region_1'].str.strip()
    df['country_region_code']=df['country_region_code'].str.lower()
    df['country_region_code']=df['country_region_code'].str.strip()
    df['date']=df['date'].str.strip()

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
 

    for i, row in df.iterrows():
       cur_state=df.at[i, 'sub_region_1']
       print(cur_state)
       position=str(cur_state).find(',')
       if (position>0):
          state=cur_state[position+1:]
          state=str(state).strip()
          state=str(state).upper()
          print(state)
          if state in states:
              df.at[i, 'sub_region_1']=states[state].lower()

    print(df)

    #4. groupby and aggregation
    print("groupby and aggregation")
    df=df.groupby(['sub_region_1', 'country_region_code', 'date']).agg({'Confirmed':'sum', 'Deaths':'sum', 'Recovered':'sum'})
    print(df)


    return df

#country_region_code,country_region,sub_region_1,sub_region_2,metro_area,iso_3166_2_code,census_fips_code,date,retail_and_recreation_percent_change_from_baseline,grocery_and_pharmacy_percent_change_from_baseline,parks_percent_change_from_baseline,transit_stations_percent_change_from_baseline,workplaces_percent_change_from_baseline,residential_percent_change_from_baseline
def parse_mobility_data(data_path):
    df = pd.read_csv(data_path, sep=',', header=0, encoding='utf-8', low_memory=False)
    print(df)

    #1. aggregate based on country region
    #it includes both aggregated and non aggregated values
 
    #2. remove county level statistics

    df = df[pd.notnull(df['sub_region_2'])]    


    #3  to lowercase
    print("to lowercase for the other table") 
    df['sub_region_1']=df['sub_region_1'].str.lower()
    df['sub_region_1']=df['sub_region_1'].str.strip()
    df['country_region_code']=df['country_region_code'].str.lower()
    df['country_region_code']=df['country_region_code'].str.strip()
    df['date']=df['date'].str.strip()

    print(df)
    return df

#download

def download():
    if (os.path.isfile('source-datasets/Global_Mobility_Report.csv')):
        print("file Global_Mobility_Report.csv exists in source-datasets/")
    else:
        os.system('wget https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv')  
        os.system('mv Global_Mobility_Report.csv source-datasets/')


if __name__ == '__main__':
    input_date = str(sys.argv[1])
    print(input_date)
    download()
    df1=parse_coronavirus_data('source-datasets/'+input_date+'.csv', input_date)
    df1.to_csv('left.csv', encoding='utf-8')
    df2=parse_mobility_data('source-datasets/Global_Mobility_Report.csv')
    df2.to_csv('right.csv', encoding='utf-8')
    #join/merge  
    joined=df1.merge(df2, how='inner', on=['sub_region_1','country_region_code','date'])
    print(joined)    
    joined.to_csv('target-datasets/'+input_date+'.csv', encoding='utf-8')

