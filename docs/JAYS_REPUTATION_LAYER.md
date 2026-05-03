# Jay's Reputation Layer

Status: ACTIVE_DOCTRINE
Epoch: GROK_EPOCH_001
Operator: Jay Wisdom
Public identity: jaywisdom.base
Research anchor: jaywisdom.eth
System: Personal / Business / Private / Family / ALMS

## Core thesis

Jay's Reputation Layer separates public proof, business trust, private life, family identity, and ALMS verification so no layer impersonates another.

Reputation must be earned by receipts, preserved by boundaries, and protected from AI-generated narrative drift.

```text
Personal voice is not business authority.
Business identity is not private access.
Private life is not public evidence.
Family identity is not wallet authority.
ALMS receipts are not personal worth.
```

## Five reputation domains

```json
{
  "personal": "Jay's public voice, ideas, humor, learning, and creative expression",
  "business": "professional credibility, projects, research, client/public-facing work",
  "private": "non-public life, sensitive records, private communications, personal security",
  "family": "Wisdom Family learning, legacy, consent, child-safe and household-safe boundaries",
  "alms": "receipt-backed verification, replay, roots, public explanations, anchors"
}
```

## Domain separation rule

No domain may silently promote a claim into another domain.

Examples:

```json
{
  "personal_post": "may express opinion but cannot claim ALMS VERIFIED without receipt",
  "business_claim": "must cite project evidence or receipt when factual",
  "private_record": "must not be exposed as public proof without consent",
  "family_artifact": "must pass Family 702 safety before public release",
  "alms_receipt": "proves artifact state, not human value"
}
```

## Reputation states

```json
[
  "DRAFT",
  "PRIVATE",
  "FAMILY_REVIEW",
  "BUSINESS_REVIEW",
  "PUBLIC_CLAIM",
  "RECEIPT_BACKED",
  "REPLAYED",
  "ROOTED",
  "ANCHORED",
  "BLOCKED",
  "RETRACTED",
  "CORRECTED"
]
```

## Protected boundaries

1. Private records are private by default.
2. Family artifacts require safety review before publication.
3. Business claims require evidence when factual.
4. Public claims may be funny, but proof labels must remain exact.
5. ALMS can verify artifacts; it cannot define personal worth.
6. Zora identities can distribute reputation artifacts; they cannot replace receipts.
7. AI models may summarize reputation signals; they may not assign final reputation authority.

## AI reputation protection

AI systems must not create, alter, or amplify reputation claims about Jay, the Wisdom Family, or ALMS without traceability.

Required fields for AI-generated reputation claims:

```json
{
  "claim": "string",
  "domain": "personal | business | private | family | alms",
  "source": "string",
  "receipt_path": "string | UNSET",
  "status": "SUGGESTION | UNVERIFIED_CLAIM | RECEIPT_BACKED | REPLAYED | ROOTED | ANCHORED",
  "correction_path": "string"
}
```

## Public labels

Allowed public labels:

```json
[
  "PERSONAL_OPINION",
  "BUSINESS_PROFILE",
  "FAMILY_SAFE_ARTIFACT",
  "RESEARCH_IN_PROGRESS",
  "RECEIPT_BACKED",
  "REPLAYED",
  "ROOTED",
  "ANCHOR_PENDING"
]
```

Blocked labels unless receipts exist:

```json
[
  "VERIFIED",
  "OFFICIAL",
  "CERTIFIED",
  "ONCHAIN_CONFIRMED",
  "ENS_COMPLETE",
  "CONTRACT_CONFIRMED"
]
```

## Reputation recovery

If a public claim is wrong, the system must support correction without erasure.

```text
wrong claim -> correction receipt -> version bump -> public explanation -> updated reputation state
```

Correction is not weakness. Uncorrected drift is weakness.

## Operation Lilu / Zora identity boundary

Operation Lilu may publish identity cards, learning artifacts, Meme Court records, and public explanation cards.

But:

```text
Zora identity is distribution.
ALMS is verification.
Jay remains the operator.
Receipts remain the authority.
```

## ALMS reputation rule

```text
A reputation claim becomes durable only when it has a source, receipt, replay status, and correction path.
```

## Next action

Apply this layer to public pages, Zora identity cards, family artifacts, business profiles, and citizen verification interfaces.
