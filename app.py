"""Reflection A/B demo — compare Generic coach vs sample Retreat guide."""

from __future__ import annotations

import json
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from intelligence import (
    GenericRunError,
    GuideOutput,
    GuideRunError,
    get_active_model,
    run_generic,
    run_guide,
)
from prompts import get_defaults

load_dotenv()

SCENARIOS_PATH = Path(__file__).parent / "scenarios.json"
GUIDE_FALLBACK = (
    "I wasn't able to shape a structured reflection just now. "
    "Take a breath—what feels most true in what you shared?"
)

CUSTOM_PLACEHOLDER = "What's on your mind? (1–3 sentences)"


def _load_scenarios() -> list[dict]:
    return json.loads(SCENARIOS_PATH.read_text())


def _scenario_labels(scenarios: list[dict]) -> dict[str, str]:
    labels = {s["id"]: s["label"] for s in scenarios}
    labels["custom"] = "Your own words"
    return labels


def _prefill_for(scenario_id: str, scenarios: list[dict]) -> str:
    if scenario_id == "custom":
        return ""
    for scenario in scenarios:
        if scenario["id"] == scenario_id:
            return scenario["user_text"]
    return ""


def _init_session(scenarios: list[dict]) -> None:
    if "prompts" not in st.session_state:
        st.session_state.prompts = get_defaults()
    if "scenario_id" not in st.session_state:
        st.session_state.scenario_id = "rest"
    if "user_text" not in st.session_state:
        st.session_state.user_text = _prefill_for("rest", scenarios)
    if "text_dirty" not in st.session_state:
        st.session_state.text_dirty = False
    if "last_run" not in st.session_state:
        st.session_state.last_run = None
    if "last_generic_output" not in st.session_state:
        st.session_state.last_generic_output = None
    if "last_guide_output" not in st.session_state:
        st.session_state.last_guide_output = None


def _sync_prompt_edits() -> None:
    for key in ("generic_system", "guide_system", "fewshot_user", "fewshot_assistant"):
        widget_key = f"edit_{key}"
        if widget_key in st.session_state:
            st.session_state.prompts[key] = st.session_state[widget_key]


def _snapshot_prompts() -> dict[str, str]:
    return dict(st.session_state.prompts)


def _render_generic_column(text: str) -> None:
    st.subheader("Generic coach")
    st.caption("Default supportive coach — tips and encouragement")
    if st.session_state.last_generic_output is None:
        st.info("Click Compare to see a response.")
        return
    st.markdown(st.session_state.last_generic_output)
    last_run = st.session_state.last_run
    if last_run:
        with st.expander("View prompt used"):
            st.code(last_run["generic_system"], language=None)
            st.caption(f"Human message: {text[:200]}{'…' if len(text) > 200 else ''}")
            st.caption(f"Model: {get_active_model()} · temperature 0.6 · max_tokens 800")


def _render_guide_column(text: str) -> None:
    st.subheader("Retreat guide")
    st.caption("Sample retreat guide — methodology + structure")
    output: GuideOutput | None = st.session_state.last_guide_output
    if output is None:
        st.info("Click Compare to see a response.")
        return
    st.markdown(
        f'<div class="guide-panel"><strong>Reflection</strong><p>{output.reflection}</p>'
        + (
            f'<strong>Something to sit with</strong><p>{output.follow_up_question}</p>'
            if output.follow_up_question
            else ""
        )
        + "</div>",
        unsafe_allow_html=True,
    )
    last_run = st.session_state.last_run
    if last_run:
        with st.expander("View prompt used"):
            st.code(last_run["guide_system"], language=None)
            st.text("Few-shot user:")
            st.code(last_run["fewshot_user"], language=None)
            st.text("Few-shot assistant:")
            st.code(last_run["fewshot_assistant"], language=None)
            st.caption(f"Human message: {text[:200]}{'…' if len(text) > 200 else ''}")
            st.caption(f"Model: {get_active_model()} · temperature 0.6 · max_tokens 800")


