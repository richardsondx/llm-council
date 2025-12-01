"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Council members - list of OpenRouter model identifiers
COUNCIL_MODELS = [
    "openai/gpt-5.1",
    "google/gemini-3-pro-preview",
    "anthropic/claude-sonnet-4.5",
    "x-ai/grok-4",
]

# Chairman model - synthesizes final response
CHAIRMAN_MODEL = "google/gemini-3-pro-preview"

# Optional: Roles for each council member (must match order of COUNCIL_MODELS)
# If None, no specific role is assigned.
COUNCIL_ROLES = [
    "Macroeconomics and Industrial Policy Strategist",        # gpt-5.1
    "Geopolitics and National Security Analyst",              # claude-sonnet-4.5
    "Infrastructure, Energy, and Technology Systems Planner", # grok-4
    "Demography, Migration, and Social Policy Specialist",    # gemini-3-pro preview (as a voting member)
]
# Optional: Role for the chairman
CHAIRMAN_ROLE = "Cross-Domain Integrator and Final Policy Arbiter"

# OpenRouter API endpoint
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Data directory for conversation storage
DATA_DIR = "data/conversations"
