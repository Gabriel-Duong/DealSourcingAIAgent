# DealSourcingAIAgent

## Overview

**DealSourcingAIAgent** is a local-first AI assistant designed for venture capital analysts to streamline the triage process of evaluating startup pitch decks. This tool automates classification and information extraction tasks using local LLMs, enabling analysts to prioritize high-quality deals with more efficiency and consistency. All computation is done on-device, preserving confidentiality and eliminating API costs.

---

## Architecture & Technology

* **Language & Framework**: Python 3.13 with [FastAPI](https://fastapi.tiangolo.com/) for building RESTful APIs.
* **LLM Engine**: [Mistral 7B](https://ollama.com/library/mistral) served locally via [Ollama](https://ollama.com).
* **Document Parsing**: [`pdfplumber`](https://github.com/jsvine/pdfplumber) for extracting text from PDF pitch decks.
* **Prompting Strategy**: Custom-engineered zero-shot prompts for classification and signal extraction.
* **Environment**: Python `venv` for virtual environment isolation.
* **Tools**: VSCode for development, GitHub for version control, Swagger UI for API testing.

---

## Workflow

```text
1. Upload PDF via API
   ↓
2. Extract text using pdfplumber
   ↓
3. Choose endpoint:
   - /classify → returns "strong" or "weak"
   - /extract-signals → returns structured business insights
   ↓
4. Return JSON response to the user (via Swagger UI or future UI)
```

---

## Current Functionality

* Accepts `.pdf` pitch decks through an API endpoint.
* Extracts raw text using `pdfplumber`.
* Sends text to a local instance of Mistral 7B for:

  * Binary classification of deal quality.
  * Extraction of 5 core VC-relevant signals:

    * Market Potential
    * Team/Founder Experience
    * Competitive Positioning
    * Business Model
    * Exit Strategy
* Returns structured JSON results.

---

## Project Structure

```bash
DealSourcingAIAgent/
├── app/
│   ├── main.py            # FastAPI route definitions
│   ├── classifier.py      # Core logic to interact with LLM via Ollama
│   ├── prompts.py         # Prompt templates for classification/extraction
│   └── utils.py           # PDF parsing and helper functions
├── uploads/               # Temporary storage for uploaded pitch decks
├── venv/                  # Virtual Python environment
├── requirements.txt       # Dependencies for pip installation
└── README.md              # Project documentation (this file)
```

---

## Future Directions

### 1. Frontend Integration

Replace Swagger UI with a lightweight HTML/Jinja2 interface or a full SPA using React or Svelte. The frontend will support:

* File uploads
* Display of extracted signals
* Manual annotations and decision logging

### 2. Intelligent Scoring & Prioritization

Enhance the LLM prompt to return not just descriptions but numerical scores (e.g., 1–5) for each startup signal. This allows the backend to auto-rank and cluster promising deals.

### 3. Persistence Layer

Add data persistence using SQLite or integrations with Notion, Airtable, or Google Sheets. Enable long-term tracking and collaborative review across analyst teams.

### 4. Security & Collaboration

Introduce user authentication and Dockerization for secure deployment across internal teams. Enable multi-user access with permission levels.

### 5. Human Feedback Loop

Incorporate a feedback system where human corrections are logged and used to refine prompt strategies or even fine-tune future model iterations.

---

## Getting Started

### Prerequisites

* macOS with M1/M2 chip or equivalent
* Python 3.13
* [Ollama installed](https://ollama.com/)

### Installation

```bash
# Clone repo and create environment
git clone https://github.com/yourusername/DealSourcingAIAgent.git
cd DealSourcingAIAgent
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start Ollama with Mistral model
ollama run mistral

# Run FastAPI server
uvicorn app.main:app --reload
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) to access Swagger UI.

---

## License

This project is developed for internal research and prototyping purposes. License and usage restrictions to be determined.

---

## Author

Gabriel Duong 
