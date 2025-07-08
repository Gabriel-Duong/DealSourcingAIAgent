CLASSIFY_PROMPT = """
Classify this deal as either "strong" or "weak".

Pitch Deck Content:
{text}
IMPORTANT
Answer with only: strong or weak.
"""

EXTRACTION_PROMPT = """
You are a venture capital analyst. Read the following pitch deck text and extract 5 signals in structured JSON:

- market_potential: Estimate of market size and scalability
- team_experience: Backgrounds and strengths of the team
- competitive_positioning: Differentiation from competitors
- business_model: How they make money
- exit_strategy: Potential for acquisition or IPO

Pitch Deck:
{text}

Respond in the following format with key metrics:
{{
  "market_potential": "...",
  "team_experience": "...",
  "competitive_positioning": "...",
  "business_model": "...",
  "exit_strategy": "..."
}}
"""
