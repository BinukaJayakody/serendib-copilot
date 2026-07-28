"""
Model selection layer.

We deliberately use TWO providers and THREE distinct models, each picked for
a specific sub-task based on latency, cost, context window, and reasoning
quality. See README.md for the full comparison table and justification.

    Sub-task                         Provider  Model
    --------------------------------------------------------------------
    Intent routing (classification)  Groq      llama-3.1-8b-instant
    Retrieval re-rank / reflection   Groq      llama-3.3-70b-versatile
    Deep reasoning / final synthesis OpenRouter anthropic/claude-3.5-haiku

Both providers expose OpenAI-compatible chat completion endpoints, so a
single thin client handles both — only the base_url, api_key, and model
name change per call.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Optional

import requests

GROQ_BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# --- Model registry: one place to change models/providers per sub-task ---
MODEL_REGISTRY = {
    "router": {
        "provider": "groq",
        "model": "llama-3.1-8b-instant",
    },
    "rerank_reflect": {
        "provider": "groq",
        "model": "llama-3.3-70b-versatile",
    },
    "synthesis": {
        "provider": "openrouter",
        "model": "anthropic/claude-3.5-haiku",
    },
}


@dataclass
class LLMResponse:
    text: str
    provider: str
    model: str
    latency_s: float
    error: Optional[str] = None


def _call_groq(model: str, system: str, user: str, max_tokens: int = 512) -> LLMResponse:
    api_key = os.environ.get("GROQ_API_KEY")
    t0 = time.time()
    if not api_key:
        return LLMResponse(text="", provider="groq", model=model,
                            latency_s=0.0, error="GROQ_API_KEY not set")
    try:
        resp = requests.post(
            GROQ_BASE_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "max_tokens": max_tokens,
                "temperature": 0.2,
            },
            timeout=30,
        )
       resp.raise_for_status()
           data = resp.json()
           text = data["choices"][0]["message"]["content"]
           return LLMResponse(text=text, provider="groq", model=model, latency_s=time.time() - t0)
       except requests.HTTPError as e:
           detail = ""
           try:
               detail = e.response.json().get("error", {}).get("message", e.response.text)
           except Exception:  # noqa: BLE001
               detail = getattr(e.response, "text", str(e))
           return LLMResponse(text="", provider="groq", model=model,
                               latency_s=time.time() - t0,
                               error=f"{e.response.status_code}: {detail}")
       except Exception as e:  # noqa: BLE001
           return LLMResponse(text="", provider="groq", model=model,
                               latency_s=time.time() - t0, error=str(e))


def _call_openrouter(model: str, system: str, user: str, max_tokens: int = 800) -> LLMResponse:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    t0 = time.time()
    if not api_key:
        return LLMResponse(text="", provider="openrouter", model=model,
                            latency_s=0.0, error="OPENROUTER_API_KEY not set")
    try:
        resp = requests.post(
            OPENROUTER_BASE_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://github.com/",
                "X-Title": "Serendib Spice & Tea Co-Pilot",
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "max_tokens": max_tokens,
                "temperature": 0.3,
            },
            timeout=45,
        )
        resp.raise_for_status()
        data = resp.json()
        text = data["choices"][0]["message"]["content"]
        return LLMResponse(text=text, provider="openrouter", model=model, latency_s=time.time() - t0)
    except requests.HTTPError as e:
        detail = ""
        try:
            detail = e.response.json().get("error", {}).get("message", e.response.text)
        except Exception:  # noqa: BLE001
            detail = getattr(e.response, "text", str(e))
        return LLMResponse(text="", provider="openrouter", model=model,
                            latency_s=time.time() - t0,
                            error=f"{e.response.status_code}: {detail}")
    except Exception as e:  # noqa: BLE001
        return LLMResponse(text="", provider="openrouter", model=model,
                            latency_s=time.time() - t0, error=str(e))


def call_llm(task: str, system: str, user: str, max_tokens: int = 512) -> LLMResponse:
    """Route a call to the model registered for `task`
    (one of: 'router', 'rerank_reflect', 'synthesis')."""
    cfg = MODEL_REGISTRY[task]
    if cfg["provider"] == "groq":
        return _call_groq(cfg["model"], system, user, max_tokens=max_tokens)
    return _call_openrouter(cfg["model"], system, user, max_tokens=max_tokens)
