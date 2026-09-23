import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Supermarket Sales Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE - DARK / LIGHT MODE
# ============================================================

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True


# ============================================================
# THEME
# ============================================================

if st.session_state.dark_mode:

    BG = "#0B1020"
    CARD = "#111827"
    CARD_2 = "#151D31"
    TEXT = "#F8FAFC"
    MUTED = "#94A3B8"
    BORDER = "#263249"
    PRIMARY = "#8B5CF6"
    SECONDARY = "#3B82F6"
    SUCCESS = "#22C55E"
    PLOTLY_TEMPLATE = "plotly_dark"

else:

    BG = "#F5F7FB"
    CARD = "#FFFFFF"
    CARD_2 = "#F8FAFC"
    TEXT = "#111827"
    MUTED = "#64748B"
    BORDER = "#E2E8F0"
    PRIMARY = "#7C3AED"
    SECONDARY = "#2563EB"
    SUCCESS = "#16A34A"
    PLOTLY_TEMPLATE = "plotly_white"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    f"""
    <style>

    /* Main application */
    .stApp {{
        background: {BG};
        color: {TEXT};
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background: {CARD};
        border-right: 1px solid {BORDER};
    }}

    section[data-testid="stSidebar"] * {{
        color: {TEXT};
    }}

    /* Main content width */
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }}

    /* Streamlit title */
    h1 {{
        color: {TEXT} !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }}

    h2, h3 {{
        color: {TEXT} !important;
    }}

    /* Captions */
    .stCaption {{
        color: {MUTED} !important;
    }}

    /* KPI cards */
    .kpi-card {{
        background: linear-gradient(
            135deg,
            {CARD},
            {CARD_2}
        );
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 20px;
        min-height: 145px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.10);
        transition: transform 0.2s ease;
    }}

    .kpi-card:hover {{
        transform: translateY(-3px);
    }}

    .kpi-label {{
        font-size: 13px;
        font-weight: 700;
        color: {MUTED};
        letter-spacing: 0.8px;
        margin-bottom: 10px;
    }}

    .kpi-value {{
        font-size: 27px;
        font-weight: 800;
        color: {TEXT};
        margin-bottom: 5px;
    }}

    .kpi-description {{
        font-size: 12px;
        color: {MUTED};
    }}

    /* Insight cards */
    .insight-card {{
        background: {CARD};
        border: 1px solid {BORDER};
        border-left: 4px solid {PRIMARY};
        border-radius: 12px;
        padding: 18px;
        min-height: 135px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    }}

    .insight-title {{
        font-size: 15px;
        font-weight: 800;
        color: {TEXT};
        margin-bottom: 8px;
    }}

    .insight-text {{
        font-size: 13px;
        line-height: 1.6;
        color: {MUTED};
    }}

    /* Section headers */
    .section-title {{
        font-size: 22px;
        font-weight: 800;
        color: {TEXT};
        margin-top: 25px;
        margin-bottom: 3px;
    }}

    .section-description {{
        color: {MUTED};
        font-size: 13px;
        margin-bottom: 15px;
    }}

    /* Sidebar labels */
    [data-testid="stWidgetLabel"] p {{
        font-weight: 600 !important;
    }}

    /* Buttons */
    .stButton > button {{
        border-radius: 10px;
        border: 1px solid {BORDER};
        font-weight: 600;
    }}

    /* Dataframe */
    [data-testid="stDataFrame"] {{
        border-radius: 12px;
        overflow: hidden;
    }}

    /* Divider */
    hr {{
        border-color: {BORDER};
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

DATA_PATH = "../data/SuperMarket Analysis.csv"

try:
    df = pd.read_csv(DATA_PATH)

except FileNotFoundError:
    st.error(
        "❌ CSV file not found. Please make sure the file is named "
        "'SuperMarket Analysis.csv' and is inside the data folder."
    )
    st.stop()


# ============================================================
# DATA PREPARATION
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Date
if "date" in df.columns:
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

# Time
if "time" in df.columns:

    parsed_time = pd.to_datetime(
        df["time"].astype(str),
        errors="coerce"
    )

    df["hour"] = parsed_time.dt.hour

else:
    df["hour"] = 0


# ============================================================
# FEATURE ENGINEERING
# ============================================================

if "date" in df.columns:

    df["month"] = df["date"].dt.month

    df["month_name"] = df["date"].dt.month_name()

    df["day_name"] = df["date"].dt.day_name()


def get_time_period(hour):

    if pd.isna(hour):
        return "Unknown"

    hour = int(hour)

    if hour < 12:
        return "Morning"

    elif hour < 17:
        return "Afternoon"

    elif hour < 21:
        return "Evening"

    else:
        return "Night"


df["time_period"] = df["hour"].apply(get_time_period)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ⚙️ Dashboard Controls")

    st.caption(
        "Use the filters below to explore supermarket sales."
    )

    st.divider()

    # Theme button

    theme_button = (
        "☀️ Switch to Light Mode"
        if st.session_state.dark_mode
        else "🌙 Switch to Dark Mode"
    )

    if st.button(
        theme_button,
        use_container_width=True
    ):

        st.session_state.dark_mode = (
            not st.session_state.dark_mode
        )

        st.rerun()

    st.divider()

    st.markdown("### 🔎 Filters")

    # --------------------------------------------------------
    # Branch
    # --------------------------------------------------------

    branches = sorted(
        df["branch"].dropna().unique()
    )

    selected_branches = st.multiselect(
        "Branch",
        branches,
        default=branches
    )

    # --------------------------------------------------------
    # City
    # --------------------------------------------------------

    cities = sorted(
        df["city"].dropna().unique()
    )

    selected_cities = st.multiselect(
        "City",
        cities,
        default=cities
    )

    # --------------------------------------------------------
    # Customer Type
    # --------------------------------------------------------

    customer_types = sorted(
        df["customer_type"].dropna().unique()
    )

    selected_customer_types = st.multiselect(
        "Customer Type",
        customer_types,
        default=customer_types
    )

    # --------------------------------------------------------
    # Gender
    # --------------------------------------------------------

    genders = sorted(
        df["gender"].dropna().unique()
    )

    selected_genders = st.multiselect(
        "Gender",
        genders,
        default=genders
    )

    # --------------------------------------------------------
    # Product Line
    # --------------------------------------------------------

    product_lines = sorted(
        df["product_line"].dropna().unique()
    )

    selected_product_lines = st.multiselect(
        "Product Line",
        product_lines,
        default=product_lines
    )

    # --------------------------------------------------------
    # Payment
    # --------------------------------------------------------

    payments = sorted(
        df["payment"].dropna().unique()
    )

    selected_payments = st.multiselect(
        "Payment Method",
        payments,
        default=payments
    )

    st.divider()

    st.markdown("### 📁 Dataset")

    st.caption("SuperMarket Analysis.csv")

    st.caption(
        f"Records: {len(df):,}"
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df[
    df["branch"].isin(selected_branches)
    & df["city"].isin(selected_cities)
    & df["customer_type"].isin(selected_customer_types)
    & df["gender"].isin(selected_genders)
    & df["product_line"].isin(selected_product_lines)
    & df["payment"].isin(selected_payments)
].copy()


# ============================================================
# HEADER
# ============================================================

st.title("🛒 Supermarket Sales Analytics")

st.caption(
    "Interactive Business Intelligence Dashboard for "
    "sales performance, customer behavior, product analytics "
    "and operations."
)

st.markdown(
    "**PYTHON**  •  **PANDAS**  •  **PLOTLY**  •  **STREAMLIT**"
)

st.divider()


# ============================================================
# EMPTY DATA CHECK
# ============================================================

if filtered_df.empty:

    st.warning(
        "⚠️ No records match the selected filters. "
        "Please change the filters from the sidebar."
    )

    st.stop()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_sales = filtered_df["sales"].sum()

total_gross_income = filtered_df["gross_income"].sum()

total_transactions = filtered_df["invoice_id"].nunique()

total_quantity = filtered_df["quantity"].sum()

avg_transaction = (
    total_sales / total_transactions
    if total_transactions > 0
    else 0
)

avg_rating = filtered_df["rating"].mean()


# ============================================================
# KPI SECTION
# ============================================================

st.markdown(
    '<div class="section-title">📊 Key Performance Indicators</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Real-time metrics based on the selected filters.'
    '</div>',
    unsafe_allow_html=True
)


kpi1, kpi2, kpi3 = st.columns(3)
kpi4, kpi5, kpi6 = st.columns(3)


with kpi1:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">💰 TOTAL SALES</div>
            <div class="kpi-value">
                {total_sales:,.2f}
            </div>
            <div class="kpi-description">
                Total revenue
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with kpi2:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">📈 GROSS INCOME</div>
            <div class="kpi-value">
                {total_gross_income:,.2f}
            </div>
            <div class="kpi-description">
                Gross income generated
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with kpi3:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">🧾 TRANSACTIONS</div>
            <div class="kpi-value">
                {total_transactions:,}
            </div>
            <div class="kpi-description">
                Unique invoices
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with kpi4:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">📦 QUANTITY SOLD</div>
            <div class="kpi-value">
                {total_quantity:,}
            </div>
            <div class="kpi-description">
                Items sold
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with kpi5:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">🛒 AVG. TRANSACTION</div>
            <div class="kpi-value">
                {avg_transaction:,.2f}
            </div>
            <div class="kpi-description">
                Average invoice value
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with kpi6:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">⭐ AVG. RATING</div>
            <div class="kpi-value">
                {avg_rating:.2f}/10
            </div>
            <div class="kpi-description">
                Customer rating
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SALES OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">📈 Sales Overview</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Revenue trend and product category performance.'
    '</div>',
    unsafe_allow_html=True
)


sales_col1, sales_col2 = st.columns(2)


# ------------------------------------------------------------
# Monthly Sales
# ------------------------------------------------------------

with sales_col1:

    if "date" in filtered_df.columns:

        monthly_sales = (
            filtered_df
            .groupby(
                ["month", "month_name"],
                as_index=False
            )["sales"]
            .sum()
            .sort_values("month")
        )

        fig_month = px.line(
            monthly_sales,
            x="month_name",
            y="sales",
            markers=True,
            template=PLOTLY_TEMPLATE,
            title="Monthly Sales Trend"
        )

        fig_month.update_traces(
            line=dict(
                width=3
            ),
            marker=dict(
                size=9
            )
        )

        fig_month.update_layout(
            xaxis_title="Month",
            yaxis_title="Sales",
            hovermode="x unified",
            margin=dict(
                l=10,
                r=10,
                t=55,
                b=10
            )
        )

        st.plotly_chart(
            fig_month,
            use_container_width=True
        )


# ------------------------------------------------------------
# Product Line Sales
# ------------------------------------------------------------

with sales_col2:

    product_sales = (
        filtered_df
        .groupby("product_line", as_index=False)["sales"]
        .sum()
        .sort_values(
            "sales",
            ascending=True
        )
    )

    fig_product = px.bar(
        product_sales,
        x="sales",
        y="product_line",
        orientation="h",
        template=PLOTLY_TEMPLATE,
        title="Sales by Product Line",
        text_auto=".2s"
    )

    fig_product.update_layout(
        xaxis_title="Sales",
        yaxis_title="Product Line",
        margin=dict(
            l=10,
            r=10,
            t=55,
            b=10
        )
    )

    st.plotly_chart(
        fig_product,
        use_container_width=True
    )


# ============================================================
# CUSTOMER ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">👥 Customer Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Customer segments and purchasing distribution.'
    '</div>',
    unsafe_allow_html=True
)


customer_col1, customer_col2 = st.columns(2)


# ------------------------------------------------------------
# Customer Type
# ------------------------------------------------------------

with customer_col1:

    customer_sales = (
        filtered_df
        .groupby(
            "customer_type",
            as_index=False
        )["sales"]
        .sum()
    )

    fig_customer = px.pie(
        customer_sales,
        names="customer_type",
        values="sales",
        hole=0.55,
        template=PLOTLY_TEMPLATE,
        title="Sales by Customer Type"
    )

    fig_customer.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    fig_customer.update_layout(
        margin=dict(
            l=10,
            r=10,
            t=55,
            b=10
        )
    )

    st.plotly_chart(
        fig_customer,
        use_container_width=True
    )


# ------------------------------------------------------------
# Gender
# ------------------------------------------------------------

with customer_col2:

    gender_sales = (
        filtered_df
        .groupby(
            "gender",
            as_index=False
        )["sales"]
        .sum()
    )

    fig_gender = px.bar(
        gender_sales,
        x="gender",
        y="sales",
        template=PLOTLY_TEMPLATE,
        title="Sales by Gender",
        text_auto=".2s"
    )

    fig_gender.update_layout(
        xaxis_title="Gender",
        yaxis_title="Sales",
        margin=dict(
            l=10,
            r=10,
            t=55,
            b=10
        )
    )

    st.plotly_chart(
        fig_gender,
        use_container_width=True
    )


# ============================================================
# OPERATIONS ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">⚙️ Operations Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Payment behavior and transaction timing.'
    '</div>',
    unsafe_allow_html=True
)


operations_col1, operations_col2 = st.columns(2)


# ------------------------------------------------------------
# Payment
# ------------------------------------------------------------

with operations_col1:

    payment_sales = (
        filtered_df
        .groupby(
            "payment",
            as_index=False
        )["sales"]
        .sum()
        .sort_values(
            "sales",
            ascending=False
        )
    )

    fig_payment = px.bar(
        payment_sales,
        x="payment",
        y="sales",
        template=PLOTLY_TEMPLATE,
        title="Sales by Payment Method",
        text_auto=".2s"
    )

    fig_payment.update_layout(
        xaxis_title="Payment Method",
        yaxis_title="Sales",
        margin=dict(
            l=10,
            r=10,
            t=55,
            b=10
        )
    )

    st.plotly_chart(
        fig_payment,
        use_container_width=True
    )


# ------------------------------------------------------------
# Time Period
# ------------------------------------------------------------

with operations_col2:

    time_order = [
        "Morning",
        "Afternoon",
        "Evening",
        "Night"
    ]

    time_sales = (
        filtered_df
        .groupby(
            "time_period",
            as_index=False
        )["sales"]
        .sum()
    )

    time_sales["time_period"] = pd.Categorical(
        time_sales["time_period"],
        categories=time_order,
        ordered=True
    )

    time_sales = time_sales.sort_values(
        "time_period"
    )

    fig_time = px.bar(
        time_sales,
        x="time_period",
        y="sales",
        template=PLOTLY_TEMPLATE,
        title="Sales by Time Period",
        text_auto=".2s"
    )

    fig_time.update_layout(
        xaxis_title="Time Period",
        yaxis_title="Sales",
        margin=dict(
            l=10,
            r=10,
            t=55,
            b=10
        )
    )

    st.plotly_chart(
        fig_time,
        use_container_width=True
    )


# ============================================================
# BRANCH PERFORMANCE
# ============================================================

st.markdown(
    '<div class="section-title">🏪 Branch Performance</div>',
    unsafe_allow_html=True
)


branch_sales = (
    filtered_df
    .groupby(
        ["branch", "city"],
        as_index=False
    )
    .agg(
        total_sales=("sales", "sum"),
        transactions=("invoice_id", "nunique"),
        quantity=("quantity", "sum"),
        avg_transaction=("sales", "mean")
    )
    .sort_values(
        "total_sales",
        ascending=False
    )
)


fig_branch = px.bar(
    branch_sales,
    x="branch",
    y="total_sales",
    color="city",
    text_auto=".2s",
    template=PLOTLY_TEMPLATE,
    title="Branch Sales Performance"
)

fig_branch.update_layout(
    xaxis_title="Branch",
    yaxis_title="Total Sales",
    legend_title="City",
    margin=dict(
        l=10,
        r=10,
        t=55,
        b=10
    )
)

st.plotly_chart(
    fig_branch,
    use_container_width=True
)


# Branch table

st.dataframe(
    branch_sales.style.format(
        {
            "total_sales": "{:,.2f}",
            "avg_transaction": "{:,.2f}",
            "transactions": "{:,}",
            "quantity": "{:,}"
        }
    ),
    use_container_width=True,
    hide_index=True
)


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.markdown("## 💡 Business Insights")

st.caption(
    "Key observations from the filtered dataset."
)

# ------------------------------------------------------------
# Leading Product
# ------------------------------------------------------------

product_summary = (
    filtered_df
    .groupby("product_line")["sales"]
    .sum()
    .sort_values(ascending=False)
)

leading_product = product_summary.index[0]


# ------------------------------------------------------------
# Highest Branch
# ------------------------------------------------------------

branch_summary = (
    filtered_df
    .groupby("branch")["sales"]
    .sum()
    .sort_values(ascending=False)
)

highest_branch = branch_summary.index[0]


# ------------------------------------------------------------
# Leading Customer Segment
# ------------------------------------------------------------

customer_summary = (
    filtered_df
    .groupby("customer_type")["sales"]
    .sum()
    .sort_values(ascending=False)
)

leading_customer = customer_summary.index[0]


# ------------------------------------------------------------
# Leading Payment
# ------------------------------------------------------------

payment_summary = (
    filtered_df
    .groupby("payment")["sales"]
    .sum()
    .sort_values(ascending=False)
)

leading_payment = payment_summary.index[0]


# ------------------------------------------------------------
# Leading Time Period
# ------------------------------------------------------------

time_summary = (
    filtered_df
    .groupby("time_period")["sales"]
    .sum()
    .sort_values(ascending=False)
)

leading_time = time_summary.index[0]


# ============================================================
# INSIGHT CARDS - STREAMLIT NATIVE
# ============================================================

ins1, ins2 = st.columns(2)

with ins1:

    st.info(
        f"🏆 **Leading Product Category**\n\n"
        f"{leading_product} generated the highest sales "
        f"among the selected product categories."
    )

with ins2:

    st.info(
        f"🏪 **Highest-Sales Branch**\n\n"
        f"Branch {highest_branch} recorded the highest "
        f"sales among the selected branches."
    )


ins3, ins4 = st.columns(2)

with ins3:

    st.info(
        f"👥 **Customer Segment**\n\n"
        f"{leading_customer} customers generated the "
        f"highest sales contribution."
    )

with ins4:

    st.info(
        f"💳 **Payment & Time Pattern**\n\n"
        f"{leading_payment} recorded the highest sales "
        f"among payment methods, while {leading_time} "
        f"recorded the highest sales among time periods."
    )
# ============================================================
# FILTERED DATA
# ============================================================

st.divider()

with st.expander(
    "📋 View Filtered Transaction Data"
):

    st.caption(
        f"Showing {len(filtered_df):,} records "
        f"after applying the selected filters."
    )

    display_df = filtered_df.copy()

    # Make date readable

    if "date" in display_df.columns:

        display_df["date"] = (
            display_df["date"]
            .dt.strftime("%Y-%m-%d")
        )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🛒 Supermarket Sales Analytics  •  "
    "Built with Python • Pandas • Plotly • Streamlit"
)