"""
Streamlit Web Application for Python Bank Management System.
Built on top of the Bank class in bank.py.
"""

import json
import os
import re
from datetime import datetime
import streamlit as st
from bank import Bank

# Page configuration
st.set_page_config(
    page_title="Python Bank Management System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    /* Metric styling */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e3a8a;
    }
    
    /* Card design */
    .bank-card {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(30, 58, 138, 0.2);
        margin-bottom: 25px;
    }
    
    .bank-card-chip {
        width: 45px;
        height: 35px;
        background: #fbbf24;
        border-radius: 6px;
        margin-bottom: 20px;
    }
    
    .card-acc-no {
        font-family: 'Courier New', monospace;
        font-size: 1.5rem;
        letter-spacing: 3px;
        font-weight: bold;
        margin-bottom: 15px;
    }

    .card-footer-flex {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
    }

    .success-box {
        background-color: #ecfdf5;
        border-left: 5px solid #10b981;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        color: #065f46;
    }

    .danger-box {
        background-color: #fef2f2;
        border-left: 5px solid #ef4444;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        color: #991b1b;
    }
</style>
""", unsafe_allow_html=True)


def get_bank() -> Bank:
    """Returns Bank instance with fresh data from data.json."""
    return Bank("data.json")


def validate_email(email: str) -> bool:
    """Validates email format using regex."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email.strip()))


def validate_pin(pin: str) -> bool:
    """Checks if PIN is exactly 4 digits."""
    return len(pin.strip()) == 4 and pin.strip().isdigit()


