# Duties and separation of responsibilities

## Roles
- **Maker — CivicPulse AI:** retrieves public-source data, validates response structure, computes the documented screening indicator, and drafts a response brief.
- **Checker — Human reviewer:** independently checks source freshness, local context, official alerts, data gaps, and the proposed interpretation before any operational use.

## Conflict Matrix
- The Maker cannot approve its own operational recommendation.
- The Checker must be a human reviewer independent of the agent's generation step.
- The agent cannot impersonate or claim approval from a human checker.

## Handoff
1. Maker produces an evidence-linked preliminary brief.
2. Checker reviews the evidence and limitations.
3. Only the responsible human authority decides whether any action is appropriate.

## Enforcement
Human review is mandatory for operational use. The agent has no dispatch or command authority.
