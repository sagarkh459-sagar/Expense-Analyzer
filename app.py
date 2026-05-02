import re

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="HDFC Bank Expense Analyzer", layout="wide")
st.title("💸 HDFC Bank Expense Analyzer")

st.markdown(
    "Upload your HDFC bank statement Excel file. This app currently supports HDFC statement exports "
    "saved as `.xls` or `.xlsx` from HDFC online banking."
)
st.markdown(
    "#### Supported HDFC statement format\n"
)
st.markdown(
    "#### How to export HDFC statement as Excel\n"
    "1. Login to HDFC NetBanking or Mobile Banking.\n"
    "2. Open the account statement / transaction history section.\n"
    "3. Set the desired date range.\n"
    "4. Choose Export / Download and select `Excel`.\n"
    "5. Upload the downloaded file here."
)

uploaded_file = st.file_uploader(
    "Upload your HDFC bank statement (Excel .xls or .xlsx)",
    type=["xls", "xlsx"],
)


def normalize_header(value):
    if value is None:
        return ""
    return re.sub(r"[^a-z0-9]+", " ", str(value).strip().lower())


def parse_amount(value):
    if value is None:
        return None
    text = str(value).strip().replace(",", "").replace("₹", "")
    text = re.sub(r"[^0-9.-]", "", text)
    if text in ("", ".", "-", "-.", "-.0"):
        return None
    try:
        return float(text)
    except ValueError:
        return None


def find_header_row(df):
    def row_keywords(row, keywords):
        normalized = [normalize_header(x) for x in row]
        return any(keyword in normalized for keyword in keywords)

    for idx, row in df.iterrows():
        normalized = [normalize_header(x) for x in row]
        has_date = any(word in normalized for word in ["date", "txn date", "transaction date"])
        has_desc = any(word in normalized for word in ["narration", "description", "particulars", "remarks", "transaction description"])
        has_amount = any(word in normalized for word in ["withdrawal", "deposit", "debit", "credit", "dr", "cr", "withdrawal amt", "deposit amt", "amount", "amt"])
        if has_date and has_desc and has_amount:
            return idx

    # Fallback: header row may appear without explicit amount keyword in some exports.
    for idx, row in df.iterrows():
        normalized = [normalize_header(x) for x in row]
        has_date = any(word in normalized for word in ["date", "txn date", "transaction date"])
        has_desc = any(word in normalized for word in ["narration", "description", "particulars", "remarks", "transaction description"])
        if has_date and has_desc:
            return idx

    return None


def read_hdfc_statement(file):
    df = pd.read_excel(file, header=None, dtype=str, sheet_name=0)
    header_row = find_header_row(df)
    if header_row is None:
        return None, (
            "Could not find the statement header row. "
            "Ensure the file contains a row with Date and Narration / Description."
        )

    header = [str(x).strip() if x is not None else "" for x in df.iloc[header_row]]
    data = df.iloc[header_row + 1 :].reset_index(drop=True)
    data.columns = header
    data = data.loc[:, data.columns.notna()]
    data = data[~data.apply(lambda row: row.astype(str).str.strip().eq("").all(), axis=1)]
    return data, None


def categorize_transaction(description):
    text = str(description).lower()
    if any(word in text for word in ["swiggy", "zomato", "dominos", "restaurant", "dining"]):
        return "Food"
    if any(word in text for word in ["uber", "ola", "taxi", "cab", "flight", "train", "bus"]):
        return "Travel"
    if any(word in text for word in ["petrol", "fuel", "bharat petroleum", "iocl", "hpcl", "indianoil"]):
        return "Petrol"
    if "upi" in text:
        return "UPI"
    if any(word in text for word in ["recharge", "topup", "mobikwik", "paytm", "phonepe"]):
        return "Recharge"
    if any(word in text for word in ["apollo", "pharmacy", "medic", "medicine", "pharma"]):
        return "Pharmacy"
    if any(word in text for word in ["grocer", "bigbasket", "dmart", "reliance", "supermarket", "grocery"]):
        return "Groceries"
    if any(word in text for word in ["electricity", "water", "bill", "internet", "broadband", "insurance", "rent"]):
        return "Utilities"
    if any(word in text for word in ["amazon", "flipkart", "myntra", "ajio", "shopping", "paytm mall"]):
        return "Shopping"
    if any(word in text for word in ["movie", "netflix", "prime", "spotify", "cinema", "entertainment"]):
        return "Entertainment"
    return "Others"


