import streamlit as st


st.title("Budget Pal")
st.write("Welcome! I am your budgeting pal who is here to help you track your income and expenses.")


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

from budget.auth import signup, login
from budget.storage import load_user_data, save_user_data
from budget.income import set_fixed_income, add_extra_income, total_monthly_income
from budget.spending import set_fixed_expense, add_daily_expense, total_monthly_expenses

if not st.session_state.logged_in:
    st.subheader("Login or Sign Up")
    option = st.selectbox("Choose", ["Login", "Sign Up"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")


    if st.button("Submit"):
        if option == "Login":
            success, msg = login(username, password)
        else:
            success, msg = signup(username, password)
        
        if success:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(msg)
            st.rerun()
        else:
            st.error(msg)
    st.stop()

if st.session_state.logged_in:

    username = st.session_state.username
    data = load_user_data(username)

    st.success(f"Logged in as {username}")

menu = st.selectbox(
    "Choose an option",
    [
        "Set Fixed Income",
        "Add Extra Income",
        "Set Fixed Expense",
        "Add Daily Expense",
        "View Monthly Summary"
    ]
)

if menu == "Set Fixed Income":
    amount = st.number_input("Monthly Salary", min_value=0.0)

    if st.button("Save Salary"):
        data = set_fixed_income(data, amount)
        save_user_data(username, data)
        st.success("Fixed income saved")

elif menu == "Add Extra Income":
    month = st.selectbox("Month", [
        "January", "February", "March", "April", "May", "June", "July",
        "August", "September", "October", "November", "December"
    ])

    day = st.number_input("Day", min_value=1, max_value=31)
    amount = st.number_input("Amount", min_value=0.0)
    note = st.text_input("Note")

    if st.button("Add Income"):
        data = add_extra_income(data, month, day, amount, note)
        save_user_data(username, data)
        st.success("Income added")

elif menu == "Add Daily Expense":
    month = st.selectbox("Month", [
        "January", "February", "March", "April", "May", "June", "July",
        "August", "September", "October", "November", "December"
    ])
    day = st.number_input("Day", min_value=1, max_value=31)
    amount = st.number_input("Amount", min_value=0.0)
    note = st.text_input("Note")

    if st.button("Add Expense"):
        data = add_daily_expense(data, month, day, amount, note)
        save_user_data(username, data)
        st.success("Expense added")

elif menu == "Set Fixed Expense":
    name = st.text_input("Expense name (Rent, Phone, etc)")
    amount = st.number_input("Monthly amount", min_value=0.0)

    if st.button("Save Fixed Expense"):
        data = set_fixed_expense(data, name, amount)
        save_user_data(username, data)
        st.success("Fixed expense saved")

elif menu == "View Monthly Summary":
    month = st.selectbox(
        "Which month do you want to view?",
        list(data["monthly"].keys()) or
        ["No data yet"]
    )

    income = total_monthly_income(data, month)
    expenses = total_monthly_expenses(data, month)
    
    st.write("### Summary")
    st.write("Income:", income)
    st.write("Expenses:", expenses)
    st.write("Remaining:", income - expenses)

    st.subheader("Transaction Timeline")

    transactions = []

    month_data = data["monthly"].get(month, {})

    for inc in month_data.get("income", []):
        transactions.append({
            "day": inc["day"],
            "amount": f"+${inc['amounnt']}",
            "note": inc["note"]
        })

    for exp in month_data.get("expenses", []):
        transactions.append({
            "day": exp["day"],
            "amount": f"+${exp['amounnt']}",
            "note": exp["note"]    
        })

    transactions.sort(keys=lambda x:["day"])

    for t in transactions:
        st.write(
            f"Day {t['day']}  |  {t['amount']}  |  {t['note']}"
        )
