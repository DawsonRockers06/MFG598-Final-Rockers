import os
import zipfile
import pandas as pd
import streamlit as st
from sklearn.linear_model import LinearRegression
import numpy as np
import plotly.graph_objects as go

# Title and header for the Streamlit app
countyEmoji = "📍"
usEmoji = "🌎"
usFlag = '\U0001F1FA\U0001F1F8'
st.markdown(f"<h1 style='text-align: center;'>{usEmoji} US AQI Visualizer {usEmoji}</h1>", unsafe_allow_html=True)

# Define the path to the uploaded zip file and extraction directory
zipPath = "AQI_BY_COUNTY_25_YEARS.zip"
extractedDir = "aqiData"

# Extract the ZIP file if not already extracted
if not os.path.exists(extractedDir):
    with zipfile.ZipFile(zipPath, 'r') as zipRef:
        zipRef.extractall(extractedDir)

# Load all CSV files from the extracted directory into a single DataFrame
subdirPath = os.path.join(extractedDir, 'AQI_BY_COUNTY_25_YEARS')
csvFiles = [os.path.join(subdirPath, f) for f in os.listdir(subdirPath) if f.endswith('.csv')]
dfList = [pd.read_csv(file) for file in csvFiles]
aqiDf = pd.concat(dfList, ignore_index=True)

# Streamlit UI: Dropdown to select a state
state = st.selectbox(f"Select a state {usFlag}", sorted(aqiDf['State'].unique()))

# Streamlit UI: Dropdown to select a county based on the selected state
counties = sorted(aqiDf[aqiDf['State'] == state]['County'].unique())
county = st.selectbox(f"Select a County {countyEmoji}", counties)

# Streamlit UI: Slider to select a range of years
years = sorted(aqiDf['Year'].unique())
selectedYears = st.slider("Select year range", min_value=min(years), max_value=max(years), value=(min(years), max(years)))

# Filter the DataFrame based on the selected state, county, and year range
filteredDf = aqiDf[
    (aqiDf['State'] == state) &
    (aqiDf['County'] == county) &
    (aqiDf['Year'].between(selectedYears[0], selectedYears[1]))
]

# Filter the DataFrame for state-level data (ignoring county)
filteredDf2 = aqiDf[
    (aqiDf['State'] == state) &
    (aqiDf['Year'].between(selectedYears[0], selectedYears[1]))
]

# Display the filtered county-level data
st.write(f"Showing data specifically for **{county}** County **{state}** from **{selectedYears[0]}** to **{selectedYears[1]}**")
st.dataframe(filteredDf.reset_index(drop=True), use_container_width=True)

# Plot county-level AQI trend over time
if st.checkbox("Show AQI trend over time by County"):
    chartDf = (
        filteredDf.groupby("Year")["Median AQI"]
        .mean()
        .reset_index()
        .sort_values("Year")
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=chartDf["Year"],
        y=chartDf["Median AQI"],
        mode='lines+markers',
        name='County AQI',
        line=dict(color='blue')
    ))
    fig.update_layout(
        title=f"{county} County AQI Trend",
        xaxis_title="Year",
        yaxis_title="Median AQI",
        template="plotly_white"
    )
    st.plotly_chart(fig)

# Display the filtered state-level data
st.write(f"Showing data for all of **{state}** from **{selectedYears[0]}** to **{selectedYears[1]}**")
st.dataframe(filteredDf2.reset_index(drop=True), use_container_width=True)

# Plot state-level AQI trend over time
if st.checkbox("Show AQI trend over time by State"):
    chartDf2 = (
        filteredDf2.groupby("Year")["Median AQI"]
        .mean()
        .reset_index()
        .sort_values("Year")
    )

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=chartDf2["Year"],
        y=chartDf2["Median AQI"],
        mode='lines+markers',
        name='State AQI',
        line=dict(color='green')
    ))
    fig2.update_layout(
        title=f"{state} State AQI Trend",
        xaxis_title="Year",
        yaxis_title="Median AQI",
        template="plotly_white"
    )
    st.plotly_chart(fig2)

# Display summary statistics for the filtered county-level data
if st.checkbox("Show summary statistics"):
    st.write(filteredDf.describe())

# Predict future AQI data using linear regression
if st.checkbox("Predict future AQI data"):
    # Slider to select the number of future years to predict
    futureYears = st.slider("Select number of future years to predict", min_value=1, max_value=20, value=5)

    # Prepare historical data for training the regression model
    historicalData = filteredDf2.groupby("Year")["Median AQI"].mean().reset_index()
    X = historicalData["Year"].values.reshape(-1, 1)  # Feature: Year
    y = historicalData["Median AQI"].values  # Target: Median AQI

    # Train a linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Generate future years and predict AQI values
    lastYear = historicalData["Year"].max()
    futureYearsArray = np.arange(lastYear + 1, lastYear + futureYears + 1).reshape(-1, 1)
    futureAqi = model.predict(futureYearsArray)

    # Create a DataFrame for the predicted data
    futureData = pd.DataFrame({
        "Year": futureYearsArray.flatten(),
        "Median AQI": futureAqi
    })

    # Combine historical and predicted data for visualization
    combinedData = pd.concat([historicalData, futureData])

    # Plot historical and predicted AQI data
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=historicalData["Year"],
        y=historicalData["Median AQI"],
        mode='lines+markers',
        name='Historical Data',
        line=dict(color='blue')
    ))
    fig3.add_trace(go.Scatter(
        x=futureData["Year"],
        y=futureData["Median AQI"],
        mode='lines+markers',
        name='Predicted Data',
        line=dict(color='orange', dash='dash')
    ))

    # Update the layout of the graph
    fig3.update_layout(
        title="AQI Prediction",
        xaxis_title="Year",
        yaxis_title="Median AQI",
        legend_title="Data Type",
        template="plotly_white"
    )

    # Display the graph in Streamlit
    st.plotly_chart(fig3)