def main() -> None:
    st.set_page_config(page_title="Reflection comparison", layout="wide")
    st.markdown(
        """<style>
        div[data-testid="column"]:first-of-type { opacity: 0.92; }
        .guide-panel { padding: 1rem; border-radius: 8px; background: #FFFCF8; }
        </style>""",
        unsafe_allow_html=True,
    )

    scenarios = _load_scenarios()
    labels = _scenario_labels(scenarios)
    _init_session(scenarios)

    st.title("Reflection comparison")
    st.caption("Prototype — intelligence layer demo (sample retreat guide)")

    with st.sidebar:
        st.warning(
            "Not medical advice, therapy, or emergency support. "
            "For product demonstration only."
        )
        st.header("Scenario")
        choice = st.radio(
            "Choose a starting point",
            options=list(labels.keys()),
            format_func=lambda k: labels[k],
            horizontal=True,
            key="scenario_radio",
            index=list(labels.keys()).index(st.session_state.scenario_id),
        )
        if choice != st.session_state.scenario_id:
            st.session_state.scenario_id = choice
            if not st.session_state.text_dirty:
                st.session_state.user_text = _prefill_for(choice, scenarios)

        with st.expander("Expert mode", expanded=False):
            st.caption(
                "Edit prompts below, then click Compare again. "
                "Changes apply to the next run only (session). "
                "Reset restores prompts.py defaults."
            )
            tab_generic, tab_guide, tab_few = st.tabs(
                ["Generic coach", "Retreat guide", "Few-shot example"]
            )
            with tab_generic:
                st.text_area(
                    "System prompt",
                    value=st.session_state.prompts["generic_system"],
                    height=200,
                    key="edit_generic_system",
                )
            with tab_guide:
                st.text_area(
                    "System prompt",
                    value=st.session_state.prompts["guide_system"],
                    height=280,
                    key="edit_guide_system",
                )
            with tab_few:
                st.text_area(
                    "Few-shot user",
                    value=st.session_state.prompts["fewshot_user"],
                    height=80,
                    key="edit_fewshot_user",
                )
                st.text_area(
                    "Few-shot assistant (JSON)",
                    value=st.session_state.prompts["fewshot_assistant"],
                    height=120,
                    key="edit_fewshot_assistant",
                )
            if st.button("Reset prompts to defaults"):
                st.session_state.prompts = get_defaults()
                for key in (
                    "edit_generic_system",
                    "edit_guide_system",
                    "edit_fewshot_user",
                    "edit_fewshot_assistant",
                ):
                    st.session_state.pop(key, None)
                st.rerun()

    user_text = st.text_area(
        "Your words",
        value=st.session_state.user_text,
        height=120,
        max_chars=2000,
        placeholder=CUSTOM_PLACEHOLDER if st.session_state.scenario_id == "custom" else None,
        key="user_text_area",
    )
    if user_text != st.session_state.user_text:
        st.session_state.text_dirty = True
    st.session_state.user_text = user_text

    with st.expander("How this works"):
        st.markdown(
            f"Both arms use the same model (**{get_active_model()}**) with different prompts. "
            "Generic coach gets a supportive system prompt; the sample retreat guide adds "
            "structure, rules, and a few-shot example. Edit prompts in **Expert mode**, "
            "then Compare again—week one replaces defaults in `prompts.py` with your facilitators' voice."
        )

    compare = st.button("Compare", type="primary")
    if compare:
        if not user_text.strip():
            st.error("Please enter a few words before comparing.")
        else:
            _sync_prompt_edits()
            snapshot = _snapshot_prompts()
            st.session_state.last_run = snapshot
            with st.spinner("Comparing both guides…"):
                try:
                    st.session_state.last_generic_output = run_generic(
                        user_text, snapshot
                    )
                except GenericRunError as exc:
                    st.session_state.last_generic_output = None
                    st.session_state.generic_error = str(exc)
                else:
                    st.session_state.pop("generic_error", None)

                try:
                    st.session_state.last_guide_output = run_guide(user_text, snapshot)
                except GuideRunError as exc:
                    st.session_state.last_guide_output = GuideOutput(
                        reflection=GUIDE_FALLBACK,
                        follow_up_question=None,
                    )
                    st.session_state.guide_error = str(exc)
                else:
                    st.session_state.pop("guide_error", None)

    col_generic, col_guide = st.columns(2)
    with col_generic:
        if st.session_state.get("generic_error"):
            st.error(st.session_state["generic_error"])
        _render_generic_column(user_text)
    with col_guide:
        if st.session_state.get("guide_error"):
            st.warning(
                "Guide used fallback copy after a parse/API issue. "
                f"({st.session_state['guide_error']})"
            )
        _render_guide_column(user_text)


if __name__ == "__main__":
    main()
