from litellm import acompletion
from pydantic import BaseModel
import json
import re

MODEL_NAME = "gemini/gemma-3-27b-it"

class EvaluationMetrics(BaseModel):
    hr_compliance: int
    meaning_preservation: int
    passive_aggressiveness: int
    reasoning: str

async def evaluate_translation(original_rant: str, translated_email: str) -> dict:
    system_prompt = (
        "You are an objective LLM evaluator. Score the provided corporate translation "
        "based on the original rant. Assess hr_compliance, meaning_preservation, and "
        "passive_aggressiveness each on a scale of 1-5. "
        "You MUST return ONLY a valid JSON object with the keys: hr_compliance, "
        "meaning_preservation, passive_aggressiveness, and reasoning. "
        "Do not include markdown or text outside the JSON block."
    )
    
    try:
        response = await acompletion(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Original Rant: {original_rant}\n\nTranslation: {translated_email}"}
            ],
            temperature=0.0
        )
        
        # Pydantic structured output isn't supported by this model, fallback to robust manual parsing
        raw_content = response.choices[0].message.content.strip()
        if raw_content.startswith("```json"):
            raw_content = raw_content[7:-3].strip()
        elif raw_content.startswith("```"):
            raw_content = raw_content[3:-3].strip()
            
        eval_metrics = json.loads(raw_content)
        return eval_metrics
    except Exception as e:
        print(f"DEBUG: Evaluation failed: {e}")
        return {
            "hr_compliance": 0,
            "meaning_preservation": 0,
            "passive_aggressiveness": 0,
            "reasoning": f"Failed to generate evaluation: {e}"
        }
    

