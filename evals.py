from litellm import completion
import json
import re

MODEL_NAME = "gemini/gemma-3-27b-it"

def evaluate_translation(original_rant: str, translated_email: str) -> dict:
    # We add a very explicit instruction to the prompt since we aren't using "Strict Mode"
    system_prompt = (
        "You are an objective LLM evaluator. Score the provided corporate translation "
        "based on the original rant. You MUST return ONLY a valid JSON object. "
        "Do not include any conversational filler or markdown formatting like ```json."
        "\n\nRequired JSON Keys:\n"
        "- 'hr_compliance' (int 1-5)\n"
        "- 'meaning_preservation' (int 1-5)\n"
        "- 'passive_aggressiveness' (int 1-5)\n"
        "- 'reasoning' (string)"
    )
    
    response = completion(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Original Rant: {original_rant}\n\nTranslation: {translated_email}"}
        ],
        # REMOVED: response_format={ "type": "json_object" } 
        temperature=0.0
    )
    
    
    raw_content = response.choices[0].message.content.strip()

    # Improved Regex: Extract anything between the first { and last }
    match = re.search(r'(\{.*\})', raw_content, re.DOTALL)
    
    if match:
        clean_json = match.group(1)
    else:
        clean_json = raw_content

    try:
        return json.loads(clean_json)
    except json.JSONDecodeError:
        print(f"DEBUG: Failed to parse JSON. Raw output was: {raw_content}")
        # Return the EXACT keys the API expects, but with 'failure' values
        return {
            "hr_compliance": 0,
            "meaning_preservation": 0,
            "passive_aggressiveness": 0,
            "reasoning": f"Failed to parse LLM response: {raw_content[:50]}"
        }
