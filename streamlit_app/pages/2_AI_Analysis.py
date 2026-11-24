import streamlit as st
import pandas as pd
import joblib
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Customer Analysis",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "churn_model.pkl"
FEATURE_PATH = MODEL_DIR / "feature_columns.pkl"
ENCODER_PATH = MODEL_DIR / "label_encoders.pkl"
TARGET_ENCODER_PATH = MODEL_DIR / "target_encoder.pkl"


# ============================================================
# LOAD MODEL
# ============================================================

try:

    model = joblib.load(MODEL_PATH)

    feature_columns = joblib.load(FEATURE_PATH)

    label_encoders = joblib.load(ENCODER_PATH)

    target_encoder = joblib.load(TARGET_ENCODER_PATH)

except Exception as e:

    st.error("❌ Unable to load AI model files.")

    st.error(str(e))

    st.stop()


# ============================================================
# TITLE
# ============================================================

st.title("🤖 AI Customer Analysis")

st.write(
    "Artificial Intelligence is analyzing the customer profile "
    "and predicting the customer's churn risk."
)

st.divider()


# ============================================================
# CHECK CUSTOMER DATA
# ============================================================

if "customer_data" not in st.session_state:

    st.error(
        "❌ No customer information found."
    )

    st.info(
        "Please go to Customer Information page "
        "and enter customer details first."
    )

    st.stop()


customer = st.session_state["customer_data"]


st.success(
    "✅ Customer information received successfully."
)


# ============================================================
# CUSTOMER TYPE
# ============================================================

customer_type = st.session_state.get(
    "customer_type",
    "New Customer"
)


if customer_type == "Existing Customer":

    st.info(
        "🔎 Existing customer information was loaded from the dataset."
    )

else:

    st.info(
        "🆕 New customer information was entered manually."
    )


# ============================================================
# CUSTOMER PROFILE
# ============================================================

st.subheader("👤 Customer Profile")

c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "Customer",
        customer.get(
            "customerID",
            "New Customer"
        )
    )


with c2:

    st.metric(
        "Contract",
        customer.get(
            "Contract",
            "N/A"
        )
    )


with c3:

    st.metric(
        "Tenure",
        f"{customer.get('tenure', 0)} Months"
    )


with c4:

    st.metric(
        "Monthly Charges",
        f"₹ {float(customer.get('MonthlyCharges', 0)):.2f}"
    )


st.divider()


# ============================================================
# PREPARE CUSTOMER DATA
# ============================================================

input_data = customer.copy()


# Remove fields which are not model features

input_data.pop(
    "customerID",
    None
)

input_data.pop(
    "name",
    None
)

input_data.pop(
    "Churn",
    None
)


# Convert dictionary to DataFrame

input_df = pd.DataFrame(
    [input_data]
)


# ============================================================
# CLEAN NUMERICAL COLUMNS
# ============================================================

numeric_columns = [
    "SeniorCitizen",
    "tenure",
    "MonthlyCharges",
    "TotalCharges"
]


for col in numeric_columns:

    if col in input_df.columns:

        input_df[col] = pd.to_numeric(
            input_df[col],
            errors="coerce"
        )


# ============================================================
# HANDLE MISSING NUMERICAL VALUES
# ============================================================

for col in numeric_columns:

    if col in input_df.columns:

        if input_df[col].isna().any():

            input_df[col] = input_df[col].fillna(0)


# ============================================================
# ENCODE CATEGORICAL FEATURES
# ============================================================

encoding_error = False


for col, encoder in label_encoders.items():

    if col not in input_df.columns:

        continue


    value = input_df[col].iloc[0]


    if pd.isna(value):

        st.error(
            f"❌ Missing value found in: {col}"
        )

        encoding_error = True

        continue


    value = str(value)


    # Check whether value exists
    # in training categories

    if value not in encoder.classes_:

        st.error(
            f"❌ Unknown value '{value}' "
            f"found in column '{col}'."
        )

        encoding_error = True

        continue


    input_df[col] = encoder.transform(
        input_df[col].astype(str)
    )


