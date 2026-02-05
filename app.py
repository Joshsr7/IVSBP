import streamlit as st
import streamlit.components.v1 as components

if "page" not in st.session_state:
    st.session_state.page = "Home"



st.title("Budget Pal")
st.write("Welcome! I am your budgeting pal who is here to help you track your income and expenses.")

CATEGORIES = [
    "Food",
    "Gas",
    "Housing",
    "Bills",
    "Subscriptions",
    "Fun",
    "Other"
]


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

from budget.auth import signup, login
from budget.storage import load_user_data, save_user_data
from budget.income import set_fixed_income, add_extra_income, total_monthly_income
from budget.spending import set_fixed_expense, add_daily_expense, total_monthly_expenses
from budget.storage import delete_income, delete_expense



if not st.session_state.logged_in:
    st.subheader("Login or Sign Up")

    with st.form("auth_form"):
        option = st.selectbox("Choose", ["Login", "Sign Up"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Submit")

    if submitted:
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

    
    if not isinstance(data, dict):
        data = {
            "fixed_income": 0,
            "fixed_expenses": [],
            "monthly": {}
        }

    data.setdefault("fixed_expenses", [])
    data.setdefault("monthly", {})

    st.success(f"Logged in as {username}")


st.header("Current Month")

current_month = st.selectbox(
    "Select month",
    [
        "January", "February", "March", "April", "May", "June", "July",
        "August", "September", "October", "November", "December"
    ]
)


st.markdown("### Menu")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("🏠 Home"):
        st.session_state.page = "Home"

with col2:
    if st.button("➕ Income"):
        st.session_state.page = "Add Income"

with col3:
    if st.button("💸 Expense"):
        st.session_state.page = "Add Expense"

with col4:
    if st.button("💼 Salary"):
        st.session_state.page = "Fixed Income"

with col5:
    if st.button("📌 Bills"):
        st.session_state.page = "Fixed Expense"


if st.session_state.page == "Fixed Income":
    amount = st.number_input("Monthly Salary", min_value=0.0)

    if st.button("Save Salary"):
        data = set_fixed_income(data, amount)
        st.success("Fixed income saved")

elif st.session_state.page == "Add Income":
    month = current_month

    day = st.number_input("Day", min_value=1, max_value=31)
    amount = st.number_input("Amount", min_value=0.0)
    note = st.text_input("Note")

    if st.button("Add Income"):
        data = add_extra_income(username, data, month, day, amount, note)
        st.success("Income added")

elif st.session_state.page == "Add Expense":
    month = current_month
    
    day = st.number_input("Day", min_value=1, max_value=31)
    amount = st.number_input("Amount", min_value=0.0)
    note = st.text_input("Note")

    category = st.selectbox("Category", CATEGORIES)

    if st.button("Add Expense"):
        data = add_daily_expense(
            username,
            data, 
            month, 
            day, 
            amount, 
            note, 
            category or "Other"
        )
        st.success("Expense added")

elif st.session_state.page == "Fixed Expense":
    name = st.text_input("Expense name (Rent, Phone, etc)")
    amount = st.number_input("Monthly amount", min_value=0.0)

    category = st.selectbox("Category", CATEGORIES)

    if st.button("Save Fixed Expense"):
        data = set_fixed_expense(username, data, name, amount, category)
        st.success("Fixed expense saved")

month = current_month

income = total_monthly_income(data, month)
expenses = total_monthly_expenses(data, month)
    
st.write("### Summary")
st.write("Income:", income)
st.write("Expenses:", expenses)
st.write("Remaining:", income - expenses)

st.subheader("Transaction Timeline")

transactions = []

month_data = data["monthly"].get(month, {})

for i, inc in enumerate(month_data.get("income", [])):
    transactions.append({
    "day": inc["day"],
    "amount": inc["amount"],
    "note": inc["note"],
    "type": "income",
    "index": i
})
for i, exp in enumerate(month_data.get("expenses", [])):
    transactions.append({
    "day": exp["day"],
    "amount": exp["amount"],
    "note": exp.get("note", ""),
    "type": "expense",
    "category": exp.get("category", "Other"),
    "index": i
})

transactions.sort(key=lambda x: x["day"])

balance = 0

for t in transactions:

    colA, colB = st.columns([4,1])

    with colA:
        if t["type"] == "expense":
            balance -= t["amount"]
            sign = "🔴 -"
        else:
            balance += t["amount"]
            sign = "🟢 +"

        st.markdown(f"### Day {t['day']}")
        st.write(f"{sign}${t['amount']:,.2f}")
        st.write(t["note"])
        st.caption(f"Balance: ${balance:,.2f}")

    with colB:
        if st.button("🗑️", key=f"del_{t['type']}_{t['index']}"):
            if t["type"] == "income":
                delete_income(username, data, month, t["index"])
            else:
                delete_expense(username, data, month, t["index"])

            st.rerun()

    st.divider()




