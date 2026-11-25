import streamlit as st
import pandas as pd
from pathlib import Path
import random
import string

st.set_page_config(page_title="Customer Information", page_icon="👤", layout="wide")

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "customer_churn.csv"
NEW_CUSTOMER_PATH = BASE_DIR / "data" / "new_customers.csv"

df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip()
if "customerID" in df.columns:
    df["customerID"] = df["customerID"].astype(str).str.strip()

# --- PUDHU CUSTOMERS FILE AH LOAD PANNU ---
if NEW_CUSTOMER_PATH.exists():
    new_df = pd.read_csv(NEW_CUSTOMER_PATH)
    new_df.columns = new_df.columns.str.strip()
    if "customerID" in new_df.columns:
        new_df["customerID"] = new_df["customerID"].astype(str).str.strip()
    # Rendu dataset ah serthu theduvathuku
    combined_df = pd.concat([df, new_df], ignore_index=True)
else:
    new_df = pd.DataFrame()
    combined_df = df

# --- PUDHU ID CREATE PANRA FUNCTION ---
def generate_new_id():
    # Ex: NEW-1001, NEW-1002 nu varum
    existing_ids = set(combined_df["customerID"].astype(str).tolist()) if "customerID" in combined_df.columns else set()
    if NEW_CUSTOMER_PATH.exists():
        try:
            count = len(pd.read_csv(NEW_CUSTOMER_PATH)) + 1001
        except:
            count = 1001
    else:
        count = 1001
    while True:
        new_id = f"NEW-{count}"
        if new_id not in existing_ids:
            return new_id
        count += 1

st.markdown("""<style>.main{background-color:#F8FAFC}.block-container{padding-top:2rem}.title{font-size:42px;font-weight:700;color:#172554}.subtitle{font-size:18px;color:#475569}</style>""", unsafe_allow_html=True)
st.markdown("""<div class="title">👤 Customer Information</div><div class="subtitle">Enter customer details and analyze their churn risk using AI.</div>""", unsafe_allow_html=True)
st.divider()

st.subheader("🔍 Customer Type")
customer_type = st.radio("Choose how you want to analyze the customer:", ["Existing Customer", "New Customer"], horizontal=True)

if customer_type == "Existing Customer":
    st.info("Enter a Customer ID from the dataset. Old customers & previously created New customers can login here.")
    col1, col2 = st.columns([3, 1])
    with col1:
        customer_id_input = st.text_input("Customer ID", placeholder="Example: 7590-VHVEG or NEW-1001")
    with col2:
        st.write("")
        load_customer = st.button("🔎 Load Customer", use_container_width=True)
    if load_customer:
        if customer_id_input.strip() == "":
            st.warning("Please enter a Customer ID.")
        else:
            search_id = customer_id_input.strip()
            # Combined la thedu - Old + New rendu me kedaikum
            customer_result = combined_df[combined_df["customerID"].str.lower() == search_id.lower()]
            if len(customer_result) == 0:
                st.error(f"Customer ID '{search_id}' was not found.")
                st.session_state["loaded_customer"] = None
            else:
                customer_row = customer_result.iloc[0].to_dict()
                st.session_state["loaded_customer"] = customer_row
                st.success(f"Welcome back! Customer {customer_row['customerID']} loaded. (Old Customer)")
    customer = st.session_state.get("loaded_customer")
else:
    customer = None
    st.info("New customer selected. Enter name, we will create a New Customer ID for you.")

st.divider()
st.subheader("👤 Customer Details")