# ============================================================
# STOP IF ENCODING ERROR
# ============================================================

if encoding_error:

    st.error(
        "Some customer values could not be "
        "converted using the saved encoders."
    )

    st.write("Customer Input:")

    st.dataframe(
        input_df,
        use_container_width=True
    )

    st.stop()


# ============================================================
# CHECK REQUIRED FEATURES
# ============================================================

missing_features = [
    col
    for col in feature_columns
    if col not in input_df.columns
]


if missing_features:

    st.error(
        "❌ Some model features are missing."
    )

    st.write(
        "Missing Features:"
    )

    st.write(
        missing_features
    )

    st.stop()


# ============================================================
# ARRANGE FEATURES IN TRAINING ORDER
# ============================================================

input_df = input_df[
    feature_columns
]


# ============================================================
# VIEW AI INPUT
# ============================================================

with st.expander(
    "🔍 View Data Sent to AI Model"
):

    st.dataframe(
        input_df,
        use_container_width=True
    )


# ============================================================
# AI PREDICTION
# ============================================================

try:

    prediction = model.predict(
        input_df
    )[0]

    probability = model.predict_proba(
        input_df
    )[0]

except Exception as e:

    st.error(
        "❌ AI prediction failed."
    )

    st.error(
        str(e)
    )

    st.stop()


# ============================================================
# CHURN / RETENTION PROBABILITY
# ============================================================

classes = list(
    model.classes_
)


# Find probability according to class

if 1 in classes:

    churn_index = classes.index(1)

    churn_probability = (
        probability[churn_index] * 100
    )

else:

    churn_probability = 0


if 0 in classes:

    retention_index = classes.index(0)

    retention_probability = (
        probability[retention_index] * 100
    )

else:

    retention_probability = 100 - churn_probability


churn_probability = round(
    churn_probability,
    2
)

retention_probability = round(
    retention_probability,
    2
)


# ============================================================
# SAVE RESULT
# ============================================================

st.session_state["prediction"] = int(
    prediction
)

st.session_state["risk"] = churn_probability


# ============================================================
# AI PREDICTION RESULT
# ============================================================

st.divider()

st.header(
    "🎯 AI Prediction Result"
)


if int(prediction) == 1:

    st.error(
        f"""
# 🔴 HIGH CHURN RISK

### Churn Probability

# {churn_probability}%

The AI model predicts that this customer
has a high possibility of leaving the company.
"""
    )

else:

    st.success(
        f"""
# 🟢 LOW CHURN RISK

### Retention Probability

# {retention_probability}%

The AI model predicts that this customer
is likely to stay with the company.
"""
    )


# ============================================================
# PROBABILITY CARDS
# ============================================================

st.divider()

c1, c2 = st.columns(2)


with c1:

    st.metric(
        "📉 Churn Probability",
        f"{churn_probability}%"
    )


with c2:

    st.metric(
        "❤️ Retention Probability",
        f"{retention_probability}%"
    )


# ============================================================
# AI DIAGNOSIS
# ============================================================

st.divider()

st.header(
    "🧠 AI Diagnosis"
)


reasons = []


if customer.get("Contract") == "Month-to-month":

    reasons.append(
        "📄 Customer has a Month-to-Month contract."
    )


if float(
    customer.get(
        "MonthlyCharges",
        0
    )
) >= 80:

    reasons.append(
        "💰 Monthly charges are relatively high."
    )


if customer.get(
    "InternetService"
) == "Fiber optic":

    reasons.append(
        "🌐 Customer uses Fiber Optic Internet."
    )


if customer.get(
    "PaymentMethod"
) == "Electronic check":

    reasons.append(
        "💳 Customer uses Electronic Check payment."
    )


