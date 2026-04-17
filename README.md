# 🚀 LexSight AI  
### Multilingual Contract Intelligence & Risk Analysis System

LexSight AI is an AI-powered contract analysis platform that extracts obligations, detects anomalies, and evaluates risk levels from legal documents. It supports multilingual contracts by translating them into a unified language before processing, enabling consistent and reliable analysis.

---

## 📌 Problem Statement

Organizations deal with large volumes of contracts across different languages. Manual review is:

- Time-consuming  
- Inconsistent  
- Prone to human error  

Existing automated tools rely heavily on keyword matching, which leads to:

- False risk detection  
- Missed obligations  
- Lack of contextual understanding  

---

## 🎯 Objective

The goal of LexSight AI is to:

- Automate contract review  
- Extract meaningful obligations  
- Detect logical anomalies (not just keywords)  
- Provide accurate risk classification  
- Support multilingual documents  

---

## 🧠 Key Features

- 🌐 **Multilingual Support**  
  Automatically translates contracts into English for consistent processing  

- 📄 **Obligation Extraction**  
  Identifies legally binding clauses using structured patterns  

- ⚠️ **Anomaly Detection**  
  Detects:
  - Missing clauses (payment, termination, etc.)
  - Ambiguous language  
  - Logical inconsistencies  

- 📊 **Risk Classification**
  - High Risk → Missing critical clauses  
  - Medium Risk → Ambiguity or inconsistency  
  - Low Risk → Minor issues  

- 🧾 **Executive Summary**
  Generates a human-readable explanation of contract quality  

---

## 🏗️ System Architecture
Frontend (Next.js)
↓
Backend API (FastAPI)
↓
Translation Layer
↓
Clause Extraction Engine
↓
Anomaly & Risk Analysis Engine

---

## ⚙️ Tech Stack

### Frontend
- Next.js  
- React.js  
- Tailwind CSS  

### Backend
- FastAPI  
- Python  

### AI / Processing
- NLP-based rule engine  
- Translation APIs  
- Logical anomaly scoring  

### Deployment
- Vercel (Frontend)  
- Render (Backend + Intelligence)  

---

## 🔄 Workflow

1. Upload contract (PDF)
2. Extract text
3. Translate (if needed)
4. Detect obligations
5. Analyze anomalies
6. Classify risks
7. Generate report

---

## 🧮 Core Logic

### Obligation Detection

Sentences containing legal intent are extracted:
"shall", "must", "agrees to"
### Anomaly Scoring
A = Σ (wᵢ · f(cᵢ))


Where:
- `f(cᵢ)` = anomaly presence in clause  
- `wᵢ` = severity weight  

---

### Risk Classification


High Risk → A > Threshold_high
Medium Risk → Threshold_mid < A ≤ Threshold_high
Low Risk → A ≤ Threshold_mid
---

## 📸 Output Preview

Add your screenshot here:



---

## 📊 Example Output

| Metric        | Value |
|--------------|------|
| Obligations  | 316  |
| Anomalies    | 494  |
| High Risk    | 483  |

---

## 🚀 Installation & Setup

### 1. Clone Repository


git clone https://github.com/shreshth1005/TR-031-InfiniteIntruder.git

cd TR-031-InfiniteIntruder


---

### 2. Backend Setup


cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 5000


---

### 3. Intelligence Engine


cd intelligence
pip install -r requirements.txt
uvicorn main:app --reload --port 8000


---

### 4. Frontend Setup


cd frontend3d-app
npm install
npm run dev


---

## 🌍 Deployment Links

- Backend → https://tr031-backend.onrender.com  
- Intelligence → https://tr031-intelligence.onrender.com  

---

## 📈 Advantages Over Traditional Systems

| Feature | Traditional Systems | LexSight AI |
|--------|-------------------|-------------|
| Multilingual Support | ❌ | ✅ |
| Logical Analysis | ❌ | ✅ |
| Context Awareness | ❌ | ✅ |
| Risk Accuracy | Low | High |

---

## ⚠️ Limitations

- Translation quality may affect analysis  
- Complex legal language may reduce accuracy  
- Rule-based logic may miss rare edge cases  

---

## 🔮 Future Scope

- Transformer-based NLP (BERT / Legal-BERT)  
- Semantic embeddings  
- AI-based clause reasoning  
- Legal knowledge graphs  
- Reinforcement learning for risk scoring  

---

## 👨‍💻 Author

**Shreshth Mehrotra**  
SRM Institute of Science and Technology  

---

## 📜 License

This project is intended for academic and research purposes.

---

## ⭐ Final Note

LexSight AI moves beyond simple keyword detection by introducing structured reasoning into contract analysis. It provides a scalable and practical solution for real-world legal intelligence systems.
