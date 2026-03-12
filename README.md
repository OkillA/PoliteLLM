# 👔 PoliteLLM: The Corporate Email Translator

PoliteLLM is a "production-ready" microservice that takes your unfiltered, angry workplace rants and translates them into perfectly polished, passive-aggressive corporate speak.

## ✨ Features
- **FastAPI Backend**: Fully asynchronous auto-generated OpenAPI/Swagger endpoints.
- **LiteLLM Integration**: Seamlessly powered by Google's **Gemma 3 27B IT** utilizing async `acompletion` for high-concurrency requests.
- **High-Performance Observability**: Custom JSONL (JSON Lines) file logging callbacks to track latency, token usage, and simulated cost with $O(1)$ write operations.
- **LLM-as-a-Judge**: Robust automated evaluation scoring translations on HR Compliance, Meaning Preservation, and "Passive-Aggressiveness" levels using manual JSON extraction fallbacks.

## 🛠️ Tech Stack
- **LLM:** Gemma 3 27B IT (via Google AI Studio)
- **Framework:** FastAPI / Pydantic (Asynchronous)
- **Orchestration:** LiteLLM (`acompletion`)
- **Environment:** Python 3.10+
