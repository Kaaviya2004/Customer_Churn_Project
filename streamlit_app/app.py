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
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}

.title{
    text-align:center;
    font-size:52px;
    font-weight:800;
    color:#1E3A8A;
}
.subtitle{
    text-align:center;
    font-size:22px;
    color:#64748B;
    margin-bottom:35px;
}
.card{
    background:white;
    padding:30px;
    border-radius:18px;
    box-shadow:0px 8px 18px rgba(0,0,0,.10);
    margin-top:20px;
    min-height: 180px;
}
.stButton>button{
    width:100%;
    height:55px;
    font-size:20px;
    border-radius:15px;
    background:#2563EB;
    color:white;
    font-weight:bold;
    border:none;
}
.stButton>button:hover{
    background:#1D4ED8;
    color:white;
}
</style>
""", unsafe_allow_html=True)

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
""", unsafe_allow_html=True)

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
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
<div class="card">
<h2>🤖 AI Prediction</h2>
✔ Predict Churn<br>
✔ Confidence Score<br>
✔ Customer Risk
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div class="card">
<h2>🧠 AI Diagnosis</h2>
✔ Explain Why<br>
✔ Risk Factors<br>
✔ Customer Behaviour
</div>
""", unsafe_allow_html=True)

with col3:
    st.markdown("""
<div class="card">
<h2>🎁 Retention Plan</h2>
✔ AI Recommendation<br>
✔ Revenue Saving<br>
✔ Best Offer
</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# --------------------------------------
# Start Button - CORRECTED
# --------------------------------------
st.info("👇 Click below to start customer analysis.")

if st.button("🚀 Start Customer Analysis"):
    try:
        st.switch_page("pages/1_Customer_Form.py")
    except Exception as e:
        st.error("Pages folder la 1_Customer_Form.py file illa! Check pannu Kaaviya!")
        st.write(e)

st.write("")
st.write("")
st.caption("Developed using Python • SQL Server • Machine Learning • Streamlit")