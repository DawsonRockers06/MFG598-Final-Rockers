import os
import zipfile
import pandas as pd
import streamlit as st
from sklearn.linear_model import LinearRegression
import numpy as np
import plotly.graph_objects as go

# Title
county_emoji = "📍"
us_emoji = "🌎"
us_flag = '\U0001F1FA\U0001F1F8'
st.markdown(f"<h1 style='text-align: center;'>{us_emoji} US AQI Visualizer {us_emoji}</h1>", unsafe_allow_html=True)

# Define the path to the uploaded zip file
zip_path = "AQI_BY_COUNTY_25_YEARS.zip" 
extracted_dir = "aqi_data"

# Extract the ZIP file if not already extracted
if not os.path.exists(extracted_dir):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extracted_dir)

# Build subdir path and load all CSV files
subdir_path = os.path.join(extracted_dir, 'AQI_BY_COUNTY_25_YEARS')
csv_files = [os.path.join(subdir_path, f) for f in os.listdir(subdir_path) if f.endswith('.csv')]

# Load all CSVs into one DataFrame
df_list = [pd.read_csv(file) for file in csv_files]
aqi_df = pd.concat(df_list, ignore_index=True)

# Streamlit UI
state = st.selectbox(f"Select a state {us_flag}", sorted(aqi_df['State'].unique()))
counties = sorted(aqi_df[aqi_df['State'] == state]['County'].unique())
county = st.selectbox(f"Select a County {county_emoji}", counties)

# Optional year filter
years = sorted(aqi_df['Year'].unique())
selected_years = st.slider("Select year range", min_value=min(years), max_value=max(years), value=(min(years), max(years)))

# Filtered DataFrame
filtered_df = aqi_df[
    (aqi_df['State'] == state) & 
    (aqi_df['County'] == county) &
    (aqi_df['Year'].between(selected_years[0], selected_years[1]))]

filtered_df2 = aqi_df[
    (aqi_df['State'] == state) & 
    (aqi_df['Year'].between(selected_years[0], selected_years[1]))]

# Display
st.write(f"Showing data specifically for **{county}** County **{state}** from **{selected_years[0]}** to **{selected_years[1]}**")
st.dataframe(filtered_df.reset_index(drop=True))

#Created a Graph of the AQI over time by state and county
if st.checkbox("Show AQI trend over time by County"):
    chart_df = (
        filtered_df.groupby("Year")["Median AQI"]
        .mean()
        .reset_index()
        .sort_values("Year")
    )

    st.line_chart(chart_df.rename(columns={"Median AQI": "Average Median AQI"}).set_index("Year"))

st.write(f"Showing data for all of **{state}** from **{selected_years[0]}** to **{selected_years[1]}**")
st.dataframe(filtered_df2)

#Creates a Graph of the AQI over time by state
if st.checkbox("Show AQI trend over time by State"):
    chart_df2 = (
        filtered_df2.groupby("Year")["Median AQI"]
        .mean()
        .reset_index()
        .sort_values("Year")
    )

    st.line_chart(chart_df2.rename(columns={"Median AQI": "Average Median AQI"}).set_index("Year"))

# Summary stats (optional)
if st.checkbox("Show summary statistics"):
    st.write(filtered_df.describe())

# Add a slider for predicting future AQI data
if st.checkbox("Predict future AQI data"):
    future_years = st.slider("Select number of future years to predict", min_value=1, max_value=20, value=5)

    # Prepare data for prediction
    historical_data = filtered_df2.groupby("Year")["Median AQI"].mean().reset_index()
    X = historical_data["Year"].values.reshape(-1, 1)  # Feature: Year
    y = historical_data["Median AQI"].values  # Target: Median AQI

    # Train a linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Generate future years
    last_year = historical_data["Year"].max()
    future_years_array = np.arange(last_year + 1, last_year + future_years + 1).reshape(-1, 1)

    # Predict future AQI values
    future_aqi = model.predict(future_years_array)

    # Combine historical and predicted data for visualization
    future_data = pd.DataFrame({
        "Year": future_years_array.flatten(),
        "Median AQI": future_aqi
    })
    combined_data = pd.concat([historical_data, future_data])

    # Create a Plotly figure
    fig = go.Figure()

    # Add historical data as a solid blue line
    fig.add_trace(go.Scatter(
        x=historical_data["Year"],
        y=historical_data["Median AQI"],
        mode='lines',
        name='Historical Data',
        line=dict(color='blue', width=2)
    ))

    # Add predicted data as a dashed yellow line
    fig.add_trace(go.Scatter(
        x=future_data["Year"],
        y=future_data["Median AQI"],
        mode='lines',
        name='Predicted Data',
        line=dict(color='yellow', width=2, dash='dash')
    ))

    # Update layout for better visualization
    fig.update_layout(
        title="AQI Prediction",
        xaxis_title="Year",
        yaxis_title="Median AQI",
        legend_title="Data Type",
        template="plotly_white"
    )

    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig)