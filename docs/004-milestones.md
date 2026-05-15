# AlphaTrace Milestones

This document defines the milestones for AlphaTrace development. Each milestone is a vertical slice of user-facing functionality that can be demonstrated independently. Milestones are organized around user workflows, not technical layers.

Every milestone includes:
- **Jobs-to-be-Done (JTBD)** — full format with situation, motivation, and expected outcome
- **Acceptance Criteria** — testable bullets that define "done"
- **Concepts** — which concept YAML specs must be implemented
- **Sync Rules** — which sync YAML specs must be implemented
- **Guards** — cross-concept rules enforced at the sync layer
- **CLI Commands** — user-facing interface for the milestone
- **Demo Script** — how to verify the milestone works end-to-end

---

## Milestone 0: Project Foundation

**Goal:** Establish the development environment and application scaffolding so contributors can build and run the tool.

### Jobs-to-be-Done

- **JTBD 0.1:** When I clone the repository, I want to set up the development environment with a single command so that I can start contributing without friction.
- **JTBD 0.2:** When I run the tool for the first time, I want to see a help menu and version info so that I know the installation succeeded.

### Acceptance Criteria

- [ ] `uv` manages Python version and virtual environment
- [ ] `pyproject.toml` configures dependencies (fastapi, alembic, pydantic, sqlite)
- [ ] `ruff` linting and formatting passes on an empty codebase
- [ ] `ty` type checking passes on an empty codebase
- [ ] `alphatrace --version` returns a version string
- [ ] `alphatrace --help` shows available commands
- [ ] Sync engine scaffold exists in `app/engine/sync_engine.py`
- [ ] FastAPI app scaffold exists in `app/main.py`
- [ ] CLI scaffold exists in `app/cli.py`
- [ ] SQLite database initializes on first run
- [ ] `AGENTS.md` documents build/test/lint commands

### Concepts to Implement

None — infrastructure only.

### Sync Rules to Implement

None — infrastructure only.

### Guards

None.

### CLI Commands

```bash
alphatrace --version
alphatrace --help
```

### Demo Script

```bash
git clone <repo>
cd alphatrace
uv sync
uv run alphatrace --version   # Should print version
uv run alphatrace --help       # Should show command structure
```

---

## Milestone 1: Look Up a Company

**Goal:** A user can look up a company by ticker, store its profile, fetch financial metrics, market price history, and dividend data.

### Jobs-to-be-Done

- **JTBD 1.1:** When I hear about a company (e.g., "AAPL is having a good quarter"), I want to look up its basic profile by ticker so that I can see what the company does and decide if it's worth analyzing further.
- **JTBD 1.2:** When I've found a company I'm curious about, I want to fetch its financial metrics (ROE, Debt-to-Equity, Cash Flow) so that I can do a quick sanity check on its fundamentals.
- **JTBD 1.3:** When I'm tracking a company, I want to fetch its historical price data and dividend history so that I have the raw data needed for valuation.

### Acceptance Criteria

- [ ] Can add a company by ticker symbol (`alphatrace company add AAPL`)
- [ ] Company profile stored: ticker, name, sector, industry, business description
- [ ] Can view company profile (`alphatrace company show AAPL`)
- [ ] Can fetch financial metrics from yfinance (`alphatrace financials fetch AAPL`)
- [ ] Financial metrics stored: ROE, Owner Earnings, Debt-to-Equity, free cash flow, operating cash flow, book value per share, shares outstanding
- [ ] Can view financial metrics (`alphatrace financials show AAPL`)
- [ ] Can fetch historical market data (`alphatrace marketdata fetch AAPL --start 2020-01-01`)
- [ ] Market data stored: date, open, high, low, close, adjusted_close, volume, market_cap
- [ ] Can view current price (`alphatrace marketdata current AAPL`)
- [ ] Can fetch dividend history (`alphatrace dividend fetch AAPL`)
- [ ] Dividend data stored: ex_dividend_date, amount_per_share
- [ ] Data persists across CLI restarts (SQLite)
- [ ] Running fetch again updates existing data (replaces metrics, appends new prices/dividends)

### Concepts to Implement

| Concept | YAML Spec | Description |
|---------|-----------|-------------|
| `Company` | [company.yaml](concepts/company.yaml) | Core entity — ticker, name, sector, industry, business description |
| `FinancialMetrics` | [financial_metrics.yaml](concepts/financial_metrics.yaml) | ROE, Owner Earnings, Debt-to-Equity, cash flows, book value |
| `MarketData` | [market_data.yaml](concepts/market_data.yaml) | Historical and current price data (OHLCV + market cap) |
| `Dividend` | [dividend.yaml](concepts/dividend.yaml) | Dividend payment history (ex-dividend date + amount) |

### Sync Rules to Implement

None — no downstream concepts exist yet for cross-concept syncs.

### Guards

None.

### CLI Commands

```bash
alphatrace company add <TICKER>
alphatrace company show <TICKER>
alphatrace financials fetch <TICKER>
alphatrace financials show <TICKER>
alphatrace marketdata fetch <TICKER> [--start YYYY-MM-DD] [--end YYYY-MM-DD]
alphatrace marketdata current <TICKER>
alphatrace dividend fetch <TICKER>
alphatrace dividend show <TICKER>
```

### Demo Script

```bash
# Add Apple to the database
uv run alphatrace company add AAPL

# Verify company profile
uv run alphatrace company show AAPL

# Fetch financial metrics from yfinance
uv run alphatrace financials fetch AAPL

# View the numbers
uv run alphatrace financials show AAPL

# Fetch 2 years of price history
uv run alphatrace marketdata fetch AAPL --start 2024-01-01

# Check current price
uv run alphatrace marketdata current AAPL

# Fetch dividend history
uv run alphatrace dividend fetch AAPL

# Verify data persisted
uv run alphatrace company show AAPL
```

---

## Milestone 2: Calculate What a Company is Worth

**Goal:** A user can calculate intrinsic value via DCF and see the margin of safety — whether the stock is overvalued, fairly priced, or undervalued.

### Jobs-to-be-Done

- **JTBD 2.1:** When I've reviewed a company's financials and they look decent, I want to calculate its intrinsic value using a DCF model so that I know what the business is actually worth based on its cash flows.
- **JTBD 2.2:** When I know a company's intrinsic value and current price, I want to see its margin of safety percentage so that I know if the stock is trading at a discount (buy opportunity) or premium (overvalued).
- **JTBD 2.3:** When new financial data arrives or market price changes, I want the margin of safety to update automatically so that I always see the current status without manual recalculation.

### Acceptance Criteria

- [ ] Can calculate intrinsic value with default DCF assumptions (`alphatrace value calculate AAPL`)
- [ ] DCF inputs stored: growth rate, discount rate (WACC), terminal growth rate
- [ ] Fair value estimate produced and stored
- [ ] Can update DCF assumptions (`alphatrace value assumptions AAPL --growth 0.05 --discount 0.09 --terminal 0.025`)
- [ ] Can calculate margin of safety (`alphatrace mos calculate AAPL`)
- [ ] Margin of safety stored: target buy price, MOS %, status (overvalued/fair/undervalued)
- [ ] Sync: When `FinancialMetrics.update` → `IntrinsicValue.recalculate` runs automatically
- [ ] Sync: When `IntrinsicValue.recalculate` → `MarginOfSafety.recalculate_status` runs automatically
- [ ] Sync: When `MarketData.fetch_historical` or `get_current` detects price change → `MarginOfSafety.recalculate_status` runs
- [ ] Alert created when price drops below target buy price (Alert type: `price_drop`)
- [ ] Can view alerts (`alphatrace alert list`)
- [ ] Can acknowledge/dismiss alerts (`alphatrace alert ack <id>`)
- [ ] Can show full valuation summary (`alphatrace value show AAPL`)

### Concepts to Implement

| Concept | YAML Spec | Description |
|---------|-----------|-------------|
| `IntrinsicValue` | [intrinsic_value.yaml](concepts/intrinsic_value.yaml) | DCF valuation — fair value, growth/discount/terminal rates |
| `MarginOfSafety` | [margin_of_safety.yaml](concepts/margin_of_safety.yaml) | Target buy price, MOS %, status (overvalued/fair/undervalued) |
| `Alert` | [alert.yaml](concepts/alert.yaml) | Notifications for price drops, recalculation needed, target hits |

### Sync Rules to Implement

| Sync Rule | YAML Spec | Trigger → Action |
|-----------|-----------|------------------|
| `on_financial_metrics_update_recalculate_intrinsic_value` | [syncs/on_financial_metrics_update_recalculate_intrinsic_value.yaml](syncs/on_financial_metrics_update_recalculate_intrinsic_value.yaml) | `FinancialMetrics.update` → `IntrinsicValue.recalculate` |
| `on_intrinsic_value_recalculate_update_margin_of_safety` | [syncs/on_intrinsic_value_recalculate_update_margin_of_safety.yaml](syncs/on_intrinsic_value_recalculate_update_margin_of_safety.yaml) | `IntrinsicValue.recalculate` → `MarginOfSafety.recalculate_status` |
| `on_market_data_update_check_alerts` | [syncs/on_market_data_update_check_alerts.yaml](syncs/on_market_data_update_check_alerts.yaml) | `MarketData.fetch_historical`/`get_current` → check price vs MOS → `Alert.create` if price dropped below target |

### Guards

None for this milestone.

### CLI Commands

```bash
alphatrace value calculate <TICKER>
alphatrace value assumptions <TICKER> [--growth RATE] [--discount RATE] [--terminal RATE]
alphatrace value show <TICKER>
alphatrace mos calculate <TICKER>
alphatrace mos show <TICKER>
alphatrace alert list
alphatrace alert ack <ALERT_ID>
alphatrace alert dismiss <ALERT_ID>
```

### Demo Script

```bash
# Start with Apple in the database
uv run alphatrace company add AAPL
uv run alphatrace financials fetch AAPL
uv run alphatrace marketdata fetch AAPL --start 2024-01-01

# Calculate intrinsic value using DCF
uv run alphatrace value calculate AAPL

# View the fair value estimate
uv run alphatrace value show AAPL

# Adjust assumptions (lower growth, higher discount rate for conservatism)
uv run alphatrace value assumptions AAPL --growth 0.04 --discount 0.10

# Recalculate with new assumptions
uv run alphatrace value calculate AAPL

# Calculate margin of safety
uv run alphatrace mos calculate AAPL

# View MOS status (should show overvalued/fair/undervalued + %)
uv run alphatrace mos show AAPL

# Demonstrate auto-recalculation: update financials
uv run alphatrace financials fetch AAPL
# → Should trigger IntrinsicValue.recalculate → MarginOfSafety.recalculate_status

# Check for any price-drop alerts
uv run alphatrace alert list
```

---

## Milestone 3: Decide Whether to Invest

**Goal:** A user can create an investment memo that consolidates thesis, pre-mortem, checklist audit, and moat assessment into a final BUY/PASS/HOLD recommendation.

### Jobs-to-be-Done

- **JTBD 3.1:** When I've valued a company and it looks undervalued, I want to create an investment thesis so that I can articulate the bull cases and kill-switch conditions for my own clarity and future reference.
- **JTBD 3.2:** Before I invest, I want to run a pre-mortem analysis so that I confront how the investment could fail in 5 years and avoid being blindsided by downside risks.
- **JTBD 3.3:** Before I buy, I want to complete a structured checklist (Circle of Competence, Moat, Management, Financials, Valuation) so that I have a disciplined go/no-go framework and don't skip critical analysis.
- **JTBD 3.4:** When I've completed all analysis documents, I want to finalize an investment memo with a BUY/PASS/HOLD recommendation so that I have a point-in-time record of my decision that I can review later.
- **JTBD 3.5:** When I finalize a memo, I want all linked documents to lock in so that the analysis remains immutable and I can't accidentally modify a finalized decision.

### Acceptance Criteria

- [ ] Can create an investment memo (`alphatrace memo create AAPL`)
- [ ] Memo creation auto-creates linked documents (sync rule):
  - InvestmentThesis
  - PreMortem
  - ChecklistAudit
  - MoatStrengthAssessment
  - AIDueDiligence
- [ ] Can write investment thesis: 3 bull cases, 3 kill-switch conditions, thesis text
- [ ] Can run pre-mortem: add failure scenarios, risk factors, mitigation notes
- [ ] Can complete checklist audit: mark Circle of Competence, Moat, Management, Financials, Valuation as done
- [ ] Checklist calculates overall pass/fail when all items marked done
- [ ] Can assess moat strength: rate Model, Data, Switching Cost, Margins → overall moat rating
- [ ] Can assess AI due diligence: Data Sovereignty, Architecture, Talent & Execution, Unit Economics
- [ ] Can finalize memo (`alphatrace memo finalize AAPL`)
- [ ] Finalize requires all linked documents complete (sync rule check)
- [ ] Finalize locks in recommendation (BUY/PASS/HOLD), target price from MarginOfSafety, confidence level
- [ ] Finalize triggers DecisionLog.record (even if BiasAudit is stubbed for Milestone 5)
- [ ] Can view finalized memo with all linked artifacts (`alphatrace memo show AAPL`)
- [ ] Can archive a memo (`alphatrace memo archive AAPL`)
- [ ] Can review memo without modifying finalized ones

### Concepts to Implement

| Concept | YAML Spec | Description |
|---------|-----------|-------------|
| `InvestmentMemo` | [investment_memo.yaml](concepts/investment_memo.yaml) | Point-in-time recommendation with linked artifacts, outcomes tracking |
| `InvestmentThesis` | [investment_thesis.yaml](concepts/investment_thesis.yaml) | Bull cases, kill-switch conditions, thesis text |
| `PreMortem` | [pre_mortem.yaml](concepts/pre_mortem.yaml) | Failure scenarios, risk factors, lollapalooza score, kill-switch metric |
| `ChecklistAudit` | [checklist_audit.yaml](concepts/checklist_audit.yaml) | Circle of Competence, Moat, Management, Financials, Valuation — pass/fail |
| `MoatStrengthAssessment` | [moat_strength_assessment.yaml](concepts/moat_strength_assessment.yaml) | Model/Data/Switching Cost/Margins ratings → overall moat |
| `AIDueDiligence` | [ai_due_diligence.yaml](concepts/ai_due_diligence.yaml) | AI-specific moat: Data Sovereignty, Architecture, Talent, Unit Economics |

### Sync Rules to Implement

| Sync Rule | YAML Spec | Trigger → Action |
|-----------|-----------|------------------|
| `on_investment_memo_create_trigger_documents` | [syncs/on_investment_memo_create_trigger_documents.yaml](syncs/on_investment_memo_create_trigger_documents.yaml) | `InvestmentMemo.create` → create `InvestmentThesis`, `PreMortem`, `ChecklistAudit`, `MoatStrengthAssessment`, `AIDueDiligence` |
| `on_investment_memo_finalize_trigger_downstream` | [syncs/on_investment_memo_finalize_trigger_downstream.yaml](syncs/on_investment_memo_finalize_trigger_downstream.yaml) | `InvestmentMemo.finalize` → `DecisionLog.record_decision` + finalize linked docs (stub BiasAudit for now) |

### Guards

None for this milestone (ChecklistAudit pass guard and Lollapalooza guard come in Milestone 5).

### CLI Commands

```bash
alphatrace memo create <TICKER>
alphatrace memo show <TICKER>
alphatrace memo finalize <TICKER>
alphatrace memo archive <TICKER>
alphatrace thesis edit <TICKER>  # add bull cases, kill-switches, text
alphatrace thesis show <TICKER>
alphatrace premortem edit <TICKER>  # add scenarios, risks, mitigations
alphatrace premortem show <TICKER>
alphatrace checklist show <TICKER>
alphatrace checklist mark <TICKER> <ITEM>  # mark done (competence/moat/management/financials/valuation)
alphatrace moat show <TICKER>
alphatrace moat rate <TICKER> <FEATURE> <RATING>  # rate model/data/switching/margins
alphatrace ai-dd show <TICKER>
alphatrace ai-dd rate <TICKER> <DIMENSION> <RATING>  # rate sovereignty/architecture/talent/unit-economics
```

### Demo Script

```bash
# Start with Apple analyzed
uv run alphatrace company add AAPL
uv run alphatrace financials fetch AAPL
uv run alphatrace value calculate AAPL
uv run alphatrace mos calculate AAPL

# Create investment memo (auto-creates all linked documents)
uv run alphatrace memo create AAPL

# View the empty memo structure
uv run alphatrace memo show AAPL

# Fill out investment thesis
uv run alphatrace thesis edit AAPL
# (Interactive: add 3 bull cases, 3 kill-switches, thesis text)

# View thesis
uv run alphatrace thesis show AAPL

# Complete pre-mortem
uv run alphatrace premortem edit AAPL
# (Interactive: add failure scenarios, risk factors, mitigations)

# Complete checklist audit
uv run alphatrace checklist mark AAPL competence
uv run alphatrace checklist mark AAPL moat
uv run alphatrace checklist mark AAPL management
uv run alphatrace checklist mark AAPL financials
uv run alphatrace checklist mark AAPL valuation

# Check overall pass/fail
uv run alphatrace checklist show AAPL

# Assess moat strength
uv run alphatrace moat rate AAPL model "High Moat"
uv run alphatrace moat rate AAPL data "High Moat"
uv run alphatrace moat rate AAPL switching "Low Moat"
uv run alphatrace moat rate AAPL margins "High Moat"

# Assess AI due diligence (for tech companies)
uv run alphatrace ai-dd rate AAPL sovereignty "High Moat"
uv run alphatrace ai-dd rate AAPL architecture "High Moat"

# Finalize the memo (triggers DecisionLog.record)
uv run alphatrace memo finalize AAPL
# → Should require all documents complete
# → Should lock in BUY/PASS/HOLD recommendation + target price + confidence

# View finalized memo
uv run alphatrace memo show AAPL
# → Should show recommendation, target price, all linked artifacts
# → Should NOT allow editing finalized documents
```

---

## Milestone 4: Build a Focused Portfolio

**Goal:** A user can maintain a watchlist, open positions, track a focused portfolio of 10-30 stocks, and enforce disciplined allocation limits.

### Jobs-to-be-Done

- **JTBD 4.1:** When I'm researching multiple companies, I want to add them to a watchlist so that I can monitor their margin of safety status in one place without deciding to buy yet.
- **JTBD 4.2:** When I've finalized a BUY memo for a company, I want to open a position so that it's tracked in my portfolio with my actual shares and cost basis.
- **JTBD 4.3:** When I'm building my portfolio, I want to see all my positions and their allocation percentages so that I know if I'm too concentrated in one stock or if I've exceeded the focused portfolio limit (10-30 stocks).
- **JTBD 4.4:** When a position goes against me and I want to sell, I want to liquidate (partially or fully) so that my portfolio reflects the current holdings.
- **JTBD 4.5:** When I make changes to my portfolio, I want the allocation percentages to recalculate automatically so that I always see current state without manual updates.

### Acceptance Criteria

- [ ] Can create a portfolio (`alphatrace portfolio create "My Portfolio"`)
- [ ] Can add companies to watchlist (`alphatrace watchlist add AAPL --note "Strong moat"`)
- [ ] Can add tags to watchlist entries (`alphatrace watchlist tag AAPL "tech"`)
- [ ] Can view watchlist with MOS status for each company (`alphatrace watchlist show`)
- [ ] Can open a position (`alphatrace portfolio add AAPL --shares 10 --cost-basis 150`)
- [ ] Sync: `Position.create` → `Portfolio.add_position` runs automatically
- [ ] Cannot exceed 30 stocks in portfolio (guard: `Portfolio.size_limit_not_exceeded`)
- [ ] Position size (% of portfolio) calculated automatically
- [ ] Can view portfolio: all positions, total value, cash, allocation percentages
- [ ] Can liquidate position partially (`alphatrace portfolio liquidate AAPL --shares 5`)
- [ ] Can liquidate position fully (`alphatrace portfolio liquidate AAPL`)
- [ ] Sync: `Position.liquidate` (shares=0) → `Portfolio.remove_position` runs automatically
- [ ] Can remove companies from watchlist (`alphatrace watchlist remove AAPL`)
- [ ] Can update watchlist notes (`alphatrace watchlist note AAPL "Reconsider after earnings"`)
- [ ] Portfolio enforces maximum position size (no single holding > configured % — e.g., 20%)
- [ ] Can update cash position (`alphatrace portfolio cash --add 10000` / `--withdraw 5000`)

### Concepts to Implement

| Concept | YAML Spec | Description |
|---------|-----------|-------------|
| `Watchlist` | [watchlist.yaml](concepts/watchlist.yaml) | Track companies of interest with notes and tags |
| `Position` | [position.yaml](concepts/position.yaml) | Holding: shares, cost basis, position size %, date acquired |
| `Portfolio` | [portfolio.yaml](concepts/portfolio.yaml) | Collection of positions, total value, cash, rebalancing rules |

### Sync Rules to Implement

| Sync Rule | YAML Spec | Trigger → Action |
|-----------|-----------|------------------|
| `on_position_create_add_to_portfolio` | [syncs/on_position_create_add_to_portfolio.yaml](syncs/on_position_create_add_to_portfolio.yaml) | `Position.create` → `Portfolio.add_position` (guard: size limit ≤30) |
| `on_position_liquidate_remove_from_portfolio` | [syncs/on_position_liquidate_remove_from_portfolio.yaml](syncs/on_position_liquidate_remove_from_portfolio.yaml) | `Position.liquidate` (shares=0) → `Portfolio.remove_position` |

### Guards

| Guard | Description |
|-------|-------------|
| `Portfolio.size_limit_not_exceeded` | Cannot exceed 30 stocks in focused portfolio |
| `Position.max_allocation` | No single position may exceed configured maximum % (e.g., 20%) |

