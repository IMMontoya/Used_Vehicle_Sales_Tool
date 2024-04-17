# Import third-party libraries
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import statsmodels.api as sm  # For the ols trendline in the scatter plots


# Load the data from the csv file
df = pd.read_csv('vehicles_us_cleaned.csv')  # Cleaned per the EDA notebook


# Drop the unnecessary columns
df = df.drop(columns=['cylinders', 'transmission',
             'type', 'paint_color', 'is_4wd', 'date_posted', 'days_listed'])


# Set the template for the plotly figures
px_template = 'plotly_dark'

# ---------------------------------#

# Title
st.title('Used Vehicle Sales Tool')

# ---------------------------------#
# Section 1


# Header
st.header('Price Distribution for Selected Vehicle')

# Create three columns for the necessary arguments: make, model, and year
arg_col1, arg_col2, arg_col3 = st.columns(3)

with arg_col1:
    # Create a select box for the manufacturers
    manufacturers_list = sorted(df['make'].unique())
    manufacturer = st.selectbox('Select a manufacturer', manufacturers_list)
    # Filter the data
    filtered_df = df[df['make'] == manufacturer]

with arg_col2:
    # Create a select box for the models
    model_list = sorted(filtered_df['model'].unique())
    model = st.selectbox('Select a model', model_list)
    # Filter the data
    filtered_df = filtered_df[filtered_df['model'] == model]

with arg_col3:
    # Create a select box for the years
    year_list = sorted(filtered_df['year'].unique(), reverse=True)
    year = st.selectbox('Select a year', year_list)
    # Filter the data
    filtered_df = filtered_df[filtered_df['year'] == year]

# Options for more detailed filtering
opt_arg_col1, opt_arg_col2, opt_arg_col3 = st.columns(3)

with opt_arg_col1:
    # Create a checkbox for the condition
    condition_chbox = st.checkbox('Specify the Condition?')
    if condition_chbox:
        condition_list = sorted(filtered_df['condition'].unique())
        condition = st.selectbox('Select a condition', condition_list)
        # Filter the data
        filtered_df = filtered_df[filtered_df['condition'] == condition]

with opt_arg_col2:
    # Create a checkbox for the fuel type
    fuel_chbox = st.checkbox('Specify the Fuel Type?')
    if fuel_chbox:
        fuel_list = sorted(filtered_df['fuel_type'].unique())
        fuel = st.selectbox('Select a fuel type', fuel_list)
        # Filter the data
        filtered_df = filtered_df[filtered_df['fuel_type'] == fuel]

with opt_arg_col3:
    # Create a checkbox for the odometer
    odometer_chbox = st.checkbox('Specify the Milage?')
    if odometer_chbox:
        # Display message to user
        st.write(
            'Note: Vehicles with no odometer reading will be excluded when specifying the milage.')
        # Create a slider for the odometer
        min_odometer = int(filtered_df['odometer_miles'].min())
        max_odometer = int(filtered_df['odometer_miles'].max())
        if min_odometer == max_odometer:  # If all vehicles have the same odometer reading
            st.write(
                f'All vehicles have an odometer reading of {min_odometer} miles.')
        else:
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
stats['Description'] = ['# of matching vehicles in dataset', 'Average price (USD)',
                        'Minimum price (USD)', '25th percentile (USD)', 'Median price (USD)', '75th percentile (USD)', 'Maximum price (USD)']
# Re-arrange the columns
stats = stats[['Description', 'price']]
# Rename the price column
stats.rename(columns={'price': 'Value'}, inplace=True)
# Format the Value column to nearest cent
stats['Value'] = stats['Value'].apply(
    lambda x: f'{x:.2f}')
# Reset the index
stats = stats.reset_index(drop=True)

# Create a histogram of the prices
price_dist_fig = px.histogram(filtered_df, x='price',
                              histnorm='percent', template=px_template, labels={'price': 'Price in USD'}, width=350)


# Set two columns for the histogram and the stats
hist_col, stats_col = st.columns(2)

with hist_col:
    # Show the histogram
    st.plotly_chart(price_dist_fig)

with stats_col:
    # Insert spacer with a specific height
    st.write("<div style='margin-top: 55px'></div>", unsafe_allow_html=True)
    # Show the stats
    st.write("Here are the stats for your selection based on the dataset:")
    st.table(stats)

# ---------------------------------#
# Section 2

# Header
st.header('Selected Vehicle Depreciation')

# Drop NaN values in the odometer column
filtered_df = filtered_df.dropna(subset=['odometer_miles'])

# Calculate slope and intercept for the linear regression for the depreciation statement
# Calculate the unique counts of odometer readings and prices
unique_odometers = filtered_df['odometer_miles'].nunique()
unique_prices = filtered_df['price'].nunique()

# Check if there is enough variation in odometer readings and prices
if unique_odometers > 1 and unique_prices > 1:
    # Perform the regression
    slope, intercept = np.polyfit(
        filtered_df['odometer_miles'], filtered_df['price'], 1)
    depreciation = slope * 1000
    depreciation_str = f'Based on the dataset, your selected vehicle depreciates by ${(-1 * depreciation):.2f} per 1,000 miles.'
else:
    # Set depreciation message since no variability
    depreciation_str = 'Insufficient data variability to calculate depreciation.'

# Create the scatter plot
fig = px.scatter(filtered_df, x='odometer_miles', y='price',
                 trendline='ols', template=px_template, labels={'price': 'Price in USD', 'odometer_miles': 'Miles on Odometer'})

# Only show if Oddometer is not specified
if odometer_chbox:
    # Message for the user
    st.write(
        'Please deselect "Specify the Milage?" to see the depreciation per odometer milage.')
else:
    # Show the depreciation message
    st.write(depreciation_str)
    # Show the scatter plot
    st.plotly_chart(fig)

# ---------------------------------#
# Section 3

st.header('All Results for the Selected Vehicle')

# Change column names for displaying the dataframe
df_display = filtered_df.copy()
df_display.columns = ['Price (USD)', 'Make', 'Model',
                      'Year', 'Condition', 'Fuel Type', 'Odometer (miles)']
# Show the df
st.table(df_display)
