# open-data-study
We study the schema evolutions, schema diversities of open data, as well as the code to handle these changes.

## Schema Evolution in Open Data

### Example: Integration of JHU COVID-19 data and Google Global Mobility data

The schema of the JHU COVID-19 data (https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports) evolves fast at a weekly to monthly frequency.

We developed python code using Pandas dataframe to integrate JHU COVID-19 data and Google's Global mobility data, which is planned to run every day to create a daily table that contains following columns:


|No.|column name|
|---|---|
|1|sub_region_1|
|2|country_region_code|
|3|LastUpdate|
|4|Confirmed|
|5|Deaths|
|6|Recovered|
|7|date|
|8|country_region|
|9|sub_region_2|
|10|metro_area|
|11|iso_3166_2_code|
|12|census_fips_code|
|13|retail_and_recreation_percent_change_from_baseline|
|14|grocery_and_pharmacy_percent_change_from_baseline|
|15|parks_percent_change_from_baseline|
|16|transit_stations_percent_change_from_baseline|
|17|workplaces_percent_change_from_baseline|
|18|residential_percent_change_from_baseline


While our code could work well in the first several days, we find it broke down soon due to schema changes in the source datasets. We fixed the problem, but the code to fix that problem broke again after a few days. In this repository, we uploaded our initial data integration code, and the datasets that it can integrate. In addition, we also upload more versions of code, with each version handling a major schema evolution in the source datasets.

## Estimate the engineering efforts when schema changes happen

Plese refer to [here](covid-19-mobility-integration/initial-integration/README.md) for more details of this task.