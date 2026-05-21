# Reflection agent

Streamlit app with LangChain, managed with [uv](https://docs.astral.sh/uv/).

## Setup

```bash
uv sync
```

Packages are resolved with `exclude-newer = "7 days"` so only releases at least 7 days old are used.

## Run the hello-world app

```bash
uv run streamlit run app/hello.py
```

Open http://localhost:8501 in your browser.
