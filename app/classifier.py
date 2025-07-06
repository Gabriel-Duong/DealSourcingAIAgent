import requests
from app.prompts import PROMPT_TEMPLATE
from app.prompts import EXTRACTION_PROMPT

OLLAMA_API_URL = "http://localhost:11434/api/generate"

def classify_pitch(text):
    prompt = PROMPT_TEMPLATE.format(text=text[:4000])  # truncate if too long

    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_API_URL, json=payload)
    output = response.json()["response"].strip().lower()

    return output  # expected: "strong" or "weak"

def extract_signals(text):
    prompt = EXTRACTION_PROMPT.format(text=text[:4000])  # adjust size if needed

    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post("http://localhost:11434/api/generate", json=payload)
    content = response.json()["response"]

    # Optional: safely parse JSON-like string
    import json
    try:
        extracted = json.loads(content)
    except json.JSONDecodeError:
        extracted = {"error": "LLM did not return valid JSON", "raw_response": content}

    return extracted
