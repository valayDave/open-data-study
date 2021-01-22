# Estimate the engineering efforts when schema changes happen

We conduct this experiment to study what are the engineering efforts when scheme  changes happened in data integration tasks.

---

<!-- TOC -->

- [Estimate the engineering efforts when schema changes happen](#estimate-the-engineering-efforts-when-schema-changes-happen)
  - [Background](#background)
  - [Data Integration Tasks](#data-integration-tasks)
      - [Task 1](#task-1)
      - [Task 2](#task-2)
      - [Task 3](#task-3)
      - [Task 4](#task-4)
      - [Task 5](#task-5)
      - [Task 6](#task-6)
      - [Task 7](#task-7)
      - [Task 8](#task-8)
  - [How to run the data integration tasks](#how-to-run-the-data-integration-tasks)
    - [Required library](#required-library)
    - [Run python code](#run-python-code)
    - [How to validate your result is correct](#how-to-validate-your-result-is-correct)
    - [How to fix the codes if schema changes break the existing code](#how-to-fix-the-codes-if-schema-changes-break-the-existing-code)
  - [How to conduct this experiment](#how-to-conduct-this-experiment)
  - [More info](#more-info)
    - [Dataset schemas](#dataset-schemas)

<!-- /TOC -->

---
## Background

Suppose you are a data analysis who tries to analyze the impacts of COVID-19 on mobility or how the mobility can increase or decrease the spread of COVID-19.  You decide to first join the following two tables: [JHU COVID-19 Daily Report Data](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports) (**left table**) and the [Google Mobility Data](https://www.google.com/covid19/mobility/) (**right table**).

---
## Data Integration Tasks

We think about 8 scenarios that data analysis may face when performing the joining to study the human efforts when schema changes happen. There is no schema changes happened on the **right table**.

In some tasks, you are required to group the records. The aggregation logics are:
- Confirmed: `sum`
- Deaths: `sum`
- Recovered: `sum`
- Active: `sum`
- Latitude: `average`
- Longitude: `average`
- Incidence Rate: `average`
- Case Fatality Ratio: `average`

#### Task 1
Analyze the data reported at the **country** level. In the left table, besides the `country_region_code` and `date` columns, we also select the `Confirmed`, `Deaths`, and `Recovered` columns. These three columns are also called **basic columns**.

#### Task 2
Analyze the data reported at the **country** level. In the left table, we will select all available columns provided in the source file. 

#### Task 3
Analyze the data reported at the **state** level. *The selection of columns for the left table is the same as **Task 1***.

#### Task 4
Analyze the data reported at the **state** level. *The selection of columns for the left table is the same as **Task 2***.

#### Task 5
Analyze the data reported at the **county** level. *The selection of columns for the left table is the same as **Task 1***.

#### Task 6
Analyze the data reported at the **county** level. *The selection of columns for the left table is the same as **Task 2***.

#### Task 7
The existing data source is no longer available. So, we decide to switch our **left table** data source to [NYTimes COVID-19](https://github.com/nytimes/covid-19-data) data repository. We use the all columns provided by the NYTimes and perform a inner join at the county level.

*Note: for this task, we only perform the join on the data of 06-30-2020.*


#### Task 8
The existing data source is no longer available. So, we decide to switch our **left table** data source to [JHU time_series_covid19_confirmed_US](https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv). This data file only contains the number of **confirmed cases** in the US. We **need to**:
- rename the column `6/30/20` to `Confirmed`
- add another column `date`, whose value is `2020-06-30`
- select the `country_region_code`, `sub_region_1`, `sub_region_2`, `Confirmed` and `date` of the left table, then perform  join. 

*Note: for this task, we only perform the join on the data of 06-30-2020.*

---

## How to run the data integration tasks

### Required library 

It is better to create a **virtual environment** to install the required library without mess up your environment. like: `conda create -n myenv python=3.6`

Run `pip install -r requirements.txt ` in the current folder to install the required library.

### Run python code


`integration_tasks.py` is the **main file** you need to run.
`utils.py` defines multiple functions used by *integration_tasks.py*.

You need to pass a **date** as the argument to the main file, which in **%m-%d-%Y** format.

For example:

`python integration_tasks.py 03-01-2020`

*Note*
- *if you are using **Windows**, you need to run the code under a command window like **Git Bash**, which supports `unzip` and `rm` commands.*
- *you may see some warning message when running the code, like follows. You can safely ignore these messages.*

```
WARNING:root:burma was not found to a matched area
WARNING:root:congo (brazzaville) was not found to a matched area
WARNING:root:congo (kinshasa) was not found to a matched area
```

### How to validate your result is correct

We pre-generated ground truth data for each case which covers the date range from **02-15-2020** to **06-30-2020**. The **main file** is constructed as multiple *unit tests*. Each test is corresponding to one integration test. Your result will be automatically verified by code. After you run the main file, you will see some results like the following:

```
WARNING:root:burma was not found to a matched area
WARNING:root:congo (brazzaville) was not found to a matched area
WARNING:root:congo (kinshasa) was not found to a matched area
WARNING:root:diamond princess was not found to a matched area
WARNING:root:laos was not found to a matched area
WARNING:root:ms zaandam was not found to a matched area
WARNING:root:west bank and gaza was not found to a matched area
test_country_level_with_basic_columns (__main__.TestIntegration) ... ok
test_country_level_with_extra_columns (__main__.TestIntegration) ... ok
test_county_level_with_basic_columns (__main__.TestIntegration) ... ok
test_county_level_with_extra_columns (__main__.TestIntegration) ... ok
test_left_table_replaced_by_jhu_timeseries (__main__.TestIntegration) ... ok
test_left_table_replaced_by_nytime (__main__.TestIntegration) ... ok
test_state_level_with_basic_columns (__main__.TestIntegration) ... ok
test_state_level_with_extra_columns (__main__.TestIntegration) ... ok

----------------------------------------------------------------------
Ran 8 tests in 7.831s

OK
```
```
WARNING:root:burma was not found to a matched area
WARNING:root:congo (brazzaville) was not found to a matched area
WARNING:root:congo (kinshasa) was not found to a matched area
WARNING:root:diamond princess was not found to a matched area
WARNING:root:laos was not found to a matched area
WARNING:root:ms zaandam was not found to a matched area
WARNING:root:west bank and gaza was not found to a matched area
test_country_level_with_basic_columns (__main__.TestIntegration) ... ok
test_country_level_with_extra_columns (__main__.TestIntegration) ... FAIL
test_county_level_with_basic_columns (__main__.TestIntegration) ... ok
test_county_level_with_extra_columns (__main__.TestIntegration) ... FAIL
test_left_table_replaced_by_jhu_timeseries (__main__.TestIntegration) ... ok
test_left_table_replaced_by_nytime (__main__.TestIntegration) ... ok
test_state_level_with_basic_columns (__main__.TestIntegration) ... ok
test_state_level_with_extra_columns (__main__.TestIntegration) ... FAIL

======================================================================
FAIL: test_country_level_with_extra_columns (__main__.TestIntegration)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "integration_tasks_fixed_0528.py", line 98, in test_country_level_with_extra_columns
    pd.testing.assert_frame_equal(joined, joined_exp, check_dtype=False)
  File "C:\Miniconda3\lib\site-packages\pandas\_testing.py", line 1561, in assert_frame_equal
    raise_assert_detail(
  File "C:\Miniconda3\lib\site-packages\pandas\_testing.py", line 1036, in raise_assert_detail
    raise AssertionError(msg)
AssertionError: DataFrame are different

DataFrame shape mismatch
[left]:  (125, 20)
[right]: (125, 22)

======================================================================
FAIL: test_county_level_with_extra_columns (__main__.TestIntegration)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "integration_tasks_fixed_0528.py", line 193, in test_county_level_with_extra_columns
    pd.testing.assert_frame_equal(joined, joined_exp, check_dtype=False)
  File "C:\Miniconda3\lib\site-packages\pandas\_testing.py", line 1561, in assert_frame_equal
    raise_assert_detail(
  File "C:\Miniconda3\lib\site-packages\pandas\_testing.py", line 1036, in raise_assert_detail
    raise AssertionError(msg)
AssertionError: DataFrame are different

DataFrame shape mismatch
[left]:  (2594, 20)
[right]: (2594, 22)

======================================================================
FAIL: test_state_level_with_extra_columns (__main__.TestIntegration)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "integration_tasks_fixed_0528.py", line 147, in test_state_level_with_extra_columns
    pd.testing.assert_frame_equal(joined, joined_exp, check_dtype=False)
  File "C:\Miniconda3\lib\site-packages\pandas\_testing.py", line 1561, in assert_frame_equal
    raise_assert_detail(
  File "C:\Miniconda3\lib\site-packages\pandas\_testing.py", line 1036, in raise_assert_detail
    raise AssertionError(msg)
AssertionError: DataFrame are different

DataFrame shape mismatch
[left]:  (230, 20)
[right]: (230, 22)

----------------------------------------------------------------------
Ran 8 tests in 7.783s

FAILED (failures=3)
```

### How to fix the codes if schema changes break the existing code

We have added multiple **flags**, ```# FIXME if broken```, into the main file to indicate the section you may need to modify if a test fails. 

For example:
```python
def test_country_level_with_basic_columns(self):
        # Aggregate data into country level
        # FIXME if broken   <------- the section may need modification
        left = self.df1.groupby(['country_region_code', 'date']).agg( # <------- the section may need modification
            {'Confirmed':'sum', 'Deaths':'sum', 'Recovered':'sum'})  # <------- the section may need modification

        # Select the data that is reported at the country level
        index = ~self.df2[['sub_region_1', 'sub_region_2', 'metro_area']].notna().any(axis=1)
        right = self.df2[index]
```

Also, you may need to modify the `utils.py` to pass the integration tests. We do not add any flag to indicate the part needs to be modified. It is your job to locate the place.

## How to conduct this experiment

After you have the understanding of the integration tasks and how to run the code, you can first run the code from the date within `02/15/2020 - 02/29/2020`, to make sure your code passes **6 out of 8** tests. This is the default setting. 

The requirements to submit your result:
1. you need to submit your codes that can pass all tests with a given **date** between `03/01/2020` and `06/30/2020`.
2. start a timer to measure the time you spend passing tests separately. You can use the following template to submit your result.
```
Time to fix data integration tasks:
    Task 1:
    Task 2:
    Task 3:
    Task 4:
    Task 5:
    Task 6:
    Task 7:
    Task 8:
``` 

## More info
### Dataset schemas

**Left table** is the daily COVID-19 case reported by JHU. The explanation of each column is [here](https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/README.md).

Example of daily report:

| FIPS  | Admin2    | Province_State | Country_Region | Last_Update         | Lat                | Long_               | Confirmed | Deaths | Recovered | Active |
|-------|-----------|----------------|----------------|---------------------|--------------------|---------------------|-----------|--------|-----------|--------|
| 45001 | Abbeville | South Carolina | US             | 2020-05-01 02:32:28 | 34.22333378        | -82.46170658        | 31        | 0      | 0         | 31     |
| 22001 | Acadia    | Louisiana      | US             | 2020-05-01 02:32:28 | 30.295064899999996 | -92.41419698        | 130       | 10     | 0         | 120    |
| 51001 | Accomack  | Virginia       | US             | 2020-05-01 02:32:28 | 37.76707161        | -75.63234615        | 264       | 4      | 0         | 260    |
| 16001 | Ada       | Idaho          | US             | 2020-05-01 02:32:28 | 43.4526575         | -116.24155159999998 | 671       | 16     | 0         | 655    |
| 19001 | Adair     | Iowa           | US             | 2020-05-01 02:32:28 | 41.33075609        | -94.47105874        | 1         | 0      | 0         | 1      |

**Right table** is the Google Mobility Report to describe how visits and length of stay at different places change compared to a baseline. More details can be seen [here](https://www.google.com/covid19/mobility/data_documentation.html?hl=en).

Example of Google Mobility Report:

| country_region_code | country_region | sub_region_1 | sub_region_2       | metro_area | iso_3166_2_code | census_fips_code | date    | retail_and_recreation_percent_change_from_baseline | grocery_and_pharmacy_percent_change_from_baseline | parks_percent_change_from_baseline | transit_stations_percent_change_from_baseline | workplaces_percent_change_from_baseline | residential_percent_change_from_baseline |
|---------------------|----------------|--------------|--------------------|------------|-----------------|------------------|---------|----------------------------------------------------|---------------------------------------------------|------------------------------------|-----------------------------------------------|-----------------------------------------|------------------------------------------|
| GB                  | United Kingdom | Kent         | Borough of   Swale |            |                 |                  | ####### | -56                                                | -15                                               | 58                                 | -46                                           | -53                                     | 22                                       |
| GB                  | United Kingdom | Kent         | Borough of Swale   |            |                 |                  | ####### | -62                                                | -19                                               | 38                                 | -36                                           | -37                                     | 13                                       |
| GB                  | United Kingdom | Kent         | Borough of Swale   |            |                 |                  | ####### | -64                                                | -24                                               | 50                                 | -30                                           | -26                                     | 9                                        |
| GB                  | United Kingdom | Kent         | Borough of Swale   |            |                 |                  | ####### | -47                                                | -14                                               | 78                                 | -42                                           | -51                                     | 20                                       |
| GB                  | United Kingdom | Kent         | Borough of Swale   |            |                 |                  | ####### | -49                                                | -11                                               | 107                                | -44                                           | -51                                     | 20                                       |