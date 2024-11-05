import openai
import os

OPENAI_MODEL = "gpt-4o-mini"
OPENAI_TEMPERATURE = 0.7
MILLION = 1000000
OPENAI_INPUT_TOKEN_PRICE = 0.15 / MILLION
OPENAI_OUTPUT_TOKEN_PRICE = 0.6 / MILLION


def get_client() -> openai.OpenAI:
    """Instantiate OpenAI Client"""

    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    return client

def calculate_prompt_price(input_tokens: int, output_tokens: int) -> int:
    """Calculated in USD how much did a prompt cost"""

    return input_tokens * OPENAI_INPUT_TOKEN_PRICE + output_tokens * OPENAI_OUTPUT_TOKEN_PRICE

def analyze_sentiment(client:openai.OpenAI, input:str) -> str:
    """Analyzes sentiment of the input and returns formatted output in Markdown"""

    messages=[{"role": "system", 
               "content": "You are an expert in analysing sentiment in human interaction."
               "User will input excerpt from a conversation."
               "Extract people in the conversation, topics discusses and sentiment of each person per topic."
               "Provide concise answer."},
              {"role": "user", 
               "content": input}]

    assistant_reponse = client.chat.completions.create(
        messages=messages,
        model=OPENAI_MODEL,
        temperature=OPENAI_TEMPERATURE
    )
    
    response_text = assistant_reponse.choices[0].message.content

    input_cost = calculate_prompt_price(assistant_reponse.usage.prompt_tokens, assistant_reponse.usage.completion_tokens) * 100

    return f"""## Sentiment Analysis

{response_text}
---
Analysis cost: {input_cost:.4f} USD cents
"""