# 0004 - Enhancing Vision with Bias Concepts

**Date:** 2026-04-10

## Session Objective

Reviewed a chat discussing Charlie Munger's "Psychology of Human Misjudgment" and applied those concepts to AlphaTrace's vision and candidate concepts documents. The goal was to add a psychological defense layer to protect users from their own cognitive biases when making investment decisions.

## Key Decisions

| Decision | Choice | Rationale |
|---------|--------|-----------|
| Psychological layer as core feature | Core rather than optional plugin | Differentiates AlphaTrack from generic stock analyzers; makes it a "Council of Contrarians" |
| New BiasAudit concept | Added to concepts list | Owns bias detection state, exposes actions, maintains operational principle of adjusting bias weights based on historical accuracy |
| DecisionLog concept | Added | Captures user decisions with context for later bias analysis |
| AgentPersona concept | Added | Enables users to adopt different psychological personas (Contrarian, Skeptic, Optimizer) |
| Lollapalooza detection system | Added | Identifies when multiple biases combine for amplified effect |
| New sync rules and guards | Implemented | Bias-aware guard rules that intervene when user is likely acting from a cognitive bias rather than rational analysis |

## Trade-offs Considered

- **Core vs Plugin**: Choosing to add psychological layer as core functionality increases complexity but differentiates the product. Decided core since psychological safety is central to the value proposition.
- **User Control vs Protection**: Balancing between giving users freedom and protecting them from biases. The guard system provides warnings rather than blocking decisions.
- **Complex Bias Taxonomy vs Simplicity**: Rather than tracking all 25 Munger biases, focused on high-impact ones that matter for investment decisions.

## Concept Design / WYSIWID Observations

The BiasAudit concept follows the WYSIWID pattern cleanly:

- **Owns its state**: Bias weights, historical accuracy data, detected biases per decision
- **Exposes actions**: `assess_decision()`, `adjust_weights()`, `detect_lollapalooza()`
- **Maintains operational principle**: Bias weights are adjusted based on historical accuracy - if a bias consistently leads to poor decisions, its weight increases and triggers more aggressive guards

The DecisionLog concept stores uninterpreted atoms (decision_id, context) that BiasAudit can later analyze. This creates a clean separation where DecisionLog doesn't need to understand biases - it just records decisions, and sync rules connect the two.

## Blog Angles

- "How AI can protect you from your own psychology" - The idea that the biggest risk to investors is themselves
- "The Munger-fied investment agent" - Building on Charlie Munger's framework in software
- "Building a Council of Contrarians" - Using AI to counteract natural human biases rather than amplifying them

## Next Steps

- Refine the BiasAudit state model with specific bias types
- Define the sync rules for when BiasAudit detects dangerous bias combinations
- Create guard configurations for different risk tolerances