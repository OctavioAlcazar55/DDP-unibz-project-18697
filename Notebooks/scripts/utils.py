import os

import pandas as pd
import numpy as np
import time

import warnings
warnings.filterwarnings("ignore")

drop_columns_dict = {"daily": ['FIPS','Admin2','Province_State','Last_Update','Lat','Long_',
                               'Active','Combined_Key','Incident_Rate','Case_Fatality_Ratio'],
                     "cumulative": ['Province/State','Lat','Long'],
                     "stringency_index": ['country_code','region_code','region_name','jurisdiction']
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
def drop_columns(data, data_source="daily"):

    columns_to_drop = drop_columns_dict[data_source]
    
    # Reading CSV file in a DataFrame
    df = data.drop(columns_to_drop, axis=1)

    print("Removed {0} columns from dataframe".format(len(columns_to_drop)))
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