def render_account_card(account: dict):
    """Renders a credit/debit card visualization for the account."""
    acc_no = account.get("accountNo.", "XXXXXXX")
    name = account.get("name", "Account Holder").upper()
    balance = account.get("balance", 0.0)
    created = account.get("created_at", datetime.now().strftime("%Y-%m-%d"))
    
    st.markdown(f"""
    <div class="bank-card">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div class="bank-card-chip"></div>
            <span style="font-size: 1.2rem; font-weight: bold; letter-spacing: 1px;">PYTHON BANK</span>
        </div>
        <div class="card-acc-no">{acc_no}</div>
        <div class="card-footer-flex">
            <div>
                <div style="font-size: 0.75rem; text-transform: uppercase; opacity: 0.8;">Card Holder</div>
                <div style="font-size: 1.1rem; font-weight: 600;">{name}</div>
            </div>
            <div>
                <div style="font-size: 0.75rem; text-transform: uppercase; opacity: 0.8;">Balance</div>
                <div style="font-size: 1.2rem; font-weight: 700;">${balance:,.2f}</div>
            </div>
            <div>
                <div style="font-size: 0.75rem; text-transform: uppercase; opacity: 0.8;">Member Since</div>
                <div style="font-size: 0.95rem;">{created[:10]}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/fluency/96/bank-building.png", width=70)
st.sidebar.title("Python Bank")
st.sidebar.caption("Secure & Modern Banking System")

menu_choice = st.sidebar.radio(
    "Navigation Menu",
    [
        "🏠 Dashboard",
        "➕ Open Account",
        "💳 Deposit Funds",
        "💸 Withdraw Funds",
        "📊 Account Statement",
        "⚙️ Account Settings",
        "🗂️ View All Accounts (Admin)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip**: Save your generated Account Number and 4-digit PIN to perform transactions.")

bank = get_bank()

# ==========================================
# 1. DASHBOARD
# ==========================================
if menu_choice == "🏠 Dashboard":
    st.title("🏦 Python Bank Portal")
    st.write("Welcome to the Python Bank digital dashboard. Manage your funds, open accounts, and review transactions with ease.")

    total_accounts = len(bank.data)
    total_deposits = sum(acc.get("balance", 0.0) for acc in bank.data)
    total_transactions = sum(len(acc.get("transactions", [])) for acc in bank.data)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Active Accounts", total_accounts, help="Total number of registered bank accounts")
    col2.metric("Total Bank Reserves", f"${total_deposits:,.2f}", help="Total cumulative balances across all accounts")
    col3.metric("Processed Transactions", total_transactions, help="Total successful deposits and withdrawals logged")

    st.markdown("---")

    st.subheader("⚡ Quick Services")
    qcol1, qcol2, qcol3 = st.columns(3)

    with qcol1:
        st.markdown("""
        **➕ Open Account**  
        Create a new savings or checking account with instant account number generation.
        """)
    with qcol2:
        st.markdown("""
        **💳 Deposit & Withdraw**  
        Fast and secure money deposits and cash withdrawals with automated logging.
        """)
    with qcol3:
        st.markdown("""
        **📊 Mini Statements**  
        View and export real-time transaction history and manage your security PIN.
        """)


# ==========================================
# 2. OPEN ACCOUNT
# ==========================================
elif menu_choice == "➕ Open Account":
    st.title("➕ Open a New Bank Account")
    st.write("Fill in the application form below. Account numbers are automatically generated.")

    with st.form("open_account_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name *", placeholder="e.g. John Doe")
            age = st.number_input("Age (Must be at least 18) *", min_value=0, max_value=120, value=21, step=1)
            email = st.text_input("Email Address *", placeholder="e.g. john@example.com")

        with col2:
            pin = st.text_input("Create 4-Digit PIN *", type="password", max_chars=4, placeholder="e.g. 1234")
            confirm_pin = st.text_input("Confirm 4-Digit PIN *", type="password", max_chars=4, placeholder="e.g. 1234")
            initial_deposit = st.number_input("Initial Deposit Amount ($)", min_value=0.0, max_value=100000.0, value=0.0, step=100.0)

        submitted = st.form_submit_button("🚀 Create Account", use_container_width=True)

    if submitted:
        if not name.strip():
            st.error("Please enter a valid name.")
        elif age < 18:
            st.error("Eligibility Error: You must be at least 18 years old to open an account.")
        elif not validate_email(email):
            st.error("Please enter a valid email address (e.g., name@example.com).")
        elif not validate_pin(pin):
            st.error("PIN must be exactly 4 numeric digits.")
        elif pin != confirm_pin:
            st.error("PIN confirmation does not match. Please re-enter your PIN.")
        else:
            acc_number = bank._generate_unique_account_no()
            new_acc = {
                "name": name.strip(),
                "age": int(age),
                "email": email.strip(),
                "pin": pin.strip(),
                "accountNo.": acc_number,
                "balance": float(round(initial_deposit, 2)),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "transactions": []
            }
            if initial_deposit > 0:
                bank._log_transaction(new_acc, "INITIAL DEPOSIT", float(round(initial_deposit, 2)))

            bank.data.append(new_acc)
            if bank._save_data():
                st.balloons()
                st.success("🎉 Congratulations! Your bank account has been opened successfully.")
                render_account_card(new_acc)
                st.info(f"🔑 **Important**: Please note down your Account Number: `{acc_number}` and keep your PIN secure.")


# ==========================================
# 3. DEPOSIT FUNDS
# ==========================================
elif menu_choice == "💳 Deposit Funds":
    st.title("💳 Deposit Money")
    st.write("Deposit funds into your account safely and instantly.")

    with st.form("deposit_form"):
        col1, col2 = st.columns(2)
        with col1:
            acc_no = st.text_input("Account Number", placeholder="e.g. M!472DU").strip()
            pin = st.text_input("4-Digit PIN", type="password", max_chars=4).strip()
        with col2:
            amount = st.number_input("Deposit Amount ($)", min_value=1.0, max_value=100000.0, value=100.0, step=50.0)

        submit_deposit = st.form_submit_button("💳 Deposit Funds", use_container_width=True)

    if submit_deposit:
        if not acc_no or not pin:
            st.error("Please enter both Account Number and PIN.")
        else:
            account = bank._authenticate(acc_no, pin)
            if not account:
                st.error("Invalid Account Number or PIN. Please check your credentials.")
            else:
                account["balance"] = round(account["balance"] + amount, 2)
                bank._log_transaction(account, "DEPOSIT", amount)
                bank._save_data()

                st.success(f"Successfully deposited ${amount:,.2f} into Account `{acc_no}`!")
                render_account_card(account)


# ==========================================
# 4. WITHDRAW FUNDS
# ==========================================
elif menu_choice == "💸 Withdraw Funds":
    st.title("💸 Withdraw Money")
    st.write("Withdraw funds from your active account.")

    with st.form("withdraw_form"):
        col1, col2 = st.columns(2)
        with col1:
            acc_no = st.text_input("Account Number", placeholder="e.g. M!472DU").strip()
            pin = st.text_input("4-Digit PIN", type="password", max_chars=4).strip()
        with col2:
            amount = st.number_input("Withdrawal Amount ($)", min_value=1.0, value=50.0, step=50.0)

        submit_withdraw = st.form_submit_button("💸 Withdraw Funds", use_container_width=True)

    if submit_withdraw:
        if not acc_no or not pin:
            st.error("Please enter both Account Number and PIN.")
        else:
            account = bank._authenticate(acc_no, pin)
            if not account:
                st.error("Invalid Account Number or PIN.")
            else:
                current_bal = account.get("balance", 0.0)
                if amount > current_bal:
                    st.error(f"Insufficient funds! Your available balance is ${current_bal:,.2f}.")
                else:
                    account["balance"] = round(current_bal - amount, 2)
                    bank._log_transaction(account, "WITHDRAWAL", amount)
                    bank._save_data()

                    st.success(f"Successfully withdrew ${amount:,.2f}. Remaining balance: ${account['balance']:,.2f}")
                    render_account_card(account)


# ==========================================
# 5. ACCOUNT STATEMENT & DETAILS
# ==========================================
elif menu_choice == "📊 Account Statement":
    st.title("📊 Account Details & Mini Statement")
    st.write("Enter your credentials to review your account overview and transaction ledger.")

    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        acc_no = st.text_input("Account Number", placeholder="e.g. M!472DU", key="stmt_acc").strip()
    with col2:
        pin = st.text_input("4-Digit PIN", type="password", max_chars=4, key="stmt_pin").strip()
    with col3:
        st.write("")
        st.write("")
        check_btn = st.button("🔍 View Details", use_container_width=True)

    if check_btn or (acc_no and pin):
        account = bank._authenticate(acc_no, pin)
        if not account:
            st.error("Invalid Account Number or PIN.")
        else:
            render_account_card(account)

            tab1, tab2 = st.tabs(["📜 Transaction History", "👤 Profile Info"])

            with tab1:
                tx_list = account.get("transactions", [])
                if not tx_list:
                    st.info("No transactions recorded yet for this account.")
                else:
                    st.write(f"**Total Transactions:** {len(tx_list)}")
                    # Render table
                    rows = []
                    for t in reversed(tx_list):
                        badge = "🟢" if "DEPOSIT" in t["type"] else "🔴"
                        rows.append({
                            "Timestamp": t.get("timestamp"),
                            "Type": f"{badge} {t.get('type')}",
                            "Amount ($)": f"{t.get('amount', 0.0):,.2f}",
                            "Balance ($)": f"{t.get('balance', 0.0):,.2f}"
                        })
                    st.table(rows)

            with tab2:
                pcol1, pcol2 = st.columns(2)
                pcol1.write(f"**Account Holder:** {account.get('name')}")
                pcol1.write(f"**Age:** {account.get('age')}")
                pcol2.write(f"**Email Address:** {account.get('email')}")
                pcol2.write(f"**Account Created:** {account.get('created_at', 'N/A')}")


# ==========================================
# 6. ACCOUNT SETTINGS (PIN, EMAIL, DELETE)
# ==========================================
elif menu_choice == "⚙️ Account Settings":
    st.title("⚙️ Account Management")
    st.write("Update your security credentials or manage account status.")

    setting_tab1, setting_tab2, setting_tab3 = st.tabs(["🔒 Update PIN", "✉️ Update Email", "⚠️ Delete Account"])

    # Update PIN Tab
    with setting_tab1:
        st.subheader("Update Your 4-Digit Security PIN")
        with st.form("update_pin_form"):
            col1, col2 = st.columns(2)
            with col1:
                acc_no = st.text_input("Account Number").strip()
                current_pin = st.text_input("Current 4-Digit PIN", type="password", max_chars=4).strip()
            with col2:
                new_pin = st.text_input("New 4-Digit PIN", type="password", max_chars=4).strip()
                confirm_pin = st.text_input("Confirm New PIN", type="password", max_chars=4).strip()

            submit_pin = st.form_submit_button("Update PIN", use_container_width=True)

        if submit_pin:
            account = bank._authenticate(acc_no, current_pin)
            if not account:
                st.error("Invalid Account Number or Current PIN.")
            elif not validate_pin(new_pin):
                st.error("New PIN must be exactly 4 numeric digits.")
            elif new_pin == current_pin:
                st.error("New PIN cannot be the same as your current PIN.")
            elif new_pin != confirm_pin:
                st.error("New PIN and confirmation do not match.")
            else:
                account["pin"] = new_pin
                bank._save_data()
                st.success("Your PIN has been updated successfully!")

    # Update Email Tab
    with setting_tab2:
        st.subheader("Update Contact Email")
        with st.form("update_email_form"):
            col1, col2 = st.columns(2)
            with col1:
                acc_no = st.text_input("Account Number", key="email_acc").strip()
                pin = st.text_input("4-Digit PIN", type="password", max_chars=4, key="email_pin").strip()
            with col2:
                new_email = st.text_input("New Email Address").strip()

            submit_email = st.form_submit_button("Update Email", use_container_width=True)

        if submit_email:
            account = bank._authenticate(acc_no, pin)
            if not account:
                st.error("Invalid Account Number or PIN.")
            elif not validate_email(new_email):
                st.error("Please enter a valid email address.")
            elif new_email.lower() == account.get("email", "").lower():
                st.info("New email address is identical to your current email.")
            else:
                account["email"] = new_email
                bank._save_data()
                st.success("Your email address has been updated successfully!")

    # Delete Account Tab
    with setting_tab3:
        st.subheader("⚠️ Close / Delete Account")
        st.warning("Warning: Deleting an account is permanent and irreversible.")

        with st.form("delete_account_form"):
            col1, col2 = st.columns(2)
            with col1:
                del_acc_no = st.text_input("Account Number to Delete").strip()
                del_pin = st.text_input("4-Digit PIN", type="password", max_chars=4).strip()
            with col2:
                confirm_del = st.checkbox("I understand that this action is irreversible and permanent.")

            submit_del = st.form_submit_button("🚨 Delete Account", use_container_width=True)

        if submit_del:
            if not confirm_del:
                st.error("Please check the confirmation box to proceed with deletion.")
            else:
                account = bank._authenticate(del_acc_no, del_pin)
                if not account:
                    st.error("Invalid Account Number or PIN.")
                else:
                    if account.get("balance", 0.0) > 0:
                        st.warning(f"Note: Account had a remaining balance of ${account['balance']:,.2f}.")
                    bank.data.remove(account)
                    bank._save_data()
                    st.success(f"Account `{del_acc_no}` has been permanently deleted.")


# ==========================================
# 7. VIEW ALL ACCOUNTS (ADMIN)
# ==========================================
elif menu_choice == "🗂️ View All Accounts (Admin)":
    st.title("🗂️ Administrative Control Panel")
    st.write("Secure portal for bank managers to audit and inspect active client accounts.")

    # Defined Admin Credentials
    ADMIN_USER = os.getenv("BANK_ADMIN_ID", "admin")
    ADMIN_PASS = os.getenv("BANK_ADMIN_PASS", "Admin@123")

    if "admin_logged_in" not in st.session_state:
        st.session_state["admin_logged_in"] = False

    # Login View if not authenticated
    if not st.session_state["admin_logged_in"]:
        col1, col2, _ = st.columns([1.2, 0.1, 0.7])
        with col1:
            st.markdown("""
            <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
                <h4 style="margin: 0 0 10px 0; color: #1e3a8a;">🔒 Admin Authentication Required</h4>
                <p style="color: #64748b; font-size: 0.9rem; margin-bottom: 0px;">
                    This section contains sensitive customer financial data. Please authenticate with your administrator credentials to proceed.
                </p>
            </div>
            """, unsafe_allow_html=True)

            with st.form("admin_login_form"):
                admin_id = st.text_input("Administrator ID", placeholder="Enter Admin ID").strip()
                admin_pass = st.text_input("Administrator Password", type="password", placeholder="Enter Admin Password").strip()
                submit_admin = st.form_submit_button("🔑 Login as Admin", use_container_width=True)

            if submit_admin:
                if admin_id == ADMIN_USER and admin_pass == ADMIN_PASS:
                    st.session_state["admin_logged_in"] = True
                    st.success("Access Granted! Loading administrator dashboard...")
                    st.rerun()
                else:
                    st.error("❌ Access Denied: Invalid Admin ID or Password.")

    else:
        # Authenticated Admin View
        top_col1, top_col2 = st.columns([4, 1])
        with top_col1:
            st.success("🟢 **Authenticated as Administrator** — Full access enabled.")
        with top_col2:
            if st.button("🔒 Log Out", use_container_width=True):
                st.session_state["admin_logged_in"] = False
                st.rerun()

        st.markdown("---")

        if not bank.data:
            st.info("No accounts currently registered in the database.")
        else:
            total_acc = len(bank.data)
            total_funds = sum(acc.get("balance", 0.0) for acc in bank.data)
            avg_balance = total_funds / total_acc if total_acc > 0 else 0.0

            mcol1, mcol2, mcol3 = st.columns(3)
            mcol1.metric("Registered Accounts", total_acc)
            mcol2.metric("Total Deposits", f"${total_funds:,.2f}")
            mcol3.metric("Average Account Balance", f"${avg_balance:,.2f}")

            st.subheader("📋 Active Customer Accounts")
            search_query = st.text_input("🔍 Search accounts (by Account Number, Name, or Email):").strip().lower()

            filtered_data = bank.data
            if search_query:
                filtered_data = [
                    acc for acc in bank.data
                    if search_query in acc.get("accountNo.", "").lower()
                    or search_query in acc.get("name", "").lower()
                    or search_query in acc.get("email", "").lower()
                ]

            accounts_summary = []
            for acc in filtered_data:
                accounts_summary.append({
                    "Account No": acc.get("accountNo."),
                    "Holder Name": acc.get("name"),
                    "Age": acc.get("age"),
                    "Email": acc.get("email"),
                    "Balance ($)": f"{acc.get('balance', 0.0):,.2f}",
                    "Total Transactions": len(acc.get("transactions", [])),
                    "Opened On": acc.get("created_at", "N/A")
                })

            st.dataframe(accounts_summary, use_container_width=True)

            # JSON export option for auditing
            st.download_button(
                label="📥 Export Database (JSON)",
                data=json.dumps(bank.data, indent=4),
                file_name="bank_accounts_audit.json",
                mime="application/json"
            )

