# Data Stewardship Rules

1. **Synthetic only.** Never copy or infer production data. All values must be
   generated via rules defined in the repository.
2. **Schema evolution.** Additive schema changes require review by a data
   steward; breaking changes require product owner approval plus LOB sign-off.
3. **PII hygiene.** Even though data is synthetic, avoid sensitive combinations
   that could be mistaken for real customer information.
4. **Versioning discipline.** Every snapshot must include updated metadata and
   version labels before distribution.
5. **Prompt alignment.** Use the relevant sub-prompt when modifying schemas,
   generators, validators, or governance files so that the Critic step verifies
   compliance.
