# Decision log

1. **AppleSupport**: high volume, varied technical issues, repeatable resolution patterns.
2. **10 intents**: small enough to be operationally useful; avoids fragile over-granularity.
3. **Single primary intent**: clean routing/evaluation; multi-intent cases become an explicit failure mode.
4. **Retrieval-grounded reply drafting**: reduces unsupported policy invention.
5. **Conservative escalation**: account, payment, data-loss and hardware/safety cases default to humans.
6. **Confidence + retrieval thresholds**: both semantic certainty and precedent strength matter.
7. **Auto-handle precision is first-class**: safe selective automation beats reckless high coverage.
8. **Macro-F1**: rare intents must count.
9. **Two baselines**: majority class and keyword router.
10. **LLM judge is not trusted alone**: compare against human-scored examples.
11. **Historical replies are not current policy**: they are behavioral precedents only.
12. **PII signals escalate**: no account-sensitive automation.
13. **Subsample by design**: full dataset is unnecessary for this proof.
14. **No multi-turn memory in v1**: prove first-turn triage before adding state.
15. **Reproducibility over benchmark chasing**: fixed seeds and CPU-friendly tooling.
