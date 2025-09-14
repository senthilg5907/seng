import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# -------------------------------
# Step 1: Setup App
# -------------------------------
st.set_page_config(page_title="💧 Water Intake Tracker", layout="centered")

st.title("💧 Water Intake Tracker")
st.write("Track your daily water intake and stay hydrated for a healthy body!")

# -------------------------------
# Step 2: Data Storage (CSV)
# -------------------------------
DATA_FILE = "water_intake.csv"

# Initialize storage
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["date", "intake"])
    df.to_csv(DATA_FILE, index=False)

# Load data
df = pd.read_csv(DATA_FILE)

# -------------------------------
# Step 3: Set Goal & Input Intake
# -------------------------------
goal = st.number_input("Set your daily water goal (liters)", min_value=1.0, max_value=10.0, value=3.0, step=0.5)

today = datetime.today().strftime("%Y-%m-%d")
today_intake = df[df["date"] == today]["intake"].sum() if today in df["date"].values else 0.0

st.write(f"📅 Today: **{today}**")
st.write(f"💧 Water consumed so far: **{today_intake:.2f} L** / {goal} L")

add_intake = st.number_input("Add water intake (liters)", min_value=0.1, max_value=2.0, step=0.1)

if st.button("➕ Add Intake"):
    new_row = pd.DataFrame({"date": [today], "intake": [add_intake]})
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success(f"Added {add_intake:.2f} L for today!")

# -------------------------------
# Step 4: Progress Bar
# -------------------------------
today_intake = df[df["date"] == today]["intake"].sum() if today in df["date"].values else 0.0
progress = min(today_intake / goal, 1.0)
st.progress(progress)

if today_intake >= goal:
    st.success("🎉 Goal reached! Stay hydrated!")
else:
    st.info(f"You need {goal - today_intake:.2f} L more to reach today's goal.")

# -------------------------------
# Step 5: Weekly Chart
# -------------------------------
st.subheader("📊 Weekly Hydration Progress")

df["date"] = pd.to_datetime(df["date"])
last_7_days = df[df["date"] >= (datetime.today() - pd.Timedelta(days=6))]

weekly_summary = last_7_days.groupby("date")["intake"].sum()

fig, ax = plt.subplots(figsize=(8, 4))
weekly_summary.plot(kind="bar", color="skyblue", edgecolor="black", ax=ax)
ax.axhline(goal, color="red", linestyle="--", label=f"Goal ({goal}L)")
ax.set_ylabel("Water Intake (L)")
ax.set_title("Last 7 Days Hydration")
ax.legend()
st.pyplot(fig)
