# Syncs Documentation

This directory contains the sync specification YAMLs for the application, following the **WYSIWID** (What You See Is What It Does) pattern.

## Sync Pattern

Syncs orchestrate cross-concept coordination. They are the **only** place where one concept triggers actions in another concept. Concepts themselves never import or call other concepts directly.

### Sync YAML Structure

```yaml
sync: "unique-sync-identifier"
description: "Brief purpose of the sync"
when:  # Trigger: Action completion that kicks off the sync
  concept: "ConceptName"
  action: "action_name"
where:  # Guards: Sync-layer conditions (NEVER in concept YAMLs)
  - condition: "Human-readable condition"
    query:
      concept: "ConceptName"
      action: "action_name"
      args: ["arg1"]
then:  # Invocations: Downstream cross-concept actions
  - concept: "ConceptName"
    action: "action_name"
    args: ["arg1"]
    compensating_action:  # Rollback for failed syncs
      concept: "ConceptName"
      action: "undo_action"
      args: ["arg1"]
```

## Core Principles

1. **Concepts are islands** — A concept file must never import from another concept
2. **Cross-concept references are opaque IDs** — Only `company_id`, `position_id`, etc. never full objects
3. **Syncs live in `syncs/`** — Not inside concepts
4. **Actions return ActionRecords** — The sync engine uses these to trigger downstream rules
5. **Guards are sync-layer concerns** — In `where` sections, never inside concept actions
6. **Compensating actions for rollback** — In `then[].compensating_action` sections

## Syncs by Trigger Concept

### Triggered by Position
| Sync | Purpose |
|------|---------|
| [on_position_create_add_to_portfolio.yaml](on_position_create_add_to_portfolio.yaml) | Add new positions to portfolio |
| [on_position_liquidate_remove_from_portfolio.yaml](on_position_liquidate_remove_from_portfolio.yaml) | Remove liquidated positions from portfolio |

### Triggered by InvestmentMemo
| Sync | Purpose |
|------|---------|
| [on_investment_memo_create_trigger_documents.yaml](on_investment_memo_create_trigger_documents.yaml) | Auto-create all analysis documents |
| [on_investment_memo_finalize_trigger_downstream.yaml](on_investment_memo_finalize_trigger_downstream.yaml) | Finalize documents and record decision |

### Triggered by FinancialMetrics
| Sync | Purpose |
|------|---------|
| [on_financial_metrics_update_recalculate_intrinsic_value.yaml](on_financial_metrics_update_recalculate_intrinsic_value.yaml) | Recalculate intrinsic value when metrics update |

### Triggered by IntrinsicValue
| Sync | Purpose |
|------|---------|
| [on_intrinsic_value_recalculate_update_margin_of_safety.yaml](on_intrinsic_value_recalculate_update_margin_of_safety.yaml) | Update margin of safety after IV recalculation |

### Triggered by MarginOfSafety
| Sync | Purpose |
|------|---------|
| [on_margin_of_safety_undervalued_alert.yaml](on_margin_of_safety_undervalued_alert.yaml) | Alert when stock becomes undervalued |

### Triggered by MarketData
| Sync | Purpose |
|------|---------|
| [on_market_data_update_check_alerts.yaml](on_market_data_update_check_alerts.yaml) | Check for price drop alerts |

### Triggered by DecisionLog
| Sync | Purpose |
|------|---------|
| [on_decision_log_record_create_bias_audit.yaml](on_decision_log_record_create_bias_audit.yaml) | Auto-create bias audit for decisions |

### Triggered by BiasAudit
| Sync | Purpose |
|------|---------|
| [on_bias_audit_lollapalooza_alert.yaml](on_bias_audit_lollapalooza_alert.yaml) | Alert on high lollapalooza effect |

### Triggered by AgentPersona
| Sync | Purpose |
|------|---------|
| [on_agent_persona_set_active_update_bias_sensitivities.yaml](on_agent_persona_set_active_update_bias_sensitivities.yaml) | Update bias sensitivities on persona change |

## Sync Flow Diagram

```
Position.create
    └──> Portfolio.add_position

InvestmentMemo.create
    ├──> InvestmentThesis.create
    ├──> PreMortem.create
    ├──> ChecklistAudit.create
    ├──> MoatStrengthAssessment.create
    └──> AIDueDiligence.create

InvestmentMemo.finalize
    ├──> DecisionLog.record_decision
    ├──> InvestmentThesis.finalize
    ├──> PreMortem.finalize
    └──> BiasAudit.finalize

FinancialMetrics.update
    └──> IntrinsicValue.recalculate
            └──> MarginOfSafety.recalculate_status
                    └──> Alert.create (if undervalued)

MarketData.fetch_historical
    └──> Alert.create (if price drop)

DecisionLog.record_decision
    └──> BiasAudit.create

BiasAudit.calculate_lollapalooza
    └──> Alert.create (if score > 7)

AgentPersona.set_active
    └──> BiasAudit.update_bias_sensitivities
```

## Implementation Note

These are **specification** YAMLs documenting the intended sync behavior. The actual implementation lives in `app/syncs/` as Python modules that register with the sync engine in `app/engine/sync_engine.py`.