### CLI Commands

```bash
alphatrace portfolio create <NAME> [--cash AMOUNT]
alphatrace portfolio show
alphatrace portfolio cash [--add AMOUNT|--withdraw AMOUNT]
alphatrace portfolio add <TICKER> --shares N [--cost-basis PRICE]
alphatrace portfolio liquidate <TICKER> [--shares N]
alphatrace watchlist add <TICKER> [--note TEXT] [--tag TAG]
alphatrace watchlist remove <TICKER>
alphatrace watchlist show
alphatrace watchlist tag <TICKER> <TAG>
alphatrace watchlist note <TICKER> <TEXT>
```

### Demo Script

```bash
# Create portfolio with initial cash
uv run alphatrace portfolio create "My Portfolio" --cash 100000

# Add companies to watchlist
uv run alphatrace watchlist add AAPL --note "Strong moat, fair value" --tag "tech"
uv run alphatrace watchlist add MSFT --note "AI leader" --tag "tech"
uv run alphatrace watchlist add GOOGL --note "Search dominance" --tag "tech"

# View watchlist (should show MOS status for each)
uv run alphatrace watchlist show

# Analyze and decide to buy AAPL
uv run alphatrace financials fetch AAPL
uv run alphatrace value calculate AAPL
uv run alphatrace memo create AAPL
uv run alphatrace memo finalize AAPL  # BUY recommendation

# Open position in AAPL
uv run alphatrace portfolio add AAPL --shares 10 --cost-basis 150

# View portfolio (should show AAPL position, allocation %, total value)
uv run alphatrace portfolio show

# Try to add 30+ stocks (should fail with guard error)
# (Simulate or actually add 30+ positions)

# Liquidate half the AAPL position
uv run alphatrace portfolio liquidate AAPL --shares 5

# View updated portfolio
uv run alphatrace portfolio show

# Liquidate remaining AAPL
uv run alphatrace portfolio liquidate AAPL
# → Should trigger auto-removal from portfolio

# Verify AAPL removed from positions
uv run alphatrace portfolio show
```

---

## Milestone 5: Track Outcomes and Detect Bias

**Goal:** A user's decisions are logged, psychological biases are detected, lollapalooza alerts fire, and a personal bias profile is built over time.

### Jobs-to-be-Done

- **JTBD 5.1:** When I make an investment decision, I want it automatically logged so that I have a historical record I can review to learn from my past decisions.
- **JTBD 5.2:** When I'm analyzing a company, I want to see which cognitive biases might be influencing my decision so that I can consciously counteract them before committing capital.
- **JTBD 5.3:** When multiple biases converge (lollapalooza effect), I want a high-severity alert so that I know my decision-making is likely compromised and I should require more evidence.
- **JTBD 5.4:** When I've held a position for a significant period (1yr/3yr/5yr/10yr), I want to see the actual outcome vs. my original prediction so that I can assess the accuracy of my analysis and improve.
- **JTBD 5.5:** When I review my decision history, I want to see my personal bias vulnerabilities so that I know which psychological traps I'm most prone to and can be extra vigilant.
- **JTBD 5.6:** When I want a different analytical perspective, I want to switch agent personas (Contrarian, Rational Architect, Antagonistic Auditor) so that I get challenged from different angles.

### Acceptance Criteria

- [ ] DecisionLog records every memo finalization (context, summary, user_confidence, agent_confidence)
- [ ] Sync: `InvestmentMemo.finalize` → `DecisionLog.record_decision` works (fully wired)
- [ ] Sync: `DecisionLog.record_decision` → `BiasAudit.create` runs automatically
- [ ] BiasAudit detects biases: Social Proof, Authority Bias, Sunk Cost, Anchoring, etc.
- [ ] BiasAudit assigns severity scores (1-10) per detected bias
- [ ] BiasAudit calculates lollapalooza score (1-10) and detects lollapalooza (multiple biases converging)
- [ ] Sync: `BiasAudit.calculate_lollapalooza` (score > 7) → `Alert.create` (type: `recalculation_needed`)
- [ ] Can view bias audit for a decision (`alphatrace bias show <memo_id>`)
- [ ] Can view personal bias profile (`alphatrace bias profile`)
- [ ] Can configure agent personas (`alphatrace persona set CONTRARIAN`)
- [ ] Sync: `AgentPersona.set_active` → `BiasAudit.update_bias_sensitivities` runs automatically
- [ ] Can view decision log (`alphatrace decision log`)
- [ ] Can update actual outcomes on decisions (`alphatrace decision outcome <id> OVERPERFORMED`)
- [ ] InvestmentMemo tracks OutcomeSnapshots at 1yr/3yr/5yr/10yr horizons
- [ ] Can calculate outcomes (`alphatrace memo outcome AAPL --horizon 1yr`)
- [ ] Alert created when lollapalooza detected (score > 7)
- [ ] Can acknowledge bias-related alerts (`alphatrace alert ack <id>`)
- [ ] Guards enforced:
  - `ChecklistAudit.pass` required for `Position.add`
  - `BiasAudit.Lollapalooza_Score < 7` required for `Position.add`
  - `Portfolio.size_limit_not_exceeded` (from M4)

### Concepts to Implement

| Concept | YAML Spec | Description |
|---------|-----------|-------------|
| `BiasAudit` | [bias_audit.yaml](concepts/bias_audit.yaml) | Detects biases, severity scores, lollapalooza detection, adjusted confidence |
| `DecisionLog` | [decision_log.yaml](concepts/decision_log.yaml) | Historical record of decisions, outcomes, post-hoc analysis |
| `AgentPersona` | [agent_persona.yaml](concepts/agent_persona.yaml) | Configurable personas: Contrarian, Rational Architect, Antagonistic Auditor |
| `OutcomeSnapshot` | Nested in [investment_memo.yaml](concepts/investment_memo.yaml) | Records actual returns at 1yr/3yr/5yr/10yr horizons |

