# MFG598 Final Project – Dawson Rockers

Welcome to the final project repository for MFG598, created by Dawson Rockers, a Robotics Engineering student at Arizona State University.

This project is a Streamlit-based web application that allows users to explore, visualize, and forecast historical air quality data (AQI) for U.S. counties and states over the last 25 years. It combines interactive data filtering, visualization, and machine learning-based prediction in an intuitive user interface.

## 🔧 Project Overview

The goal of this project was to create a data-driven interactive tool that enables exploration of long-term AQI trends across the United States. Users can:

- Select specific states and counties to view AQI data

- Compare historical trends over time

- Generate interactive plots of AQI trends using Plotly

- View summary statistics

- Predict future AQI values using a linear regression model

The dataset is sourced from a ZIP archive containing annual AQI CSV files for all U.S. counties from the past 25 years. The app automatically unzips and aggregates the data for seamless analysis.

## 📁 Repository Contents
- [Requirements](requirements.txt) - This file must be installed using -

        pip install -r requirements.txt
  before the "Final Code" will work.
- [Final Code](FinalCode.py) – The main Python script that generates the plot.
- [Compiled Test Files](AllTestFiles) - A file containing all of the tesst files leading up to the final python file
- [ReadMe](README.md) – This file.
    
## 📌 Key Features

- Interactive AQI Data Exploration: Select U.S. states and counties to visualize Air Quality Index (AQI) data across a 25-year period.

- Dynamic Filtering: Use sliders to define custom year ranges and explore location-specific air quality trends.

- Dual-Level Analysis: View AQI trends and statistics at both county and state levels.

- Data Visualizations: Generate interactive time-series plots using Plotly to illustrate AQI trends.

- Predictive Modeling: Forecast future AQI values using linear regression based on historical data.

- Streamlit Web App Interface: User-friendly UI with dropdowns, sliders, checkboxes, and embedded dataframes.

## 🛠 Tools Used
    
- Python 3.12.2

## 👨‍🎓 Author

- Dawson Rockers
- Senior, Robotics Engineering
- Arizona State University – Polytechnic Campus
- Email: drockers16@gmail.com