if customer is not None:
    default_customer_id = str(customer.get("customerID", ""))
    # Old customer na - Name iruntha atha kaatu, illa na Old Customer
    default_customer_name = str(customer.get("customerName", customer.get("name", "")))
    if default_customer_name == "" or default_customer_name == "nan":
        default_customer_name = "Old Customer"
    default_gender = customer.get("gender", "Female")
    default_senior = "Yes" if str(customer.get("SeniorCitizen", 0)) == "1" else "No"
    default_partner = customer.get("Partner", "No")
    default_dependents = customer.get("Dependents", "No")
    default_tenure = int(float(customer.get("tenure", 0)))
    default_phone = customer.get("PhoneService", "Yes")
    default_multiple = customer.get("MultipleLines", "No phone service")
    default_internet = customer.get("InternetService", "DSL")
    default_security = customer.get("OnlineSecurity", "No")
    default_backup = customer.get("OnlineBackup", "No")
    default_protection = customer.get("DeviceProtection", "No")
    default_support = customer.get("TechSupport", "No")
    default_tv = customer.get("StreamingTV", "No")
    default_movies = customer.get("StreamingMovies", "No")
    default_contract = customer.get("Contract", "Month-to-month")
    default_paperless = customer.get("PaperlessBilling", "Yes")
    default_payment = customer.get("PaymentMethod", "Electronic check")
    try: default_monthly = float(customer.get("MonthlyCharges", 70))
    except: default_monthly = 70.0
    try: default_total = float(customer.get("TotalCharges", 0))
    except: default_total = 0.0
else:
    default_customer_id = "Will be auto-generated"
    default_customer_name = ""
    default_gender = "Female"; default_senior = "No"; default_partner = "No"; default_dependents = "No"
    default_tenure = 12; default_phone = "Yes"; default_multiple = "No phone service"
    default_internet = "DSL"; default_security = "No"; default_backup = "No"
    default_protection = "No"; default_support = "No"; default_tv = "No"; default_movies = "No"
    default_contract = "Month-to-month"; default_paperless = "Yes"; default_payment = "Electronic check"
    default_monthly = 70.0; default_total = 840.0

with st.form("customer_information_form"):
    col1, col2 = st.columns(2)
    with col1:
        customer_id_display = st.text_input("Customer ID", value=default_customer_id, disabled=True)
        customer_name = st.text_input("Customer Name", value=default_customer_name, placeholder="Ex: Kayal")
        gender = st.selectbox("Gender", ["Female", "Male"], index=0 if default_gender == "Female" else 1)
        senior = st.selectbox("Senior Citizen", ["No", "Yes"], index=1 if default_senior == "Yes" else 0)
        partner = st.selectbox("Partner", ["No", "Yes"], index=1 if default_partner == "Yes" else 0)
        dependents = st.selectbox("Dependents", ["No", "Yes"], index=1 if default_dependents == "Yes" else 0)
    with col2:
        tenure = st.slider("Tenure (Months)", min_value=0, max_value=72, value=default_tenure)
        monthly = st.number_input("Monthly Charges (₹)", min_value=0.0, max_value=200.0, value=default_monthly, step=1.0)
        total = st.number_input("Total Charges (₹)", min_value=0.0, max_value=10000.0, value=default_total, step=10.0)
    st.divider()
    st.subheader("📞 Phone Services")
    col1, col2 = st.columns(2)
    with col1: phone = st.selectbox("Phone Service", ["No", "Yes"], index=1 if default_phone == "Yes" else 0)
    with col2:
        multiple_options = ["No", "Yes", "No phone service"]
        multiple = st.selectbox("Multiple Lines", multiple_options, index=multiple_options.index(default_multiple) if default_multiple in multiple_options else 0)
    st.divider()
    st.subheader("🌐 Internet Services")
    col1, col2 = st.columns(2)
    with col1:
        internet_options = ["DSL", "Fiber optic", "No"]
        internet = st.selectbox("Internet Service", internet_options, index=internet_options.index(default_internet) if default_internet in internet_options else 0)
        security_options = ["No", "Yes", "No internet service"]
        security = st.selectbox("Online Security", security_options, index=security_options.index(default_security) if default_security in security_options else 0)
        backup_options = ["No", "Yes", "No internet service"]
        backup = st.selectbox("Online Backup", backup_options, index=backup_options.index(default_backup) if default_backup in backup_options else 0)
    with col2:
        protection_options = ["No", "Yes", "No internet service"]
        protection = st.selectbox("Device Protection", protection_options, index=protection_options.index(default_protection) if default_protection in protection_options else 0)
        support_options = ["No", "Yes", "No internet service"]
        support = st.selectbox("Tech Support", support_options, index=support_options.index(default_support) if default_support in support_options else 0)
    st.divider()
    st.subheader("🎬 Entertainment")
    col1, col2 = st.columns(2)
    with col1:
        tv_options = ["No", "Yes", "No internet service"]
        tv = st.selectbox("Streaming TV", tv_options, index=tv_options.index(default_tv) if default_tv in tv_options else 0)
    with col2:
        movies_options = ["No", "Yes", "No internet service"]
        movies = st.selectbox("Streaming Movies", movies_options, index=movies_options.index(default_movies) if default_movies in movies_options else 0)
    st.divider()
    st.subheader("💳 Billing Information")
    col1, col2 = st.columns(2)
    with col1:
        contract_options = ["Month-to-month", "One year", "Two year"]
        contract = st.selectbox("Contract", contract_options, index=contract_options.index(default_contract) if default_contract in contract_options else 0)
        paperless_options = ["No", "Yes"]
        paper = st.selectbox("Paperless Billing", paperless_options, index=paperless_options.index(default_paperless) if default_paperless in paperless_options else 0)
    with col2:
        payment_options = ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
        payment = st.selectbox("Payment Method", payment_options, index=payment_options.index(default_payment) if default_payment in payment_options else 0)
    st.divider()
    analyze_customer = st.form_submit_button("🤖 Analyze Customer", use_container_width=True)

