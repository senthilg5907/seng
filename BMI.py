import streamlit as st
import matplotlib.pyplot as plt

# --- Page Config ---
st.set_page_config(page_title="BMI Calculator", page_icon="⚖️", layout="centered")
st.title("⚖️ Interactive BMI Calculator")
st.markdown("Use sliders and options to calculate your BMI instantly. No submit button needed!")

# --- Measurement System ---
system = st.radio("Select Measurement System", ["Metric (cm/kg)", "Imperial (ft-in/lbs)"])

# --- Inputs ---
if system == "Metric (cm/kg)":
    height_cm = st.slider("📏 Height (cm)", 100, 220, 170)
    weight_kg = st.slider("⚖️ Weight (kg)", 30, 150, 70)
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)

else:
    col1, col2 = st.columns(2)
    with col1:
        height_ft = st.slider("📏 Height (feet)", 3, 7, 5)
    with col2:
        height_in = st.slider("📏 Height (inches)", 0, 11, 6)
    weight_lbs = st.slider("⚖️ Weight (lbs)", 66, 330, 154)

    total_inches = height_ft * 12 + height_in
    height_m = total_inches * 0.0254
    weight_kg = weight_lbs * 0.453592
    bmi = weight_kg / (height_m ** 2)

# --- BMI Category Function ---
def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight", "#3498db", "⚠️ Consider a balanced diet with more calories."
    elif 18.5 <= bmi < 24.9:
        return "Normal weight", "#2ecc71", "✅ Keep up with your healthy lifestyle!"
    elif 25 <= bmi < 29.9:
        return "Overweight", "#f39c12", "⚠️ Try regular exercise and balanced nutrition."
    else:
        return "Obese", "#e74c3c", "❗ Consult a healthcare provider for guidance."

category, color, tip = bmi_category(bmi)

# --- Display Results ---
st.markdown(f"""
<div style='text-align: center; padding:20px; border-radius:15px; background-color:{color}; color:white;'>
    <h2>Your BMI: {bmi:.2f}</h2>
    <h3>Category: {category}</h3>
</div>
""", unsafe_allow_html=True)

# --- Extra Visual Gauge ---
fig, ax = plt.subplots(figsize=(6,1))
ax.barh([0], [bmi], color=color, height=0.3)
ax.axvline(18.5, color='blue', linestyle='--', label='Normal Range')
ax.axvline(24.9, color='blue', linestyle='--')
ax.set_xlim(10, 40)
ax.set_yticks([])
ax.set_xlabel("BMI Scale")
ax.legend()
st.pyplot(fig)

# --- Health Tip ---
st.success(tip)

st.info("⚡ Adjust the sliders above to see your BMI update instantly!")