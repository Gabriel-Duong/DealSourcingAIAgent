CLASSIFY_PROMPT = """
You are an experienced venture capital analyst.

Given the text of a pitch deck, your task is to classify the startup as either:
- "strong" — if the company has high potential for scale, solid team, good market fit, and clear monetization strategy
- "weak" — if the company lacks these fundamentals or the content is irrelevant

Only respond with one word: "strong" or "weak". Do not explain. Be strict.

Pitch deck content:
{text}
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
