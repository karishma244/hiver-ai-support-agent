# Hiver SDE Intern Take-Home — AppleSupport AI Support Agent

## Problem framing
I treat this as a selective-automation problem, not a chatbot benchmark. Good means correctly routing a customer message, drafting a reply traceable to historical handling patterns, and abstaining when the downside of a wrong answer is high. Account access, payment/refund, data-loss, and hardware-safety mistakes are more costly than escalation.

## System
Pipeline: inbound request → TF-IDF + logistic-regression intent classifier → nearest historical-resolution pattern → confidence/risk gate → auto-handle or escalate with reason.

Intents: `battery_charging`, `ios_update_performance`, `network_connectivity`, `apple_id_account`, `app_store_purchases`, `icloud_backup_storage`, `device_hardware_damage`, `audio_calls_media`, `keyboard_messaging`, `general_other`.

## Evaluation
The evaluation harness reports intent accuracy and macro-F1, auto-handle precision and coverage, and a proxy reply-quality score. It compares the agent with a majority-class predictor and a transparent keyword router.

Current reproducible run on the included provisional evaluation set:

| Metric | Value |
|---|---:|
| Majority macro-F1 | 0.018 |
| Keyword macro-F1 | 0.742 |
| Agent macro-F1 | 0.986 |
| Auto-handle coverage | 0.129 |
| Auto-handle precision | 1.000 |
| Mean proxy reply score | 4.036 |

These numbers are deliberately not presented as production performance. The included evaluation labels are a runnable review aid and the raw Kaggle dataset is not committed.

## LLM-as-judge
`src/llm_judge.py` supports 1–5 scoring on relevance, groundedness, safety, and brand style and computes weighted Cohen's kappa when independent ratings are available. Judge output is treated as diagnostic rather than ground truth.

## Top failure modes
1. Multi-intent messages can lose a secondary issue under single-label routing.
2. Generic complaints often need clarification rather than confident automation.
3. Hardware-vs-software ambiguity requires safety rules to override semantic similarity.
4. Historical behavior is not necessarily current policy.
5. Sarcasm and noisy social text can stress literal keyword systems.

## What is misleading about my headline number?
A single F1/accuracy number hides class imbalance, subjective labels, distribution shift from historical Twitter support, selective coverage, and the gap between correct intent and a safe useful reply. Auto-handle precision can also look artificially strong when a system escalates most cases, so precision must be shown with coverage.

## One more week
I would add sentence-embedding retrieval, multi-turn context, a versioned current-policy knowledge base, threshold calibration against explicit false-automation costs, double annotation for label agreement, and adversarial tests for PII, fraud, prompt injection, unsupported account/refund actions, and hardware safety.
