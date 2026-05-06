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
st.subheader("Proportion of Deaths by Top 10 States")

top10_state_deaths = (
    filtered_df.groupby("State")["Number of deaths"]
    .sum()
    .nlargest(10)
)

fig, ax = plt.subplots()
top10_state_deaths.plot(kind="pie", autopct="%1.1f%%", ax=ax)
ax.set_ylabel("")
st.pyplot(fig)

# Summary
top_state = top10_state_deaths.idxmax()
top_value = top10_state_deaths.max()
total_top10 = top10_state_deaths.sum()
top_share = (top_value / total_top10) * 100

st.markdown(
    f"""
**Summary:**  
- **{top_state}** contributes the largest share at **{top_share:.1f}%** of deaths among the top 10 states.  
- Together, these states account for **{total_top10:,}** deaths, indicating fatalities are concentrated in a limited number of regions.  
"""
)

# =====================
# CHART 5
# =====================
st.subheader("Trend of Deaths Per Year Per State")

yearly_state_deaths = (
    filtered_df.groupby(["Year", "State"])["Number of deaths"]
    .sum()
    .unstack()
)

fig, ax = plt.subplots(figsize=(10, 6))
yearly_state_deaths.plot(ax=ax)
ax.set_xlabel("Year")
ax.set_ylabel("Number of Deaths")

st.pyplot(fig)

# Summary
total_per_year = yearly_state_deaths.sum(axis=1)
peak_year = total_per_year.idxmax()
peak_value = total_per_year.max()
overall_total = total_per_year.sum()

st.markdown(
    f"""
**Summary:**  
- The highest number of deaths occurred in **{peak_year}**, with **{peak_value:,}** recorded cases.  
- Across all years and states, a total of **{overall_total:,}** deaths were recorded.  
- The trend shows how fatalities vary over time across different states, with some states experiencing sharper increases than others.  
"""
)

# =====================
# CHART 6
st.subheader("Incident Type with Highest Average Deaths")

avg_deaths = (
    filtered_df.groupby("Incident")["Number of deaths"]
    .mean()
    .nlargest(10)
)

fig, ax = plt.subplots()
avg_deaths.plot(kind="barh", ax=ax, color="teal")
ax.invert_yaxis()
ax.set_xlabel("Average Number of Deaths")

st.pyplot(fig)

# Summary
top_incident = avg_deaths.idxmax()
top_value = avg_deaths.max()

st.markdown(
    f"""
**Summary:**  
- **{top_incident}** has the highest average deaths per incident at **{top_value:.1f}**.  
- This indicates that, on average, this type of incident tends to be more severe compared to others in the dataset.  
"""
)

# =====================
# CHART 7
# =====================
st.subheader("Most Frequent Incident Type")

fig, ax = plt.subplots()
filtered_df["Incident"].value_counts().nlargest(10).plot(kind="barh", ax=ax)
st.pyplot(fig)
