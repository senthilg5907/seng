import streamlit as st

# -------------------------------
# Currency Converter with Static Rates
# -------------------------------

st.set_page_config(page_title="💱 Currency Converter", page_icon="💱", layout="centered")

st.title("💱 Currency Converter")
st.markdown("Convert between INR, USD, EUR, GBP, and JPY with static rates.")

# Static exchange rates (relative to 1 USD for simplicity)
exchange_rates = {
    "USD": 1.0,
    "INR": 83.0,
    "EUR": 0.93,
    "GBP": 0.80,
    "JPY": 147.5,
}

# -------------------------------
# UI
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    from_currency = st.selectbox(
        "From Currency",
        options=list(exchange_rates.keys()),
        index=0,
    )

with col2:
    to_currency = st.selectbox(
        "To Currency",
        options=list(exchange_rates.keys()),
        index=1,
    )

amount = st.number_input("Enter Amount 💰", min_value=0.0, step=1.0)

# -------------------------------
# Conversion Logic
# -------------------------------
if st.button("Convert 🔄", use_container_width=True):
    if from_currency == to_currency:
        st.info("⚠️ Both currencies are the same, conversion not needed!")
    else:
        # Convert to USD first, then to target currency
        amount_in_usd = amount / exchange_rates[from_currency]
        converted_amount = amount_in_usd * exchange_rates[to_currency]

        st.success(
            f"🎉 {amount:,.2f} {from_currency} = **{converted_amount:,.2f} {to_currency}**"
        )

# -------------------------------
# Styling
# -------------------------------
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        font-size: 18px;
        padding: 10px 24px;
    }
    .stSelectbox, .stNumberInput {
        background-color: #f5f5f5;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
