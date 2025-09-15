# app.py
import streamlit as st
import pandas as pd
from datetime import date, datetime
import altair as alt

st.set_page_config(page_title="Gym Workout Logger", layout="wide")

# --- Helper: create empty DataFrame structure
def empty_log_df():
    return pd.DataFrame(
        columns=["Date", "Exercise", "Sets", "Reps", "Weight (kg)", "Volume (kg)"]
    )

# --- Initialize session state
if "workout_log" not in st.session_state:
    st.session_state.workout_log = empty_log_df()

# --- Title / Intro
st.title("🏋️ Gym Workout Logger")
st.markdown(
    "Log exercises (sets, reps, weight), track **total volume** (sets×reps×weight), "
    "and view **weekly progress** as bar charts."
)

# --- Layout: left = form, right = summary
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Add a workout")
    with st.form("add_workout_form", clear_on_submit=True):
        ex_date = st.date_input("Date", value=date.today())
        exercise = st.text_input("Exercise name (e.g., Bench Press)")
        sets = st.number_input("Sets", min_value=1, max_value=20, value=3, step=1)
        reps = st.number_input("Reps per set", min_value=1, max_value=100, value=8, step=1)
        weight = st.number_input("Weight (kg)", min_value=0.0, value=20.0, step=0.5, format="%.2f")
        submit = st.form_submit_button("Add to log ✅")

        if submit:
            if not exercise.strip():
                st.error("Please enter an exercise name.")
            else:
                # compute volume
                volume = float(sets) * float(reps) * float(weight)
                new_row = {
                    "Date": ex_date.isoformat(),
                    "Exercise": exercise.strip(),
                    "Sets": int(sets),
                    "Reps": int(reps),
                    "Weight (kg)": float(weight),
                    "Volume (kg)": float(round(volume, 2)),
                }
                st.session_state.workout_log = pd.concat(
                    [st.session_state.workout_log, pd.DataFrame([new_row])],
                    ignore_index=True,
                )
                st.success(f"Logged {sets}×{reps} {exercise} @ {weight} kg  — Volume {round(volume,2)} kg")

with col2:
    st.subheader("Quick actions")
    # Download CSV
    if not st.session_state.workout_log.empty:
        csv = st.session_state.workout_log.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download workout CSV",
            data=csv,
            file_name=f"workout_log_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
        )
    # Demo data
    if st.button("Load demo data"):
        demo = pd.DataFrame([
            {"Date": (date.today()).isoformat(), "Exercise": "Bench Press", "Sets": 3, "Reps": 8, "Weight (kg)": 60.0},
            {"Date": (date.today()).isoformat(), "Exercise": "Squat", "Sets": 4, "Reps": 6, "Weight (kg)": 100.0},
            {"Date": (date.today()).isoformat(), "Exercise": "Deadlift", "Sets": 3, "Reps": 5, "Weight (kg)": 140.0},
            # older week
            {"Date": (date.today().replace(day=max(1, date.today().day - 10))).isoformat(), "Exercise": "Bench Press", "Sets": 3, "Reps": 8, "Weight (kg)": 55.0},
            {"Date": (date.today().replace(day=max(1, date.today().day - 10))).isoformat(), "Exercise": "Squat", "Sets": 4, "Reps": 6, "Weight (kg)": 95.0},
        ])
        # compute Volume
        demo["Volume (kg)"] = demo["Sets"] * demo["Reps"] * demo["Weight (kg)"]
        # append
        st.session_state.workout_log = pd.concat(
            [st.session_state.workout_log, demo], ignore_index=True
        )
        st.success("Demo data loaded ✅")

    # Danger zone: clear history
    with st.expander("Danger zone — clear all history"):
        if st.button("Clear history"):
            st.session_state.workout_log = empty_log_df()
            st.success("Workout history cleared.")

# --- Show workout history
st.markdown("---")
st.subheader("📋 Workout history")
if st.session_state.workout_log.empty:
    st.info("No workouts logged yet. Use the form to add your first workout.")
else:
    # Display table (convert types nicely)
    df_display = st.session_state.workout_log.copy()
    # Ensure numeric columns are correct types for nicer display & sorting
    for c in ["Sets", "Reps", "Weight (kg)", "Volume (kg)"]:
        if c in df_display.columns:
            df_display[c] = pd.to_numeric(df_display[c], errors="coerce")
    # Convert Date to datetime for nicer sorting in display
    try:
        df_display["Date"] = pd.to_datetime(df_display["Date"]).dt.date
    except Exception:
        pass
    st.dataframe(df_display.sort_values(by="Date", ascending=False).reset_index(drop=True), use_container_width=True)

# --- Weekly progress (bar chart)
st.markdown("---")
st.subheader("📊 Weekly Progress (bar chart)")

if st.session_state.workout_log.empty:
    st.info("Add workouts to see weekly progress.")
else:
    # Prepare data
    df = st.session_state.workout_log.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    # Normalize numeric columns
    df["Volume (kg)"] = pd.to_numeric(df["Volume (kg)"], errors="coerce").fillna(0.0)
    # Week start (Monday)
    df["WeekStart"] = df["Date"] - pd.to_timedelta(df["Date"].dt.weekday, unit="d")
    df["WeekStart"] = df["WeekStart"].dt.normalize()

    # Aggregate weekly total volume per exercise
    weekly = df.groupby(["WeekStart", "Exercise"], as_index=False)["Volume (kg)"].sum()
    weekly = weekly.sort_values(["WeekStart", "Exercise"])

    # Allow user to pick exercise or All
    exercises = sorted(df["Exercise"].unique().tolist())
    selected = st.selectbox("Choose exercise to view", options=["All exercises"] + exercises)

    if selected == "All exercises":
        # Stacked bar per week (each exercise colored)
        # Prepare melt: weekly already is long-form; use Altair stacked bars
        chart = (
            alt.Chart(weekly)
            .mark_bar()
            .encode(
                x=alt.X("WeekStart:T", title="Week starting"),
                y=alt.Y("Volume (kg):Q", title="Total weekly volume (kg)"),
                color=alt.Color("Exercise:N", title="Exercise"),
                tooltip=[alt.Tooltip("WeekStart:T", title="Week start"),
                         alt.Tooltip("Exercise:N"),
                         alt.Tooltip("Volume (kg):Q", format=".2f")],
            )
            .properties(height=420)
            .interactive()
        )
        st.altair_chart(chart, use_container_width=True)

    else:
        # Filter for that exercise
        ex_weekly = weekly[weekly["Exercise"] == selected].copy()
        if ex_weekly.empty:
            st.info("No data for this exercise yet.")
        else:
            chart = (
                alt.Chart(ex_weekly)
                .mark_bar()
                .encode(
                    x=alt.X("WeekStart:T", title="Week starting"),
                    y=alt.Y("Volume (kg):Q", title=f"Total weekly volume — {selected} (kg)"),
                    tooltip=[alt.Tooltip("WeekStart:T", title="Week start"),
                             alt.Tooltip("Volume (kg):Q", format=".2f")],
                )
                .properties(height=420)
                .interactive()
            )
            st.altair_chart(chart, use_container_width=True)

    # Also show the weekly numbers in a table for reference
    st.markdown("**Weekly totals (table)**")
    st.dataframe(weekly.sort_values(["WeekStart", "Exercise"], ascending=[False, True]).reset_index(drop=True), use_container_width=True)

