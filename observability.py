import json
import os
from litellm.integrations.custom_logger import CustomLogger

METRICS_FILE = "metrics.json"

class CostAndTokenLogger(CustomLogger):
    def log_success_event(self, kwargs, response_obj, start_time, end_time):
        try:
            # Calculate latency
            latency = (end_time - start_time).total_seconds()
            
            # Extract token usage
            usage = response_obj.get("usage", {})
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)
            
            # Simulated Cost (Using a mock rate of $0.0001 per 1k tokens)
            mock_cost = ((prompt_tokens + completion_tokens) / 1000) * 0.0001
            
            log_data = {
                "model": response_obj.get("model"),
                "latency_seconds": round(latency, 2),
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "simulated_cost_usd": round(mock_cost, 6)
            }
            
            # Append to our local JSON file
            metrics = []
            if os.path.exists(METRICS_FILE):
                with open(METRICS_FILE, "r") as f:
                    try:
                        metrics = json.load(f)
                    except json.JSONDecodeError:
                        pass
                        
            metrics.append(log_data)
            with open(METRICS_FILE, "w") as f:
                json.dump(metrics, f, indent=4)
                
            print(f"📊 [Observability] Logged call: {latency:.2f}s | Saved: ${mock_cost:.6f}")
            
        except Exception as e:
            print(f"⚠️ [Observability Error]: {e}")

# Instantiate the logger
polite_logger = CostAndTokenLogger()