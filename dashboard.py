import streamlit as st
import pandas as pd
import plotly.express as px

# Load your enriched leads data
df = pd.read_csv("enriched_leads.csv")  # Update with your actual data source

st.title("📊 SignalBoost AI - Lead Dashboard")

# Metric Overview
st.metric("Total Leads", int(len(df)))
st.metric("Enriched Leads", int(df['enriched'].sum()))
st.metric("Average Lead Score", float(round(df['score'].mean(), 2)))

# Score Distribution
st.subheader("Lead Quality Score Distribution")
fig = px.histogram(df, x='score', nbins=10, title="Score Distribution")
st.plotly_chart(fig)

# Leads by Industry
st.subheader("Leads by Industry")
industry_fig = px.bar(df['industry'].value_counts().reset_index(), x='index', y='industry', labels={'index': 'Industry', 'industry': 'Count'})
st.plotly_chart(industry_fig)

# Leads by Country/Location
if 'location' in df.columns:
    st.subheader("Geographic Distribution of Leads")
    location_fig = px.choropleth(df, locations='location', locationmode='country names', title="Lead Locations")
    st.plotly_chart(location_fig) 