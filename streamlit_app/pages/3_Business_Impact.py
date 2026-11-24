import streamlit as st
import plotly.graph_objects as go


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Business Impact",
    page_icon="📈",
    layout="wide"
)


# =========================================================
# PAGE TITLE
# =========================================================

st.title("📈 Business Impact Dashboard")

st.write(
    "AI-powered business impact analysis based on the selected customer."
)


# =========================================================
# GET CUSTOMER DATA
# =========================================================

if "customer_data" not in st.session_state:

    st.error("❌ No customer information found.")

    st.info(
        "Please go to Customer Form, enter customer details, "
        "and click Analyze Customer first."
    )

    st.stop()


# Get customer information saved from Customer Form

customer = st.session_state["customer_data"]


# Also keep a common session variable for other pages

st.session_state["customer"] = customer


# =========================================================
# GET AI PREDICTION
# =========================================================

risk = st.session_state.get("risk", 75)

prediction = st.session_state.get("prediction", 1)


# Make sure risk is numeric

try:

    risk = float(risk)

except:

    risk = 75.0


# Make sure prediction is numeric

try:

    prediction = int(prediction)

except:

    prediction = 1


# =========================================================
# CUSTOMER INFORMATION
# =========================================================

st.divider()

st.header("👤 Customer Information")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Customer ID",
        str(customer.get("customerID", "New Customer"))
    )


with col2:

    st.metric(
        "Monthly Charges",
        f"₹ {float(customer.get('MonthlyCharges', 0)):.2f}"
    )


with col3:

    st.metric(
        "Tenure",
        f"{customer.get('tenure', 0)} Months"
    )


# =========================================================
# BUSINESS KPI CALCULATIONS
# =========================================================

monthly_charges = float(
    customer.get("MonthlyCharges", 0)
)

tenure = float(
    customer.get("tenure", 0)
)


# Estimated yearly revenue

annual_revenue = round(
    monthly_charges * 12,
    2
)


# Customer value based on current tenure

customer_value = round(
    monthly_charges * max(tenure, 1),
    2
)


# Estimated retention cost

retention_cost = round(
    monthly_charges * 2,
    2
)


# Expected saving

expected_saving = round(
    max(customer_value - retention_cost, 0),
    2
)


# =========================================================
# EXECUTIVE BUSINESS KPIs
# =========================================================

st.divider()

st.header("💼 Executive Business KPIs")


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "💰 Annual Revenue",
        f"₹ {annual_revenue:,.2f}"
    )


with c2:

    st.metric(
        "👤 Customer Value",
        f"₹ {customer_value:,.2f}"
    )


with c3:

    st.metric(
        "🎁 Retention Cost",
        f"₹ {retention_cost:,.2f}"
    )


with c4:

    st.metric(
        "📈 Expected Saving",
        f"₹ {expected_saving:,.2f}"
    )


# =========================================================
# CUSTOMER RISK SCORE
# =========================================================

st.divider()

st.header("🎯 Customer Risk Score")


fig = go.Figure(

    go.Indicator(

        mode="gauge+number",

        value=risk,

        title={
            "text": "AI Churn Risk (%)"
        },

        gauge={

            "axis": {
                "range": [0, 100]
            },

            "bar": {
                "color": "darkred"
            },

            "steps": [

                {
                    "range": [0, 40],
                    "color": "lightgreen"
                },

                {
                    "range": [40, 70],
                    "color": "gold"
                },

                {
                    "range": [70, 100],
                    "color": "tomato"
                }

            ]

        }

    )

)


st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# RISK LEVEL
# =========================================================

if risk >= 70:

    risk_level = "🔴 High Risk"

elif risk >= 40:

    risk_level = "🟡 Medium Risk"

else:

    risk_level = "🟢 Low Risk"


st.subheader(
    f"Customer Risk Level: {risk_level}"
)


# =========================================================
# AI BUSINESS DECISION
# =========================================================

st.divider()

st.header("🤖 AI Business Decision")


if prediction == 1:

    st.error(

        f"""
### 🔴 High Priority Customer

**AI Churn Risk:** {risk:.1f}%

### Recommended Actions

✅ Contact customer immediately

✅ Provide a personalized discount

✅ Offer a better service package

✅ Encourage a longer-term contract

### Estimated Annual Revenue at Risk

**₹ {annual_revenue:,.2f}**
"""

    )

else:

    st.success(

        f"""
### 🟢 Low Risk Customer

**AI Churn Risk:** {risk:.1f}%

### Recommended Actions

✅ Continue current service

✅ Reward customer loyalty

✅ Provide monthly offers

✅ Maintain customer engagement
"""

    )


# =========================================================
# CUSTOMER DETAILS
# =========================================================

st.divider()

st.header("📋 Customer Profile")


profile_col1, profile_col2 = st.columns(2)


with profile_col1:

    st.write(
        f"**Customer ID:** {customer.get('customerID', 'New Customer')}"
    )

    st.write(
        f"**Gender:** {customer.get('gender', '-')}"
    )

    st.write(
        f"**Senior Citizen:** "
        f"{'Yes' if str(customer.get('SeniorCitizen', 0)) == '1' else 'No'}"
    )

    st.write(
        f"**Partner:** {customer.get('Partner', '-')}"
    )

    st.write(
        f"**Dependents:** {customer.get('Dependents', '-')}"
    )

    st.write(
        f"**Tenure:** {customer.get('tenure', 0)} months"
    )


with profile_col2:

    st.write(
        f"**Phone Service:** {customer.get('PhoneService', '-')}"
    )

    st.write(
        f"**Internet Service:** {customer.get('InternetService', '-')}"
    )

    st.write(
        f"**Contract:** {customer.get('Contract', '-')}"
    )

    st.write(
        f"**Payment Method:** {customer.get('PaymentMethod', '-')}"
    )

    st.write(
        f"**Monthly Charges:** ₹ {monthly_charges:,.2f}"
    )

    st.write(
        f"**Total Charges:** ₹ "
        f"{float(customer.get('TotalCharges', 0)):,.2f}"
    )


# =========================================================
# GENERATE REPORT
# =========================================================

st.divider()


if st.button(
    "📄 Generate Customer Report",
    use_container_width=True
):

    # Save using the name expected by Report page

    st.session_state["customer"] = customer

    st.session_state["customer_data"] = customer

    st.session_state["risk"] = risk

    st.session_state["prediction"] = prediction

    st.switch_page(
        "pages/4_Report.py"
    )