if uploaded_file:
    statement_df, error = read_hdfc_statement(uploaded_file)
    if error:
        st.error(error)
    elif statement_df is None or statement_df.empty:
        st.error("The uploaded Excel file was parsed but no transaction rows were found.")
    else:
        df = statement_df.copy()
        df.columns = [str(c).strip() for c in df.columns]

        date_col = next((c for c in df.columns if "date" in normalize_header(c)), None)
        desc_col = next(
            (c for c in df.columns if "narration" in normalize_header(c) or "description" in normalize_header(c)),
            None,
        )
        withdrawal_col = next((c for c in df.columns if "withdrawal" in normalize_header(c)), None)
        deposit_col = next((c for c in df.columns if "deposit" in normalize_header(c)), None)

        if not withdrawal_col and not deposit_col:
            st.error(
                "Could not find Withdrawal or Deposit columns. "
                "Please upload an HDFC statement with Withdrawal Amt. and/or Deposit Amt."
            )
        else:
            df["Withdrawal"] = df[withdrawal_col].apply(parse_amount) if withdrawal_col else 0.0
            df["Deposit"] = df[deposit_col].apply(parse_amount) if deposit_col else 0.0
            df["Withdrawal"] = pd.to_numeric(df["Withdrawal"], errors="coerce").fillna(0.0)
            df["Deposit"] = pd.to_numeric(df["Deposit"], errors="coerce").fillna(0.0)
            df["Debit"] = df["Withdrawal"].abs()
            df["Credit"] = df["Deposit"].abs()
            df["Amount"] = df["Debit"].where(df["Debit"] > 0, df["Credit"])
            df["Type"] = df.apply(
                lambda row: "Debit"
                if row["Debit"] > 0
                else ("Credit" if row["Credit"] > 0 else "Other"),
                axis=1,
            )
            df["Description"] = df[desc_col] if desc_col else ""
            df["Category"] = df["Description"].apply(categorize_transaction)

            total_debit = df["Debit"].sum()
            total_credit = df["Credit"].sum()
            net_flow = total_credit - total_debit

            st.subheader("Statement Preview")
            st.dataframe(df.head(12))

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Spent (Debit)", f"₹{total_debit:,.2f}")
            col2.metric("Total Credit", f"₹{total_credit:,.2f}")
            col3.metric("Net Flow", f"₹{net_flow:,.2f}")

            st.subheader("Expense Category Breakdown")
            summary = df.groupby("Category")["Debit"].sum().sort_values(ascending=False)
            st.bar_chart(summary)

            fig, ax = plt.subplots(figsize=(8, 8))
            wedges, texts, autotexts = ax.pie(
                summary,
                autopct='%1.1f%%',
                pctdistance=0.85,
                startangle=90,
                wedgeprops=dict(width=0.3),
            )
            ax.legend(summary.index, loc="center left", bbox_to_anchor=(1, 0.5))
            ax.set_ylabel("")
            st.pyplot(fig)

            if date_col:
                df[date_col] = pd.to_datetime(df[date_col], errors="coerce", dayfirst=True)
                if df[date_col].notna().any():
                    monthly = df.groupby(df[date_col].dt.to_period("M"))["Debit"].sum().sort_index()
                    st.subheader("Monthly Expense Trend")
                    st.line_chart(monthly.astype(float))

            csv = df.to_csv(index=False)
            st.download_button(
                label="Download Processed Data as CSV",
                data=csv,
                file_name="processed_expenses.csv",
                mime="text/csv",
            )
