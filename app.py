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


def update_model_list():
    if selected_manufacturers:
        filtered_df = df[df['make'].isin(selected_manufacturers)]
        return filtered_df['model'].unique().tolist()
    return []


def update_manufacturer_list():
    if selected_models:
        filtered_df = df[df['model'].isin(selected_models)]
        return filtered_df['make'].unique().tolist()
    return []


# Title and header
st.title('Dynamic Filtering Example')
st.header('Price Distribution')

# Manufacturers widget
all_manufacturers = st.checkbox('All Manufacturers', key='all_manufacturers')
manufacturer_list = df['make'].unique().tolist()

if all_manufacturers:
    selected_manufacturers = manufacturer_list
else:
    selected_manufacturers = st.multiselect(
        'Select Manufacturers',
        options=manufacturer_list,
        default=manufacturer_list if all_manufacturers else []
    )

# Update the model list based on selected manufacturers
model_list = update_model_list()

# Models widget
all_models = st.checkbox('All Models', key='all_models')
if all_models:
    selected_models = model_list
else:
    selected_models = st.multiselect(
        'Select Models',
        options=model_list,
        default=model_list if all_models else []
    )

# Update the manufacturer list based on selected models
# This should be carefully handled to avoid conflicts; you might choose to skip this step or ensure it does not cause infinite loops
# manufacturer_list = update_manufacturer_list()

# Display selections
# st.write("Selected Manufacturers:", selected_manufacturers)
# st.write("Selected Models:", selected_models)
