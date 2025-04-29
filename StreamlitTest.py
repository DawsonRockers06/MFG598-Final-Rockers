# streamlit_app.py

import os
import zipfile
import pandas as pd
import streamlit as st


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