### Sync Rules to Implement

| Sync Rule | YAML Spec | Trigger → Action |
|-----------|-----------|------------------|
| `on_decision_log_record_create_bias_audit` | [syncs/on_decision_log_record_create_bias_audit.yaml](syncs/on_decision_log_record_create_bias_audit.yaml) | `DecisionLog.record_decision` → `BiasAudit.create` |
| `on_bias_audit_lollapalooza_alert` | [syncs/on_bias_audit_lollapalooza_alert.yaml](syncs/on_bias_audit_lollapalooza_alert.yaml) | `BiasAudit.calculate_lollapalooza` (score > 7) → `Alert.create` (type: `recalculation_needed`) |
| `on_agent_persona_set_active_update_bias_sensitivities` | [syncs/on_agent_persona_set_active_update_bias_sensitivities.yaml](syncs/on_agent_persona_set_active_update_bias_sensitivities.yaml) | `AgentPersona.set_active` → `BiasAudit.update_bias_sensitivities` |

### Guards

| Guard | Description |
|-------|-------------|
| `ChecklistAudit.pass` | Cannot add to portfolio without passing checklist |
| `BiasAudit.Lollapalooza_Score < 7` | Cannot add to portfolio if lollapalooza score ≥ 7 (multiple biases converging) |
| `Portfolio.size_limit_not_exceeded` | Cannot exceed 30 stocks in focused portfolio (from M4) |
| `Position.max_allocation` | No single position may exceed configured maximum % (from M4) |

### CLI Commands

```bash
alphatrace decision log
alphatrace decision show <DECISION_ID>
alphatrace decision outcome <DECISION_ID> <OUTCOME>
alphatrace bias show <MEMO_ID>
alphatrace bias profile
alphatrace persona list
alphatrace persona set <PERSONA_TYPE>
alphatrace persona show <PERSONA_TYPE>
alphatrace memo outcome <TICKER> --horizon <1yr|3yr|5yr|10yr>
alphatrace alert list
alphatrace alert ack <ALERT_ID>
```

### Demo Script

```bash
# Configure agent persona
uv run alphatrace persona list
uv run alphatrace persona set CONTRARIAN

# Analyze and finalize a memo (triggers full downstream: DecisionLog + BiasAudit)
uv run alphatrace company add AAPL
uv run alphatrace financials fetch AAPL
uv run alphatrace value calculate AAPL
uv run alphatrace memo create AAPL
uv run alphatrace memo finalize AAPL  # BUY

# View the decision log
uv run alphatrace decision log
# → Should show the BUY decision with context, summary, confidence

# View bias audit for this memo
uv run alphatrace bias show <memo_id>
# → Should show detected biases, severity scores, lollapalooza score

# If lollapalooza detected (score > 7), check alerts
uv run alphatrace alert list
# → Should show recalculation_needed alert

# Acknowledge the alert
uv run alphatrace alert ack <alert_id>

# Try to add to portfolio (should enforce guards)
uv run alphatrace portfolio add AAPL --shares 10 --cost-basis 150
# → Should check: ChecklistAudit.pass? BiasAudit.Lollapalooza_Score < 7? Portfolio.size < 30?

# View personal bias profile
uv run alphatrace bias profile
# → Should show which biases you're most prone to

# After 1 year, calculate actual outcome
uv run alphatrace memo outcome AAPL --horizon 1yr
# → Fetches price at finalization and current, calculates total return with dividends
# → Stores OutcomeSnapshot (OVERPERFORMED/UNDERPERFORMED/MEETS_EXPECTATIONS)

# Switch to different persona for next analysis
uv run alphatrace persona set RATIONAL_ARCHITECT
uv run alphatrace persona show RATIONAL_ARCHITECT
# → Should show different bias sensitivities
```

---

## Milestone 6: Complete Workflow Integration

**Goal:** The full AlphaTrace workflow connects seamlessly — research → value → decide → track — with all 10 sync rules wired, all guards enforced, and a streamlined end-to-end CLI command.

### Jobs-to-be-Done

- **JTBD 6.1:** When I want to analyze a company end-to-end, I want a single command that runs the full workflow so that I can go from "heard about a ticker" to "finalized investment decision" without running multiple commands.
- **JTBD 6.2:** When I'm using AlphaTrace regularly, I want all the sync rules to fire automatically so that data flows between concepts without manual intervention.
- **JTBD 6.3:** When I try to perform an action that violates a guard rule, I want a clear error message so that I understand what constraint I'm violating and how to fix it.
- **JTBD 6.4:** When I want to demonstrate AlphaTrace to someone else, I want a working end-to-end flow so that they can see the value of the tool in under 5 minutes.

### Acceptance Criteria

- [ ] All 19 concepts implemented and working together
- [ ] All 10 sync rules implemented and wired to the sync engine
- [ ] All 4 guards implemented and enforced
- [ ] End-to-end command: `alphatrace analyze AAPL` runs:
  1. `Company.add` (if not exists)
  2. `FinancialMetrics.fetch`
  3. `MarketData.fetch_historical`
  4. `Dividend.fetch_for_company`
  5. `IntrinsicValue.calculate`
  6. `MarginOfSafety.calculate`
  7. `InvestmentMemo.create` (auto-creates all linked docs)
  8. Interactive: fill out thesis, pre-mortem, checklist, moat, AI due diligence
  9. `InvestmentMemo.finalize` (auto: DecisionLog.record + BiasAudit + lock docs)
