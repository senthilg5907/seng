import streamlit as st

# ---------------------------------
# Step 1: Page Setup
# ---------------------------------
st.set_page_config(page_title="🌍 Unit Converter", layout="centered")
st.title("🌍 Universal Unit Converter")
st.write("Convert Currency, Temperature, Length, and Weight instantly!")

# ---------------------------------
# Step 2: Create Tabs
# ---------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["💰 Currency", "🌡️ Temperature", "📏 Length", "⚖️ Weight"])

# ---------------------------------
# Step 3: Currency Converter
# ---------------------------------
with tab1:
    st.subheader("💰 Currency Converter")
    amount = st.number_input("Enter Amount", min_value=0.0, value=1.0, step=0.5)
    from_currency = st.selectbox("From Currency", ["USD", "EUR", "INR", "GBP"])
    to_currency = st.selectbox("To Currency", ["USD", "EUR", "INR", "GBP"])

    # Fixed conversion rates (demo purpose)
    rates = {
        "USD": {"EUR": 0.92, "INR": 83.0, "GBP": 0.79, "USD": 1},
        "EUR": {"USD": 1.09, "INR": 90.0, "GBP": 0.86, "EUR": 1},
        "INR": {"USD": 0.012, "EUR": 0.011, "GBP": 0.0095, "INR": 1},
        "GBP": {"USD": 1.27, "EUR": 1.16, "INR": 105.0, "GBP": 1}
    }

    result = amount * rates[from_currency][to_currency]
    st.success(f"💱 {amount} {from_currency} = {result:.2f} {to_currency}")

# ---------------------------------
# Step 4: Temperature Converter
# ---------------------------------
with tab2:
    st.subheader("🌡️ Temperature Converter")
    temp = st.number_input("Enter Temperature", value=0.0)
    option = st.radio("Conversion Type:", ["Celsius to Fahrenheit", "Fahrenheit to Celsius"])

    if option == "Celsius to Fahrenheit":
        result = (temp * 9/5) + 32
        st.success(f"{temp} °C = {result:.2f} °F")
    else:
        result = (temp - 32) * 5/9
        st.success(f"{temp} °F = {result:.2f} °C")

# ---------------------------------
# Step 5: Length Converter
# ---------------------------------
with tab3:
    st.subheader("📏 Length Converter")
    length = st.number_input("Enter Length", value=1.0)
    unit = st.radio("Conversion Type:", ["Meters to Feet", "Feet to Meters"])

    if unit == "Meters to Feet":
        result = length * 3.28084
        st.success(f"{length} meters = {result:.2f} feet")
    else:
        result = length / 3.28084
        st.success(f"{length} feet = {result:.2f} meters")

# ---------------------------------
# Step 6: Weight Converter
# ---------------------------------
with tab4:
    st.subheader("⚖️ Weight Converter")
    weight = st.number_input("Enter Weight", value=1.0)
    unit = st.radio("Conversion Type:", ["Kilograms to Pounds", "Pounds to Kilograms"])

    if unit == "Kilograms to Pounds":
        result = weight * 2.20462
        st.success(f"{weight} kg = {result:.2f} lbs")
    else:
        result = weight / 2.20462
        st.success(f"{weight} lbs = {result:.2f} kg")

