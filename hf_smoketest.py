import os
from huggingface_hub import InferenceClient

model = os.getenv("MODEL_ID", "google/gemma-2-2b-it")
token = os.environ["HF_TOKEN"]
client = InferenceClient(token=token)

resp = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "Say 'pong' only."}],
    max_tokens=8,
    temperature=0,
)
print("MODEL:", model)
print("REPLY:", resp.choices[0].message.content)
