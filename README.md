# HDFC Bank Expense Analyzer

A simple Streamlit app that analyzes HDFC bank statement Excel exports. This tool is designed to parse HDFC account statement files, extract transaction data, calculate debit and credit totals, categorize expenses, and visualize spending trends.

## Features

- Supports HDFC Excel exports (`.xls` and `.xlsx`)
- Detects HDFC statement header rows and loads transaction data
- Parses `Date`, `Narration`, `Withdrawal Amt.`, `Deposit Amt.`
- Calculates total debit, total credit, and net flow
- Categorizes expenses into groups like Petrol, UPI, Recharge, Pharmacy, Groceries, Utilities, and more
- Shows expense breakdown charts and monthly trends
- Provides CSV download for processed data

## Usage

1. Install dependencies:
   ```bash
   pip install streamlit pandas matplotlib xlrd
   ```
2. Run the app:
   ```bash
   streamlit run app.py
   ```
3. Open the local Streamlit URL displayed in the terminal.
4. Upload your HDFC bank statement Excel file.

## Notes

- This app is currently optimized for HDFC bank statement exports.
- Choose the Excel export option from HDFC NetBanking or Mobile Banking.
- The app automatically detects the statement header row and reads transaction rows.

## Files

- `app.py` — main Streamlit application
- `.gitignore` — ignored files and folders
- `README.md` — project documentation