- [ ] `alphatrace track` shows watchlist with live MOS status for all companies
- [ ] `alphatrace portfolio show` displays full portfolio with positions, allocation, total value
- [ ] All guards produce clear, actionable error messages
- [ ] Edge cases handled:
  - Fetching data for invalid ticker → clear error
  - Finalizing memo with incomplete docs → lists what's missing
  - Adding 31st stock → "Portfolio limit reached (30 stocks max)"
  - Adding position with lollapalooza score ≥ 7 → "Decision likely compromised (Lollapalooza score: X). Require 3 non-anecdotal data points."
- [ ] Lint passes (`ruff check`)
- [ ] Type check passes (`ty`)
- [ ] Basic integration test covers the full workflow

### Concepts to Implement

All 19 concepts (verification that all are complete):

| # | Concept | YAML Spec | Milestone Introduced |
|---|---------|-----------|---------------------|
| 1 | `Company` | [company.yaml](concepts/company.yaml) | M1 |
| 2 | `FinancialMetrics` | [financial_metrics.yaml](concepts/financial_metrics.yaml) | M1 |
| 3 | `MarketData` | [market_data.yaml](concepts/market_data.yaml) | M1 |
| 4 | `Dividend` | [dividend.yaml](concepts/dividend.yaml) | M1 |
| 5 | `IntrinsicValue` | [intrinsic_value.yaml](concepts/intrinsic_value.yaml) | M2 |
| 6 | `MarginOfSafety` | [margin_of_safety.yaml](concepts/margin_of_safety.yaml) | M2 |
| 7 | `Alert` | [alert.yaml](concepts/alert.yaml) | M2 |
| 8 | `InvestmentMemo` | [investment_memo.yaml](concepts/investment_memo.yaml) | M3 |
| 9 | `InvestmentThesis` | [investment_thesis.yaml](concepts/investment_thesis.yaml) | M3 |
| 10 | `PreMortem` | [pre_mortem.yaml](concepts/pre_mortem.yaml) | M3 |
| 11 | `ChecklistAudit` | [checklist_audit.yaml](concepts/checklist_audit.yaml) | M3 |
| 12 | `MoatStrengthAssessment` | [moat_strength_assessment.yaml](concepts/moat_strength_assessment.yaml) | M3 |
| 13 | `AIDueDiligence` | [ai_due_diligence.yaml](concepts/ai_due_diligence.yaml) | M3 |
| 14 | `Watchlist` | [watchlist.yaml](concepts/watchlist.yaml) | M4 |
| 15 | `Position` | [position.yaml](concepts/position.yaml) | M4 |
| 16 | `Portfolio` | [portfolio.yaml](concepts/portfolio.yaml) | M4 |
| 17 | `BiasAudit` | [bias_audit.yaml](concepts/bias_audit.yaml) | M5 |
| 18 | `DecisionLog` | [decision_log.yaml](concepts/decision_log.yaml) | M5 |
| 19 | `AgentPersona` | [agent_persona.yaml](concepts/agent_persona.yaml) | M5 |

### Sync Rules to Implement

All 10 sync rules (verification that all are wired):

| # | Sync Rule | YAML Spec | Milestone Introduced |
|---|-----------|-----------|---------------------|
| 1 | `on_financial_metrics_update_recalculate_intrinsic_value` | [syncs/on_financial_metrics_update_recalculate_intrinsic_value.yaml](syncs/on_financial_metrics_update_recalculate_intrinsic_value.yaml) | M2 |
| 2 | `on_intrinsic_value_recalculate_update_margin_of_safety` | [syncs/on_intrinsic_value_recalculate_update_margin_of_safety.yaml](syncs/on_intrinsic_value_recalculate_update_margin_of_safety.yaml) | M2 |
| 3 | `on_market_data_update_check_alerts` | [syncs/on_market_data_update_check_alerts.yaml](syncs/on_market_data_update_check_alerts.yaml) | M2 |
| 4 | `on_investment_memo_create_trigger_documents` | [syncs/on_investment_memo_create_trigger_documents.yaml](syncs/on_investment_memo_create_trigger_documents.yaml) | M3 |
| 5 | `on_investment_memo_finalize_trigger_downstream` | [syncs/on_investment_memo_finalize_trigger_downstream.yaml](syncs/on_investment_memo_finalize_trigger_downstream.yaml) | M3 |
| 6 | `on_position_create_add_to_portfolio` | [syncs/on_position_create_add_to_portfolio.yaml](syncs/on_position_create_add_to_portfolio.yaml) | M4 |
| 7 | `on_position_liquidate_remove_from_portfolio` | [syncs/on_position_liquidate_remove_from_portfolio.yaml](syncs/on_position_liquidate_remove_from_portfolio.yaml) | M4 |
| 8 | `on_decision_log_record_create_bias_audit` | [syncs/on_decision_log_record_create_bias_audit.yaml](syncs/on_decision_log_record_create_bias_audit.yaml) | M5 |
| 9 | `on_bias_audit_lollapalooza_alert` | [syncs/on_bias_audit_lollapalooza_alert.yaml](syncs/on_bias_audit_lollapalooza_alert.yaml) | M5 |
| 10 | `on_agent_persona_set_active_update_bias_sensitivities` | [syncs/on_agent_persona_set_active_update_bias_sensitivities.yaml](syncs/on_agent_persona_set_active_update_bias_sensitivities.yaml) | M5 |

