# Import third-party libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# Create test title
st.title('Streamlit App')

# Load our data and create a new column manufacturer by getting the first word from the model column
df = pd.read_csv('vehicles_us.csv')
df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])

# Set text header above dataframe
st.header("Data Viewer")

# Display the dataframe
st.dataframe(df)
