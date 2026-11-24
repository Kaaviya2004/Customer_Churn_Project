import streamlit as st

# --------------------------------------
# Page Configuration
# --------------------------------------

st.set_page_config(
    page_title="AI Customer Retention Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------
# Custom CSS
# --------------------------------------

st.markdown("""
<style>

.main{
    background-color:#F5F7FB;
}

.block-container{
    padding-top:2rem;
}

/* Hide Streamlit Menu */
#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}

/* Main Title */

.title{
    text-align:center;
    font-size:52px;
    font-weight:800;
    color:#1E3A8A;
}

/* Subtitle */

.subtitle{
    text-align:center;
    font-size:22px;
    color:#64748B;
    margin-bottom:35px;
}

/* Card */

.card{

background:white;

padding:30px;

border-radius:18px;

box-shadow:0px 8px 18px rgba(0,0,0,.10);

margin-top:20px;

}

/* Button */

.stButton>button{

width:100%;

height:55px;

font-size:20px;

border-radius:15px;

background:#2563EB;

color:white;

font-weight:bold;

}

.stButton>button:hover{

background:#1D4ED8;

color:white;

}

</style>
""",unsafe_allow_html=True)

# --------------------------------------
# Hero Section
# --------------------------------------

st.markdown("""
<div class='title'>

🤖 AI Customer Retention Assistant

</div>

<div class='subtitle'>

Predict Customer Churn using Artificial Intelligence

</div>

""",unsafe_allow_html=True)

st.write("")

st.success("""
Welcome 👋

This AI Assistant helps companies identify customers who are likely to leave.

Instead of simply displaying dashboards, this application predicts customer churn,
explains the reasons, recommends the best retention strategy,
and estimates the business impact.
""")

st.write("")

# --------------------------------------
# Features
# --------------------------------------

col1,col2,col3=st.columns(3)

with col1:

    st.markdown("""

<div class="card">

## 🤖 AI Prediction

✔ Predict Churn

✔ Confidence Score

✔ Customer Risk

</div>

""",unsafe_allow_html=True)

with col2:

    st.markdown("""

<div class="card">

## 🧠 AI Diagnosis

✔ Explain Why

✔ Risk Factors

✔ Customer Behaviour

</div>

""",unsafe_allow_html=True)

with col3:

    st.markdown("""

<div class="card">

## 🎁 Retention Plan

✔ AI Recommendation

✔ Revenue Saving

✔ Best Offer

</div>

""",unsafe_allow_html=True)

st.write("")
st.write("")

# --------------------------------------
# Start Button
# --------------------------------------

st.info("👇 Click below to start customer analysis.")

if st.button("🚀 Start Customer Analysis"):

    st.switch_page("pages/1_Customer_Form.py")

st.write("")
st.write("")

st.caption("Developed using Python • SQL Server • Machine Learning • Streamlit")
