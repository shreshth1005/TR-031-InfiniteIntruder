import streamlit as st
import pandas as pd
import time
import os
from utils import (
    load_json_file,
    count_high_risk,
    count_medium_risk,
    format_obligations,
    format_anomalies,
    format_summary
)

st.set_page_config(page_title="AI Contract Analyzer", layout="wide")

st.title("AI Contract Obligation Analyzer")
st.write("Upload a contract PDF to extract obligations, detect anomalies, and generate a clear executive summary.")

st.sidebar.header("Demo Control Panel")
st.sidebar.write("Owner: Shreshth")
data_mode = st.sidebar.radio("Select Data Source", ["Sample Data", "Integrated Output"])

uploaded_file = st.file_uploader("Step 1: Upload Contract PDF", type=["pdf"])

def get_data():
    if data_mode == "Integrated Output" and os.path.exists("output.json"):
        return load_json_file("output.json")
    return load_json_file("sample_output.json")

if uploaded_file is not None:
    st.success("Step 2: PDF uploaded successfully")

    file_details = {
        "File Name": uploaded_file.name,
        "File Type": uploaded_file.type,
        "File Size (KB)": round(uploaded_file.size / 1024, 2)
    }

    st.subheader("Uploaded File Details")
    st.json(file_details)

    with st.spinner("Step 3: Analyzing contract..."):
        time.sleep(2)
        data = get_data()

    obligations = format_obligations(data)
    anomalies = format_anomalies(data)
    summary = format_summary(data)

    st.success("Step 4: Analysis complete")

    st.subheader("Quick Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Obligations", len(obligations))
    col2.metric("Anomalies", len(anomalies))
    col3.metric("High Risk", count_high_risk(anomalies))
    col4.metric("Medium Risk", count_medium_risk(anomalies))

    st.divider()

    st.subheader("Extracted Obligations")
    obligations_df = pd.DataFrame(obligations)
    st.dataframe(obligations_df, use_container_width=True)

    st.divider()

    st.subheader("Risk & Anomaly Detection")
    anomalies_df = pd.DataFrame(anomalies)
    st.dataframe(anomalies_df, use_container_width=True)

    for anomaly in anomalies:
        severity = anomaly["severity"].lower()
        message = f"{anomaly['clause_id']} | {anomaly['issue']} | {anomaly['description']}"

        if severity == "high":
            st.error(message)
        elif severity == "medium":
            st.warning(message)
        else:
            st.success(message)

    st.divider()

    st.subheader("Executive Summary")
    st.info(summary)

else:
    st.info("Upload a PDF to begin the demo.")