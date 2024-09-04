# Used Vehicle Sales App

This Streamlit application provides detailed analytics on used vehicle advertisements prices, allowing users to explore price distributions and depreciation based on a variety of filters such as make, model, year, condition, fuel type, and odometer readings. It is designed for potential buyers, sellers, or analysts interested in the used car market.

## Table of Contents

[Application](https://used-vehicle-sales-tool.onrender.com/#price-distribution-for-selected-vehicle)  
[Notebook](/notebooks/EDA.ipynb)  
[Installation](#installation)  
[Features](#features)  
[Usage](#usage)  
[Libraries Used](#libraries-used)

## Installation

To run this application locally, you need Python and several dependencies:

```bash
git clone https://github.com/IMMontoya/Used_Vehicle_Sales_Tool.git
cd Used_Vehicle_Sales_Tool
pip install -r requirements.txt
streamlit run app.py
```

## Features

- **Dynamic Filtering**: Select from dropdowns to filter vehicles by manufacturer, model, and year.
- **Conditional Filters**: Further refine your search by condition, fuel type, and odometer range through interactive checkboxes and sliders.
- **Price Distribution Visualization**: View a histogram displaying the distribution of prices for the selected vehicle category.
- **Depreciation Analysis**: Calculate and display the depreciation per 1,000 miles using linear regression, provided there's sufficient data variability.
- **Data Table Display**: View a detailed table of vehicles matching the selected criteria.
- **Responsive Design**: The application is designed to adjust to various screen sizes, providing a seamless experience across devices.

## Usage  

Once the application is running, navigate through the interface:

1. Select a manufacturer, model, and year.
2. Optionally specify conditions like vehicle condition, fuel type, and mileage.
3. View histograms, statistics, and depreciation information based on your selections.
4. The final section displays a detailed table of all vehicles that match your criteria.

## Libraries Used

Python 3.11.8  
plotly version=5.15.0  
numpy version=1.26.4  
pandas version=2.0.3  
streamlit version=1.25.0  
