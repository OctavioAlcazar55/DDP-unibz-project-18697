import os

import pandas as pd
import numpy as np
import time

import re

import warnings
warnings.filterwarnings("ignore")

# Listed columns to drop for the different data sources
# Daily data columns have changed many times, having four different versions of column names

drop_columns_dict = {"daily_v0": ['Province/State','Last Update','Country/Region'],
                     # from Jan 22, 2020 until Feb 29, 2020 (Country/Region column)
                     
                     # from Mar 01, 2020 until Mar 21, 2020 (Country/Region column)
                     "daily_v1": ['Province/State','Last Update',
                                  'Latitude','Longitude','Country/Region'],
                     
                     # from Mar 22, 2020 until May 28, 2020 (Country_Region column name)
                     "daily_v2": ['FIPS','Admin2','Province_State','Last_Update',
                                  'Lat','Long_','Active','Combined_Key','Country_Region'],
                     
                     # from May 29, 2020 until Nov 08, 2020 (Country_Region column)
                     "daily_v3": ['FIPS','Admin2','Province_State','Last_Update','Lat','Long_',
                                  'Active','Combined_Key','Incidence_Rate','Case-Fatality_Ratio',
                                  'Country_Region'],
                     
                     # from Nov 09, 2020 until today (Country_Region column)
                     "daily_v4": ['FIPS','Admin2','Province_State','Last_Update','Lat','Long_',
                                  'Active','Combined_Key','Incident_Rate','Case_Fatality_Ratio',
                                  'Country_Region'],
                     
                     "cumulative": ['Province/State','Lat','Long','Country/Region'],
                     "stringency_index": ['country_code','region_code','region_name',
                                          'jurisdiction','country_name']
}

# Function for reading input files and storing data into a Pandas DataFrame
def read_data(file_path):

    # Reading CSV file in a DataFrame
    df = pd.read_csv(file_path)
    
    # Some CSV files have an additional first column, check if it is the case
    if df.columns[0] == "Unnamed: 0":
        df.drop(columns=df.columns[0], axis=1, inplace=True)

    return df

# Function for returning number of rows and columns, and missing value information
def initial_dataframe_check(data):

    # Get number of rows and columns
    num_rows = data.shape[0]
    num_columns = data.shape[1]
    
    # Get number of rows and columns with missing values (NAs)
    num_rows_with_null_values = (data.T.isna().sum().values > 0).sum()
    num_columns_with_null_values = (data.isna().sum().values > 0).sum()
    
    # Percentage of null values from entire dataframe
    null_values_percentage = np.round((data.isna().sum().sum() / (num_rows*num_columns))*100, 
                                      3)
    
    # Concatenate output values and output dataframe
    values = [num_rows, num_columns, num_rows_with_null_values, 
              num_columns_with_null_values, null_values_percentage]
    
    index_names = ["# Rows", "# Columns", "# Rows with NAs", 
                   "# Columns with NAs", "% Null Values in Dataframe"]
  
    return pd.DataFrame(values, columns=["Values"], index=index_names)

# Function for deleting non-relevant columns from a given data source
def drop_columns(data, file_path,
                 data_source="daily"):

    if data_source == "daily":
        date = file_path.split("/")[-1].split(".")[0]
        month = date.split("-")[0]
        day   = date.split("-")[1]
        year  = date.split("-")[2]
        
        if year > "2020":
            data_source = "daily_v4"
        elif month > "11":
            data_source = "daily_v4"
        elif month == "11" and day >= "09":
            data_source = "daily_v4"
        elif month > "05":
            data_source = "daily_v3"
        elif month == "05" and day >= "29":
            data_source = "daily_v3"
        elif month > "03":
            data_source = "daily_v2"
        elif month == "03" and day >= "22":
            data_source = "daily_v2"
        elif month > "02":
            data_source = "daily_v1"
        else:
            data_source = "daily_v0"
            
    columns_to_drop = drop_columns_dict[data_source][:-1]
    country_column = drop_columns_dict[data_source][-1]
    
    # removing columns from dataframe
    df = data.drop(columns_to_drop, axis=1)

    print("Removed {0} columns from dataframe".format(len(columns_to_drop)))
    
    # Renaming column
    df.rename(columns={country_column: "Country"}, inplace=True)
    
    # Sorting dataframe by column and reset index
    df.sort_values("Country", inplace=True)
    df = df.reset_index(drop=True)
    
    return df

# Function for intersection or outer difference between two lists (converted to sets
def get_list_inner_outer_join(first_list, second_list, 
                              operation="outer"):
    
    # outer means to get values which are not part of both lists
    if operation == "outer":
        return sorted(list(set(first_list).symmetric_difference(set(second_list))))
    else: # operation == "inner" - intersection for both lists
        return sorted(list(set(first_list) & set(second_list)))
    
# Function for extending dataframe with updated time series data
def update_timeseries_dataframe(file_path, data,
                                data_type="cumulative", 
                                operation="outer"):
    
    # 1. Get update data source and open it as a Pandas Dataframe
    updated_df = read_data(file_path)
    
    # 2. Drop unnecesary columns and check null values information
    updated_df = drop_columns(updated_df, data_source=data_type)
    
    # 3. Compute outer intersection of columns between original and updated dataframes
    to_add_columns = get_list_inner_outer_join(data.columns, 
                                               updated_df.columns, 
                                               operation=operation)
    
    # 4. Append new date columns into the existing dataframe
    data = data.join(updated_df.loc[:, to_add_columns])
    
    return data

# Function for finding countries on a given dataset with more than one entry
# Thius typically means that the data is collected by region or state
def get_countries_split_by_regions(data, country_column="Country"):
    
    countries_to_aggregate = []
    
    list_unique_countries = np.unique(data[country_column])

    for country in list_unique_countries:
        retrieved_rows = data.loc[data[country_column]==country].shape[0]
    
        if retrieved_rows > 1:
            countries_to_aggregate.append(country)
        
    print("There are {0} countries where data needs to be aggregated.".format(len(countries_to_aggregate)))

    return countries_to_aggregate

# Function that aggregates rows belonging to the same country for outputting one aggregated value
def country_aggregation_dataframe(data, countries_list,
                                  country_column="Country",
                                  data_type="cumulative"):
    
    for country in countries_list:
        
        if data_type == "cumulative" or data_type == "daily":         
            aggregated_series = data.loc[data[country_column]==country].sum()
            aggregated_series.values[0] = country
        else: # data_type == "stringency_index"
            aggregated_series = data.loc[data[country_column]==country].mean()
        
        drop_indexes = list(data.loc[data[country_column]==country].index)
        keep_index = drop_indexes[0]
        
        if data_type == "cumulative" or data_type == "daily":
            data.iloc[keep_index] = aggregated_series # have to include country name in series
        else: # data_type == "stringency_index"
            data.iloc[keep_index, 1:] = aggregated_series

        data = data.drop(drop_indexes[1:]).reset_index(drop=True)
        
    return data

# Function that formats the country names for each data source
def country_list_formatting(data, data_source="stringency_index",
                            country_column="Country"):
    
    if data_source == "stringency_index":
        # remove countries which are only part of SI dataframe
        countries_to_remove = ['Aruba','Bermuda','Faeroe Islands','Greenland',
                               'Guam','Hong Kong','Macao','Palestine','Puerto Rico',
                               'Turkmenistan','United States Virgin Islands']
        
        data = data.drop(data[data[country_column].isin(countries_to_remove)].index)
        data = data.reset_index(drop=True)
        
        # rename countries so that they have same names as daily/cumulative data
        data.loc[data[country_column]=="Cape Verde", country_column] = "Cabo Verde"
        data.loc[data[country_column]=="Kyrgyz Republic", country_column] = "Kyrgyzstan"
        data.loc[data[country_column]=="Slovak Republic", country_column] = "Slovakia"
        
    elif data_source == "cumulative":
        countries_to_remove = ['Antarctica','Antigua and Barbuda','Armenia','Diamond Princess',
                               'Equatorial Guinea','Guinea-Bissau','Holy See','Korea, North',
                               'MS Zaandam','Maldives','Marshall Islands','Micronesia',
                               'Montenegro','North Macedonia','Palau','Saint Kitts and Nevis',
                               'Saint Lucia','Saint Vincent and the Grenadines','Samoa',
                               'Sao Tome and Principe','Summer Olympics 2020',
                               'West Bank and Gaza','Winter Olympics 2022']
        
        data = data.drop(data[data[country_column].isin(countries_to_remove)].index)
        data = data.reset_index(drop=True)
        
        # rename countries so that they have same names as daily/cumulative data
        data.loc[data[country_column]=='Burma', country_column] = 'Myanmar'
        data.loc[data[country_column]=='Congo (Brazzaville)', country_column] = 'Congo'
        data.loc[data[country_column]=='Congo (Kinshasa)', country_column] = 'Democratic Republic of Congo'
        data.loc[data[country_column]=='Czechia', country_column] = 'Czech Republic'
        data.loc[data[country_column]=='Korea, South', country_column] = 'South Korea'
        data.loc[data[country_column]=='Taiwan*', country_column] = 'Taiwan'
        data.loc[data[country_column]=='US', country_column] = 'United States'

    # daily data - check for different versions of dataset
    else:
        pass
    
    print("There have been {0} countries removed from the dataset.".format(len(countries_to_remove)))
    
    # By error proof on US4, dataframe needs to be sorted by country name
    return data.sort_values(country_column, ascending=True)

