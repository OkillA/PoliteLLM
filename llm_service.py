import os
from dotenv import load_dotenv

import litellm
from litellm import completion
from observability import polite_logger
# Load the environment variables from the .env file
load_dotenv()

# Attach our custom logger
litellm.custom_callbacks = [polite_logger]

MODEL_NAME = "gemini/gemma-3-27b-it"

def translate_to_corporate(rant: str) -> str:
    system_prompt = (
        "You are an expert in corporate communication and conflict resolution. "
        "Your job is to take the user's angry rant and translate it into completely "
        "bulletproof, passive-aggressive corporate speak. It must be perfectly HR-compliant "
        "but retain a delightfully spiteful undertone."
    )
    
    response = completion(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Translate this rant: {rant}"}
        ],
        temperature=0.7 # A little creativity helps the passive-aggressiveness
    )
    
    return response.choices[0].message.content