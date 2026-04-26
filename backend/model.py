import os
import torch
from transformers import RobertaTokenizer
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "Salesforce/codet5-base")

# Force CPU device - no MPS
DEVICE = torch.device("cpu")

print(f"[model] Loading {MODEL_NAME} on {DEVICE} ...")

# Load tokenizer only - skip actual model due to system incompatibility
try:
    tokenizer = RobertaTokenizer.from_pretrained(MODEL_NAME)
    print("[model] Tokenizer loaded successfully")
except Exception as e:
    print(f"[model] Warning: Failed to load tokenizer - {e}")

# Mock model for demonstration
class MockModel:
    def generate(self, input_ids, **kwargs):
        # Return mock token IDs
        return torch.tensor([[0, 1, 2, 3]])

model = MockModel()

print("[model] Mock model ready (system incompatibility workaround).")


def generate_code(prompt: str, max_new_tokens: int = 256) -> str:
    """
    Mock code generation based on prompt keywords.

    In production, this would call the actual T5 model.
    """
    prompt_lower = prompt.lower()

    if "reverse" in prompt_lower and "array" in prompt_lower:
        if "c++" in prompt_lower:
            return """#include <algorithm>
#include <vector>

void reverseArray(std::vector<int>& arr) {
    std::reverse(arr.begin(), arr.end());
}"""
        else:
            return """def reverse_array(arr):
    return arr[::-1]"""

    elif "fibonacci" in prompt_lower:
        return """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)"""

    elif "sort" in prompt_lower:
        if "python" in prompt_lower:
            return """def sort_array(arr):
    return sorted(arr)"""
        else:
            return """std::sort(arr.begin(), arr.end());"""

    else:
        return f"// Generated code for: {prompt}"
