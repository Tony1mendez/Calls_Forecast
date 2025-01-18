import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load your actual DataFrames
pediatric_forecast = pd.read_csv('pediatric_forecast.csv')
adult_forecast = pd.read_csv('adult_forecast.csv')

# Ensure 'ds' column is in datetime format
pediatric_forecast['ds'] = pd.to_datetime(pediatric_forecast['ds'])
adult_forecast['ds'] = pd.to_datetime(adult_forecast['ds'])

# Streamlit app layout
st.title("CALLS FORECAST DASHBOARD")

# Sidebar for user inputs
st.sidebar.header("FORECAST FILTERS :")

# Dropdown for selecting pediatric regions
pediatric_regions = ['forecast_CA', 'forecast_CT', 'forecast_Compact', 'forecast_MA', 'forecast_NY']
selected_pediatric_regions = st.sidebar.multiselect("Select Pediatric Agegroup Regions Forecast", pediatric_regions)

# Dropdown for selecting adult regions (adjust according to your actual columns)
adult_regions = ['forecast_CA', 'forecast_CT', 'forecast_Compact', 'forecast_MA', 'forecast_NY']  # Adjust as needed
selected_adult_regions = st.sidebar.multiselect("Select Adult Agegroup Regions Forecast", adult_regions)

# Date range selection for pediatric and adult data
start_date = st.sidebar.date_input("Start Date", pediatric_forecast['ds'].min())
end_date = st.sidebar.date_input("End Date", pediatric_forecast['ds'].max())

# Filter the pediatric DataFrame based on selected date range and regions
filtered_pediatric_data = pediatric_forecast[
    (pediatric_forecast['ds'] >= pd.Timestamp(start_date)) & 
    (pediatric_forecast['ds'] <= pd.Timestamp(end_date))
]

# Filter the adult DataFrame based on selected date range and regions
filtered_adult_data = adult_forecast[
    (adult_forecast['ds'] >= pd.Timestamp(start_date)) & 
    (adult_forecast['ds'] <= pd.Timestamp(end_date))
]

# Create the pediatric figure
fig_pediatric = go.Figure()

# Add traces for each selected pediatric region
for region in selected_pediatric_regions:
    if region in filtered_pediatric_data.columns:  # Check if the region exists in the filtered data
        fig_pediatric.add_trace(go.Scatter(x=filtered_pediatric_data['ds'], y=filtered_pediatric_data[region], mode='lines', name=region))

# Update layout of the pediatric figure
fig_pediatric.update_layout(title='Pediatric Forecast', xaxis_title='Date', yaxis_title='Forecasted Calls')

# Display the pediatric figure in the Streamlit app
st.header("Pediatric Age Group Forecast:")
st.plotly_chart(fig_pediatric)

# Create the adult figure
fig_adult = go.Figure()

# Add traces for each selected adult region
for region in selected_adult_regions:
    if region in filtered_adult_data.columns:  # Check if the region exists in the filtered data
        fig_adult.add_trace(go.Scatter(x=filtered_adult_data['ds'], y=filtered_adult_data[region], mode='lines', name=region))

# Update layout of the adult figure
fig_adult.update_layout(title='Adult Forecast', xaxis_title='Date', yaxis_title='Forecasted Calls')

# Display the adult figure in the Streamlit app
st.header("Adult Age Group Forecast:")
st.plotly_chart(fig_adult)

# Sidebar for combined forecast filters
st.sidebar.header("Combined Forecast Filters")

# Dropdown for selecting combined regions (same as above)
combined_regions = ['total_forecast_CA', 'total_forecast_CT', 'total_forecast_Compact', 'total_forecast_MA', 'total_forecast_NY'] # Combine selections from both forecasts

selected_combined_regions = st.sidebar.multiselect("Select Combined Agegroup Regions Forecast", combined_regions)

# Date range selection for combined data
start_date_combined = st.sidebar.date_input("Start Date (Combined)", pediatric_forecast['ds'].min())
end_date_combined = st.sidebar.date_input("End Date (Combined)", pediatric_forecast['ds'].max())

combined_df = pd.merge(adult_forecast, pediatric_forecast, on='ds', suffixes=('_adult', '_pediatric'))

# Initialize a list for new total columns
total_columns = []

# Loop through the columns of adult_forecast (excluding 'ds')
for col in adult_forecast.columns[2:]:  # Skip the ds column
    total_col_name = f'total_{col}'
    combined_df[total_col_name] = combined_df[f'{col}_adult'] + combined_df[f'{col}_pediatric']
    total_columns.append(total_col_name)

# Select relevant columns for final output
final_df = combined_df[['ds'] + total_columns]

# Display the final DataFrame in the Streamlit app
 

# Filter the combined DataFrame based on selected date range and combined regions
filtered_combined_data = combined_df[
    (combined_df['ds'] >= pd.Timestamp(start_date_combined)) & 
    (combined_df['ds'] <= pd.Timestamp(end_date_combined))
]

# Create the combined figure
fig_combined = go.Figure()

# Add traces for each selected combined region
for region in selected_combined_regions:
    if region in filtered_combined_data.columns:  # Check if the region exists in the filtered data
        fig_combined.add_trace(go.Scatter(x=filtered_combined_data['ds'], 
                                           y=filtered_combined_data[region], 
                                           mode='lines', 
                                           name=region))

# Update layout of the combined figure
fig_combined.update_layout(title='Combined Age Group Forecast', xaxis_title='Date', yaxis_title='Forecasted Calls')

# Display the combined figure in the Streamlit app
st.header("Combined Age Group Forecast:")
st.plotly_chart(fig_combined)

st.header('PEDIATRIC FORECAST DATASET: ')
st.dataframe(pediatric_forecast.drop('Unnamed: 0',axis=1))

st.header('ADULT FORECAST DATASET: ')
st.dataframe(adult_forecast.drop('Unnamed: 0',axis=1))

st.header('COMBINED FORECAST DATASET: ') 
st.dataframe(final_df)