### Guards (All Enforced)

| # | Guard | Description | Milestone Introduced |
|---|-------|-------------|---------------------|
| 1 | `ChecklistAudit.pass` | Cannot add to portfolio without passing checklist | M5 |
| 2 | `BiasAudit.Lollapalooza_Score < 7` | Cannot add to portfolio if lollapalooza score ≥ 7 | M5 |
| 3 | `Portfolio.size_limit_not_exceeded` | Cannot exceed 30 stocks in focused portfolio | M4 |
| 4 | `Position.max_allocation` | No single position may exceed configured maximum % | M4 |

### CLI Commands

```bash
# End-to-end workflow
alphatrace analyze <TICKER>
# Interactive workflow: fetch data → calculate value → create memo → fill docs → finalize

# Tracking commands
alphatrace track                    # Show watchlist with live MOS status
alphatrace portfolio show           # Full portfolio view
alphatrace decision log             # Decision history
alphatrace bias profile             # Personal bias vulnerabilities

# Individual commands (still available)
alphatrace company add <TICKER>
alphatrace financials fetch <TICKER>
alphatrace value calculate <TICKER>
alphatrace memo create <TICKER>
alphatrace memo finalize <TICKER>
alphatrace portfolio add <TICKER> --shares N --cost-basis PRICE
```

### Demo Script (5-Minute End-to-End)

```bash
# 1. Analyze a company end-to-end (30 seconds)
uv run alphatrace analyze AAPL
# → Fetches company profile, financials, market data, dividends
# → Calculates intrinsic value and margin of safety
# → Creates investment memo with all linked documents
# → Interactive: fill out thesis, pre-mortem, checklist, moat assessment
# → Finalizes memo → records decision → generates bias audit

# 2. Show the finalized memo (15 seconds)
uv run alphatrace memo show AAPL
# → Shows recommendation (BUY/PASS/HOLD), target price, confidence
# → Lists all linked artifacts (thesis, pre-mortem, checklist, etc.)

# 3. Add to portfolio (15 seconds)
uv run alphatrace portfolio add AAPL --shares 10 --cost-basis 150
# → Enforces guards: ChecklistAudit.pass? Lollapalooza < 7? Portfolio < 30?

# 4. Show portfolio (10 seconds)
uv run alphatrace portfolio show
# → Shows all positions, allocation %, total value, cash

# 5. Show watchlist with live MOS (15 seconds)
uv run alphatrace track
# → Shows all watched companies with current MOS status

# 6. Show decision log and bias profile (15 seconds)
uv run alphatrace decision log
uv run alphatrace bias profile

# 7. Demonstrate guard violation (15 seconds)
uv run alphatrace portfolio add MSFT --shares 100 --cost-basis 400
# → If lollapalooza score ≥ 7 or checklist not passed:
#    "Cannot add position: Decision likely compromised (Lollapalooza score: 8).
#     Require 3 non-anecdotal data points to proceed."
```

---

## Milestone Summary

| Milestone | Name | Key User Workflow | Concepts | Syncs | Guards |
|-----------|------|-------------------|----------|-------|--------|
| 0 | Project Foundation | Set up and run the tool | 0 | 0 | 0 |
| 1 | Look Up a Company | Research a ticker, fetch financials/prices | 4 | 0 | 0 |
| 2 | Calculate Value | DCF valuation, margin of safety, alerts | 3 | 3 | 0 |
| 3 | Decide to Invest | Memo, thesis, pre-mortem, checklist, moat | 6 | 2 | 0 |
| 4 | Build a Portfolio | Watchlist, positions, focused portfolio | 3 | 2 | 2 |
| 5 | Track Outcomes & Bias | Decision log, bias audit, lollapalooza, personas | 4 (1 nested) | 3 | 4 |
| 6 | Full Integration | End-to-end workflow, all syncs/guards wired | 19 total | 10 total | 4 total |

---

## Dependencies Between Milestones

```
M0 (Foundation)
 └── M1 (Look Up a Company)
      └── M2 (Calculate Value) ───┐
           ┌───────────────────────┘
           │
           ▼
      M3 (Decide to Invest)
           └── M4 (Build Portfolio) ──┐
                ┌─────────────────────┘
                ▼
           M5 (Track Outcomes & Bias)
                └── M6 (Full Integration)
```

Each milestone builds on the previous. M2 requires M1 (needs financials + market data). M3 requires M2 (needs intrinsic value + MOS for target price). M4 requires M3 (needs finalized memo to add to portfolio). M5 requires M3 + M4 (needs decisions to log + portfolio to track). M6 integrates everything.

---

## Out of Scope for Initial Milestones

These features from the vision document are intentionally deferred beyond Milestone 6:

- **Web dashboard** — Visual portfolio tracking, charts, alerts (FastAPI layer exists in M0, but UI is deferred)
- **Backtesting** — Test thesis against historical data (requires significant historical data infrastructure)
- **Multi-source data** — SEC EDGAR, Morningstar, premium providers (yfinance is sufficient for M1-M6)
- **Local AI option** — Run models like Llama locally (infrastructure concern, not domain concept)
- **Collaboration** — Share analysis files, export to PDF (multi-user, auth, export features)
- **Council of Contrarians** — Multi-agent debate between 3 personas (extends M5's AgentPersona concept)
- **Personal Bias Profile learning** — Adjusting bias weights based on historical accuracy (extends M5's DecisionLog)
- **Background polling** — Auto-refresh market data for watched companies (on-demand fetch in M1-M6)

These can be planned as follow-on milestones (M7+) once the core workflow is solid.