# Function that formats the timestamp values to a common one
def formatting_timestamp_string(data, country_column="Country"):

    months_str_int_map = {
        "Jan" : "1",
        "Feb" : "2",
        "Mar" : "3",
        "Apr" : "4",
        "May" : "5",
        "Jun" : "6",
        "Jul" : "7",
        "Aug" : "8",
        "Sep" : "9",
        "Oct" : "10",
        "Nov" : "11",
        "Dec" : "12"
    }

    updated_timestamps = [country_column]

    for timestamp in data.columns[1:]:
    
        # Any character that is not a numeric digit from 0 to 9
        string_month = re.findall(r"[\D']+", timestamp)[0]
        month = months_str_int_map[string_month]
    
        # Any numeric digit from 0 to 9
        day = re.findall(r"[\d']+", timestamp)[0]
        year = re.findall(r"[\d']+", timestamp)[1][2:] # last part of year 20-21-22
    
        # Format string for day if needed 
        if day.startswith("0"):
            day = day[1:]
    
        # Order of timestamp
        formatted_timestamp = "/".join([month, day, year])
    
        updated_timestamps.append(formatted_timestamp)
        
    return updated_timestamps

# Function that fixes all the country names for daily data sources useful for aggregation and merging
def check_daily_data_countries(data, file_path,
                               country_column="Country",
                               repeated_country=[["Mainland China", "China"],
                                                 ["UK", "United Kingdom"]]):
    
    update_country_name = {
        " Azerbaijan": "Azerbaijan",
        "The Bahamas": "Bahamas",
        "Bahamas, The": "Bahamas",
        "Ivory Coast": "Cote d'Ivoire",
        "Burma": "Myanmar",
        "Cape Verde": "Cabo Verde",
        "Congo (Brazzaville)": "Congo",
        "Republic of the Congo": "Congo",
        "Congo (Kinshasa)": "Democratic Republic of Congo",
        "Czechia": "Czech Republic",
        "Korea, South": "South Korea",
        "The Gambia": "Gambia",
        "Gambia, The": "Gambia",
        "Republic of Ireland": "Ireland",
        "Republic of Korea": "South Korea",
        "Iran (Islamic Republic of)": "Iran",
        "Republic of Moldova": "Moldova",
        "Russian Federation": "Russia",
        "Taipei and environs": "Taiwan",
        "Taiwan*": "Taiwan",
        "East Timor": "Timor-Leste",
        "US": "United States",
        "Viet Nam": "Vietnam"
    }

    date  = file_path.split("/")[-1].split(".")[0]
    month = date.split("-")[0]
    day   = date.split("-")[1]
    year  = date.split("-")[2]
        
    if year > "2020":
        pass
    elif month > "03":
        pass
    elif month == "03" and day > "12":
        pass
    elif month == "03" and ((day == "12") or (day == "11")):
        # delete zero values columns for Mainland China
        drop_indexes = list(data.loc[data[country_column]==repeated_country[0][0]].index)
        data = data.drop(drop_indexes).reset_index(drop=True)
    elif month == "03" and day <= "10":
        # delete values for UK and China
        drop_indexes = list(data.loc[(data[country_column]==repeated_country[0][1]) &\
                                    (data[country_column]==repeated_country[1][1])].index)
        data = data.drop(drop_indexes).reset_index(drop=True)
        data.loc[data[country_column]==repeated_country[1][0], country_column] = repeated_country[1][1]
        data.loc[data[country_column]==repeated_country[0][0], country_column] = repeated_country[0][1]
    elif month == "02":
        # delete values for UK and China
        drop_indexes = list(data.loc[(data[country_column]==repeated_country[0][1]) &\
                                    (data[country_column]==repeated_country[1][1])].index)
        data = data.drop(drop_indexes).reset_index(drop=True)
        data.loc[data[country_column]==repeated_country[1][0], country_column] = repeated_country[1][1]
        data.loc[data[country_column]==repeated_country[0][0], country_column] = repeated_country[0][1]
    elif month == "01" and day == "31":
        # delete values for UK and China
        drop_indexes = list(data.loc[(data[country_column]==repeated_country[0][1]) &\
                                    (data[country_column]==repeated_country[1][1])].index)
        data = data.drop(drop_indexes).reset_index(drop=True)
        data.loc[data[country_column]==repeated_country[1][0], country_column] = repeated_country[1][1]
        data.loc[data[country_column]==repeated_country[0][0], country_column] = repeated_country[0][1]
    else:
        # delete zero values column for China and rename Mainland China to China
        drop_indexes = list(data.loc[data[country_column]==repeated_country[0][1]].index)
        data = data.drop(drop_indexes).reset_index(drop=True)
        data.loc[data[country_column]==repeated_country[0][0], country_column] = repeated_country[0][1]

    # remove countries if present
    countries_to_remove = ['Antarctica','Antigua and Barbuda','Armenia','Aruba','Bermuda',
                           'Cayman Islands', 'Curacao','Channel Islands','Cruise Ship',
                           'Diamond Princess','Equatorial Guinea','Faroe Islands','French Guiana',
                           'Gibraltar','Greenland','Guinea-Bissau','Guadeloupe','Guam',
                           'Guernsey','Holy See','Hong Kong','Hong Kong SAR','Jersey','Korea, North',
                           'MS Zaandam','Macao','Macao SAR','Macau','Maldives',
                           'Marshall Islands','Martinique','Mayotte','Micronesia','Montenegro',
                           'North Ireland','North Macedonia','occupied Palestinian territory',
                           'Others','Palau','Palestine','Puerto Rico','Palau','Reunion',
                           'Saint Barthelemy','Saint Kitts and Nevis','Saint Lucia','Saint Martin',
                           'Saint Vincent and the Grenadines','Samoa','Sao Tome and Principe',
                           'St. Martin','Summer Olympics 2020','Turkmenistan',
                           'United States Virgin Islands','Vatican City',
                           'West Bank and Gaza','Winter Olympics 2022']
    
    data = data.drop(data[data[country_column].isin(countries_to_remove)].index)
    data = data.reset_index(drop=True)
    
    # rename countries if needed
    countries_to_rename = get_list_inner_outer_join(np.unique(data[country_column]), 
                                                    list(update_country_name.keys()), 
                                                    operation="inner")
    if len(countries_to_rename) > 0:
        for country in countries_to_rename:
            data.loc[data[country_column]==country, country_column] = update_country_name[country]
    
    return data.sort_values(country_column, ascending=True)

# Function that calculates difference of two consecutive timestamps for daily cases data
def calculating_daily_differences(data, column,
                                  country_column="Country",
                                  date_column="Timestamps"):
    
    timestamps = np.unique(data[date_column])
    difference_data = []

    for idx in range(len(timestamps)-1):
        for country in np.unique(data[country_column]):
            
            day_one = data.loc[(data[country_column]==country) & 
                               (data[date_column]==timestamps[idx]),
                               column].item()
            day_two = data.loc[(data[country_column]==country) & 
                               (data[date_column]==timestamps[idx+1]),
                               column].item()
            daily_new = day_two - day_one
        
            difference_data.append(daily_new)   
    
    # initiating the list with zeros, as comparisons are not possible for first day
    initial_difference_data = [0] * len(np.unique(data[country_column]))
    difference_data = initial_difference_data + difference_data
                                   
    data["Daily "+(" ".join(column.split(" ")[1:]))] = difference_data
                                   
    return data