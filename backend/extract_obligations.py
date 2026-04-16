from extract_text import extract_text_from_pdf
import re
import json

def extract_party(sentence):
    words = sentence.split()
    if len(words) > 0:
        return words[0]  # simple assumption
    return "Unknown"

def extract_deadline(sentence):
    match = re.search(r'\b\d+\s*(days|weeks|months|years)\b', sentence.lower())
    return match.group() if match else ""

def extract_condition(sentence):
    if "if" in sentence.lower():
        return sentence
    return ""

def extract_consequence(sentence):
    if "penalty" in sentence.lower() or "liable" in sentence.lower():
        return sentence
    return ""


def extract_obligations(text):
    obligations = []

    sentences = re.split(r'[.\n]', text)

    for sentence in sentences:
        sentence = sentence.strip()

        if len(sentence) < 25:
            continue

        if any(word in sentence.lower() for word in ["shall", "must", "agree", "will", "required"]):

            obligation = {
                "party": extract_party(sentence),
                "action": sentence,
                "deadline": extract_deadline(sentence),
                "condition": extract_condition(sentence),
                "consequence": extract_consequence(sentence),
                "confidence_score": round(len(sentence) / 100, 2)  # simple scoring
            }

            obligations.append(obligation)

    return obligations

def analyze_obligations(obligations):
    print("Step 3: Analyzing obligations for risks...")

    anomalies = []

    for obj in obligations:
        text = obj["action"].lower()

        # Debugging output for clarity
        #print(f"Analyzing clause: {text}")

        if "shall" in text:
         anomalies.append({
        "issue": "Mandatory obligation detected",
        "severity": "Medium",
        "clause": obj["action"],
        "reason": "Use of 'shall' indicates a legally binding obligation, increasing enforcement risk."
    })

        elif "agree" in text:
         anomalies.append({
        "issue": "Agreement clause",
        "severity": "Low",
        "clause": obj["action"],
        "reason": "Indicates mutual agreement but is less strict compared to mandatory obligations."
    })
            

    return anomalies

def process_contract(pdf_path):
    from extract_text import extract_text_from_pdf

    print("Step 1: Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)

    print("Step 2: Extracting obligations...")
    obligations = extract_obligations(text)

    print("Step 3: Analyzing obligations...")
    anomalies = analyze_obligations(obligations)

    print("Step 4: Generating summary...")
    summary = f"{len(obligations)} obligations found, {len(anomalies)} risks detected."

    return {
        "obligations": obligations,
        "anomalies": anomalies,
        "summary": summary
    }
def extractor_agent(pdf_path):
    print("🟢 Extractor Agent Working...")

    from extract_text import extract_text_from_pdf

    text = extract_text_from_pdf(pdf_path)
    obligations = extract_obligations(text)

    return obligations  

def analyzer_agent(obligations):
    print("🔴 Analyzer Agent Working...")

    anomalies = analyze_obligations(obligations)

    return anomalies  

def summary_agent(obligations, anomalies):
    print("\n🔵 Summary Agent Working...\n")

    summary = f"AI system extracted {len(obligations)} obligations and detected {len(anomalies)} risks."

    print("====================================")
    print("📊 FINAL SUMMARY")
    print("====================================")
    print(summary)

    return summary
    
def agent_controller(pdf_path):
    print("\n🤖 Multi-Agent System Started...\n")

    obligations = extractor_agent(pdf_path)

    print("\n➡️ Analyzer starting...\n")
    anomalies = analyzer_agent(obligations)

    print("\n➡️ Summary starting...\n")
    summary = summary_agent(obligations, anomalies)

    print("\n🤖 Multi-Agent Execution Completed\n")

    return {
        "obligations": obligations,
        "anomalies": anomalies,
        "summary": summary
    }


if __name__ == "__main__":
    result = agent_controller("sample_contract.pdf")

    print("\n--- FINAL OUTPUT ---\n")
    import json

import json

print("\n--- FINAL OUTPUT (SHORT) ---\n")

print("\nSummary:")
print(result["summary"])

print("\nTop 5 Obligations:")
for obj in result["obligations"][:5]:
    print(json.dumps(obj, indent=2))

print("\nTop Risks:")
for risk in result["anomalies"][:5]:
    print("-----")
    print("Issue:", risk["issue"])
    print("Severity:", risk["severity"])
    print("Clause:", risk["clause"])
    print("Reason:", risk["reason"])