if analyze_customer:
    # ===== CORRECT LOGIC =====
    if customer is not None:
        # OLD CUSTOMER - ID potu vanthavanga
        final_customer_id = str(customer.get("customerID", ""))
        final_customer_name = customer_name.strip() if customer_name.strip() != "" else "Old Customer"
        final_customer_type = "Old Customer"
    else:
        # NEW CUSTOMER - Pudhu ID create pannu
        if customer_name.strip() == "":
            st.error("Please enter Customer Name for New Customer!")
            st.stop()
        final_customer_name = customer_name.strip()
        final_customer_id = generate_new_id()
        final_customer_type = "New Customer"
        st.success(f"🎉 New Customer ID Created: **{final_customer_id}** - Please note it for next login!")

    customer_data = {
        "customerID": final_customer_id,
        "customerName": final_customer_name,
        "customerType": final_customer_type,
        "gender": gender, "SeniorCitizen": 1 if senior == "Yes" else 0,
        "Partner": partner, "Dependents": dependents, "tenure": tenure,
        "PhoneService": phone, "MultipleLines": multiple, "InternetService": internet,
        "OnlineSecurity": security, "OnlineBackup": backup, "DeviceProtection": protection,
        "TechSupport": support, "StreamingTV": tv, "StreamingMovies": movies,
        "Contract": contract, "PaperlessBilling": paper, "PaymentMethod": payment,
        "MonthlyCharges": monthly, "TotalCharges": total
    }

    # --- NEW CUSTOMER AH FILE LA SAVE PANNU - NEXT TIME LOGIN PANNA ---
    if final_customer_type == "New Customer":
        try:
            NEW_CUSTOMER_PATH.parent.mkdir(parents=True, exist_ok=True)
            new_row_df = pd.DataFrame([customer_data])
            if NEW_CUSTOMER_PATH.exists():
                new_row_df.to_csv(NEW_CUSTOMER_PATH, mode="a", header=False, index=False)
            else:
                new_row_df.to_csv(NEW_CUSTOMER_PATH, index=False)
        except Exception as e:
            st.warning(f"Could not save new customer: {e}")

    st.session_state["customer_data"] = customer_data
    st.session_state["customer_type"] = customer_type
    st.success("✅ Customer information saved successfully.")
    st.write("### Customer Summary")
    st.dataframe(pd.DataFrame([customer_data]), use_container_width=True, hide_index=True)
    st.info("Go to **AI Analysis** from the left menu to see the churn prediction.")