if customer.get(
    "TechSupport"
) == "No":

    reasons.append(
        "🛠 Customer does not have Tech Support."
    )


if customer.get(
    "OnlineSecurity"
) == "No":

    reasons.append(
        "🔒 Customer does not have Online Security."
    )


if float(
    customer.get(
        "tenure",
        0
    )
) < 12:

    reasons.append(
        "📅 Customer is relatively new."
    )


if len(reasons) == 0:

    st.success(
        """
### ✅ Excellent!

No major churn risk factors
were detected from the customer profile.
"""
    )

else:

    st.warning(
        "### ⚠️ AI detected the following risk factors:"
    )

    for reason in reasons:

        st.write(
            "•",
            reason
        )


# ============================================================
# PERSONALIZED RETENTION PLAN
# ============================================================

st.divider()

st.header(
    "🎁 Personalized Retention Plan"
)


if int(prediction) == 1:

    st.error(
        """
### 🔴 High Priority Customer

#### Recommended Actions

✅ Offer a personalized discount

✅ Encourage annual or two-year contract

✅ Provide free Tech Support

✅ Offer loyalty rewards

✅ Give personalized customer assistance

✅ Contact customer proactively
"""
    )

else:

    st.success(
        """
### 🟢 Customer is Stable

#### Recommended Actions

✅ Continue normal service

✅ Offer loyalty rewards

✅ Send personalized offers

✅ Maintain good customer engagement

✅ Monitor future churn signals
"""
    )


# ============================================================
# BUSINESS IMPACT
# ============================================================

st.divider()

st.header(
    "💰 Estimated Business Impact"
)


monthly_charges = float(
    customer.get(
        "MonthlyCharges",
        0
    )
)


tenure = float(
    customer.get(
        "tenure",
        0
    )
)


annual_revenue = round(
    monthly_charges * 12,
    2
)


lifetime_value = round(
    monthly_charges * max(
        tenure,
        1
    ),
    2
)


potential_saving = round(
    lifetime_value *
    churn_probability /
    100,
    2
)


c1, c2, c3 = st.columns(3)


with c1:

    st.metric(
        "Estimated Annual Revenue",
        f"₹ {annual_revenue:.2f}"
    )


with c2:

    st.metric(
        "Customer Lifetime Value",
        f"₹ {lifetime_value:.2f}"
    )


with c3:

    st.metric(
        "Potential Saving",
        f"₹ {potential_saving:.2f}"
    )


# ============================================================
# AI CONFIDENCE
# ============================================================

st.divider()

st.header(
    "📊 AI Confidence"
)


confidence = max(
    churn_probability,
    retention_probability
)


st.progress(
    int(confidence)
)


st.write(
    f"### AI Confidence Score : **{confidence:.2f}%**"
)


if churn_probability >= 70:

    st.error(
        "🔴 HIGH CHURN RISK"
    )

elif churn_probability >= 40:

    st.warning(
        "🟡 MEDIUM CHURN RISK"
    )

else:

    st.success(
        "🟢 LOW CHURN RISK"
    )


# ============================================================
# COMPLETE CUSTOMER SUMMARY
# ============================================================

st.divider()

st.subheader(
    "👤 Customer Summary"
)


c1, c2, c3 = st.columns(3)


with c1:

    st.metric(
        "Customer",
        customer.get(
            "customerID",
            "New Customer"
        )
    )


with c2:

    st.metric(
        "Contract",
        customer.get(
            "Contract",
            "N/A"
        )
    )


with c3:

    st.metric(
        "Monthly Charges",
        f"₹ {monthly_charges:.2f}"
    )


st.divider()


# ============================================================
# NAVIGATION
# ============================================================

st.subheader(
    "🔄 Analyze Another Customer"
)


if st.button(
    "👤 Back to Customer Form",
    use_container_width=True
):

    st.switch_page(
        "pages/1_Customer_Form.py"
    )