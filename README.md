# Used Vehicle Sales App

This Streamlit application provides detailed analytics on used vehicle advertisements prices, allowing users to explore price distributions and depreciation based on a variety of filters such as make, model, year, condition, fuel type, and odometer readings. It is designed for potential buyers, sellers, or analysts interested in the used car market.

You can view the application [here](https://used-vehicle-sales-tool.onrender.com/#price-distribution-for-selected-vehicle)

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

## Contributing

Feel free to fork the repository and submit pull requests. You can also open issues if you find bugs or have suggestions for improvements.

## Installation

To run this application locally, you need Python and several dependencies:

```bash
git clone https://github.com/IMMontoya/Used_Vehicle_Sales_Tool.git
cd Used_Vehicle_Sales_Tool
pip install -r requirements.txt
streamlit run app.py
```

## Path to Future Improvements

1. Incorporate more recent and larger datasets to improve the accuracy and breadth of market insights.  

2. Implement proper capitalization for vehicle makes and models (e.g., 'gmc' to 'GMC') to enhance readability.  
