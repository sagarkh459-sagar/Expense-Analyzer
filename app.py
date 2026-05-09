import re
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Where Did My Salary Go?",
    page_icon="💸",
    layout="wide",
)

st.markdown(
    """
    <style>
    [data-testid="stMetricValue"] { color: #18181B !important; opacity: 1 !important; }
    [data-testid="stMetricLabel"] { color: #71717A !important; opacity: 1 !important; }
    [data-testid="stMetricDelta"] { color: #16A34A !important; opacity: 1 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    :root {
        --bg:        #F7F6F3;
        --card:      #FFFFFF;
        --border:    #E4E2DC;
        --border-md: #D0CEC7;
        --txt-1:     #18181B;
        --txt-2:     #52525B;
        --txt-3:     #A1A1AA;
        --accent:    #4F46E5;
        --accent-bg: #EEF2FF;
        --green:     #16A34A;
        --green-bg:  #F0FDF4;
        --red:       #DC2626;
        --red-bg:    #FEF2F2;
        --amber:     #D97706;
        --amber-bg:  #FFFBEB;
    }

    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: var(--bg) !important;
        color: var(--txt-1) !important;
    }
    .block-container {
        padding: 2rem 2.5rem 5rem !important;
        max-width: 1180px !important;
    }

    h1, h2 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        color: var(--txt-1) !important;
        letter-spacing: -0.02em !important;
    }
    h2 { font-size: 1.05rem !important; margin: 0.25rem 0 1rem !important; }
    h3, h4 {
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        color: var(--txt-3) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        margin-bottom: 0.8rem !important;
    }

    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--border-md); border-radius: 99px; }

    div[data-testid="metric-container"] {
        background: #FFFFFF !important;
        border: 1px solid #E4E2DC !important;
        border-radius: 16px !important;
        padding: 18px 20px 16px !important;
        transition: border-color 0.15s;
    }
    div[data-testid="metric-container"]:hover { border-color: #D0CEC7 !important; }
    div[data-testid="metric-container"] * { opacity: 1 !important; visibility: visible !important; }
    div[data-testid="metric-container"] label,
    div[data-testid="metric-container"] [data-testid="stMetricLabel"],
    div[data-testid="metric-container"] [data-testid="stMetricLabel"] p,
    div[data-testid="metric-container"] [data-testid="stMetricLabel"] span,
    div[data-testid="metric-container"] [data-testid="stMetricLabel"] div {
        font-size: 0.68rem !important; font-weight: 600 !important;
        text-transform: uppercase !important; letter-spacing: 0.09em !important;
        color: #71717A !important; opacity: 1 !important; visibility: visible !important;
    }
    div[data-testid="metric-container"] [data-testid="stMetricValue"],
    div[data-testid="metric-container"] [data-testid="stMetricValue"] > div,
    div[data-testid="metric-container"] [data-testid="stMetricValue"] p,
    div[data-testid="metric-container"] [data-testid="stMetricValue"] span,
    div[data-testid="metric-container"] [data-testid="stMetricValue"] div,
    div[data-testid="metric-container"] [data-testid="stMetricValue"] > div > div {
        font-size: 1.5rem !important; font-weight: 700 !important;
        color: #18181B !important; letter-spacing: -0.02em !important;
        line-height: 1.2 !important; opacity: 1 !important; visibility: visible !important;
    }
    div[data-testid="metric-container"] [data-testid="stMetricDelta"],
    div[data-testid="metric-container"] [data-testid="stMetricDelta"] p,
    div[data-testid="metric-container"] [data-testid="stMetricDelta"] span,
    div[data-testid="metric-container"] [data-testid="stMetricDelta"] div {
        font-size: 0.72rem !important; color: #16A34A !important;
        opacity: 1 !important; visibility: visible !important;
    }
    div[data-testid="metric-container"] [data-testid="stMetricDelta"] svg { display: none !important; }
    div[data-testid="metric-container"] [style*="color"],
    div[data-testid="metric-container"] [style*="opacity"] { color: inherit !important; opacity: 1 !important; }

    hr { border: none !important; border-top: 1px solid var(--border) !important; margin: 1.75rem 0 !important; }

    div[data-testid="stExpander"] {
        background: var(--card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    div[data-testid="stExpander"] summary {
        font-size: 0.85rem !important; font-weight: 500 !important;
        color: var(--txt-2) !important; padding: 12px 16px !important;
        background: var(--card) !important;
    }

    div[data-testid="stFileUploader"] > div {
        background: var(--card) !important;
        border: 1.5px dashed var(--border-md) !important;
        border-radius: 14px !important; padding: 2rem 1rem !important;
        transition: border-color 0.2s, background 0.2s !important;
    }
    div[data-testid="stFileUploader"] > div:hover {
        border-color: var(--accent) !important; background: var(--accent-bg) !important;
    }
    div[data-testid="stFileUploader"] label {
        font-weight: 500 !important; color: var(--txt-2) !important; font-size: 0.9rem !important;
    }

    div[data-testid="stTabs"] [role="tablist"] {
        background: #EEECEA !important; border-radius: 10px !important;
        padding: 3px !important; border-bottom: none !important; gap: 2px !important;
    }
    div[data-testid="stTabs"] [role="tab"] {
        border-radius: 8px !important; font-size: 0.8rem !important; font-weight: 500 !important;
        color: var(--txt-2) !important; padding: 6px 16px !important;
        border: none !important; transition: color 0.15s !important;
    }
    div[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        background: var(--card) !important; color: var(--txt-1) !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.07) !important;
    }
    div[data-testid="stTabs"] [role="tabpanel"] { padding-top: 1rem !important; }

    div[data-testid="stDataFrame"] {
        border-radius: 12px !important; border: 1px solid var(--border) !important; overflow: hidden !important;
    }

    div[data-testid="stDownloadButton"] button {
        background: var(--txt-1) !important; color: #FFFFFF !important;
        border: none !important; border-radius: 10px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 600 !important;
        font-size: 0.83rem !important; padding: 0.55rem 1.5rem !important;
        letter-spacing: 0.01em !important; transition: background 0.15s !important;
    }
    div[data-testid="stDownloadButton"] button:hover { background: #3F3F46 !important; }

    div[data-testid="stTextInput"] input {
        border-radius: 10px !important; border: 1px solid var(--border) !important;
        background: var(--card) !important; font-size: 0.87rem !important;
        padding: 10px 14px !important; color: var(--txt-1) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        transition: border-color 0.15s, box-shadow 0.15s !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: var(--accent) !important; box-shadow: 0 0 0 3px rgba(79,70,229,0.1) !important;
    }

    div[data-testid="stAlert"] { border-radius: 12px !important; font-size: 0.87rem !important; }

    /* ── Hero ── */
    .hero-wrap {
        background: var(--card); border: 1px solid var(--border);
        border-radius: 20px; padding: 2rem 2.25rem 1.8rem;
        margin-bottom: 1.5rem; position: relative; overflow: hidden;
    }
    .hero-wrap::before {
        content: ''; position: absolute; top: 0; right: 0;
        width: 320px; height: 100%;
        background: radial-gradient(ellipse at top right, #EEF2FF 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-eyebrow {
        font-size: 0.68rem; font-weight: 600; text-transform: uppercase;
        letter-spacing: 0.12em; color: var(--accent); margin-bottom: 10px;
    }
    .hero-title {
        font-size: 1.9rem; font-weight: 700; color: var(--txt-1);
        line-height: 1.15; margin-bottom: 10px; letter-spacing: -0.025em;
    }
    .hero-sub { font-size: 0.92rem; color: var(--txt-2); line-height: 1.7; max-width: 520px; }
    .hero-tip {
        font-size: 0.8rem; color: var(--amber); font-weight: 500;
        margin-top: 8px; display: flex; align-items: center; gap: 6px;
    }
    .hero-badges { display: flex; gap: 8px; margin-top: 1.2rem; flex-wrap: wrap; }
    .hero-badge {
        background: var(--bg); border: 1px solid var(--border); border-radius: 99px;
        padding: 4px 12px; font-size: 0.73rem; font-weight: 500;
        color: var(--txt-2); letter-spacing: 0.01em;
    }

    /* ── Section heads ── */
    .sec-head { display: flex; align-items: center; gap: 10px; margin: 0.25rem 0 1.1rem; }
    .sec-head-icon {
        width: 30px; height: 30px; background: var(--accent-bg); border-radius: 8px;
        display: flex; align-items: center; justify-content: center; font-size: 15px; flex-shrink: 0;
    }
    .sec-head-text { font-size: 1rem; font-weight: 700; color: var(--txt-1); letter-spacing: -0.015em; }

    /* ── Insight cards ── */
    .insight-card {
        background: var(--card); border: 1px solid var(--border);
        border-left: 3px solid var(--accent); border-radius: 0 12px 12px 0;
        padding: 13px 18px; margin-bottom: 9px; font-size: 0.875rem;
        color: var(--txt-2); line-height: 1.65;
    }
    .insight-card strong, .insight-card b { color: var(--txt-1); font-weight: 600; }
    .insight-card.warning { border-left-color: var(--red); background: var(--red-bg); }
    .insight-card.warning strong, .insight-card.warning b { color: #991B1B; }
    .insight-card.good { border-left-color: var(--green); background: var(--green-bg); }
    .insight-card.good strong, .insight-card.good b { color: #14532D; }

    /* ── Score card ── */
    .score-card {
        background: var(--card); border: 1px solid var(--border); border-radius: 16px;
        padding: 20px 24px; margin-bottom: 1rem;
    }
    .score-title { font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.09em; color: var(--txt-3); margin-bottom: 8px; }
    .score-value { font-size: 2rem; font-weight: 700; color: var(--txt-1); letter-spacing: -0.03em; }
    .score-bar-bg { background: #E4E2DC; border-radius: 99px; height: 8px; margin: 10px 0; }
    .score-bar-fill { height: 8px; border-radius: 99px; transition: width 0.4s; }
    .score-bullets { font-size: 0.82rem; color: var(--txt-2); line-height: 1.8; margin-top: 8px; }

    /* ── Top txn rows ── */
    .top-txn {
        display: flex; align-items: center; justify-content: space-between;
        background: var(--card); border: 1px solid var(--border); border-radius: 12px;
        padding: 11px 16px; margin-bottom: 7px; font-size: 0.875rem;
        color: var(--txt-2); transition: border-color 0.15s;
    }
    .top-txn:hover { border-color: var(--border-md); }
    .top-txn .left { display: flex; align-items: center; gap: 10px; min-width: 0; }
    .top-txn .cat-badge {
        display: inline-block; background: var(--accent-bg); color: #3730A3;
        border-radius: 6px; padding: 3px 9px; font-size: 0.7rem; font-weight: 600;
        white-space: nowrap; letter-spacing: 0.02em; flex-shrink: 0;
    }
    .top-txn .desc {
        color: var(--txt-1); font-weight: 500; white-space: nowrap;
        overflow: hidden; text-overflow: ellipsis;
    }
    .top-txn .amount {
        font-weight: 700; font-size: 0.95rem; color: var(--red);
        white-space: nowrap; margin-left: 16px; flex-shrink: 0;
    }

    /* ── Fix My Data section ── */
    .fix-card {
        background: var(--card); border: 1px solid var(--border); border-radius: 12px;
        padding: 12px 16px; margin-bottom: 8px;
    }
    .fix-desc { font-size: 0.875rem; font-weight: 500; color: var(--txt-1); margin-bottom: 2px; }
    .fix-amount { font-size: 0.8rem; color: var(--red); font-weight: 600; }

    .info-strip {
        background: var(--accent-bg); border: 1px solid #C7D2FE; border-radius: 10px;
        padding: 10px 16px; font-size: 0.83rem; color: #3730A3; font-weight: 500;
        margin-bottom: 1rem; display: flex; align-items: center; gap: 8px;
    }

    .empty-state {
        text-align: center; padding: 5rem 2rem; background: var(--card);
        border: 1.5px dashed var(--border-md); border-radius: 20px; margin-top: 1rem;
    }
    .empty-state .icon { font-size: 2.25rem; margin-bottom: 14px; }
    .empty-state .title { font-size: 1.05rem; font-weight: 700; color: var(--txt-1); margin-bottom: 8px; letter-spacing: -0.01em; }
    .empty-state .sub { font-size: 0.85rem; color: var(--txt-3); }

    .chart-card { background: var(--card); border: 1px solid var(--border); border-radius: 14px; padding: 1.25rem 1.4rem 1rem; }
    .chart-title { font-size: 0.72rem; font-weight: 600; color: var(--txt-3); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 14px; }

    .footer-note {
        text-align: center; font-size: 0.75rem; color: var(--txt-3);
        margin-top: 2.5rem; padding-top: 1.5rem; border-top: 1px solid var(--border); letter-spacing: 0.01em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────

# All valid spending categories — UPI removed as a category
CATEGORIES = [
    "Food", "Travel", "Shopping", "Bills", "Rent",
    "Entertainment", "Own Account Transfer", "Sent to Others",
    "Health", "Groceries", "Petrol", "Recharge", "Salary", "Others",
]

# Categories shown in the "Fix My Data" dropdown (exclude system categories)
FIX_CATEGORIES = [
    "Food", "Travel", "Shopping", "Bills", "Rent",
    "Entertainment", "Sent to Others", "Health", "Groceries",
    "Petrol", "Recharge", "Others",
]

# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown(
    """
    <div class="hero-wrap">
        <div class="hero-eyebrow">Personal Finance · HDFC Bank</div>
        <div class="hero-title">💸 Where Did My Salary Go?</div>
        <div class="hero-sub">
            Analyze your HDFC bank statement with smart UPI parsing, salary detection, and accurate expense tracking.
        </div>
        <div class="hero-tip">
            💡 Tip: For best results, categorize uncategorized transactions using Fix My Data below.
        </div>
        <div class="hero-badges">
            <span class="hero-badge">🔒 Processed locally</span>
            <span class="hero-badge">🏦 Optimized for HDFC</span>
            <span class="hero-badge">🔄 Self-transfer detection</span>
            <span class="hero-badge">📊 Smart insights</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.info("Optimized for HDFC bank statements. Supports .xls and .xlsx exports from HDFC NetBanking.")

with st.expander("📋 How to export your HDFC statement as Excel", expanded=False):
    st.markdown(
        """
        1. Login to **HDFC NetBanking** or the Mobile App.
        2. Go to **Account Statement / Transaction History**.
        3. Set your desired **date range** (e.g., last 3 months).
        4. Click **Download / Export** and choose **Excel (.xls / .xlsx)**.
        5. Upload the file below — that's it!
        """
    )

st.markdown(
    '<div class="info-strip">📁 &nbsp;Supports <strong>.xls</strong> and <strong>.xlsx</strong> exported directly from HDFC NetBanking or Mobile Banking.</div>',
    unsafe_allow_html=True,
)
uploaded_file = st.file_uploader(
    "Drop your HDFC statement here or click to browse",
    type=["xls", "xlsx"],
    help="Your file is processed locally and never stored.",
    label_visibility="visible",
)


# ─────────────────────────────────────────────
#  HELPER UTILITIES
# ─────────────────────────────────────────────

def normalize_header(value: str) -> str:
    """Lowercase + strip punctuation for fuzzy column matching."""
    if value is None:
        return ""
    return re.sub(r"[^a-z0-9]+", " ", str(value).strip().lower())


def parse_amount(value) -> float | None:
    """Safely parse an amount string to float, returning None on failure."""
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


def fmt(amount: float) -> str:
    """Format a float as ₹ with Indian comma notation."""
    return f"₹{amount:,.0f}"


def find_header_row(df: pd.DataFrame) -> int | None:
    """
    Scan rows top-to-bottom until we find one that looks like a statement header
    (contains date + description columns, ideally also an amount column).
    """
    date_kw   = {"date", "txn date", "transaction date", "value date"}
    desc_kw   = {"narration", "description", "particulars", "remarks", "transaction description"}
    amount_kw = {"withdrawal", "deposit", "debit", "credit", "dr", "cr",
                 "withdrawal amt", "deposit amt", "amount", "amt"}

    for idx, row in df.iterrows():
        normalized = {normalize_header(x) for x in row}
        has_date   = bool(normalized & date_kw)
        has_desc   = bool(normalized & desc_kw)
        has_amount = bool(normalized & amount_kw)
        if has_date and has_desc and has_amount:
            return idx
    # Fallback — accept header without explicit amount keyword
    for idx, row in df.iterrows():
        normalized = {normalize_header(x) for x in row}
        if (normalized & date_kw) and (normalized & desc_kw):
            return idx
    return None


def read_hdfc_statement(file) -> tuple[pd.DataFrame | None, str | None]:
    """
    Read an HDFC Excel export and return (DataFrame, error_message).
    Returns (None, error) on failure.
    """
    try:
        df = pd.read_excel(file, header=None, dtype=str, sheet_name=0)
    except Exception as exc:
        return None, f"Could not read the Excel file: {exc}"

    header_row = find_header_row(df)
    if header_row is None:
        return None, (
            "Could not find the statement header row. "
            "Make sure the file has a row with Date and Narration / Description columns."
        )

    header = [str(x).strip() if x else "" for x in df.iloc[header_row]]
    data   = df.iloc[header_row + 1:].reset_index(drop=True)
    data.columns = header

    data = data.loc[:, data.columns.notna()]
    data = data[~data.apply(lambda r: r.astype(str).str.strip().eq("").all(), axis=1)]
    return data, None


# ─────────────────────────────────────────────
#  UPI NARRATION PARSER
# ─────────────────────────────────────────────

_UPI_PIPE_RE = re.compile(r"UPI[/-](?:DR|CR)?[/-]?\d*[/-]?([^/@\-]+)", re.IGNORECASE)
_UPI_AT_RE   = re.compile(r"([a-zA-Z0-9._]+)@([a-zA-Z]+)")
_UPI_DASH_RE = re.compile(r"UPI-([^-]+)-", re.IGNORECASE)


def parse_upi_narration(narration: str) -> dict:
    """
    Extract structured info from a UPI / NEFT narration string.
    Returns dict with: merchant, upi_id, clean (readable label).
    """
    text     = str(narration).strip()
    merchant = None
    upi_id   = None

    vpa_match = _UPI_AT_RE.search(text)
    if vpa_match:
        upi_id   = vpa_match.group(0).lower()
        raw_name = vpa_match.group(1)
        raw_name = re.sub(r"\d{4,}$", "", raw_name)
        merchant = raw_name.replace(".", " ").replace("_", " ").title().strip()

    if not merchant:
        m = _UPI_PIPE_RE.search(text)
        if m:
            candidate = m.group(1).strip()
            if len(candidate) > 2 and not candidate.isdigit():
                merchant = candidate.title()

    if not merchant:
        m = _UPI_DASH_RE.search(text)
        if m:
            candidate = m.group(1).strip()
            if len(candidate) > 2 and not candidate.isdigit():
                merchant = candidate.title()

    if merchant:
        clean = merchant
    elif upi_id:
        clean = upi_id
    else:
        clean = re.sub(
            r"\b(UPI|NEFT|IMPS|REF|NO|DR|CR|BY|TO|FROM|TRANSFER|PAYMENT|TXN|ID)\b",
            "", text, flags=re.IGNORECASE,
        )
        clean = re.sub(r"\d{6,}", "", clean)
        clean = re.sub(r"[/\-]+", " ", clean)
        clean = re.sub(r"\s+", " ", clean).strip()

    return {"merchant": merchant, "upi_id": upi_id, "clean": clean or text}


# ─────────────────────────────────────────────
#  SELF-TRANSFER DETECTION
# ─────────────────────────────────────────────

_SELF_TRANSFER_KW = [
    "self", "own account", "own transfer", "self transfer",
    "neft to self", "imps to self", "transfer to self",
]
_OWN_BANK_KW = [
    "hdfc bank fd", "fd creation", "sweep in", "sweep out",
    "internal transfer", "auto sweep", "rd instalment",
    "emi payment hdfc", "hdfc rd",
]


def detect_self_transfer(narration: str, user_name: str = "") -> bool:
    """
    Return True if the transaction looks like a transfer to the user's own account.
    Checks self-transfer keywords, own-bank patterns, and optionally the user's name in UPI narrations.
    """
    text = str(narration).lower()

    if any(kw in text for kw in _SELF_TRANSFER_KW):
        return True
    if any(kw in text for kw in _OWN_BANK_KW):
        return True
    if user_name:
        name_parts = [p.lower() for p in user_name.split() if len(p) > 2]
        if name_parts and "upi" in text:
            if sum(1 for part in name_parts if part in text) >= 2:
                return True
    return False


# ─────────────────────────────────────────────
#  SALARY DETECTION
# ─────────────────────────────────────────────

_SALARY_KW = [
    "salary", "sal ", "sal/", "sal-", "payroll", "stipend",
    "monthly pay", "ctc", "emolument", "wages", "neft cr", "neft-cr",
]
_EMPLOYER_KW = [
    "pvt ltd", "private limited", "technologies", "solutions", "infosys",
    "tcs", "wipro", "hcl", "accenture", "cognizant", "capgemini",
    "ltd ", "llp", "inc ", "corp",
]


def detect_salary(narration: str, amount: float) -> bool:
    """
    Return True if this credit transaction looks like a salary payment.
    Uses keyword matching and NEFT credit heuristics with employer signals.
    """
    text = str(narration).lower()
    if any(kw in text for kw in _SALARY_KW):
        return True
    if amount >= 5000 and ("neft" in text or "imps" in text):
        if any(kw in text for kw in _EMPLOYER_KW):
            return True
    return False


# ─────────────────────────────────────────────
#  CATEGORIZATION
# ─────────────────────────────────────────────

def categorize_transaction(description: str, merchant: str = "") -> str:
    """
    Categorize a transaction based on description and merchant name.
    NOTE: UPI is a payment method — it is NOT used as a category.
    Instead, UPI transactions are classified into proper spending categories.
    Returns one of the CATEGORIES constants.
    """
    text = (str(description) + " " + str(merchant)).lower()

    # ── Salary / Income ──────────────────────────────────────────────
    if any(w in text for w in ["salary", "sal credit", "payroll", "neft cr", "stipend"]):
        return "Salary"

    # ── Rent ─────────────────────────────────────────────────────────
    if any(w in text for w in ["rent", "house rent", "rental", "pg rent", "hostel"]):
        return "Rent"

    # ── Food & Dining ────────────────────────────────────────────────
    if any(w in text for w in [
        "swiggy", "zomato", "eatsure", "dominos", "mcdonald", "kfc", "subway",
        "burger king", "barbeque", "cafe", "restaurant", "dining", "hotel bill",
        "food", "biryani", "pizza", "chai", "bakery", "eatclub", "freshmenu",
        "box8", "behrouz", "lunchbox",
    ]):
        return "Food"

    # ── Travel ───────────────────────────────────────────────────────
    if any(w in text for w in [
        "uber", "ola", "rapido", "irctc", "railways", "indigo", "air india",
        "spicejet", "goibibo", "makemytrip", "redbus", "flight", "train",
        "metro", "bus", "taxi", "cab", "toll", "yatra", "cleartrip",
        "abhibus", "ixigo",
    ]):
        return "Travel"

    # ── Petrol / Fuel ────────────────────────────────────────────────
    if any(w in text for w in [
        "petrol", "fuel", "bharat petroleum", "bpcl", "iocl", "hpcl",
        "indianoil", "hp petrol", "reliance petrol", "essar",
    ]):
        return "Petrol"

    # ── Shopping ─────────────────────────────────────────────────────
    if any(w in text for w in [
        "amazon", "flipkart", "myntra", "ajio", "meesho", "nykaa",
        "tatacliq", "snapdeal", "shopsy", "shopping", "paytm mall",
        "paytmqr", "croma", "reliance digital", "vijay sales",
    ]):
        return "Shopping"

    # ── Groceries ────────────────────────────────────────────────────
    if any(w in text for w in [
        "bigbasket", "blinkit", "zepto", "jiomart", "dmart", "reliance fresh",
        "more supermarket", "grofer", "grocery", "supermarket", "dunzo",
        "milkbasket", "supr daily",
    ]):
        return "Groceries"

    # ── Bills & Utilities ────────────────────────────────────────────
    if any(w in text for w in [
        "electricity", "water bill", "gas bill", "bsnl", "jio", "airtel",
        "vi ", "vodafone", "idea", "broadband", "internet", "lic", "insurance",
        "municipal", "bbmp", "maintenance", "society", "tata power",
        "bescom", "msedcl", "mahadiscom", "bwssb",
    ]):
        return "Bills"

    # ── Entertainment ─────────────────────────────────────────────────
    if any(w in text for w in [
        "netflix", "hotstar", "amazon prime", "jiocinema", "zee5", "sonyliv",
        "spotify", "gaana", "youtube premium", "apple music",
        "movie", "cinema", "pvr", "inox", "multiplex", "gaming",
        "bookmyshow", "district", "playstation", "steam",
    ]):
        return "Entertainment"

    # ── Health & Pharmacy ─────────────────────────────────────────────
    if any(w in text for w in [
        "apollo", "medplus", "netmeds", "1mg", "pharmeasy", "pharmacy",
        "medical", "hospital", "clinic", "doctor", "health", "tata 1mg",
        "practo", "cult.fit", "cultfit",
    ]):
        return "Health"

    # ── Recharge / Wallet ─────────────────────────────────────────────
    if any(w in text for w in [
        "recharge", "topup", "mobikwik", "paytm", "phonepe wallet", "freecharge",
    ]):
        return "Recharge"

    # ── Sent to Others (personal UPI transfer, not a merchant) ────────
    # UPI to a person: VPA looks personal (no business keywords present)
    if "upi" in text:
        biz_signals = [
            "store", "shop", "mart", "pay", "tech", "service", "pvt", "ltd",
            "foods", "cafe", "kitchen", "delivery", "enterprise", "trading",
        ]
        if merchant and not any(b in merchant.lower() for b in biz_signals):
            name_parts = [p for p in merchant.split() if len(p) > 2]
            if len(name_parts) >= 1:
                return "Sent to Others"
        # Fall through — UPI transactions that don't match any merchant heuristic
        # will land in Others so the user can Fix My Data them correctly.

    return "Others"


# ─────────────────────────────────────────────
#  SMART INSIGHTS
# ─────────────────────────────────────────────

def calculate_insights(
    expense_df: pd.DataFrame,
    total_spend: float,
    total_credit: float,
    salary_received: float,
    self_transfer_amt: float,
) -> list[dict]:
    """
    Generate actionable, specific insights based on the user's spending patterns.
    Returns a list of dicts with 'text' and 'kind' keys (kind: warning | good | info).
    """
    insights = []
    if total_spend == 0:
        return insights

    cat_totals = expense_df.groupby("Category")["Debit"].sum().sort_values(ascending=False)
    cat_totals = cat_totals[cat_totals.index != "Salary"]
    if cat_totals.empty:
        return insights

    others_pct = cat_totals.get("Others", 0) / total_spend * 100
    food_spend = cat_totals.get("Food", 0)

    # 1 — High uncategorized spending
    if others_pct > 30:
        insights.append({
            "text": (
                f"Most of your spending ({others_pct:.1f}%) is uncategorized. "
                "Use <strong>Fix My Data</strong> below to improve insights."
            ),
            "kind": "warning",
        })

    # 2 — High food spend
    if total_spend > 0 and food_spend / total_spend > 0.25:
        insights.append({
            "text": (
                f"Food spending is high ({food_spend / total_spend * 100:.1f}% of total). "
                "Consider reducing online orders."
            ),
            "kind": "info",
        })

    # 3 — Spending exceeds income
    if total_spend > total_credit:
        insights.append({
            "text": "Your spending exceeds your income. Check discretionary expenses like Entertainment or Shopping.",
            "kind": "warning",
        })

    # 4 — Own account transfers excluded
    if self_transfer_amt > 0:
        insights.append({
            "text": f"₹{self_transfer_amt:,.0f} excluded as own account transfers for accuracy.",
            "kind": "good",
        })

    # 5 — Savings rate
    if salary_received > 0:
        savings_rate = (salary_received - total_spend) / salary_received * 100
        if savings_rate < 20:
            insights.append({
                "text": (
                    f"Savings rate is {savings_rate:.1f}%. "
                    "Aim for at least 20% by cutting back on high-spend categories."
                ),
                "kind": "info",
            })

    return insights


# ─────────────────────────────────────────────
#  SPENDING HEALTH SCORE
# ─────────────────────────────────────────────

def compute_score(
    expense_df: pd.DataFrame,
    total_spend: float,
    total_credit: float,
    salary_received: float,
) -> tuple[int, list[str]]:
    """
    Compute a Spending Health Score (0–100) and return (score, explanation_bullets).
    Deductions:
      - Others > 30%  → -20
      - Food > 30%    → -10
      - Spend > income → -20
      - Savings rate < 20% → -10
    """
    score        = 100
    explanations = []

    if total_spend == 0:
        return score, ["Not enough data to compute a score."]

    cat_totals  = expense_df.groupby("Category")["Debit"].sum()
    others_pct  = cat_totals.get("Others", 0) / total_spend * 100
    food_pct    = cat_totals.get("Food", 0) / total_spend * 100

    if others_pct > 30:
        score -= 20
        explanations.append(f"High uncategorized spending ({others_pct:.1f}%)")
    if food_pct > 30:
        score -= 10
        explanations.append(f"High food expenses ({food_pct:.1f}% of spend)")
    if total_spend > total_credit:
        score -= 20
        explanations.append("Spending exceeds total income")
    if salary_received > 0:
        savings_rate = (salary_received - total_spend) / salary_received * 100
        if savings_rate < 20:
            score -= 10
            explanations.append(f"Low savings rate ({savings_rate:.1f}%)")

    if not explanations:
        explanations.append("Good spending habits — keep it up!")

    return max(0, score), explanations


# ─────────────────────────────────────────────
#  MAIN ANALYSIS — runs only when file uploaded
# ─────────────────────────────────────────────

if uploaded_file:
    statement_df, error = read_hdfc_statement(uploaded_file)

    if error:
        st.error(f"❌ {error}")
        st.info(
            "**Tip:** Make sure the file is an HDFC statement exported directly from NetBanking "
            "and not a manually edited spreadsheet."
        )
        st.stop()

    if statement_df is None or statement_df.empty:
        st.error("The file was parsed but no transaction rows were found. Please check the file.")
        st.stop()

    with st.expander("⚙️ Optional: Enter your name to improve self-transfer detection", expanded=False):
        user_name = st.text_input(
            "Your name (as it appears in UPI narrations)",
            placeholder="e.g. Rahul Sharma",
            help="Used only to detect transfers to your own account. Never stored.",
        ).strip()

    # ── Column detection ─────────────────────────────────────────────
    df = statement_df.copy()
    df.columns = [str(c).strip() for c in df.columns]

    date_col       = next((c for c in df.columns if "date"       in normalize_header(c)), None)
    desc_col       = next((c for c in df.columns if any(k in normalize_header(c) for k in
                           ["narration", "description", "particulars", "remarks"])), None)
    withdrawal_col = next((c for c in df.columns if "withdrawal" in normalize_header(c)), None)
    deposit_col    = next((c for c in df.columns if "deposit"    in normalize_header(c)), None)

    if not desc_col:
        st.error("Could not find a **Narration / Description** column in your statement.")
        st.stop()
    if not withdrawal_col and not deposit_col:
        st.error("Could not find **Withdrawal** or **Deposit** columns. Please use a full HDFC account statement.")
        st.stop()

    # ── Amount parsing ────────────────────────────────────────────────
    df["Withdrawal"] = (df[withdrawal_col].apply(parse_amount) if withdrawal_col else 0.0)
    df["Deposit"]    = (df[deposit_col].apply(parse_amount)    if deposit_col    else 0.0)
    df["Withdrawal"] = pd.to_numeric(df["Withdrawal"], errors="coerce").fillna(0.0)
    df["Deposit"]    = pd.to_numeric(df["Deposit"],    errors="coerce").fillna(0.0)
    df["Debit"]      = df["Withdrawal"].abs()
    df["Credit"]     = df["Deposit"].abs()
    df["Type"]       = df.apply(
        lambda r: "Debit" if r["Debit"] > 0 else ("Credit" if r["Credit"] > 0 else "Other"), axis=1
    )
    df["Description"] = df[desc_col].fillna("") if desc_col else ""

    # ── UPI Intelligence ──────────────────────────────────────────────
    upi_parsed       = df["Description"].apply(parse_upi_narration)
    df["Merchant"]   = upi_parsed.apply(lambda x: x["merchant"] or "")
    df["UPI_ID"]     = upi_parsed.apply(lambda x: x["upi_id"]   or "")
    df["CleanLabel"] = upi_parsed.apply(lambda x: x["clean"])

    # ── Self-transfer detection ───────────────────────────────────────
    df["IsSelfTransfer"] = df["Description"].apply(
        lambda d: detect_self_transfer(d, user_name)
    )

    # ── Salary detection (credits only) ──────────────────────────────
    df["IsSalary"] = df.apply(
        lambda r: detect_salary(r["Description"], r["Credit"]) if r["Credit"] > 0 else False,
        axis=1,
    )

    # ── Categorization — UPI is NOT a category ───────────────────────
    df["Category"] = df.apply(
        lambda r: categorize_transaction(r["Description"], r["Merchant"]), axis=1
    )
    # Override: salary credits always get Salary category
    df.loc[df["IsSalary"], "Category"] = "Salary"
    # Override: self-transfers always get Own Account Transfer category
    df.loc[df["IsSelfTransfer"], "Category"] = "Own Account Transfer"

    # ── Expense dataframe (debits, excluding self-transfers) ──────────
    # This is the single source of truth for all spending metrics
    expense_df = df[(df["Debit"] > 0) & (~df["IsSelfTransfer"])].copy()

    # ── Apply any user category corrections from session state ────────
    if "category_updates" not in st.session_state:
        st.session_state.category_updates = {}
    for idx, new_cat in st.session_state.category_updates.items():
        if idx in expense_df.index:
            expense_df.at[idx, "Category"] = new_cat

    # ── Aggregate metrics ─────────────────────────────────────────────
    total_spend       = expense_df["Debit"].sum()
    total_credit      = df["Credit"].sum()
    salary_received   = df[df["IsSalary"]]["Credit"].sum()
    self_transfer_amt = df[df["IsSelfTransfer"]]["Debit"].sum()
    net_savings       = total_credit - total_spend - self_transfer_amt

    # ════════════════════════════════════════════
    #  SECTION 1 – OVERVIEW METRICS
    # ════════════════════════════════════════════
    st.markdown(
        '<div class="sec-head"><div class="sec-head-icon">📊</div><div class="sec-head-text">Overview</div></div>',
        unsafe_allow_html=True,
    )
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Spent",           fmt(total_spend),
              help="Debit transactions excluding own account transfers")
    m2.metric("Total Credited",        fmt(total_credit))
    m3.metric("Salary Received",       fmt(salary_received) if salary_received else "—")
    m4.metric(
        "Net Savings",
        fmt(net_savings),
        delta=f"{net_savings / total_credit * 100:.1f}% savings rate" if total_credit else "",
    )
    m5.metric("Own Account Transfer",  fmt(self_transfer_amt),
              help="Excluded from spending — FD, RD, sweep, own-account moves")

    st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)
    st.markdown("---")

    # ════════════════════════════════════════════
    #  SECTION 2 – SMART INSIGHTS
    # ════════════════════════════════════════════
    st.markdown(
        '<div class="sec-head"><div class="sec-head-icon">🧠</div><div class="sec-head-text">Smart Insights</div></div>',
        unsafe_allow_html=True,
    )

    insights = calculate_insights(expense_df, total_spend, total_credit, salary_received, self_transfer_amt)
    for insight in insights:
        css_class = f"insight-card {insight['kind']}" if insight["kind"] != "info" else "insight-card"
        st.markdown(f'<div class="{css_class}">{insight["text"]}</div>', unsafe_allow_html=True)

    # ── Spending Health Score ─────────────────────────────────────────
    score, explanations = compute_score(expense_df, total_spend, total_credit, salary_received)
    score_color = "#16A34A" if score >= 75 else ("#D97706" if score >= 50 else "#DC2626")
    st.markdown(
        f"""
        <div class="score-card">
            <div class="score-title">Spending Health Score</div>
            <div class="score-value" style="color:{score_color}">💡 {score}/100</div>
            <div class="score-bar-bg">
                <div class="score-bar-fill" style="width:{score}%;background:{score_color}"></div>
            </div>
            <div class="score-bullets">
                {"".join(f"• {e}<br>" for e in explanations)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ════════════════════════════════════════════
    #  SECTION 3 – FIX MY DATA
    # ════════════════════════════════════════════
    st.markdown(
        '<div class="sec-head"><div class="sec-head-icon">🛠</div><div class="sec-head-text">Fix My Data (Improve Accuracy)</div></div>',
        unsafe_allow_html=True,
    )

    others_df = expense_df[expense_df["Category"] == "Others"].copy()

    if others_df.empty:
        st.success("✅ No uncategorized transactions found. Your data is well-categorized!")
    else:
        st.markdown(
            f"**{len(others_df)} transactions** are labeled as *Others*. "
            "Update their categories below to improve your charts and insights.",
        )
        st.markdown("<div style='margin-bottom:0.5rem'></div>", unsafe_allow_html=True)

        changed = False
        for idx, row in others_df.iterrows():
            desc  = row["CleanLabel"] or str(row["Description"])
            short = desc[:55] + ("…" if len(desc) > 55 else "")
            c1, c2, c3 = st.columns([4, 3, 1])
            with c1:
                st.markdown(f'<div class="fix-desc">{short}</div>', unsafe_allow_html=True)
            with c2:
                current = st.session_state.category_updates.get(idx, "Others")
                selected = st.selectbox(
                    "Category",
                    FIX_CATEGORIES,
                    index=FIX_CATEGORIES.index(current) if current in FIX_CATEGORIES else len(FIX_CATEGORIES) - 1,
                    key=f"fix_{idx}",
                    label_visibility="collapsed",
                )
                if selected != current:
                    st.session_state.category_updates[idx] = selected
                    changed = True
            with c3:
                st.markdown(f'<div class="fix-amount">₹{row["Debit"]:,.0f}</div>', unsafe_allow_html=True)

        if changed:
            st.rerun()

        if st.button("♻️ Reset All Category Edits"):
            st.session_state.category_updates = {}
            st.rerun()

    # Top 3 largest expenses
    st.markdown("---")
    st.markdown(
        '<p style="font-size:0.72rem;font-weight:600;text-transform:uppercase;letter-spacing:0.09em;color:#A1A1AA;margin:1.4rem 0 0.7rem">Top 3 Largest Expenses</p>',
        unsafe_allow_html=True,
    )
    top3 = expense_df.nlargest(3, "Debit")[["CleanLabel", "Description", "Debit", "Category"]]
    rank_accent = ["#4F46E5", "#DC2626", "#D97706"]
    for i, (_, row) in enumerate(top3.iterrows()):
        label = row["CleanLabel"] or str(row["Description"])
        label_short = label[:62] + ("…" if len(label) > 62 else "")
        st.markdown(
            f'<div class="top-txn">'
            f'<div class="left">'
            f'<span style="font-size:0.8rem;font-weight:700;color:{rank_accent[i]};min-width:20px">#{i+1}</span>'
            f'<span class="cat-badge">{row["Category"]}</span>'
            f'<span class="desc">{label_short}</span>'
            f'</div>'
            f'<span class="amount">{fmt(row["Debit"])}</span>'
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ════════════════════════════════════════════
    #  SECTION 4 – CATEGORY BREAKDOWN
    # ════════════════════════════════════════════
    st.markdown(
        '<div class="sec-head"><div class="sec-head-icon">🗂</div><div class="sec-head-text">Expense Breakdown</div></div>',
        unsafe_allow_html=True,
    )

    cat_summary = expense_df.groupby("Category")["Debit"].sum().sort_values(ascending=False)
    cat_summary = cat_summary[cat_summary > 0]

    PALETTE = [
        "#4F46E5", "#DC2626", "#D97706", "#16A34A", "#0284C7",
        "#9333EA", "#DB2777", "#0D9488", "#EA580C", "#6366F1", "#71717A",
    ]

    col_bar, col_pie = st.columns([3, 2], gap="medium")

    with col_bar:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig_bar, ax_bar = plt.subplots(figsize=(7, max(3.2, len(cat_summary) * 0.52)))
        fig_bar.patch.set_facecolor("none")
        ax_bar.set_facecolor("none")
        ax_bar.set_title("SPENDING BY CATEGORY", fontsize=7.5, color="#A1A1AA",
                         fontweight="600", loc="left", pad=10)
        bars = ax_bar.barh(
            cat_summary.index[::-1], cat_summary.values[::-1],
            color=PALETTE[: len(cat_summary)][::-1], edgecolor="none", height=0.62,
        )
        for bar, val in zip(bars, cat_summary.values[::-1]):
            ax_bar.text(
                bar.get_width() + (cat_summary.values.max() * 0.01),
                bar.get_y() + bar.get_height() / 2,
                f"₹{val:,.0f}", va="center", ha="left", fontsize=8, color="#71717A",
            )
        ax_bar.set_xlabel("Amount (₹)", fontsize=8.5, color="#A1A1AA", labelpad=8)
        ax_bar.tick_params(axis="y", labelsize=9, colors="#18181B", pad=4)
        ax_bar.tick_params(axis="x", labelsize=8, colors="#A1A1AA")
        ax_bar.xaxis.set_major_formatter(mticker.FuncFormatter(
            lambda x, _: f"₹{x/1000:.0f}k" if x >= 1000 else f"₹{x:.0f}"
        ))
        for spine in ax_bar.spines.values():
            spine.set_visible(False)
        ax_bar.grid(axis="x", linestyle=":", alpha=0.3, color="#E4E2DC")
        ax_bar.set_xlim(right=cat_summary.values.max() * 1.22)
        fig_bar.tight_layout(pad=1.4)
        st.pyplot(fig_bar, use_container_width=True)
        plt.close(fig_bar)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_pie:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        total_pie = cat_summary.sum()
        n         = len(cat_summary)

        def _autopct(pct):
            return f"{pct:.0f}%" if pct >= 8 else ""

        fig_h = max(4.5, 4.0 + n * 0.18)
        fig_pie, ax_pie = plt.subplots(figsize=(4.6, fig_h))
        fig_pie.patch.set_facecolor("none")
        ax_pie.set_facecolor("none")
        ax_pie.set_title("SHARE OF SPENDING", fontsize=7.5, color="#A1A1AA",
                         fontweight="600", loc="left", pad=10)
        wedges, _, autotexts = ax_pie.pie(
            cat_summary.values, autopct=_autopct, pctdistance=0.70, startangle=140,
            wedgeprops=dict(width=0.52, edgecolor="#FFFFFF", linewidth=2.5),
            colors=PALETTE[:n],
            explode=[0.03 if v / total_pie < 0.05 else 0 for v in cat_summary.values],
        )
        for at in autotexts:
            at.set_fontsize(8.5)
            at.set_color("#FFFFFF")
            at.set_fontweight("700")

        legend_labels = [
            f"{c}  {v / total_pie * 100:.0f}%"
            for c, v in zip(cat_summary.index, cat_summary.values)
        ]
        ax_pie.legend(
            wedges, legend_labels,
            loc="lower center",
            bbox_to_anchor=(0.5, -0.02 - n * 0.048),
            ncol=2, fontsize=7.5, frameon=False,
            labelcolor="#52525B", handlelength=1.0, handleheight=0.85,
            borderpad=0, columnspacing=1.0,
        )
        fig_pie.subplots_adjust(bottom=0.05 + n * 0.05)
        fig_pie.tight_layout(pad=1.0)
        st.pyplot(fig_pie, use_container_width=True)
        plt.close(fig_pie)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='margin-top:0.75rem'></div>", unsafe_allow_html=True)
    with st.expander("📋 Full Category Breakdown Table", expanded=False):
        summary_table = cat_summary.reset_index()
        summary_table.columns = ["Category", "Total Spent"]
        summary_table["% of Spending"] = (summary_table["Total Spent"] / total_spend * 100).map("{:.1f}%".format)
        summary_table["Total Spent"]   = summary_table["Total Spent"].map(fmt)
        st.dataframe(summary_table, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ════════════════════════════════════════════
    #  SECTION 5 – MONTHLY TREND
    # ════════════════════════════════════════════
    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce", dayfirst=True)
        expense_df   = expense_df.copy()
        expense_df[date_col] = pd.to_datetime(expense_df[date_col], errors="coerce", dayfirst=True)

        if expense_df[date_col].notna().any():
            st.markdown(
                '<div class="sec-head"><div class="sec-head-icon">📅</div><div class="sec-head-text">Monthly Spend Trend</div></div>',
                unsafe_allow_html=True,
            )
            monthly = (
                expense_df.groupby(expense_df[date_col].dt.to_period("M"))["Debit"]
                .sum().sort_index().astype(float)
            )
            if len(monthly) > 1:
                fig_line, ax_line = plt.subplots(figsize=(10, 3.4))
                fig_line.patch.set_facecolor("#FFFFFF")
                ax_line.set_facecolor("#FFFFFF")
                ax_line.set_title("MONTHLY EXPENSES (OWN ACCOUNT TRANSFERS EXCLUDED)",
                                  fontsize=7.5, color="#A1A1AA", fontweight="600", loc="left", pad=10)
                x_labels = monthly.index.astype(str)
                ax_line.fill_between(x_labels, monthly.values, alpha=0.08, color="#4F46E5")
                ax_line.plot(
                    x_labels, monthly.values, color="#4F46E5", linewidth=2.2,
                    marker="o", markersize=5.5, markerfacecolor="#FFFFFF",
                    markeredgewidth=2, markeredgecolor="#4F46E5",
                )
                for x, y in zip(x_labels, monthly.values):
                    ax_line.annotate(
                        f"₹{y/1000:.1f}k" if y >= 1000 else f"₹{y:.0f}",
                        (x, y), textcoords="offset points", xytext=(0, 10),
                        ha="center", fontsize=7.5, color="#4F46E5", fontweight="600",
                    )
                ax_line.set_ylabel("Amount (₹)", fontsize=8.5, color="#A1A1AA", labelpad=8)
                ax_line.tick_params(axis="both", labelsize=8.5, colors="#71717A")
                ax_line.yaxis.set_major_formatter(mticker.FuncFormatter(
                    lambda x, _: f"₹{x/1000:.0f}k" if x >= 1000 else f"₹{x:.0f}"
                ))
                for spine in ax_line.spines.values():
                    spine.set_visible(False)
                ax_line.grid(axis="y", linestyle=":", alpha=0.3, color="#E4E2DC")
                ax_line.set_ylim(bottom=0, top=monthly.values.max() * 1.2)
                fig_line.set_edgecolor("#E4E2DC")
                fig_line.tight_layout(pad=1.4)
                st.pyplot(fig_line, use_container_width=True)
                plt.close(fig_line)
            else:
                st.info("Upload at least 2 months of data to see the trend chart.")
            st.markdown("---")

    # ════════════════════════════════════════════
    #  SECTION 6 – TRANSACTION DATA & DOWNLOAD
    # ════════════════════════════════════════════
    st.markdown(
        '<div class="sec-head"><div class="sec-head-icon">🗃</div><div class="sec-head-text">Transaction Data</div></div>',
        unsafe_allow_html=True,
    )

    # Default: clean table. Only show editable version when button clicked.
    if "edit_mode" not in st.session_state:
        st.session_state.edit_mode = False

    col_btn, _ = st.columns([1, 5])
    with col_btn:
        if st.button("✏️ Edit Transactions"):
            st.session_state.edit_mode = not st.session_state.edit_mode

    if st.session_state.edit_mode:
        st.warning("Edit mode: You can modify categories and flags below.")

    tab_all, tab_expense, tab_self = st.tabs([
        f"All ({len(df)})",
        f"Expenses ({len(expense_df)})",
        f"Own Account Transfer ({len(df[df['IsSelfTransfer']])})",
    ])

    def _display_df(source_df: pd.DataFrame, editable: bool = False):
        """Build a clean display DataFrame; editable adds editor columns."""
        cols = ["CleanLabel", "Category", "Debit", "Credit", "IsSelfTransfer", "IsSalary"]
        if date_col and date_col in source_df.columns:
            cols = [date_col] + cols
        show = source_df[[c for c in cols if c in source_df.columns]].copy()
        show = show.rename(columns={
            "CleanLabel":     "Description / Merchant",
            "IsSelfTransfer": "Own Account Transfer",
            "IsSalary":       "Salary",
        })
        for col in ["Debit", "Credit"]:
            if col in show.columns:
                show[col] = show[col].apply(lambda x: f"₹{x:,.2f}" if x > 0 else "—")
        return show

    with tab_all:
        if st.session_state.edit_mode:
            st.data_editor(_display_df(df, editable=True), use_container_width=True)
        else:
            st.dataframe(_display_df(df), use_container_width=True)

    with tab_expense:
        if st.session_state.edit_mode:
            st.data_editor(_display_df(expense_df, editable=True), use_container_width=True)
        else:
            st.dataframe(_display_df(expense_df), use_container_width=True)
        st.caption(f"{len(expense_df)} expense transactions · own account transfers excluded · total {fmt(total_spend)}")

    with tab_self:
        self_df = df[df["IsSelfTransfer"]]
        if self_df.empty:
            st.info("No own account transfers detected in this statement.")
        else:
            if st.session_state.edit_mode:
                st.data_editor(_display_df(self_df, editable=True), use_container_width=True)
            else:
                st.dataframe(_display_df(self_df), use_container_width=True)
            st.caption(f"{len(self_df)} own account transfer(s) · {fmt(self_transfer_amt)} excluded from spending total.")

    # ── Download ──────────────────────────────────────────────────────
    st.markdown("<div style='margin-top:1.25rem'></div>", unsafe_allow_html=True)
    export_cols = (
        ([date_col] if date_col else [])
        + ["CleanLabel", "Description", "Merchant", "UPI_ID", "Category",
           "Debit", "Credit", "Type", "IsSelfTransfer", "IsSalary"]
    )
    export_df = df[[c for c in export_cols if c in df.columns]]
    csv_data  = export_df.to_csv(index=False)
    st.download_button(
        label="⬇️  Download Clean Report (CSV)",
        data=csv_data,
        file_name="hdfc_expense_report.csv",
        mime="text/csv",
    )

    st.markdown(
        '<div class="footer-note">Your data is processed entirely in your browser session — nothing is stored or shared.</div>',
        unsafe_allow_html=True,
    )

else:
    st.markdown(
        """
        <div class="empty-state">
            <div class="icon">📂</div>
            <div class="title">Upload your HDFC statement to get started</div>
            <div class="sub">Supports .xls and .xlsx exported from HDFC NetBanking or Mobile Banking</div>
        </div>
        """,
        unsafe_allow_html=True,
    )