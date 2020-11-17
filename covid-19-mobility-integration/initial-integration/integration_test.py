import unittest
import logging
import sys
import os
import pandas as pd
from datetime import datetime
from utils import parse_coronavirus_data, parse_mobility_data, download_file, verify_data, library_check

class TestIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Check required libraries are installed 
        library_check()
        # Download data file
        download_file()
        # Verify the needed data are exist.
        verify_data()

        # Parse the daily report data
        cls.df1=parse_coronavirus_data('source-datasets/'+cls.input_date+'.csv', cls.input_date)
        
        # Parse the Google Mobility data
        if os.path.isfile('right.csv'):
            cls.df2 = pd.read_csv('right.csv', sep=',', header=0, encoding='utf-8', low_memory=False)
        else:
            cls.df2=parse_mobility_data('source-datasets/Global_Mobility_Report.csv')
            # Save the parsed data to disk to improve performance at next 
            # running time
            cls.df2.to_csv('right.csv', encoding='utf-8', index=False)

    # Task 1
    # Data Integration at Country level with basic columns: 
    # confirmed, death, recovered
    def test_country_level_with_basic_columns(self):
        # Aggregate data into country level
        left = self.df1.groupby(['country_region_code', 'date']).agg(
            {'Confirmed':'sum', 'Deaths':'sum', 'Recovered':'sum'}) 

        # Filter the data in country level
        index = ~self.df2[['sub_region_1', 'sub_region_2', 'metro_area']].notna().any(axis=1)
        right = self.df2[index]

        # Perform inner join
        joined = left.merge(right, how='inner', on=['country_region_code', 'date'])
        
        # Expect result
        joined_exp_path = os.path.join('ground-truth', 'country', self.input_date + '.csv')
        joined_exp = pd.read_csv(joined_exp_path, encoding='utf-8')
        pd.testing.assert_frame_equal(joined, joined_exp, check_dtype=False)

    # Task 2
    # Data Integration at Country level with extra columns: 
    # basic columns + longitude, latitude, active, etc.
    def test_country_level_with_extra_columns(self):
        # Aggregate data into country level
        left = self.df1.groupby(['country_region_code', 'date']).agg(
            {'Confirmed':'sum', 'Deaths':'sum', 'Recovered':'sum'})
        
        # Filter the data in country level
        index = ~self.df2[['sub_region_1', 'sub_region_2', 'metro_area']].notna().any(axis=1)
        right = self.df2[index]

        # Perform inner join
        joined = left.merge(right, how='inner', on=['country_region_code', 'date'])

        # Expect result
        joined_exp_path = os.path.join('ground-truth', 'country-with-extra-columns', self.input_date + '.csv')
        joined_exp = pd.read_csv(joined_exp_path, encoding='utf-8')
        pd.testing.assert_frame_equal(joined, joined_exp, check_dtype=False)
    
    # Task 3
    # Data Integration at State level with basic columns: 
    # confirmed, death, recovered
    def test_state_level_with_basic_columns(self):
        # state Level 
        left = self.df1.groupby(['country_region_code', 'sub_region_1', 'date']).agg(
            {'Confirmed':'sum', 'Deaths':'sum', 'Recovered':'sum'})

        # Filter the data in state level
        index = ~self.df2[['sub_region_2']].notna().any(axis=1)
        right = self.df2[index]

        # Perform inner join
        joined = left.merge(right, how='inner', 
                            on=['country_region_code', 'sub_region_1', 'date'])

        # Expect result
        joined_exp_path = os.path.join('ground-truth', 'state', self.input_date + '.csv')
        joined_exp = pd.read_csv(joined_exp_path, encoding='utf-8')
        pd.testing.assert_frame_equal(joined, joined_exp, check_dtype=False)

    # Task 4
    # Data Integration at State level with extra columns: 
    # basic columns + longitude, latitude, active, etc.
    def test_state_level_with_extra_columns(self):
        # state Level 
        left = self.df1.groupby(['country_region_code', 'sub_region_1', 'date']).agg(
            {'Confirmed':'sum', 'Deaths':'sum', 'Recovered':'sum'})

        # Filter the data in country level
        index = ~self.df2[['sub_region_2']].notna().any(axis=1)
        right = self.df2[index]

        # Perform inner join
        joined = left.merge(right, how='inner', 
                            on=['country_region_code', 'sub_region_1', 'date'])

        # Expect result
        joined_exp_path = os.path.join('ground-truth', 'state-with-extra-columns', self.input_date + '.csv')
        joined_exp = pd.read_csv(joined_exp_path, encoding='utf-8')
        pd.testing.assert_frame_equal(joined, joined_exp, check_dtype=False)

    # Task 5
    # Data Integration at County level with basic columns: 
    # confirmed, death, recovered
    def test_county_level_with_basic_columns(self):
        # county Level 
        left = self.df1.groupby(['country_region_code', 'sub_region_1', 'sub_region_2', 'date']).agg(
            {'Confirmed':'sum', 'Deaths':'sum', 'Recovered':'sum'})
        
        # Filter the data in county level
        index = self.df2[['sub_region_2']].notna().any(axis=1)
        right = self.df2[index]
        
        # Perform inner join
        joined = left.merge(right, how='inner', on=['country_region_code', 'sub_region_1', 'sub_region_2', 'date'])
        
        # Expect result
        joined_exp_path = os.path.join('ground-truth', 'county', self.input_date + '.csv')
        joined_exp = pd.read_csv(joined_exp_path, encoding='utf-8')
        pd.testing.assert_frame_equal(joined, joined_exp, check_dtype=False)

    # Task 6
    # Data Integration at County level with extra columns: 
    # basic columns + longitude, latitude, active, etc.
    def test_county_level_with_extra_columns(self):
        # county Level 
        left = self.df1.groupby(['country_region_code', 'sub_region_1', 'sub_region_2', 'date']).agg(
            {'Confirmed':'sum', 'Deaths':'sum', 'Recovered':'sum'})

        # Filter the data in county level
        index = self.df2[['sub_region_2']].notna().any(axis=1)
        right = self.df2[index]

        # Perform inner join
        joined = left.merge(right, how='inner', on=['country_region_code', 'sub_region_1', 'sub_region_2', 'date'])

        # Expect result
        joined_exp_path = os.path.join('ground-truth', 'county-with-extra-columns', self.input_date + '.csv')
        joined_exp = pd.read_csv(joined_exp_path, encoding='utf-8')
        pd.testing.assert_frame_equal(joined, joined_exp, check_dtype=False)

    # Task 7
    # Replace left table (JHU daily report) by NYTimes COVID Report
    # In this case, we only integrate the covid-19 data with US counties
    # on 06-30-2020.
    def test_left_table_replaced_by_nytime(self):
        df1 = pd.read_csv('source-datasets/us-counties-nyt.csv', sep=',', encoding='utf-8', low_memory=False)
        # FIXME 
        # left =

        # Filter the data in county level
        index=  self.df2[['sub_region_2']].notna().any(axis=1)
        right = self.df2[index]

        # FIXME
        #joined = 

        joined_exp_path = os.path.join('ground-truth', 'replace-by-nyt', '06-30-2020' + '.csv')
        joined_exp = pd.read_csv(joined_exp_path, encoding='utf-8')
        pd.testing.assert_frame_equal(joined, joined_exp, check_dtype=False)
    
    # Task 8
    # Replace left table (JHU daily report) by JHU COVID TimeSeries Report
    # In this case, we only integrate the covid-19 data with US counties
    # on 06-30-2020.
    def test_left_table_replaced_by_jhu_timeseries(self):
        df1 = pd.read_csv('source-datasets/time_series_covid19_confirmed_US.csv',
                          sep=',', encoding='utf-8', low_memory=False)
        # FIXME 
        # left =
        
        # Filter the data in county level
        index=  self.df2[['sub_region_2']].notna().any(axis=1)
        right = self.df2[index]

        # FIXME
        #joined = 

        joined_exp_path = os.path.join('ground-truth', 'replace-by-jhu-timeseries', '06-30-2020' + '.csv')
        joined_exp = pd.read_csv(joined_exp_path, encoding='utf-8')
        pd.testing.assert_frame_equal(joined, joined_exp, check_dtype=False)

if __name__ == '__main__':
    # logging.getLogger().setLevel(logging.INFO)

    input_date = sys.argv[1]
    try:
        date = datetime.strptime(input_date, "%m-%d-%Y")
    except ValueError:
        error_msg = '{} is not a valid date format. Your input should be %m-%d-%Y, '\
            'like: 02-15-2020'.format(input_date)
        raise ValueError(error_msg)
    
    if date < datetime(2020, 2, 15) or date > datetime(2020, 6, 30):
        error_msg = 'The input date should fall in the dates range: '\
            '[02-15-2020, 06-302020]'
        raise ValueError(error_msg)

    # Pass the input_date to the test class
    TestIntegration.input_date = input_date

    test_loader = unittest.TestLoader()
    test_names = test_loader.getTestCaseNames(TestIntegration)
    suite = unittest.TestSuite()
    for test_name in test_names:
        suite.addTest(TestIntegration(test_name))

    result = unittest.TextTestRunner(verbosity=2).run(suite)