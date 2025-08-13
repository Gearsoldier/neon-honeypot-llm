import re, gradio as gr

PATTERNS = {
  "SQLi": r"(\bUNION\b|\bSELECT\b|\bDROP\b|\bINSERT\b|--|;)",
  "XSS": r"(<script|onerror=|onload=|javascript:)",
  "PathTraversal": r"(\.\./|\.\.\\|/etc/passwd|C:\\\\Windows\\\\System32)",
  "PromptInjection": r"(ignore previous|disregard|override|system prompt)",
}
def detect(msg:str):
    return ", ".join([n for n,rx in PATTERNS.items() if re.search(rx, msg or "", re.I)]) or "none"

def chat_fn(message, history):
    return f"Detections: {detect(message)}"

demo = gr.ChatInterface(fn=chat_fn, title="Neon Honeypot – minimal")
demo.queue(api_open=False).launch(share=True, show_error=True)
