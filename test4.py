from duckduckgo_search import DDGS

results = DDGS().text("Overview of the AI inference market with focus on Fireworks, Together.ai, Groq", max_results=5)
print(results)