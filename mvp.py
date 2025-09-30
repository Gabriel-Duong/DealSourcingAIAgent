# file: pipeline_mvp.py
import os
import requests

DECILE_API_URL = "https://www.decilehub.com/api/v1"
DECILE_TOKEN = "4ZW8M6LEvTQ8peVqFU9StLdo"
OLLAMA_URL = "http://localhost:11434/api/generate" # default Ollama server

def fetch_org(org_id: int):
    headers = {"Authorization": f"Bearer {DECILE_TOKEN}"}
    resp = requests.get(f"{DECILE_API_URL}/organizations/{org_id}", headers=headers)
    resp.raise_for_status()
    return resp.json()

def summarize_with_ollama(data: dict, model="gemma3:12b"):
    prompt = f"""
    Summarize this company for an investment analyst:
    Name: {data.get('name')}
    Country: {data.get('country')}
    Description: {data.get('short_description')}
    Notes: {data.get('notes')}
    """
    resp = requests.post(
        OLLAMA_URL,
        json={"model": model, "prompt": prompt, "stream": False}
    )
    resp.raise_for_status()
    return resp.json()["response"].strip()

def score_company(data: dict) -> str:
    score = 0
    # MVP binary rules — replace with real thresholds later
    if data.get("country") in ["Singapore", "Vietnam", "Norway"]:
        score += 1
    if data.get("short_description"):
        score += 1
    if "traction" in (data.get("notes") or "").lower():
        score += 1
    return "Yes" if score >= 2 else "No"

def main():
    # Example org_id; replace with an actual ID from your Decile Hub
    org_id = 805274   # TriggMe AS in your CSV
    org = fetch_org(org_id)

    summary = summarize_with_ollama(org)
    decision = score_company(org)

    print("---- Company Summary ----")
    print(summary)
    print("\n---- Decision ----")
    print(decision)

if __name__ == "__main__":
    main()
