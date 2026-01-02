def calculate_priority(row, w_days, w_amount, w_risk):
    score = (
        w_days * row["days_overdue"]
        + w_amount * (row["amount"] / 1000)
        + w_risk * row["risk_flag"] * 100
    )

    if score >= 120:
        return "High"
    elif score >= 60:
        return "Medium"
    else:
        return "Low"


def sla_status(days, warning_days, breach_days):
    if days > breach_days:
        return "🔴 Breached"
    elif days > warning_days:
        return "🟡 Warning"
    else:
        return "🟢 On Track"


def recovery_probability(row):
    if row["days_overdue"] > 180:
        return "Low"
    elif row["risk_flag"] == 1 and row["days_overdue"] > 120:
        return "Medium"
    else:
        return "High"


def calculate_metrics(df):
    metrics = df.groupby("dca").agg(
        total_cases=("case_id", "count"),
        recovered_cases=("status", lambda x: (x == "Recovered").sum()),
        escalated_cases=("status", lambda x: (x == "Escalated").sum()),
        avg_days_overdue=("days_overdue", "mean"),
    )

    metrics["recovery_rate (%)"] = (
        metrics["recovered_cases"] / metrics["total_cases"] * 100
    ).round(2)

    return metrics.reset_index()