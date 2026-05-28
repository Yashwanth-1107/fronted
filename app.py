import streamlit as st
import requests
import pandas as pd

# ======================================================
# BACKEND URL (FIXED SAFE VERSION)
# ======================================================

server = st.secrets["be_server_url"]

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(page_title="Expense Tracker", layout="centered")

# ======================================================
# TITLE
# ======================================================
st.title("💰 Expense Tracker Full Stack App")

# ======================================================
# MENU
# ======================================================
menu = st.sidebar.selectbox(
    "Menu",
    ["Add", "View", "Update", "Delete", "Analysis"]
)

# ======================================================
# ADD EXPENSE
# ======================================================
if menu == "Add":

    st.header("➕ Add Expense")

    title = st.text_input("Title")
    amount = st.number_input("Amount", min_value=1.0, step=1.0)
    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"]
    )
    payment = st.selectbox(
        "Payment",
        ["Cash", "UPI", "Card", "Net Banking"]
    )
    date = st.date_input("Date")
    desc = st.text_area("Description")

    if st.button("Add Expense"):

        if title and amount:

            payload = {
                "expense_title": title,
                "expense_amount": amount,
                "expense_category": category,
                "payment_type": payment,
                "expense_created_date": str(date),
                "expense_description": desc
            }

            try:
                r = requests.post(f"{server}/add_expense", json=payload)
                st.success(r.json().get("message", "Expense Added"))
            except Exception as e:
                st.error(f"Error: {e}")

        else:
            st.warning("Please fill required fields")

# ======================================================
# VIEW EXPENSES
# ======================================================
elif menu == "View":

    st.header("📄 All Expenses")

    try:
        r = requests.get(f"{server}/get_expenses")

        if r.status_code == 200:

            data = r.json().get("expenses", [])

            if data and len(data) > 0:
                df = pd.DataFrame(data)
                st.dataframe(df)
            else:
                st.info("No expenses found in database")

        else:
            st.error(f"Backend Error: {r.text}")

    except Exception as e:
        st.error(f"Request Failed: {e}")
# ======================================================
# UPDATE EXPENSE
# ======================================================
elif menu == "Update":

    st.header("✏️ Update Expense")

    exp_id = st.number_input("Expense ID", min_value=1)

    title = st.text_input("Title")
    amount = st.number_input("Amount", min_value=1.0, step=1.0)
    category = st.text_input("Category")
    payment = st.text_input("Payment Type")
    date = st.date_input("Date")
    desc = st.text_area("Description")

    if st.button("Update Expense"):

        payload = {
            "expense_title": title,
            "expense_amount": amount,
            "expense_category": category,
            "payment_type": payment,
            "expense_created_date": str(date),
            "expense_description": desc
        }

        try:
            r = requests.put(f"{server}/update_expense/{exp_id}", json=payload)
            st.success(r.json().get("message", "Updated Successfully"))
        except Exception as e:
            st.error(f"Error: {e}")

# ======================================================
# DELETE EXPENSE
# ======================================================
elif menu == "Delete":

    st.header("🗑 Delete Expense")

    exp_id = st.number_input("Expense ID", min_value=1)

    if st.button("Delete Expense"):

        try:
            r = requests.delete(f"{server}/delete_expense/{exp_id}")
            st.success(r.json().get("message", "Deleted Successfully"))
        except Exception as e:
            st.error(f"Error: {e}")

# ======================================================
# ANALYSIS
# ======================================================
elif menu == "Analysis":

    st.header("📊 Category Wise Analysis")

    try:
        r = requests.get(f"{server}/summary")

        if r.status_code == 200:

            data = r.json().get("summary", [])

            if data and len(data) > 0:

                df = pd.DataFrame(data)

                if "expense_category" in df.columns and "total" in df.columns:
                    st.bar_chart(df.set_index("expense_category"))

                st.dataframe(df)

            else:
                st.info("No data available for analysis")

        else:
            st.error(f"Backend Error: {r.text}")

    except Exception as e:
        st.error(f"Request Failed: {e}")