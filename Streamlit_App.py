import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("Oluwafemi.csv")

st.set_page_config(layout="wide")

# Convert dates
df["Start date"] = pd.to_datetime(df["Start date"])
df["End date"] = pd.to_datetime(df["End date"])
df["Duration"] = (df["End date"] - df["Start date"]).dt.days
df["Year"] = df["Start date"].dt.year

# =====================
# SIDEBAR FILTERS
# =====================
st.sidebar.markdown("""
Name: Oradare Oluwafemi
""")

st.sidebar.header("Filters")

min_date = df["Start date"].min().date()
max_date = df["Start date"].max().date()

selected_states = st.sidebar.multiselect(
    "Select State(s)",
    options=sorted(df["State"].dropna().unique())
)

start_date = st.sidebar.date_input("Start Date", value=min_date)
end_date = st.sidebar.date_input("End Date", value=max_date)

st.sidebar.link_button(
    "💬 Chat on WhatsApp",
    "https://wa.me/your +2349169024475?text=Hello%20👋%20I%20need%20support%20regarding%20the%20incident%20dataset.")

st.sidebar.link_button(
    "💬contact via email",
    "https://wa.me/your femikingsley1234@gmail.com?text=Hello%20👋%20I%20need%20support%20regarding%20the%20incident%20dataset.")

# =====================
# APPLY FILTERS
# =====================
filtered_df = df.copy()

if selected_states:
    filtered_df = filtered_df[filtered_df["State"].isin(selected_states)]

filtered_df = filtered_df[
    (filtered_df["Start date"] >= pd.to_datetime(start_date)) &
    (filtered_df["Start date"] <= pd.to_datetime(end_date))
]

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# =====================
# CHART 1
# =====================
st.subheader("Trend of Incidents Over Time")
incidents_per_month = filtered_df.groupby(
    filtered_df["Start date"].dt.to_period("M")
).size()

fig, ax = plt.subplots()
incidents_per_month.plot(kind="line", ax=ax)
ax.set_xlabel("Month")
ax.set_ylabel("Number of Incidents")
st.pyplot(fig)
st.markdown("Summary: Incidents show a generally increasing/decreasing/stable trend over time, peaking in the month with the highest recorded incidents.")

# =====================
# CHART 2
st.subheader("States with Highest Total Deaths")

state_deaths = filtered_df.groupby("State")["Number of deaths"].sum().sort_values(ascending=False)

fig, ax = plt.subplots()
state_deaths.plot(kind="bar", ax=ax)
st.pyplot(fig)

# Summary
top_state = state_deaths.idxmax()
top_value = state_deaths.max()
total_deaths = state_deaths.sum()

st.markdown(
    f"""
**Summary:**  
- **{top_state}** has the highest number of deaths with **{top_value:,}** cases.  
- Across all states, the total recorded deaths are **{total_deaths:,}**.  
"""
)

# =====================
# CHART 3
# =====================
st.subheader("Deadliest Incidents")

top_incidents = (
    filtered_df.groupby("Incident")["Number of deaths"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots()
top_incidents.plot(kind="barh", ax=ax, color="darkred")
ax.invert_yaxis()  # highest at the top
ax.set_xlabel("Number of Deaths")

st.pyplot(fig)

# Summary
deadliest_incident = top_incidents.idxmax()
deadliest_value = top_incidents.max()
total_top10 = top_incidents.sum()

st.markdown(
    f"""
**Summary:**  
- The deadliest incident is **{deadliest_incident}** with **{deadliest_value:,}** deaths.  
- The top 10 incidents account for a combined **{total_top10:,}** deaths.  
"""
)

# =====================
# CHART 4
# =====================
st.subheader("Proportion of Deaths by Top 10 States")
top10_state_deaths = filtered_df.groupby("State")["Number of deaths"].sum().nlargest(10)

fig, ax = plt.subplots()
top10_state_deaths.plot(kind="pie", autopct="%1.1f%%", ax=ax)
ax.set_ylabel("")
st.pyplot(fig)

# =====================
# CHART 5
# =====================
st.subheader("Trend of Deaths Per Year Per State")

fig, ax = plt.subplots(figsize=(10, 6))
filtered_df.groupby(["Year", "State"])["Number of deaths"].sum().unstack().plot(ax=ax)
st.pyplot(fig)

# =====================
# CHART 6
# =====================
st.subheader("Incident Type with Highest Average Deaths")

fig, ax = plt.subplots()
filtered_df.groupby("Incident")["Number of deaths"].mean().nlargest(10).plot(kind="barh", ax=ax)
st.pyplot(fig)

# =====================
# CHART 7
# =====================
st.subheader("Most Frequent Incident Type")

fig, ax = plt.subplots()
filtered_df["Incident"].value_counts().nlargest(10).plot(kind="barh", ax=ax)
st.pyplot(fig)
