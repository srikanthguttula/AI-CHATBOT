from typing import List, Dict, Any, Optional
from openai import OpenAI
from ..config import settings

client = OpenAI(api_key=settings.openai_api_key)


def build_system_prompt(persona: Optional[str]) -> str:
    """Builds a system prompt with an optional persona style."""
    base = "You are a helpful assistant."
    if not persona:
        return base

    personas = {
        "tutor": "You are a kind Tutor. Explain concepts simply with examples.",
        "therapist": "You are a supportive Therapist. Respond with empathy.",
    }
    return f"{base} {personas.get(persona.lower(), f'Persona: {persona}.')}"


async def chat_completion(
    message: str,
    persona: Optional[str],
    history: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Generates a chat completion from the OpenAI API."""
    system_prompt = build_system_prompt(persona)

    messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]
    if history:
        for m in history:
            if m.get("role") in {"system", "user", "assistant"}:
                messages.append({"role": m["role"], "content": m["content"]})
    messages.append({"role": "user", "content": message})

    completion = client.chat.completions.create(
        model=settings.openai_model,
        messages=messages,
        temperature=0.3,
        max_tokens=512,
    )

    choice = completion.choices[0].message
    return {
        "response": choice.content or "",
        "model": completion.model,
        "usage": {
            "prompt_tokens": getattr(completion.usage, "prompt_tokens", None),
            "completion_tokens": getattr(completion.usage, "completion_tokens", None),
            "total_tokens": getattr(completion.usage, "total_tokens", None),
        },
        "persona_applied": persona,
    }
