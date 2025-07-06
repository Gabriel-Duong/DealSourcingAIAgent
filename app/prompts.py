PROMPT_TEMPLATE = """
You are a venture capital analyst. Given the pitch deck content below, extract important information about a Start-up:

- Financial planning quality
- Market opportunity
- Team quality

Format the response in markdown table. I need to see the features intuitively.
Pitch deck:
{text}
"""
EXTRACTION_PROMPT = """
You are a venture capital analyst. Extract the following information from the startup pitch deck below:

1. Market size and scalability potential
2. Founder and team background
3. Competitive positioning
4. Business model and monetization approach
5. Exit strategy or path to profitability

Pitch deck:
{text}

Respond in JSON format like this:
{{
  "market_potential": "...",
  "team_experience": "...",
  "competition": "...",
  "business_model": "...",
  "exit_strategy": "..."
}}
"""
