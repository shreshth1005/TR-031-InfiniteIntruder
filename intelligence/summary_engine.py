def generate_summary(obligations, anomalies):
    total_obligations = len(obligations)
    total_anomalies = len(anomalies)

    high_risk = sum(1 for item in anomalies if item["severity"] == "High")
    medium_risk = sum(1 for item in anomalies if item["severity"] == "Medium")
    low_risk = sum(1 for item in anomalies if item["severity"] == "Low")

    if total_anomalies == 0:
        return (
            f"The contract contains {total_obligations} identified obligations and no major anomalies. "
            f"Overall, the document appears reasonably aligned with expected legal clause patterns."
        )

    return (
        f"The contract contains {total_obligations} identified obligations and {total_anomalies} flagged observations. "
        f"Among them, {high_risk} are high-risk, {medium_risk} are medium-risk, and {low_risk} are low-risk. "
        f"The strongest concerns relate to missing required clauses or very weak legal alignment, while lower-severity issues reflect wording or drafting quality."
    )