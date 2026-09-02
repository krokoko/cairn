# Agentic payment agent fixture profile

Minimal profile: LLM agent with tools for payments, refunds, and approvals.

## Signals

- `agent/tools/payment.py` — `charge`, `refund` tool handlers
- `agent/policy.yaml` — tool allowlist
- No static tool verification, no temporal invariants on refunds
- Production traces available

## Component classification

- Archetype: Agentic application/workflow
- Bug surface: B (money) + C (async tool orchestration)
- Criticality: High
