import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Customer Report",
    page_icon="📄",
    layout="wide"
)


# =========================================================
# PAGE TITLE
# =========================================================

st.title("📄 AI Customer Report")

st.write(
    "AI-powered customer churn and business report."
)


# =========================================================
# GET CUSTOMER DATA
# =========================================================

# First check customer_data
# This is the variable saved by Customer Form

if "customer_data" in st.session_state:

    customer = st.session_state["customer_data"]

# Otherwise check customer
# This is used when coming from Business Impact

elif "customer" in st.session_state:

    customer = st.session_state["customer"]

else:

    st.error("❌ No customer found.")

    st.info(
        "Please go to Customer Form, enter customer details "
        "and click Analyze Customer first."
    )

    st.stop()


# Keep both names available

st.session_state["customer"] = customer

st.session_state["customer_data"] = customer


# =========================================================
# GET AI RESULTS
# =========================================================

prediction = st.session_state.get(
    "prediction",
    0
)

risk = st.session_state.get(
    "risk",
    0
)


# Make risk numeric

try:

    risk = float(risk)

except:

    risk = 0.0


# Make prediction numeric

try:

    prediction = int(prediction)

except:

    prediction = 0


# =========================================================
# CUSTOMER NAME
# =========================================================

customer_name = customer.get(
    "name",
    "Customer"
)


# =========================================================
# CUSTOMER INFORMATION
# =========================================================

st.divider()

st.header("👤 Customer Information")


c1, c2 = st.columns(2)


# =========================================================
# BASIC DETAILS
# =========================================================

with c1:

    st.write("### Basic Details")

    st.write(
        "**Customer Name:**",
        customer.get("name")or customer.get("customerID", "Not Provided")
    )

    st.write(
        "**Customer ID:**",
        customer.get("customerID", "New Customer")
    )

    st.write(
        "**Gender:**",
        customer.get("gender", "-")
    )

    st.write(
        "**Senior Citizen:**",
        "Yes"
        if str(customer.get("SeniorCitizen", 0)) == "1"
        else "No"
    )

    st.write(
        "**Partner:**",
        customer.get("Partner", "-")
    )

    st.write(
        "**Dependents:**",
        customer.get("Dependents", "-")
    )

    st.write(
        "**Tenure:**",
        f"{customer.get('tenure', 0)} months"
    )


# =========================================================
# SERVICE DETAILS
# =========================================================

with c2:

    st.write("### Service Details")

    st.write(
        "**Phone Service:**",
        customer.get("PhoneService", "-")
    )

    st.write(
        "**Internet:**",
        customer.get("InternetService", "-")
    )

    st.write(
        "**Online Security:**",
        customer.get("OnlineSecurity", "-")
    )

    st.write(
        "**Online Backup:**",
        customer.get("OnlineBackup", "-")
    )

    st.write(
        "**Device Protection:**",
        customer.get("DeviceProtection", "-")
    )

    st.write(
        "**Tech Support:**",
        customer.get("TechSupport", "-")
    )

    st.write(
        "**Contract:**",
        customer.get("Contract", "-")
    )

    st.write(
        "**Payment:**",
        customer.get("PaymentMethod", "-")
    )


# =========================================================
# FINANCIAL DETAILS
# =========================================================

st.divider()

st.header("💰 Financial Details")


monthly_charges = float(
    customer.get("MonthlyCharges", 0)
)

tenure = float(
    customer.get("tenure", 0)
)


try:

    total_charges = float(
        customer.get("TotalCharges", 0)
    )

except:

    total_charges = 0.0


financial1, financial2, financial3 = st.columns(3)


with financial1:

    st.metric(
        "Monthly Charges",
        f"₹ {monthly_charges:,.2f}"
    )


with financial2:

    st.metric(
        "Total Charges",
        f"₹ {total_charges:,.2f}"
    )


with financial3:

    annual_revenue = monthly_charges * 12

    st.metric(
        "Annual Revenue",
        f"₹ {annual_revenue:,.2f}"
    )


# =========================================================
# AI PREDICTION
# =========================================================

st.divider()

st.header("🤖 AI Prediction")


if prediction == 1:

    st.error(
        f"""
## 🔴 HIGH RISK CUSTOMER

### Churn Risk Score: {risk:.1f}%

This customer has a high probability of leaving the service.
"""
    )

