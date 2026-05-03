# Recursive Practices and Model Failures

Status: ACTIVE_DOCTRINE
Epoch: GROK_EPOCH_001
Operator: Jay Wisdom
Public identity: jaywisdom.base
Research anchor: jaywisdom.eth

## Core thesis

External AI systems are useful stress nodes, not authorities.

A model can suggest, critique, summarize, and attack a proof chain. A model cannot be the proof chain.

```text
model output is not evidence
repo bytes are evidence
hashes bind evidence
replay tests evidence
roots aggregate evidence
anchors externalize evidence
```

## Trigger event

During GROK_EPOCH_001, Grok provided useful adversarial feedback but became unavailable due to rate limits and high demand.

This failure is part of the audit record.

```json
{
  "external_model": "Grok",
  "failure_mode": "rate_limit_or_high_demand",
  "system_response": "continue with repo-local verification",
  "lesson": "no proof pipeline may depend on external model availability"
}
```

## Recursive practice rules

1. AI may propose.
2. Repo must verify.
3. Hashes must come from bytes.
4. Replay must test stored artifacts.
5. Model outages become audit evidence.
6. Model confidence is not proof.
7. No external model may promote a claim to VERIFIED.
8. Legal, public, or civic claims require receipts, not narrative.

## Legal and governance boundary

If a process depends on a black-box assistant, rate limits, hidden prompts, UI state, or unavailable model context, then it is not a verification system.

It is a workflow with a liability gap.

ALMS closes that gap by making proof depend on:

- stored files,
- schemas,
- deterministic scripts,
- hashes,
- replay reports,
- roots,
- public explanations,
- optional external anchors.

## Dirty tactics the system must survive

```json
{
  "risks": [
    "AI hallucinated hash",
    "AI premature VERIFIED label",
    "AI rate limit during audit",
    "AI asks for trust instead of evidence",
    "AI collapses source_url and frozen_artifact",
    "AI confuses claim wrapper with source artifact",
    "AI gives schema field that validator does not read",
    "AI availability failure interrupts review"
  ]
}
```

## Required response pattern

When any AI system fails, drifts, or becomes unavailable:

```text
1. Freeze the current repo state.
2. Record the model failure.
3. Continue with deterministic local tools.
4. Do not wait for the model to become available.
5. Do not promote any claim based on model output alone.
```

## Current GROK_EPOCH_001 lesson

Grok was valuable as an adversarial node. It caught:

- self-referential frozen artifact risk,
- schema field mismatch,
- multi-claim root risk,
- snapshot-level proof boundary.

Grok also failed availability.

Both facts matter.

```json
{
  "grok_value": "useful adversarial review",
  "grok_limit": "not reliable infrastructure",
  "alms_response": "absorb useful findings, reject dependency"
}
```

## Doctrine

```text
External models may help break the system.
Only receipts may build trust.
```

## Next action

Keep building the MN multi-claim lane using repo-local hashes, replay, state roots, and public explanations. Treat Grok as optional pressure, not required infrastructure.
