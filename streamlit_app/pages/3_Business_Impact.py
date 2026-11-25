import streamlit as st
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(page_title="Business Impact", page_icon="📈", layout="wide")

# =========================================================
# PAGE TITLE
# =========================================================
st.title("📈 Business Impact Dashboard")
st.write("AI-powered business impact analysis based on the selected customer.")

# =========================================================
# GET CUSTOMER DATA
# =========================================================
if "customer_data" not in st.session_state:
    st.error("❌ No customer information found.")
    st.info("Please go to Customer Form, enter customer details, and click Analyze Customer first.")
    st.stop()

customer = st.session_state["customer_data"]
st.session_state["customer"] = customer

# =========================================================
# GET AI PREDICTION
# =========================================================
risk = st.session_state.get("risk", 75)
prediction = st.session_state.get("prediction", 1)
try:
    risk = float(risk)
except:
    risk = 75.0
try:
    prediction = int(prediction)
except:
    prediction = 1

# =========================================================
# CUSTOMER NAME / ID / TYPE - CORRECTED
# =========================================================
customer_id = str(customer.get("customerID", "New Customer"))
customer_name = str(customer.get("customerName", ""))
if not customer_name or customer_name == "nan":
    customer_name = str(customer.get("name", ""))
if not customer_name:
    if customer_id == "NEW-CUSTOMER":
        customer_name = "New Customer"
    else:
        customer_name = "Old Customer"

# Customer Type - Form la irunthu varum, illa na ID vachu kandupudikalam
customer_type = str(customer.get("customerType", ""))
if not customer_type:
    if customer_id.startswith("NEW-"):
        # NEW-1001 mathiri ID na - pudhusa create panna customer
        # Aana ippo Existing la vantha Old Customer
        customer_type = "Old Customer"
    elif customer_id == "NEW-CUSTOMER":
        customer_type = "New Customer"
    else:
        customer_type = "Old Customer"

# =========================================================
# CUSTOMER INFORMATION
# =========================================================
st.divider()
st.header("👤 Customer Information")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Customer ID", customer_id)

with col2:
    st.metric("Customer Name", customer_name)

with col3:
    st.metric("Customer Type", customer_type)

# Monthly / Tenure - keela thaniya
col4, col5 = st.columns(2)
with col4:
    st.metric("Monthly Charges", f"₹ {float(customer.get('MonthlyCharges', 0)):.2f}")
with col5:
    st.metric("Tenure", f"{customer.get('tenure', 0)} Months")

# =========================================================
# BUSINESS KPI CALCULATIONS
# =========================================================
monthly_charges = float(customer.get("MonthlyCharges", 0))
tenure = float(customer.get("tenure", 0))
annual_revenue = round(monthly_charges * 12, 2)
customer_value = round(monthly_charges * max(tenure, 1), 2)
retention_cost = round(monthly_charges * 2, 2)
expected_saving = round(max(customer_value - retention_cost, 0), 2)

# =========================================================
# EXECUTIVE BUSINESS KPIs
# =========================================================
st.divider()
st.header("💼 Executive Business KPIs")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("💰 Annual Revenue", f"₹ {annual_revenue:,.2f}")
with c2:
    st.metric("👤 Customer Value", f"₹ {customer_value:,.2f}")
with c3:
    st.metric("🎁 Retention Cost", f"₹ {retention_cost:,.2f}")
with c4:
    st.metric("📈 Expected Saving", f"₹ {expected_saving:,.2f}")

# =========================================================
# CUSTOMER RISK SCORE
# =========================================================
st.divider()
st.header("🎯 Customer Risk Score")
fig = go.Figure(go.Indicator(mode="gauge+number", value=risk, title={"text": "AI Churn Risk (%)"},
    gauge={"axis": {"range": [0, 100]}, "bar": {"color": "darkred"},
    "steps": [{"range": [0, 40], "color": "lightgreen"}, {"range": [40, 70], "color": "gold"}, {"range": [70, 100], "color": "tomato"}]}))
st.plotly_chart(fig, use_container_width=True)

if risk >= 70:
    risk_level = "🔴 High Risk"
elif risk >= 40:
    risk_level = "🟡 Medium Risk"
else:
    risk_level = "🟢 Low Risk"
st.subheader(f"Customer Risk Level: {risk_level}")

# =========================================================
# AI BUSINESS DECISION
# =========================================================
st.divider()
st.header("🤖 AI Business Decision")
if prediction == 1:
    st.error(f"""
### 🔴 High Priority Customer
**AI Churn Risk:** {risk:.1f}%
### Recommended Actions
✅ Contact customer immediately
✅ Provide a personalized discount
✅ Offer a better service package
✅ Encourage a longer-term contract
### Estimated Annual Revenue at Risk
**₹ {annual_revenue:,.2f}**
""")
else:
    st.success(f"""
### 🟢 Low Risk Customer
**AI Churn Risk:** {risk:.1f}%
### Recommended Actions
✅ Continue current service
✅ Reward customer loyalty
✅ Provide monthly offers
✅ Maintain customer engagement
""")

# =========================================================
# CUSTOMER DETAILS - PROFILE
# =========================================================
st.divider()
st.header("📋 Customer Profile")
profile_col1, profile_col2 = st.columns(2)
with profile_col1:
    st.write(f"**Customer ID:** {customer_id}")
    st.write(f"**Customer Name:** {customer_name}")
    st.write(f"**Customer Type:** {customer_type}")
    st.write(f"**Gender:** {customer.get('gender', '-')}")
    st.write(f"**Senior Citizen:** {'Yes' if str(customer.get('SeniorCitizen', 0)) == '1' else 'No'}")
    st.write(f"**Partner:** {customer.get('Partner', '-')}")
    st.write(f"**Dependents:** {customer.get('Dependents', '-')}")
    st.write(f"**Tenure:** {customer.get('tenure', 0)} months")
with profile_col2:
    st.write(f"**Phone Service:** {customer.get('PhoneService', '-')}")
    st.write(f"**Internet Service:** {customer.get('InternetService', '-')}")
    st.write(f"**Contract:** {customer.get('Contract', '-')}")
    st.write(f"**Payment Method:** {customer.get('PaymentMethod', '-')}")
    st.write(f"**Monthly Charges:** ₹ {monthly_charges:,.2f}")
    st.write(f"**Total Charges:** ₹ {float(customer.get('TotalCharges', 0)):,.2f}")

# =========================================================
# GENERATE REPORT
# =========================================================
st.divider()
if st.button("📄 Generate Customer Report", use_container_width=True):
    st.session_state["customer"] = customer
    st.session_state["customer_data"] = customer
    st.session_state["risk"] = risk
    st.session_state["prediction"] = prediction
    st.switch_page("pages/4_Report.py")