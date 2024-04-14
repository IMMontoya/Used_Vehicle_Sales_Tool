# Import third-party libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Import local libraries
import functions as f

# Load the data from the csv file
df = pd.read_csv('vehicles_us.csv')

# Keep only the necessary columns
keep_columns = ['price', 'model_year',
                'model', 'condition', 'fuel', 'odometer']
# ... by dropping the columns not in the keep_columns list
df = df[keep_columns]

# Drop rows missing the year since that will be a necessary filter
df = df.dropna(subset=['model_year'])
# Missing odometer can stay since they will be dropped by default when creating the scatter plot

# Strip and lowercase the string columns
string_columns = ['model', 'condition', 'fuel']
df[string_columns] = df[string_columns].apply(
    lambda x: x.str.strip().str.lower())

# Apply the normalize ford f series function to the model column
df['model'] = df['model'].apply(f.normalize_ford_f_series)

# Create make column by splitting the model column
df['make'] = df['model'].str.split(' ').str[0]
# Remove the make from the model column
df['model'] = df['model'].str.split(
    ' ').str[1:].str.join(' ')

# Rename columns to my liking
df.rename(columns={'model_year': 'year', 'fuel': 'fuel_type',
                   'odometer': 'odometer_miles'}, inplace=True)

# Rearrange the columns to my liking
df = df[['price', 'make', 'model',
         'year', 'condition', 'fuel_type', 'odometer_miles']]

# ---------------------------------#

# Set the title of the app
st.title('Temp Title')

# View the data
st.write(df)
