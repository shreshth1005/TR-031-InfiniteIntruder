import json


def load_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def count_high_risk(anomalies):
    return sum(1 for anomaly in anomalies if anomaly["severity"].lower() == "high")


def count_medium_risk(anomalies):
    return sum(1 for anomaly in anomalies if anomaly["severity"].lower() == "medium")


def format_obligations(data):
    return data.get("obligations", [])


def format_anomalies(data):
    return data.get("anomalies", [])


def format_summary(data):
    return data.get("summary", "No summary available.")