import streamlit as st
import requests
import pandas as pd

server = st.secrets["be_server_url"]

st.title("💰 Expense Tracker Full Stack App")

menu = st.sidebar.selectbox(
    "Menu",
    ["Add", "View", "Update", "Delete", "Analysis"]
)

# ================= ADD =================
if menu == "Add":

    st.header("Add Expense")

    title = st.text_input("Title")
    amount = st.number_input("Amount", min_value=1.0)
    category = st.selectbox("Category", ["Food","Travel","Shopping","Bills","Entertainment","Other"])
    payment = st.selectbox("Payment", ["Cash","UPI","Card","Net Banking"])
    date = st.date_input("Date")
    desc = st.text_area("Description")

    if st.button("Add"):

        payload = {
            "expense_title": title,
            "expense_amount": amount,
            "expense_category": category,
            "payment_type": payment,
            "expense_created_date": str(date),
            "expense_description": desc
        }

        r = requests.post(f"{server}/add_expense", json=payload)
        st.success(r.json()["message"])

# ================= VIEW =================
elif menu == "View":

    st.header("All Expenses")

    r = requests.get(f"{server}/get_expenses")
    data = r.json()["expenses"]

    st.dataframe(pd.DataFrame(data))

# ================= UPDATE =================
elif menu == "Update":

    st.header("Update Expense")

    exp_id = st.number_input("Expense ID", min_value=1)

    title = st.text_input("Title")
    amount = st.number_input("Amount", min_value=1.0)
    category = st.text_input("Category")
    payment = st.text_input("Payment")
    date = st.date_input("Date")
    desc = st.text_area("Description")

    if st.button("Update"):

        payload = {
            "expense_title": title,
            "expense_amount": amount,
            "expense_category": category,
            "payment_type": payment,
            "expense_created_date": str(date),
            "expense_description": desc
        }

        r = requests.put(f"{server}/update_expense/{exp_id}", json=payload)
        st.success(r.json()["message"])

# ================= DELETE =================
elif menu == "Delete":

    st.header("Delete Expense")

    exp_id = st.number_input("Expense ID", min_value=1)

    if st.button("Delete"):

        r = requests.delete(f"{server}/delete_expense/{exp_id}")
        st.success(r.json()["message"])

# ================= ANALYSIS =================
elif menu == "Analysis":

    st.header("Category Wise Spending")

    r = requests.get(f"{server}/summary")
    data = r.json()["summary"]

    df = pd.DataFrame(data)

    st.bar_chart(df.set_index("expense_category"))
    st.dataframe(df)