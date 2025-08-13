"""
HF router helper — tries chat.completions first, then falls back to text-generation.
Works with models like:
  - google/gemma-2-2b-it
  - Qwen/Qwen2.5-3B-Instruct
  - TinyLlama/TinyLlama-1.1B-Chat-v1.0
"""

from typing import List, Dict
from huggingface_hub import InferenceClient


def llm_reply(model_id: str, token: str, messages: List[Dict]) -> str:
    """
    messages -> OpenAI-style messages: [{"role":"system|user|assistant","content": "..."}]
    """
    # Try chat.completions (preferred)
    try:
        c = InferenceClient(token=token)
        r = c.chat.completions.create(
            model=model_id,
            messages=messages,
            max_tokens=256,
            temperature=0.3,
        )
        return (r.choices[0].message.content or "").strip()
    except Exception:
        # Fallback: stitch a prompt and use text-generation
        c = InferenceClient(model=model_id, token=token)
        stitched = []
        for m in messages:
            role = m.get("role", "user")
            stitched.append(f"{role}: {m.get('content','')}")
        prompt = "\n".join(stitched) + "\nassistant:"
        out = c.text_generation(prompt, max_new_tokens=256, temperature=0.7)
        return (out or "").strip()
