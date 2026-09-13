# Hiver AI Support Agent

SDE Intern take-home focused on AppleSupport-style customer-support conversations.

## What it does
- classifies incoming support messages into a compact intent taxonomy
- retrieves a historically grounded response pattern
- decides **auto-handle vs escalate** using intent risk, confidence, retrieval strength, and safety/PII signals
- compares against majority and keyword baselines
- includes an LLM-as-judge harness plus separate human-review utilities
- includes a Streamlit demo

## Run

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -r requirements.txt
python -m src.evaluate
python -m src.cli "My iPhone battery is draining after the latest update"
```

Demo:

```bash
streamlit run app.py
```

## Dataset
The raw Kaggle `twcs.csv` is intentionally not committed. Put it at `data/raw/twcs.csv`, then run:

```bash
python scripts_prepare.py --input data/raw/twcs.csv --out data/apple_pairs.csv
```

## Evaluation snapshot
Current reproducible run on the included AI-assisted review set:

| Metric | Value |
|---|---:|
| Majority macro-F1 | 0.018 |
| Keyword macro-F1 | 0.742 |
| Agent macro-F1 | 0.986 |
| Auto-handle coverage | 0.129 |
| Auto-handle precision | 1.000 |
| Mean proxy reply score | 4.036 |

These numbers are diagnostic, not production claims. The included labels are AI-assisted review data; I do **not** claim they were manually annotated by the candidate.

## Review tools

```bash
streamlit run review_labels.py
python -m src.evaluate
python -m src.llm_judge --n 50
streamlit run review_judge.py
```

`src/llm_judge.py` computes weighted Cohen's kappa when independent human scores are present. It does not fabricate missing human ratings.

## Repository map

```text
app.py
scripts_prepare.py
src/
  agent.py
  cli.py
  evaluate.py
  llm_judge.py
data/
  ANNOTATION_GUIDE.md
  historical_resolutions.csv
results/
  metrics.json
REPORT.md
DECISION_LOG.md
ATTRIBUTIONS.md
review_labels.py
review_judge.py
```

See `REPORT.md` for system design, evaluation interpretation, failure modes, and next steps.
