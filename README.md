# 🤖 AI Customer Retention Assistant

An AI-powered web application that predicts customer churn, analyzes business impact, and generates customer reports.

Built with **Python** and **Streamlit**, using a Machine Learning model trained on telecom customer data.

---

## 🚀 Live Demo

**Try the live application here:**

👉 https://customerchurnproject-m99t9wqfzdcychu34qtiro.streamlit.app/

[[Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://customerchurnproject-m99t9wqfzdcychu34qtiro.streamlit.app/)

---

## ✨ Features

- **👤 Customer Form**
    - Existing Customer Login using Customer ID
    - New Customer Registration with auto-generated ID (e.g., NEW-1001)
    - Old Customer / New Customer identification

- **🤖 AI Analysis**
    - Churn prediction using Machine Learning
    - Churn Risk Score in percentage
    - Risk Level: Low / Medium / High

- **📈 Business Impact Dashboard**
    - Annual Revenue
    - Customer Value
    - Retention Cost
    - Expected Saving
    - Risk Gauge Chart

- **📄 Customer Report**
    - Complete customer profile
    - Financial details
    - AI recommendation
    - Downloadable text report

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- Scikit-learn
- Plotly

---

## 📂 Project Structure

AI-Customer-Retention-Assistant/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── customer_churn.csv
│   └── new_customers.csv
│
└── pages/
    ├── 1_Customer_Form.py
    ├── 2_AI_Analysis.py
    ├── 3_Business_Impact.py
    └── 4_Report.py

    
---

## ▶️ How to Run Locally

1. Clone the repository:
```bash
git clone https://github.com/your-username/your-repo-name.git

Install dependencies:
pip install -r requirements.txt

Run the app:
streamlit run app.py

🔄 How It Works
New Customer: Enter your name → A new Customer ID is created (e.g., NEW-1001) → Customer is saved for future login.
Existing Customer: Enter your Customer ID (e.g., 7590-VHVEG or NEW-1001) → Your details are loaded → Displayed as Old Customer.
AI Analysis: The model predicts churn risk.
Business Impact: Shows revenue, value, and saving.
Report: Generates a complete downloadable report.

👩‍💻 Developed By
KaaviyaAI 
Customer Retention Assistant - Final Year Project


**Un GitHub repo link ah mattum maathikanum:**

`https://github.com/your-username/your-repo-name.git` nu iruka edathula, un repo link ah potru.

Un repo link theriyala na, GitHub la un repo ku poi mela iruka URL ah copy panni anuppu, naan maathi tharen!

**Ippo paste panni, push pannidu:**

```bash
git add README.md
git commit -m "Added live demo link"
git push