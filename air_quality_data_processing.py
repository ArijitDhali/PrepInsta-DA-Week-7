# -*- coding: utf-8 -*-
"""Air Quality Data Processing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hIP1AbuLG66VzL6U908jZdltd9ZxQ0VA

#**Week-7**
##**Indian Air Quality Index - Dasboard**
### *By Arijit Dhali [Linkedin](https://www.linkedin.com/in/arijit-dhali-b255b0138/)*
---
Since industrialization, there has been an increasing concern about environmental pollution. As mentioned in the WHO report 7 million premature deaths annually are linked to air pollution, air pollution is the world's largest single environmental risk. Moreover as reported in the NY Times article, India’s Air Pollution Rivals China’s as World’s Deadliest it has been found that India's air pollution is deadlier than China's.
We will explore India’s air pollution levels more granularly using this dataset.

---
This data is combined(across the years and states) and is largely a clean version of the Historical Daily Ambient Air Quality Data released by the Ministry of Environment and Forests and Central Pollution Control Board of India under the National Data Sharing and Accessibility Policy (NDSAP).

# **Importing Libraries & Inspection**

Here we import the necessary libraries for array operations (`numpy`) and working with datasets (`pandas`). We also import the `warnings module` to suppress warning messages, providing cleaner output. Now we proceed to ignore warnings in the code.
"""

import numpy as np                                  # Import numpy for array operations
import pandas as pd                                 # Import pandas for working with datasets
import warnings                                     # Import warnings module to handle warnings
warnings.filterwarnings('ignore')                   # Ignore warning messages

"""Here we set the file path for the CSV file containing air quality data. Now, we use the `pd.read_csv` function from pandas to read the CSV file into a DataFrame named '`air`', specifying the encoding as '`unicode_escape`'."""

url = '/content/drive/MyDrive/Prepinsta Winter Internship/Week 7/Air Quality.csv'  # Set the file path
air = pd.read_csv(url, encoding='unicode_escape')                               # Read the CSV file into a DataFrame using pandas

"""Here we use the sample method to randomly display 5 rows from the '`air`' DataFrame for a quick overview of the data."""

air.sample(5)  # Display a random sample of 5 rows from the 'air' DataFrame

"""# **Data Manipulation**

Here we retrieve the unique values in the '`type`' column of the '`air`' DataFrame using the unique method, showing the different types of air quality data available in the dataset.
"""

air['type'].unique()  # Get unique values in the 'type' column of the 'air' DataFrame

"""Here we replace multiple values in the '`type`' column of the '`air`' DataFrame to achieve consistency and simplify the categories."""

# Replace values in the 'type' column for consistency
air['type'].replace('Residential, Rural and other Areas','Residential',inplace = True)
air['type'].replace('Residential and others','Residential',inplace = True)
air['type'].replace('Industrial Areas','Industrial',inplace = True)
air['type'].replace('Industrial Area','Industrial',inplace = True)
air['type'].replace('Sensitive Area','Sensitive',inplace = True)
air['type'].replace('Sensitive Areas','Sensitive',inplace = True)

"""Now we check the unique values in the '`type`' column of the '`air`' DataFrame to confirm that the specified replacements have been successfully applied, ensuring consistency in the categories."""

air['type'].unique()  # Verify unique values in the 'type' column after replacements

"""Here we retrieve the unique values in the '`state`' column of the '`air`' DataFrame using the unique method, showing the different states represented in the dataset."""

air['state'].unique()  # Get unique values in the 'state' column of the 'air' DataFrame

"""Here we replace a specific value in the '`state`' column of the '`air`' DataFrame to achieve consistency. After the replacement, we check the unique values in the '`state`' column to confirm the change."""

# Replace a specific value in the 'state' column for consistency
air['state'].replace('andaman-and-nicobar-islands', 'Andaman and Nicobar Islands', inplace=True)
air['state'].unique()  # Verify unique values in the 'state' column after replacement

"""Here we process the '`date`' column by converting it to datetime format and extracting the '`year`' component. Missing '`year`' values are filled using forward fill, and the column is then converted to the integer type. Finally, we check for any remaining null values in the '`year`' column."""

# Convert the 'date' column to datetime format and extract the 'year' column
air['date'] = pd.to_datetime(air['date'])
air['year'] = air['date'].dt.year

# Fill missing 'year' values using forward fill and convert to integer type
air['year'].fillna(method='ffill', inplace=True)
air['year'] = air['year'].astype(int)

air['year'].isnull().sum()  # Check for any remaining null values in the 'year' column

