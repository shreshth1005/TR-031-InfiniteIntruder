def generate_summary(obligations, anomalies):
    total_obligations = len(obligations)
    total_anomalies = len(anomalies)

    high_risk = sum(1 for item in anomalies if item["severity"] == "High")
    medium_risk = sum(1 for item in anomalies if item["severity"] == "Medium")

    if total_anomalies == 0:
        return (
            f"The contract contains {total_obligations} identified obligations and no major anomalies. "
            f"Overall, the document appears structurally aligned with expected legal clause patterns."
        )

    return (
        f"The contract contains {total_obligations} identified obligations and {total_anomalies} anomalies. "
        f"Among them, {high_risk} are high-risk and {medium_risk} are medium-risk. "
        f"The strongest concerns relate to missing required clauses, weak semantic alignment, or vague legal wording."
    )