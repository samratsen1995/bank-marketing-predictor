import streamlit as st
import pickle
import pandas as pd

with open("model.pkl", "rb") as file:
    model = pickle.load(file)

st.title("Bank Marketing Predictor Model")

# Numeric inputs
age      = st.number_input("Age", min_value=18, max_value=100)
balance  = st.number_input("Balance")
day      = st.number_input("Day", min_value=1, max_value=31)
duration = st.number_input("Duration (seconds)")
campaign = st.number_input("Campaign (contacts)")
pdays    = st.number_input("Pdays (-1 if not contacted)")
previous = st.number_input("Previous (contacts)")

# Categorical inputs
job      = st.selectbox("Job", ["admin.","blue-collar","entrepreneur",
                                "housemaid","management","retired",
                                "self-employed","services","student",
                                "technician","unemployed","unknown"])
marital  = st.selectbox("Marital", ["single","married","divorced"])
education= st.selectbox("Education", ["primary","secondary","tertiary","unknown"])
contact  = st.selectbox("Contact", ["cellular","telephone","unknown"])
month    = st.selectbox("Month", ["jan","feb","mar","apr","may","jun",
                                   "jul","aug","sep","oct","nov","dec"])
poutcome = st.selectbox("Poutcome", ["success","failure","other","unknown"])

# Binary inputs
default  = st.radio("Default?",  ["yes","no"], horizontal=True)
housing  = st.radio("Housing Loan?", ["yes","no"], horizontal=True)
loan     = st.radio("Personal Loan?", ["yes","no"], horizontal=True)

# Encode binary
default_val  = 1 if default  == "yes" else 0
housing_val  = 1 if housing  == "yes" else 0
loan_val     = 1 if loan     == "yes" else 0

# Encode categorical
job_map = {"admin.":0,"blue-collar":1,"entrepreneur":2,"housemaid":3,
           "management":4,"retired":5,"self-employed":6,"services":7,
           "student":8,"technician":9,"unemployed":10,"unknown":11}
marital_map  = {"single":0,"married":1,"divorced":2}
education_map= {"primary":0,"secondary":1,"tertiary":2,"unknown":3}
contact_map  = {"cellular":0,"telephone":1,"unknown":2}
month_map    = {"jan":0,"feb":1,"mar":2,"apr":3,"may":4,"jun":5,
                "jul":6,"aug":7,"sep":8,"oct":9,"nov":10,"dec":11}
poutcome_map = {"success":0,"failure":1,"other":2,"unknown":3}


if st.button("Predict"):
    input_data = pd.DataFrame([[
        age, job_map[job], marital_map[marital], education_map[education],
        default_val, balance, housing_val, loan_val,
        contact_map[contact], day, month_map[month], duration,
        campaign, pdays, previous, poutcome_map[poutcome]
    ]], columns=['Age', 'Job', 'Marital', 'Education', 'Default', 'Balance',
                 'Housing', 'Loan', 'contact', 'Day', 'Month', 'Duration',
                 'Campaign', 'Pdays', 'Previous', 'poutcome'])
    
    result = model.predict(input_data)
    
    if result[0] == 1:
        st.success("✅ Customer is Eligible")
    else:
        st.error("❌ Customer is Not Eligible")