"""Here we create a DataFrame named '`missing`' to show the proportion of missing values in each column of the '`air`' DataFrame. The columns are then displayed in descending order based on the proportion of missing values."""

# Create a DataFrame to show the proportion of missing values in each column
missing = pd.DataFrame(air.isna().sum() / len(air))
missing.columns = ['Proportion']

# Display the columns sorted by the proportion of missing values in descending order
print(missing.sort_values(by='Proportion', ascending=False))

"""Here we define a function `state_wise` that takes a state as an argument and calculates and prints the median values for Industrial, Residential, and Sensitive types for that state using the 'air' DataFrame. The function returns these median values."""

def state_wise(states):
    # Group the 'air' DataFrame by 'state' and 'type'
    grouped = air.groupby(['state', 'type'])

    # Create a dictionary from the grouped data
    data_dict = dict(list(grouped))

    # Extract median values for Industrial, Residential, and Sensitive types for the specified state
    kar_ind = data_dict[(states, 'Industrial')].median()
    kar_res = data_dict[(states, 'Residential')].median()
    kar_sen = data_dict[(states, 'Sensitive')].median()

    # Print and return the median values for each type
    print(kar_ind, kar_res, kar_sen)
    return kar_ind, kar_res, kar_sen

"""Here we call the `state_wise` function with the argument '`Andhra Pradesh`' and store the returned median values for Industrial, Residential, and Sensitive types in respective variables (`kar_ind`, `kar_res`, `kar_sen`)."""

# Call the state_wise function for 'Andhra Pradesh' and store the results in variables
kar_ind, kar_res, kar_sen = state_wise('Andhra Pradesh')

"""Here we use the '`loc`' method to fill missing '`no2`' and '`so2`' values in the '`Andhra Pradesh`' state for Industrial, Residential, and Sensitive types using the respective median values"""

# Fill missing 'so2' values in 'Andhra Pradesh' for Industrial, Residential, and Sensitive types
air.loc[(air['state'] == 'Andhra Pradesh') & (air['type'] == 'Industrial') & (air['so2'].isnull()), 'so2'] = kar_ind['so2']
air.loc[(air['state'] == 'Andhra Pradesh') & (air['type'] == 'Residential') & (air['so2'].isnull()), 'so2'] = kar_res['so2']
air.loc[(air['state'] == 'Andhra Pradesh') & (air['type'] == 'Sensitive') & (air['so2'].isnull()), 'so2'] = kar_sen['so2']

# Fill missing 'no2' values in 'Andhra Pradesh' for Industrial, Residential, and Sensitive types
air.loc[(air['state'] == 'Andhra Pradesh') & (air['type'] == 'Industrial') & (air['no2'].isnull()), 'no2'] = kar_ind['no2']
air.loc[(air['state'] == 'Andhra Pradesh') & (air['type'] == 'Residential') & (air['no2'].isnull()), 'no2'] = kar_res['no2']
air.loc[(air['state'] == 'Andhra Pradesh') & (air['type'] == 'Sensitive') & (air['no2'].isnull()), 'no2'] = kar_sen['no2']

"""Here we print the number of missing values in the '`rspm`' and '`spm`' columns of the '`air`' DataFrame."""

# Print the number of missing values in the 'rspm' and 'spm' columns
print(air['rspm'].isnull().sum())
print(air['spm'].isnull().sum())

"""Here, we group the '`air`' DataFrame by '`location`' and '`type`', then iterate through the groups. Within each group, we sort the values by 'date' and forward-fill missing values in the 'rspm' and 'spm' columns. The results are concatenated into a new DataFrame named '`data`'."""

# Group 'air' DataFrame by 'location' and 'type' and create a new DataFrame with forward-filled 'rspm' and 'spm' values
df1 = dict(list(air.groupby(['location', 'type'])))
data = pd.DataFrame()

# Iterate through groups, sort by 'date', and forward-fill 'rspm' and 'spm' values
for key in df1:
    df2 = df1[key].sort_values('date')
    df2['rspm'].fillna(method='ffill', inplace=True)
    df2['spm'].fillna(method='ffill', inplace=True)
    data = pd.concat([data, df2])

"""Here, we group the '`data`' DataFrame by '`location`' and '`type`', then iterate through the groups. Within each group, we sort the values by 'date' and backward-fill missing values in the 'rspm' and 'spm' columns. The results are concatenated into a new DataFrame named '`data1`'."""

# Group 'data' DataFrame by 'location' and 'type' and create a new DataFrame with backward-filled 'rspm' and 'spm' values
df1 = dict(list(data.groupby(['location', 'type'])))
data1 = pd.DataFrame()

