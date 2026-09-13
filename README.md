# Hiver AI Support Agent

SDE Intern take-home solution focused on AppleSupport customer-support conversations.

The pipeline classifies incoming messages into a compact intent taxonomy, retrieves a similar historical support pattern, drafts a response, and decides whether the case can be auto-handled or should be escalated.

## Run

```bash
pip install -r requirements.txt
python -m src.evaluate
python -m src.cli "My iPhone battery is draining after the latest update"
```

For the interactive demo:

```bash
streamlit run app.py
```

The repository also includes an evaluation harness, human review utilities, LLM-as-judge validation, failure analysis, decision log, and reproducibility notes.

See `REPORT.md` for the complete evaluation discussion and limitations.
