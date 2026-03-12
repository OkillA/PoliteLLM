from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llm_service import translate_to_corporate
from evals import evaluate_translation
from typing import Optional

app = FastAPI(
    title="PoliteLLM API",
    description="Translating anger into corporate synergy.",
    version="1.0.0"
)

# Pydantic models for structured requests/responses
class RantRequest(BaseModel):
    text: str

class TranslationResponse(BaseModel):
    original: str
    translation: str

class EvaluationMetrics(BaseModel):
    hr_compliance: int
    meaning_preservation: int
    passive_aggressiveness: int
    reasoning: str

class EvalResponse(BaseModel):
    translation: str
    evaluation: EvaluationMetrics

@app.post("/translate", response_model=TranslationResponse)
async def translate_rant(request: RantRequest):
    try:
        translation = await translate_to_corporate(request.text)
        return TranslationResponse(original=request.text, translation=translation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-and-evaluate", response_model=EvalResponse)
async def process_and_evaluate(request: RantRequest):
    try:
        # 1. Translate
        translation = await translate_to_corporate(request.text)
        
        # 2. Evaluate
        evaluation = await evaluate_translation(request.text, translation)
        
        return EvalResponse(
            translation=translation,
            evaluation=evaluation
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))