# Iterate through groups, sort by 'date', and backward-fill 'rspm' and 'spm' values
for key in df1:
    df2 = df1[key].sort_values('date')
    df2['rspm'].fillna(method='bfill', inplace=True)
    df2['spm'].fillna(method='bfill', inplace=True)
    data1 = pd.concat([data1, df2])

"""Here we display the first few rows of the '`data1`' DataFrame to inspect the changes made, including the backward-filled '`rspm`' and '`spm`' values."""

data1.head()  # Display the first few rows of the 'data1' DataFrame

"""Here we print the number of missing values in the '`rspm`' and '`spm`' columns of the '`data1`' DataFrame after the backward-fill operations."""

# Print the number of missing values in the 'rspm' and 'spm' columns of the 'data1' DataFrame
print(data1['rspm'].isnull().sum())
print(data1['spm'].isnull().sum())

"""Here, we group the '`data1`' DataFrame by '`state`' and '`type`', then iterate through the groups. Within each group, missing values in '`rspm`' and '`spm`' columns are filled with the group-wise medians. The results are concatenated into a new DataFrame named '`data2`'."""

# Group 'data1' DataFrame by 'state' and 'type' and create a new DataFrame with median-filled 'rspm' and 'spm' values
df1 = dict(list(data1.groupby(['state', 'type'])))
data2 = pd.DataFrame()

# Iterate through groups and fill missing 'rspm' and 'spm' values with group-wise medians
for key in df1:
    df2 = df1[key]
    df2['rspm'].fillna(df2['rspm'].median(), inplace=True)
    df2['spm'].fillna(df2['spm'].median(), inplace=True)
    data2 = pd.concat([data2, df2])

"""Here we print the number of missing values in the '`rspm`' and '`spm`' columns of the '`data2`' DataFrame after filling missing values with group-wise medians."""

# Print the number of missing values in the 'rspm' and 'spm' columns of the 'data2' DataFrame
print(data2['rspm'].isnull().sum())
print(data2['spm'].isnull().sum())

"""Here we display the entire '`data2`' DataFrame to inspect the final dataset after filling missing values with group-wise medians."""

data2  # Display the 'data2' DataFrame

"""Here, we group the '`data2`' DataFrame by '`type`', then iterate through the groups. Within each group, missing values in '`rspm`' and '`spm`' columns are filled with the group-wise medians. The results are concatenated into a new DataFrame named '`data3`'."""

# Group 'data2' DataFrame by 'type' and create a new DataFrame with median-filled 'rspm' and 'spm' values
df1 = dict(list(data2.groupby('type')))
data3 = pd.DataFrame()

# Iterate through groups and fill missing 'rspm' and 'spm' values with group-wise medians
for key in df1:
    df2 = df1[key]
    df2['rspm'].fillna(df2['rspm'].median(), inplace=True)
    df2['spm'].fillna(df2['spm'].median(), inplace=True)
    data3 = pd.concat([data3, df2])

data3

"""Here we print the number of missing values in the '`rspm`' and '`spm`' columns of the '`data3`' DataFrame after filling missing values with group-wise medians."""

# Print the number of missing values in the 'rspm' and 'spm' columns of the 'data3' DataFrame
print(data3['rspm'].isnull().sum())
print(data3['spm'].isnull().sum())

"""Here we display the count of each type in the '`data3`' DataFrame using the `value_counts` method. This provides an overview of the distribution of types in the final processed dataset."""

data3['type'].value_counts()  # Display the count of each type in the 'data3' DataFrame

"""# **Data Saving**

Here we reset the index of the '`data3`' DataFrame and drop some unnecessary columns to obtain a cleaner and more concise dataset. The modified DataFrame is displayed using `head()`.
"""

# Reset index and drop unnecessary columns from the 'data3' DataFrame
data3.reset_index(inplace=True)
data3.drop(columns=['index', 'stn_code', 'sampling_date', 'agency', 'location_monitoring_station'], inplace=True)
data3.head()

"""Here we check for missing values in the '`data3`' DataFrame to ensure that the dataset is free of any remaining null values after the preprocessing steps."""

data3.isnull().sum()  # Check for missing values in the 'data3' DataFrame

"""Here we use the to_csv method to save a copy of the final cleaned data stored in the '`data3`' DataFrame to a CSV file named '`air_quality_cleaned_data.csv`'. The index=False parameter ensures that the index is not included in the saved file."""

data3.to_csv('air_quality_cleaned_data.csv', index=False)  # Save a copy of the final cleaned data to a CSV file