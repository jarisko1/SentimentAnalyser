import openai
import os
import json

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

    topics_to_watch = "\n".join([
        "General tone",
        "Expressed strong emotions",
        "Trends in conversation sentiment over time",
        # "Conversation topics and their frequency",
        "Emotionally triggered words",
        "Emerging concerns",
        # "Language patterns",
        "Feeling included or excluded",
        "Discrimination",
        "Harassment",
        "Mentioned overload or burnour",
        "Work-life balance",
        "Requests for help or support",
        "Providing feedback",
        "Recevied feedback",
        "Alignment with company vision",
        "Trust in company decisions",
        "Transparency in communication",
        "Innovation",
        "Motivation in work",
        "Turnover-related langauge",
        "Options in career development"
    ])
                    
    messages=[{"role": "system", 
               "content": "You are an expert in analysing sentiment and mood in human interaction."
               "User will input excerpt from a conversation."
               "Extract language of the conversation and people involved directly or indirectly."
               "Watch for following topics:"
               f"{topics_to_watch}"
               "Do not make up facts that are not in the conversation"
               "Provide concise answer in form of a JSON which will have follwing keys:"
               "language_used: language of the conversation"
               "people_involved: list of all people involved, in format person name: directly/indirectly"
               "topics: list of all topics to watch, with key for every person involved under the topic."
               "Output only topics for which there is relevant information in the conversation."},
              {"role": "user", 
               "content": input}]

    assistant_reponse = client.chat.completions.create(
        messages=messages,
        model=OPENAI_MODEL,
        temperature=OPENAI_TEMPERATURE,
        response_format={"type": "json_object"}
    )
    
    response_text = assistant_reponse.choices[0].message.content

    response_dict = json.loads(response_text)

    input_cost = calculate_prompt_price(assistant_reponse.usage.prompt_tokens, assistant_reponse.usage.completion_tokens) * 100
    response_dict["cost_in_cents"] = input_cost

    return response_dict

#     return f"""## Sentiment Analysis

# {response_text}
# ---
# Analysis cost: {input_cost:.4f} USD cents
# """