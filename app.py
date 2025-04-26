import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.dates as mdates


st.title("Faroe Fish Market Analysis")

# Select year
years = sorted([f.strip(".csv") for f in os.listdir("data") if f.endswith(".csv")])
year = st.selectbox("Select Year", years)

# Load data
df = pd.read_csv(f"data/{year}.csv")

# Select fish type
fish_options = sorted(df["type"].unique())
fish_type = st.selectbox("Select Fish Type", fish_options)

# Select analysis type
analysis_type = st.radio("Analyze by", ["Price (DKK/kg)", "Weight (tons)"])

# Filter data
df_fish = df[df["type"] == fish_type].copy()
df_fish["Date"] = pd.to_datetime(df_fish["date"], errors='coerce')
df_fish = df_fish.sort_values("Date")

# Plot
fig, ax = plt.subplots()
if analysis_type == "Price (DKK/kg)":
    ax.plot(df_fish["Date"], df_fish["avg price"], label="Price (DKK/kg)", color="blue")
    ax.set_ylabel("DKK/kg")
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
else:
    ax.plot(df_fish["Date"], df_fish["Kg"] / 1000, label="Weight (tons)", color="green")
    ax.set_ylabel("Tons")
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

# Format x-axis
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
fig.autofmt_xdate()

ax.set_title(f"{fish_type} - {analysis_type} in {year}")
ax.set_xlabel("Date")
ax.grid(True)
st.pyplot(fig)