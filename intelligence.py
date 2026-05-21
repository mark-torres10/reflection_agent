"""LangChain chains for Generic coach vs Retreat guide arms."""

from __future__ import annotations

import json
import os

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

MODEL_PRIMARY = "gpt-5-nano"
MODEL_FALLBACK = "gpt-4o-mini"
# gpt-5-nano may spend completion budget on reasoning; keep headroom for visible text.
MAX_TOKENS = 800


class GuideOutput(BaseModel):
    reflection: str = Field(description="2-4 sentence calm reflection mirroring the user")
    follow_up_question: str | None = Field(
        description="At most one optional deepening question"
    )


class IntelligenceError(Exception):
    """Base error for intelligence layer failures."""


class GenericRunError(IntelligenceError):
    """Generic coach arm failed."""


class GuideRunError(IntelligenceError):
    """Retreat guide arm failed."""


def _resolve_model() -> str:
    override = os.getenv("REFLECTION_MODEL")
    if override:
        return override
    return MODEL_PRIMARY


def _make_llm(model: str | None = None) -> ChatOpenAI:
    resolved = model or _resolve_model()
    kwargs: dict = {
        "model": resolved,
        "temperature": 0.6,
        "max_tokens": MAX_TOKENS,
    }
    if resolved.startswith("gpt-5"):
        kwargs["reasoning_effort"] = "minimal"
    return ChatOpenAI(**kwargs)


def _extract_text(result) -> str:
    if isinstance(result, str):
        return result.strip()
    content = getattr(result, "content", result)
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                parts.append(str(block.get("text", "")))
        return "".join(parts).strip()
    return str(content).strip()


_llm: ChatOpenAI | None = None
_active_model: str | None = None


def get_active_model() -> str:
    global _llm, _active_model
    if _active_model is None:
        _active_model = _resolve_model()
        _llm = _make_llm(_active_model)
    return _active_model


def get_llm() -> ChatOpenAI:
    get_active_model()
    assert _llm is not None
    return _llm


def _build_generic_chain(prompts: dict[str, str]):
    template = ChatPromptTemplate.from_messages(
        [
            ("system", prompts["generic_system"]),
            ("human", "{user_text}"),
        ]
    )
    return template | get_llm()


def _build_guide_chain(prompts: dict[str, str]):
    template = ChatPromptTemplate.from_messages(
        [
            ("system", prompts["guide_system"]),
            HumanMessage(content=prompts["fewshot_user"]),
            AIMessage(content=prompts["fewshot_assistant"]),
            ("human", "{user_text}"),
        ]
    )
    return template | get_llm().with_structured_output(GuideOutput)


def run_generic(user_text: str, prompts: dict[str, str]) -> str:
    try:
        result = _build_generic_chain(prompts).invoke({"user_text": user_text})
        content = _extract_text(result)
        if not content:
            raise GenericRunError("Empty response from generic coach")
        return content
    except IntelligenceError:
        raise
    except Exception as exc:
        raise GenericRunError(str(exc)) from exc


def run_guide(user_text: str, prompts: dict[str, str]) -> GuideOutput:
    try:
        result = _build_guide_chain(prompts).invoke({"user_text": user_text})
        if isinstance(result, GuideOutput):
            return result
        if isinstance(result, dict):
            return GuideOutput.model_validate(result)
        raise GuideRunError("Unexpected guide response type")
    except IntelligenceError:
        raise
    except Exception as exc:
        raise GuideRunError(str(exc)) from exc


def parse_fewshot_assistant(raw: str) -> dict[str, str | None]:
    data = json.loads(raw)
    return {
        "reflection": data.get("reflection", ""),
        "follow_up_question": data.get("follow_up_question"),
    }
