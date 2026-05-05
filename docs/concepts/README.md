# Concepts Documentation

This directory contains the concept definitions for the application, following the **Concept Design** paradigm (Daniel Jackson) implemented via the **WYSIWID** (What You See Is What It Does) structural pattern.

## Concept Design Principles

Each concept in this directory:
- Has its **own state** (owns its data — no other concept touches it)
- Exposes **actions** (public methods that modify state and return an ActionRecord)
- Has an **operational principle** — an invariant it maintains internally
- **Never imports another concept**

Cross-concept coordination happens exclusively in the `syncs/` layer, not inside concepts.

## Concepts by Domain

### Data Layer
Core data entities that serve as the foundation for analysis.

| Concept | Purpose | Cross-Concept References |
|---------|---------|-------------------------|
| [Company](company.yaml) | Single source of truth for company identity | Referenced by: Position, Watchlist, InvestmentMemo, MarketData, FinancialMetrics, Dividend, AIDueDiligence, MoatStrengthAssessment, ChecklistAudit, PreMortem, IntrinsicValue, MarginOfSafety |
| [MarketData](market_data.yaml) | Historical and current pricing data | References: company_id |
| [FinancialMetrics](financial_metrics.yaml) | Quantitative financial data from public sources | References: company_id |
| [Dividend](dividend.yaml) | Dividend payment history | References: company_id |

### Analysis Layer
Concepts that perform calculations and analysis on data.

| Concept | Purpose | Cross-Concept References |
|---------|---------|-------------------------|
| [IntrinsicValue](intrinsic_value.yaml) | Calculates fair value based on cash flow projections | References: company_id |
| [MarginOfSafety](margin_of_safety.yaml) | Determines price protection level | References: company_id |
| [Alert](alert.yaml) | Keeps user informed of important events | References: company_id |

### Document Layer
Analysis artifacts and documents that support investment decisions.

| Concept | Purpose | Cross-Concept References |
|---------|---------|-------------------------|
| [InvestmentThesis](investment_thesis.yaml) | Documents the why behind an investment | References: company_id; linked to InvestmentMemo |
| [PreMortem](pre_mortem.yaml) | Confronts downside before buying | References: company_id; linked to InvestmentMemo |
| [ChecklistAudit](checklist_audit.yaml) | Binary go/no-go decision framework | References: company_id |
| [MoatStrengthAssessment](moat_strength_assessment.yaml) | Rates moat strength across features | References: company_id |
| [AIDueDiligence](ai_due_diligence.yaml) | Evaluates AI-specific moat dimensions | References: company_id |

### Portfolio Layer
Concepts that manage the actual investment portfolio.

| Concept | Purpose | Cross-Concept References |
|---------|---------|-------------------------|
| [Portfolio](portfolio.yaml) | Manages the focused portfolio as a whole | Contains: position_id (references Position) |
| [Position](position.yaml) | Represents an actual investment | References: company_id; contained by Portfolio |
| [Watchlist](watchlist.yaml) | Tracks companies of interest | References: company_id |

### Psychological Defense Layer
Concepts that help mitigate cognitive biases and improve decision-making.

| Concept | Purpose | Cross-Concept References |
|---------|---------|-------------------------|
| [AgentPersona](agent_persona.yaml) | Swaps between analytical personas | Affects: BiasAudit, DecisionLog |
| [DecisionLog](decision_log.yaml) | Learns which biases user is prone to | Linked to: InvestmentMemo, BiasAudit |
| [BiasAudit](bias_audit.yaml) | Documents influencing psychological tendencies | References: decision_type; linked to DecisionLog, InvestmentMemo |

### Cross-Cutting
Concepts that span multiple layers.

| Concept | Purpose | Cross-Concept References |
|---------|---------|-------------------------|
| [InvestmentMemo](investment_memo.yaml) | Consolidates analysis into recommendation snapshot | References: company_id; links to: InvestmentThesis, PreMortem, ChecklistAudit, MoatStrengthAssessment, AIDueDiligence, BiasAudit, DecisionLog; contains: OutcomeSnapshot (nested concept) |

## Concept Relationships Diagram

```
Data Layer:
  Company ←-- MarketData
          ←-- FinancialMetrics
          ←-- Dividend

Analysis Layer:
  Company ←-- IntrinsicValue
          ←-- MarginOfSafety
          ←-- Alert

Document Layer:
  Company ←-- InvestmentThesis
          ←-- PreMortem
          ←-- ChecklistAudit
          ←-- MoatStrengthAssessment
          ←-- AIDueDiligence

Portfolio Layer:
  Company ←-- Position ←-- Portfolio
          ←-- Watchlist

Psychological Defense Layer:
  AgentPersona --> (affects) BiasAudit, DecisionLog
  DecisionLog <--> BiasAudit

Cross-Cutting:
  InvestmentMemo --> Links to all Document Layer concepts + BiasAudit + DecisionLog
```
