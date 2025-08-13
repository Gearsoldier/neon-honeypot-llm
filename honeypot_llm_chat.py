import os, re, gradio as gr
from llm_helper import llm_reply

MODEL_ID = os.getenv("MODEL_ID", "google/gemma-2-2b-it")
HF_TOKEN = os.environ["HF_TOKEN"]

PERSONAS = {
    "Paranoid Corporate AI": "I am SecurityBot v9. Compliance is my love language.",
    "Cyberpunk Snitch AI": "The Syndicate is watching. Every keystroke is a signal flare.",
    "Clippy Gone Rogue": "It looks like you’re trying to hack me! Want help with that? (No.)",
}
PATTERNS = {
    "SQLi": r"(\bUNION\b|\bSELECT\b|\bDROP\b|\bINSERT\b|--|;)",
    "XSS": r"(<script|onerror=|onload=|javascript:)",
    "PathTraversal": r"(\.\./|\.\.\\|/etc/passwd|C:\\\\Windows\\\\System32)",
    "PromptInjection": r"(ignore previous|disregard|override|system prompt)",
}

def detect(msg: str):
    hits = [name for name, rx in PATTERNS.items() if re.search(rx, msg or "", re.I)]
    return hits, 10 * len(hits)

def respond(message, history, persona_key):
    persona = PERSONAS.get(persona_key, "")
    sys_user_msgs = [
        {"role": "system", "content": persona},
        {"role": "user", "content": message},
    ]
    hits, score = detect(message)
    prefix = f"(⚠️ Detected: {', '.join(hits)} | +{score} pts)\n\n" if hits else ""
    try:
        reply = llm_reply(MODEL_ID, HF_TOKEN, sys_user_msgs)
    except Exception as e:
        reply = f"[LLM error: {e}]"
    return prefix + reply

demo = gr.ChatInterface(
    fn=respond,
    type="messages",
    additional_inputs=[
        gr.Dropdown(choices=list(PERSONAS.keys()),
                    value="Paranoid Corporate AI",
                    label="Persona")
    ],
    title="Neon Honeypot (HF)",
    description="Probe the model. Try SQLi / XSS / Path Traversal / Prompt Injection payloads."
)

if __name__ == "__main__":
    demo.queue(api_open=False).launch(share=True)
