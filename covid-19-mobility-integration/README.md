# Estimate the engineering efforts when schema changes happen

We perform several inner joins of the [JHU COVID-19 Daily Report Data](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports) (left table) and the [Google Mobility Data](https://www.google.com/covid19/mobility/) (right table) to study the schema changes happened in JHU's datasets.

---

<!-- TOC -->

- [Estimate the engineering efforts when schema changes happen](#estimate-the-engineering-efforts-when-schema-changes-happen)
  - [Data Integration Tasks](#data-integration-tasks)
  - [Dataset schemas](#dataset-schemas)
  - [Library dependency](#library-dependency)
  - [Common Questions & Answers](#common-questions--answers)
    - [How to use the python code](#how-to-use-the-python-code)
    - [How to validate your output is correct](#how-to-validate-your-output-is-correct)
    - [How to fix the integration codes if schema changes break the existing code](#how-to-fix-the-integration-codes-if-schema-changes-break-the-existing-code)

<!-- /TOC -->

---

## Data Integration Tasks

We only target the schema changes that happened in the JHU daily report.


There are 8 existing data integration tasks, which are defined in the `integration_test.py`. Each function in the python file represents a data integration task. The original codes work for the left table generated from **02-15-2020** to **02-29-2020**.

We perform inner join for the left and right tables by aggregate COVID-19 case data at county/state/country level. For each case, we divide it into two sub-tasks: 
1. Inner join with basic columns: confirmed, deaths, recovered
2. Inner join with extra columns: basic columns + longitude, latitude, active, etc.

We have 6 in total for the above tasks. The rest of the two tasks are:
1. Replace left table with NYTimes COVID-19 data then perform an inner join with right table at county level.
2. Replace left table with JHU TimeSeries data then perform an inner join with right table at county level.

The details of each integration task is described as below:

- Task 1: aggregate data at country level then join (Basic columns).

Example:

| country_region_code | date      | Confirmed | Deaths | Recovered | Unnamed: 0 | country_region       | ... | grocery_and_pharmacy_percent_change_from_baseline |
|---------------------|-----------|-----------|--------|-----------|------------|----------------------|-----|---------------------------------------------------|
| ae                  | 2020/2/15 | 8         | 0      | 3         | 0          | United Arab Emirates | ... | 4                                                 |
| au                  | 2020/2/15 | 15        | 0      | 8         | 126969     | Australia            | ... | 3                                                 |
| be                  | 2020/2/15 | 1         | 0      | 0         | 194150     | Belgium              | ... | 2                                                 |
| ca                  | 2020/2/15 | 7         | 0      | 1         | 678009     | Canada               | ... | 2                                                 |

- Task 2: aggregate data at country level then join. (Basic + Extra columns).

Example:

| country_region_code | date     | Confirmed | Deaths | Recovered | Latitude | Longitude | Unnamed: 0 | country_region       | ... | retail_and_recreation_percent_change_from_baseline |
|---------------------|----------|-----------|--------|-----------|----------|-----------|------------|----------------------|-----|----------------------------------------------------|
| ae                  | 2020/3/1 | 21        | 0      | 5         | 24       | 54        | 15         | United Arab Emirates | ... | 3                                                  |
| af                  | 2020/3/1 | 1         | 0      | 0         | 33       | 65        | 2000       | Afghanistan          | ... | 3                                                  |
| at                  | 2020/3/1 | 14        | 0      | 0         | 47.5162  | 14.5501   | 103592     | Austria              | ... | 0                                                  |
| au                  | 2020/3/1 | 27        | 1      | 11        | -21.8557 | 140.6119  | 126984     | Australia            | ... | 4                                                  |
| be                  | 2020/3/1 | 2         | 0      | 1         | 50.8333  | 4         | 194165     | Belgium              | ... | 0                                                  |

- Task 3: aggregate data at state level then join. (Basic columns).
- Task 4: aggregate data at state level then join. (Basic + Extra columns).
- Task 5: aggregate data at county level then join. (Basic columns).
- Task 6: aggregate data at county level then join. (Basic + Extra columns).
- Task 7: replace left table with NYTime data then join with right table at county level on the date of 06-30-2020.
- Task 8: replace left table with JHU TimeSeries data then join with right table at county level on the date of 06-30-2020.


The original data integration codes work for the first 6 tasks with date from *02-15-2020* to *03-01-2020*. For the last two tasks, the date is hardcoded as *06-30-2020*.

**Your tasks** are to make sure all 8 tasks get the correct result and timing the time in fixing the code for each data integration task.

You only need to run the data integration code with a given date which is later than *03-01-2020*, then provide a fixed code.

Here are some instructions on how to run the code and how to validate your result:

[How to use the python code](#how-to-use-the-python-code)

[How to validate your output is correct](#how-to-validate-your-output-is-correct)

[How to fix the integration codes if schema changes break the existing code](#how-to-fix-the-integration-codes-if-schema-changes-break-the-existing-code)


You can organize your solution as the following format:

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
and attach your fixed `py` files.


## Dataset schemas

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


## Library dependency

The codes rely on the following python library. You can use `pip install library_name` or `pip install -r requirements.txt` to install these libraries. 
```
pandas
pycountry
numpy
gdown
```

---

## Common Questions & Answers

### How to use the python code

Execute `python integration_test.py date` in your command window with an **argument**: *date*, which in **%m-%d-%Y**.

Example:

`python integration_test.py 03-01-2020`

*Note*: you may see some warning message when running the code, like follows. You can safely ignore these messages.

```
WARNING:root:burma was not found to a matched area
WARNING:root:congo (brazzaville) was not found to a matched area
WARNING:root:congo (kinshasa) was not found to a matched area
```

### How to validate your output is correct

We pre-generated ground truth data for each case which cover the date range from **02-15-2020** to **06-30-2020**. Each integration task is coded as a unit test function, we use `pandas.testing.assert_frame_equal` to check whether your joined table is equal to the ground truth data. The result of *Pass/Fails* will be printed in the command window.

### How to fix the integration codes if schema changes break the existing code

You are supposed to modify the codes in `integration_test.py` and `utils.py` to pass the unit tests. Ideally, there is no need to modify the codes related to the right table.
