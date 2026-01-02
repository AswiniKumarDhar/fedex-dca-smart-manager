import streamlit as st
import pandas as pd
from logic import (
    calculate_priority,
    calculate_metrics,
    sla_status,
    recovery_probability
)

st.set_page_config(page_title="FedEx DCA Smart Manager", layout="wide")
st.title("📊 FedEx DCA Smart Manager")

st.sidebar.header("🔐 Simulated Login (Demo Only)")

st.sidebar.caption(
    "⚠️ Demo-only login switch. Real system uses FedEx IAM."
)

user = st.sidebar.selectbox(
    "Login as (for demo)",
    ["fedex_admin", "dca_a_user", "dca_b_user", "dca_c_user"]
)

USER_ACCESS = {
    "fedex_admin": {"role": "Admin", "dca": None},
    "dca_a_user": {"role": "DCA", "dca": "DCA_A"},
    "dca_b_user": {"role": "DCA", "dca": "DCA_B"},
    "dca_c_user": {"role": "DCA", "dca": "DCA_C"},
}

current_user = USER_ACCESS[user]

if current_user["role"] == "Admin":
    st.sidebar.subheader("⚙️ Business Configuration")

    st.sidebar.markdown("### Priority Weights")
    w_days = st.sidebar.slider("Weight: Days Overdue", 0.0, 1.0, 0.5, 0.1)
    w_amount = st.sidebar.slider("Weight: Amount", 0.0, 1.0, 0.3, 0.1)
    w_risk = st.sidebar.slider("Weight: Risk", 0.0, 1.0, 0.2, 0.1)

    st.sidebar.markdown("### SLA Thresholds (Days)")
    sla_warning = st.sidebar.number_input("SLA Warning After", 1, value=60)
    sla_breach = st.sidebar.number_input("SLA Breach After", sla_warning + 1, value=120)
else:
    w_days, w_amount, w_risk = 0.5, 0.3, 0.2
    sla_warning, sla_breach = 60, 120

cases = pd.read_csv("data/cases.csv")

if current_user["role"] == "DCA":
    cases = cases[cases["dca"] == current_user["dca"]]

cases["Priority"] = cases.apply(
    calculate_priority, axis=1, args=(w_days, w_amount, w_risk)
)
cases["SLA Status"] = cases["days_overdue"].apply(
    lambda x: sla_status(x, sla_warning, sla_breach)
)
cases["Recovery Probability"] = cases.apply(
    recovery_probability, axis=1
)

tab1, tab2, tab3 = st.tabs(
    ["📁 Case Management", "📈 DCA Performance", "🧾 Audit Trail"]
)

with tab1:
    st.subheader("Centralized Case Dashboard")
    st.dataframe(cases)

with tab2:
    st.subheader("DCA Performance Metrics")
    metrics = calculate_metrics(cases)
    st.dataframe(metrics)

with tab3:
    st.subheader("Audit Trail")
    audit = pd.read_csv("data/audit_log.csv")
    st.dataframe(audit)

st.markdown("---")
st.caption("Prototype built for FedEx SMART Hackathon")