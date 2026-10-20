# 🏦 Python Bank Management System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bank-management-system-4flxevvprsp5nnmduzqtxz.streamlit.app/)
🌐 **Live Demo:** [bank-management-system-4flxevvprsp5nnmduzqtxz.streamlit.app](https://bank-management-system-4flxevvprsp5nnmduzqtxz.streamlit.app/)

A modern, robust, and secure banking management system featuring both an **interactive terminal CLI** and a **full-featured Streamlit web application**. Built with clean Python OOP principles and resilient JSON persistence.

---

## 🌟 Key Features

### 👤 Customer Operations
- **Account Creation**:
  - Age eligibility verification ($\ge 18$ years).
  - Automated generation of unique 7-character alphanumeric account numbers (e.g., `M!472DU`).
  - Strict input validation for emails (regex-checked) and 4-digit numeric PINs.
  - Optional initial deposit during setup.
  - Virtual Debit/Credit Card display with holder name, account number, and balance.
- **Deposit Funds**:
  - Secure credential verification (Account Number + PIN).
  - Instant balance updates and automated transaction recording.
- **Withdraw Funds**:
  - Insufficient funds detection and balance protection.
  - Immediate debit and transaction logging.
- **Account Details & Mini-Statement**:
  - Overview of account status, opening date, and live balance.
  - Interactive transaction history table displaying timestamps, transaction types, amounts, and resulting balances.
- **Security & Profile Updates**:
  - Dedicated PIN update with current PIN verification and confirmation matching.
  - Contact email updates with format validation.
- **Account Closure**:
  - Permanent account deletion with positive balance warnings and confirmation prompts.

### 🛡️ Administrator Operations
- **Protected Admin Panel**:
  - Secured behind an **Admin ID** and **Admin Password** login gate.
  - Session state tracking with a one-click **Log Out** button.
- **Account Auditing**:
  - Live bank metrics: Total Active Accounts, Total Reserves, and Average Account Balance.
  - Filterable table displaying all active customer profiles.
  - Real-time search across Account Numbers, Names, and Emails.
- **Data Export**:
  - Download full customer audit reports as a formatted JSON file.

### 💾 Robust Persistence
- Fault-tolerant JSON data engine in `data.json`.
- Safely handles missing, empty (0-byte), or corrupted JSON files without crashing the application.

---

## 🗂️ Project Structure

```text
Bank Management System/
│
├── app.py              # Streamlit Web Application (Modern Dashboard UI)
├── bank.py             # Core Banking Engine & Interactive Terminal CLI
├── main.py             # Original reference script
├── data.json           # JSON Database storing registered accounts and transactions
├── pyproject.toml      # Project configuration & dependencies
└── README.md           # Documentation
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python **3.12+** (tested on Python 3.12 - 3.14)
- Pip package manager

### 1. Clone or Open the Workspace
```powershell
cd "d:/Programming_Languages/Python DSA/Bank Management System"
```

### 2. Install Required Dependencies
```powershell
python -m pip install streamlit
```

---

## 🚀 How to Run

### Option 1: Live Cloud Demo (Instant Access)
Access the live deployment directly in your browser without local setup:
👉 **[Launch Live Demo on Streamlit](https://bank-management-system-4flxevvprsp5nnmduzqtxz.streamlit.app/)**

### Option 2: Local Streamlit Web Application
Launch the modern web UI in your default browser:
```powershell
python -m streamlit run app.py
```
> The dashboard will be available at: **http://localhost:8501**

### Option 3: Console Terminal CLI
Run the interactive command-line interface:
```powershell
python bank.py
```

---

## 🔐 Administrator Credentials

To access the **View All Accounts (Admin)** portal:

| Credential | Value |
| :--- | :--- |
| **Admin ID** | `admin` |
| **Admin Password** | `Admin@123` |

> [!TIP]
> You can override default administrator credentials using environment variables:
> ```powershell
> $env:BANK_ADMIN_ID="custom_admin"
> $env:BANK_ADMIN_PASS="CustomSecurePass!"
> ```

---

## 🛠️ Technology Stack

- **Language**: Python 3
- **Web UI Framework**: [Streamlit](https://streamlit.io/)
- **Data Storage**: JSON (`data.json`)
- **Security & Validation**: Regex (`re`), Hash/Masking logic, Type annotations (`typing`)

---

## 📄 License
This project is open-source and available under the standard MIT License.
