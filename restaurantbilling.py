# restaurant_billing_multi_hub.py
import streamlit as st
import pandas as pd
from io import BytesIO, StringIO
from datetime import datetime

# Try to import reportlab for PDF export
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False

# -------------------------
# Helper: safe widget key
# -------------------------
def safe_key(s: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in s)

# -------------------------
# Page config + CSS
# -------------------------
st.set_page_config(page_title="Multi-Hub Restaurant Billing", layout="wide")
st.title("🍔 Smart & Colorful Multi-Hub Restaurant Order & Billing App")

st.markdown(
    """
    <style>
    .menu-card {
        border-radius: 12px;
        padding: 12px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.06);
        transition: transform 0.15s ease-in-out;
        text-align: center;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .menu-card:hover { transform: translateY(-6px); }
    .totals-box {
        background: linear-gradient(180deg, #F0F8FF, #E3F2FD);
        padding: 14px;
        border-radius: 10px;
        border: 1px solid #cfe8ff;
        font-size: 16px;
        font-weight: 700;
    }
    .invoice-bar {
        background: #FAFAFA;
        padding: 8px;
        border-radius: 8px;
        margin-bottom: 12px;
        font-size: 14px;
    }
    .scroll-container {
        max-height: 420px;
        overflow-y: auto;
        padding-right: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# 5 hubs, total 20 items (4 items per hub)
# -------------------------
restaurants = {
    "Burger Hub": {
        "banner_color": "#FFF3E0",
        "menu": {
            "Classic Burger": {"price": 130.0, "color": "#FFE0B2"},
            "Cheese Burger": {"price": 160.0, "color": "#FFDAB9"},
            "Veggie Burger": {"price": 120.0, "color": "#FFEFD5"},
            "Fries Large": {"price": 90.0, "color": "#FFF7C2"},
        },
    },
    "Pizzeria Corner": {
        "banner_color": "#FFF8E1",
        "menu": {
            "Margherita": {"price": 220.0, "color": "#FFF1C9"},
            "Pepperoni": {"price": 260.0, "color": "#FFE7BF"},
            "Four Cheese": {"price": 300.0, "color": "#FFEFD6"},
            "Garlic Bread": {"price": 95.0, "color": "#F0F8E2"},
        },
    },
    "Pasta House": {
        "banner_color": "#F0FFF4",
        "menu": {
            "Alfredo Pasta": {"price": 210.0, "color": "#E6FFFA"},
            "Arrabiata": {"price": 200.0, "color": "#F0FFF0"},
            "Pesto Pasta": {"price": 230.0, "color": "#E9FFF6"},
            "Garlic Prawns Pasta": {"price": 320.0, "color": "#FFF0F5"},
        },
    },
    "Cafe Delight": {
        "banner_color": "#F3E8FF",
        "menu": {
            "Cappuccino": {"price": 120.0, "color": "#F3E8FF"},
            "Latte": {"price": 130.0, "color": "#F6EFFE"},
            "Blueberry Muffin": {"price": 85.0, "color": "#FFF7F0"},
            "Chocolate Brownie": {"price": 95.0, "color": "#FFF0F0"},
        },
    },
    "Asian Wok": {
        "banner_color": "#E8F7FF",
        "menu": {
            "Chicken Fried Rice": {"price": 160.0, "color": "#E8F7FF"},
            "Veg Noodles": {"price": 140.0, "color": "#F0FBF6"},
            "Manchurian": {"price": 170.0, "color": "#FFF7E6"},
            "Schezwan Noodles": {"price": 180.0, "color": "#FFF2F0"},
        },
    },
}

# -------------------------
# Top controls: choose hub + customer + order + currency + optional logo upload
# -------------------------
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    hub_choice = st.selectbox("Choose Hub / Restaurant", list(restaurants.keys()))
with col2:
    customer_name = st.text_input("Customer name", "")
with col3:
    order_no = st.text_input("Table / Order #", "")

currency_choice = st.selectbox("Currency", ["₹ - INR", "$ - USD", "€ - EUR"], index=0)
currency_symbol = currency_choice.split()[0]

logo_file = st.file_uploader("Upload restaurant logo (optional)", type=["png", "jpg", "jpeg"])

# invoice metadata
now = datetime.now()
invoice_no = f"INV{now.strftime('%Y%m%d%H%M%S')}"
timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
wish_message = "Thank you for dining with us — we hope to see you again!"

# show banner
banner_color = restaurants[hub_choice]["banner_color"]
st.markdown(
    f"<div style='background:{banner_color};padding:8px;border-radius:8px'><h3 style='margin:4px 0'>{hub_choice}</h3></div>",
    unsafe_allow_html=True,
)

st.markdown(
    f"<div class='invoice-bar'><b>Invoice:</b> {invoice_no} &nbsp;&nbsp; | &nbsp;&nbsp; <b>Date:</b> {timestamp_str} &nbsp;&nbsp; | &nbsp;&nbsp; <b>Customer:</b> {customer_name or '-'} &nbsp;&nbsp; | &nbsp;&nbsp; <b>Order:</b> {order_no or '-'}</div>",
    unsafe_allow_html=True,
)

# -------------------------
# Menu display: colorful scrollable cards (4 columns)
# -------------------------
menu = restaurants[hub_choice]["menu"]
selected_items = {}

st.markdown("### 📋 Menu")
st.markdown("<div class='scroll-container'>", unsafe_allow_html=True)

cols_per_row = 4
items = list(menu.items())
for i in range(0, len(items), cols_per_row):
    row = items[i : i + cols_per_row]
    cols = st.columns(cols_per_row)
    for col, (item_name, info) in zip(cols, row):
        with col:
            st.markdown(
                f"<div class='menu-card' style='background:{info['color']}; min-height:88px; padding-top:10px;'>"
                f"<div style='font-size:14px'>{item_name}</div>"
                f"<div style='font-size:13px; opacity:0.9'>{currency_symbol}{info['price']:.2f}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
            qty = st.number_input(
                label="Qty",
                min_value=0,
                max_value=50,
                step=1,
                key=safe_key(f"{hub_choice}_{item_name}"),
                format="%d",
            )
            if qty > 0:
                selected_items[item_name] = {"price": float(info["price"]), "quantity": int(qty)}

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Bill Summary (if any item selected)
# -------------------------
if not selected_items:
    st.info("Add quantities for items above to build the order. Use the Qty input below each card.")
    st.stop()

# Build bill rows and compute subtotal
bill_rows = []
subtotal = 0.0
for itm, det in selected_items.items():
    unit = float(det["price"])
    qty = int(det["quantity"])
    line_total = unit * qty
    line_total = round(line_total, 2)  # safe rounding
    subtotal += line_total
    bill_rows.append([itm, qty, unit, line_total])

subtotal = round(subtotal, 2)

# Tax and (optional) tip
tax_rate = st.slider("Tax rate (%)", min_value=0, max_value=30, value=5, step=1)
tip = st.number_input("Tip (optional)", min_value=0.0, value=0.0, step=1.0, format="%.2f")
tax = round(subtotal * (tax_rate / 100.0), 2)
tip = round(float(tip), 2)
total = round(subtotal + tax + tip, 2)

# Present as DataFrame
df = pd.DataFrame(bill_rows, columns=["Item", "Quantity", f"Unit Price ({currency_symbol})", f"Total ({currency_symbol})"])
# formatting numbers (so df shows nicely)
df[f"Unit Price ({currency_symbol})"] = df[f"Unit Price ({currency_symbol})"].map(lambda x: f"{x:.2f}")
df[f"Total ({currency_symbol})"] = df[f"Total ({currency_symbol})"].map(lambda x: f"{x:.2f}")

st.subheader("🧾 Bill Summary")
st.table(df)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Subtotal", f"{currency_symbol}{subtotal:.2f}")
c2.metric(f"Tax ({tax_rate}%)", f"{currency_symbol}{tax:.2f}")
c3.metric("Tip", f"{currency_symbol}{tip:.2f}")
c4.metric("Total", f"{currency_symbol}{total:.2f}")

# -------------------------
# CSV download (metadata + items + totals + wish)
# -------------------------
def build_csv_bytes():
    sio = StringIO()
    sio.write(f"Invoice No:,{invoice_no}\n")
    sio.write(f"Date:,{timestamp_str}\n")
    sio.write(f"Hub/Restaurant:,{hub_choice}\n")
    sio.write(f"Customer:,{customer_name or '-'}\n")
    sio.write(f"Order/Table:,{order_no or '-'}\n\n")
    # items
    export_df = pd.DataFrame(bill_rows, columns=["Item", "Quantity", "Unit Price", "Total"])
    export_df.to_csv(sio, index=False)
    sio.write("\n")
    sio.write(f"Subtotal:,{subtotal:.2f}\n")
    sio.write(f"Tax ({tax_rate}%):,{tax:.2f}\n")
    sio.write(f"Tip:,{tip:.2f}\n")
    sio.write(f"Total:,{total:.2f}\n\n")
    sio.write(f"Message:,{wish_message}\n")
    return sio.getvalue().encode("utf-8")

csv_bytes = build_csv_bytes()
st.download_button(
    label="📥 Download Invoice (CSV)",
    data=csv_bytes,
    file_name=f"{invoice_no}_{hub_choice.replace(' ','_')}.csv",
    mime="text/csv",
)

# -------------------------
# PDF download (A4 invoice) — only if reportlab is available
# -------------------------
def generate_pdf_invoice():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    title_style = ParagraphStyle(name="Title", parent=styles["Heading1"], alignment=1, fontSize=16)

    story = []

    # Optional logo (if uploaded)
    if logo_file is not None:
        try:
            logo_bytes = BytesIO(logo_file.read())
            img = Image(logo_bytes)
            img.drawWidth = 90
            img.drawHeight = 45
            story.append(img)
        except Exception:
            pass

    story.append(Paragraph(f"<b>{hub_choice} — Invoice</b>", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"Invoice No: <b>{invoice_no}</b>", normal))
    story.append(Paragraph(f"Date & Time: <b>{timestamp_str}</b>", normal))
    story.append(Paragraph(f"Customer: <b>{customer_name or '-'}</b>", normal))
    story.append(Paragraph(f"Order/Table: <b>{order_no or '-'}</b>", normal))
    story.append(Spacer(1, 12))

    # Items table
    table_data = [["Item", "Qty", f"Unit ({currency_symbol})", f"Total ({currency_symbol})"]]
    for row in bill_rows:
        item, qty, unit, line_total = row
        table_data.append([item, str(qty), f"{unit:.2f}", f"{line_total:.2f}"])

    table_col_widths = [260, 50, 90, 90]
    t = Table(table_data, colWidths=table_col_widths, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#f3f4f6")),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#d9d9d9")),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("ALIGN", (1,1), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

    # totals
    summary_data = [
        ["Subtotal", f"{currency_symbol}{subtotal:.2f}"],
        [f"Tax ({tax_rate}%)", f"{currency_symbol}{tax:.2f}"],
        ["Tip", f"{currency_symbol}{tip:.2f}"],
        ["Total", f"{currency_symbol}{total:.2f}"],
    ]
    summary_tbl = Table(summary_data, colWidths=[320, 170], hAlign="RIGHT")
    summary_tbl.setStyle(TableStyle([
        ("ALIGN", (1,0), (-1,-1), "RIGHT"),
        ("FONTNAME", (0,-1), (-1,-1), "Helvetica-Bold"),
        ("LINEABOVE", (0,-1), (-1,-1), 0.6, colors.HexColor("#888888")),
    ]))
    story.append(summary_tbl)
    story.append(Spacer(1, 14))

    # wish message
    story.append(Paragraph(f"<i>{wish_message}</i>", normal))
    story.append(Spacer(1, 8))

    doc.build(story)
    buffer.seek(0)
    return buffer

if REPORTLAB_AVAILABLE:
    try:
        pdf_buffer = generate_pdf_invoice()
        st.download_button(
            label="📥 Download Invoice (PDF)",
            data=pdf_buffer,
            file_name=f"{invoice_no}_{hub_choice.replace(' ','_')}.pdf",
            mime="application/pdf",
        )
    except Exception as e:
        st.error("PDF generation failed. Make sure reportlab is installed and try again.")
        st.exception(e)
else:
    st.warning("PDF export is disabled because 'reportlab' is not installed. Run: pip install reportlab")

# -------------------------
# End
# -------------------------
st.success("Invoice ready — use the CSV or PDF buttons above to download. 🎉")


