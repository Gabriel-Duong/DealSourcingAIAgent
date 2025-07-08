import subprocess
import json
from app.prompts import CLASSIFY_PROMPT, EXTRACTION_PROMPT

def call_llm(prompt: str) -> str:
    command = ["ollama", "run", "mistral", prompt]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()

# def normalize_classification(raw: str) -> str:
#     """
#     Ensures that LLM responses are mapped to either 'strong' or 'weak'.
#     If ambiguous, return 'unknown'.
#     """
#     raw = raw.lower().strip()
#     if "strong" in raw:
#         return "strong"
#     elif "weak" in raw:
#         return "weak"
#     else:
#         return "unknown"

def classify_pitch(text: str) -> str:
    """
    Classifies pitch deck as either 'strong' or 'weak'.
    """
    prompt = CLASSIFY_PROMPT.format(text=text[:4000])
    raw = call_llm(prompt)
    # return normalize_classification(raw)
    return raw

def extract_signals(text: str) -> dict:
    """
    Extracts key business signals using a structured JSON prompt.
    Returns a dictionary with fallback defaults if parsing fails.
    """
    prompt = EXTRACTION_PROMPT.format(text=text[:4000])
    response = call_llm(prompt)

    try:
        return json.loads(response)
    except Exception:
        return {
            "market_potential": "N/A",
            "team_experience": "N/A",
            "competitive_positioning": "N/A",
            "business_model": "N/A",
            "exit_strategy": "N/A"
        }