else:

    st.success(
        f"""
## 🟢 LOW RISK CUSTOMER

### Churn Risk Score: {risk:.1f}%

This customer currently has a low probability of leaving the service.
"""
    )


# =========================================================
# RISK LEVEL
# =========================================================

if risk >= 70:

    risk_level = "🔴 HIGH RISK"

elif risk >= 40:

    risk_level = "🟡 MEDIUM RISK"

else:

    risk_level = "🟢 LOW RISK"


st.write(
    f"### Customer Risk Level: {risk_level}"
)


# =========================================================
# AI RECOMMENDATION
# =========================================================

st.divider()

st.header("🎁 AI Recommendation")


if prediction == 1:

    st.warning(
        """
### Immediate Action Required

✅ Offer a personalized discount

✅ Offer annual / long-term contract

✅ Provide loyalty reward

✅ Offer technical support

✅ Customer care follow-up

✅ Try to prevent customer churn
"""
    )

else:

    st.success(
        """
### Customer is Stable

✅ Reward customer loyalty

✅ Continue existing plan

✅ Provide monthly offers

✅ Offer premium benefits

✅ Maintain customer engagement
"""
    )


# =========================================================
# BUSINESS SUMMARY
# =========================================================

st.divider()

st.header("📊 Business Summary")


customer_value = monthly_charges * max(tenure, 1)

retention_cost = monthly_charges * 2

potential_saving = max(
    customer_value - retention_cost,
    0
)


b1, b2, b3 = st.columns(3)


with b1:

    st.metric(
        "Annual Revenue",
        f"₹ {annual_revenue:,.2f}"
    )


with b2:

    st.metric(
        "Customer Value",
        f"₹ {customer_value:,.2f}"
    )


with b3:

    st.metric(
        "Potential Saving",
        f"₹ {potential_saving:,.2f}"
    )


# =========================================================
# TEXT REPORT
# =========================================================

st.divider()

st.header("📄 Report Preview")


report = f"""
AI CUSTOMER CHURN REPORT
========================================

CUSTOMER INFORMATION
----------------------------------------

Customer Name     : {customer.get("name", "Not Provided")}
Customer ID       : {customer.get("customerID", "New Customer")}
Gender            : {customer.get("gender", "-")}
Senior Citizen    : {"Yes" if str(customer.get("SeniorCitizen", 0)) == "1" else "No"}
Partner           : {customer.get("Partner", "-")}
Dependents        : {customer.get("Dependents", "-")}
Tenure            : {customer.get("tenure", 0)} months

SERVICE INFORMATION
----------------------------------------

Phone Service     : {customer.get("PhoneService", "-")}
Internet Service  : {customer.get("InternetService", "-")}
Online Security   : {customer.get("OnlineSecurity", "-")}
Online Backup     : {customer.get("OnlineBackup", "-")}
Device Protection : {customer.get("DeviceProtection", "-")}
Tech Support      : {customer.get("TechSupport", "-")}
Contract          : {customer.get("Contract", "-")}
Payment Method    : {customer.get("PaymentMethod", "-")}

FINANCIAL INFORMATION
----------------------------------------

Monthly Charges   : ₹ {monthly_charges:,.2f}
Total Charges     : ₹ {total_charges:,.2f}
Annual Revenue    : ₹ {annual_revenue:,.2f}
Customer Value    : ₹ {customer_value:,.2f}
Potential Saving  : ₹ {potential_saving:,.2f}

AI ANALYSIS
----------------------------------------

Prediction        : {"HIGH RISK" if prediction == 1 else "LOW RISK"}
Risk Score        : {risk:.1f}%
Risk Level        : {risk_level}

RECOMMENDATION
----------------------------------------

{"Immediate customer retention action is recommended."
if prediction == 1
else
"Customer is currently stable. Continue engagement and loyalty programs."}

========================================

Generated By:
AI Customer Retention Assistant
"""


st.text_area(
    "Report",
    report,
    height=450
)


# =========================================================
# DOWNLOAD REPORT
# =========================================================

st.download_button(

    label="📥 Download Customer Report",

    data=report,

    file_name="Customer_Report.txt",

    mime="text/plain",

    use_container_width=True

)