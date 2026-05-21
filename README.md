# Reflection A/B demo

Streamlit app that compares **Generic coach** vs **sample Retreat guide** on the same model and user input—proving the intelligence layer (prompts + structure), not model choice, drives the difference.

Managed with [uv](https://docs.astral.sh/uv/).

## Setup

```bash
uv sync
cp .env.example .env
# Add OPENAI_API_KEY to .env
```

Packages use `exclude-newer = "7 days"` so only releases at least 7 days old are selected.

Optional: override the model with `REFLECTION_MODEL=gpt-4o-mini` in `.env` if `gpt-5-nano` is unavailable.

## Run locally

```bash
uv run streamlit run app.py
```

Open http://localhost:8501

## Tests

```bash
uv run pytest tests/ -v
```

Unit tests mock the LLM—no API key spend.

## Demo script (~3 min)

1. **20 sec:** “Same model, same words—only the intelligence layer changes.”
2. Scenario **Rest / burnout** → **Compare**.
3. Read one Generic sentence that sounds like a wellness bot.
4. Read Guide **Reflection**; point at echoed specificity; read **Something to sit with**.
5. **30 sec:** “Week one with your facilitators replaces this sample guide—the architecture stays the same.”
6. Optional: **Hard to name feelings** scenario, Compare again.
7. Close: “Phase 1 of the roadmap—voice before fine-tuning or heavy memory.”

## Deploy (Streamlit Community Cloud)

1. Push this repo to GitHub.
2. [share.streamlit.io](https://share.streamlit.io) → **New app** → connect repo.
3. Main file path: `app.py`
4. Add secret `OPENAI_API_KEY` in app settings.
5. Open the shared URL ~2 minutes before a live call (cold start).

## Layout

```
app.py              # Streamlit compare UI + Expert mode
prompts.py          # get_defaults() — version-controlled prompts
intelligence.py     # LangChain chains (run_generic, run_guide)
scenarios.json      # Canned demo scenarios
.streamlit/config.toml
```
