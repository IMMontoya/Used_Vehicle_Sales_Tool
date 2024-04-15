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

# Change the year column to an integer
df['year'] = df['year'].astype(int)

# ---------------------------------#
# Title
st.title('Temp Title')
# ---------------------------------#

# ---------------------------------#
# Header
st.header('Price Distribution for Selected Vehicle')

# Create three columns for the necessary arguments: make, model, and year
arg_col1, arg_col2, arg_col3 = st.columns(3)

with arg_col1:
    # Create a select box for the manufacturers
    manufacturers_list = df['make'].unique()
    manufacturer = st.selectbox('Select a manufacturer', manufacturers_list)
    # Filter the data
    filtered_df = df[df['make'] == manufacturer]

with arg_col2:
    # Create a select box for the models
    model_list = filtered_df['model'].unique()
    model = st.selectbox('Select a model', model_list)
    # Filter the data
    filtered_df = filtered_df[filtered_df['model'] == model]

with arg_col3:
    # Create a select box for the years
    year_list = filtered_df['year'].unique()
    year = st.selectbox('Select a year', year_list)
    # Filter the data
    filtered_df = filtered_df[filtered_df['year'] == year]

# Options for more detailed filtering
opt_arg_col1, opt_arg_col2, opt_arg_col3 = st.columns(3)

with opt_arg_col1:
    # Create a checkbox for the condition
    condition_chbox = st.checkbox('Specify the Condition?')
    if condition_chbox:
        condition_list = filtered_df['condition'].unique()
        condition = st.selectbox('Select a condition', condition_list)
        # Filter the data
        filtered_df = filtered_df[filtered_df['condition'] == condition]

with opt_arg_col2:
    # Create a checkbox for the fuel type
    fuel_chbox = st.checkbox('Specify the Fuel Type?')
    if fuel_chbox:
        fuel_list = filtered_df['fuel_type'].unique()
        fuel = st.selectbox('Select a fuel type', fuel_list)
        # Filter the data
        filtered_df = filtered_df[filtered_df['fuel_type'] == fuel]

with opt_arg_col3:
    # Create a checkbox for the odometer
    odometer_chbox = st.checkbox('Specify the Milage?')
    if odometer_chbox:
        # Create a slider for the odometer
        min_odometer = int(filtered_df['odometer_miles'].min())
        max_odometer = int(filtered_df['odometer_miles'].max())
        odometer = st.slider('Select an odometer range', min_odometer,
                             max_odometer, (min_odometer, max_odometer))
        # Filter the data
        filtered_df = filtered_df[(filtered_df['odometer_miles'] >= odometer[0]) & (
            filtered_df['odometer_miles'] <= odometer[1])]


# Reset the index
filtered_df = filtered_df.reset_index(drop=True)

# Get the stats for the selection
stats = filtered_df['price'].describe()
# Remove the std since it is not useful
stats = stats.drop('std')
# Convert the stats to a dataframe
stats = stats.to_frame()
# Add a description column
stats['Description'] = ['# of matching vehicles in dataset', 'Average price',
                        'Minimum price', '25th percentile', 'Median price', '75th percentile', 'Maximum price']
# Re-arrange the columns
stats = stats[['Description', 'price']]
# Rename the price column
stats.rename(columns={'price': 'Value'}, inplace=True)
# Format everything but the count index to be in dollars
stats['Value'] = stats['Value'].apply(
    lambda x: f'${x:,.2f}' if x != stats.loc['count', 'Value'] else x)

# Create a histogram of the prices
price_dist_fig = px.histogram(filtered_df, x='price',
                              histnorm='percent', template='plotly_dark', labels={'price': 'Price in USD'})


# Show the histogram
st.plotly_chart(price_dist_fig)

# Show the stats
st.write("Here are the stats for your selection:", stats)

# ---------------------------------#
