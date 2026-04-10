# AlphaTrace Vision

## What is AlphaTrace?

AlphaTrace is a command-line tool that automates Warren Buffett-style investment analysis. It combines quantitative financial metrics with AI-powered qualitative reasoning to help investors research companies, calculate intrinsic value, and track when stocks hit their target "Margin of Safety" price.

## What You Can Do With AlphaTrace

### Research Companies Systematically

Instead of manually pulling financial data from multiple sources, AlphaTrace fetches everything in one command. It pulls ROE, Owner Earnings, Debt-to-Equity, and cash flow metrics from public data — then feeds those numbers to an AI model that generates a structured analysis covering the business moat, competitive landscape, and risks.

### Calculate Intrinsic Value

AlphaTrace runs Discounted Cash Flow (DCF) calculations using your chosen assumptions — growth rate, discount rate, and terminal growth. You get a conservative "fair value" estimate that you can compare against the current market price to see if a stock has a Margin of Safety.

### AI-Powered Company Analysis

AlphaTrace uses modern AI techniques to analyze companies beyond just the numbers:

| Technique | What the AI Analyzes | The "Alpha" (Insight) |
|-----------|---------------------|----------------------|
| Linguistic Auditing | CEO speech patterns/evasiveness | Early warning of internal trouble |
| Synthetic Backtesting | Generative data for "what if" scenarios | Stress-testing against 1970s-style inflation |
| Knowledge Graphs | Inter-company relationships | Predicting "contagion" if a supplier fails |
| Code-Base Analysis | Open-source contributions (GitHub) | Identifying the real tech leaders vs. "wrappers" |

### Generate Investment Documents

For every company you analyze, AlphaTrace can generate:

- **Investment Thesis** — A one-page document with your 3 bull cases, 3 kill-switch sell conditions, and the math behind your valuation
- **Pre-Mortem** — A scenario analysis imagining how the investment could fail in 5 years, forcing you to confront risk before you buy
- **Checklist Audit** — A vet-by-checklist phase covering Circle of Competence, Moat, Management, Financials, and Valuation

### Track Your Watchlist

Add companies to your portfolio tracker and AlphaTrace monitors them. It shows live Margin of Safety percentages, flags when a stock drops to your target buy price, and alerts you when intrinsic value needs recalculation (e.g., after an earnings report).

**Each tracked position includes:**
- **Kill Switch** — A specific numeric metric (e.g., "gross margin drops >2%") that triggers an automatic exit recommendation
- **Lollapalooza Score** — A 1-10 rating of how many psychological biases are currently inflating the price
- **Pre-Mortem Status** — Did the failure scenario we predicted 12 months ago start materializing?

### Build a Focused Portfolio

AlphaTrace is built around the Focused Portfolio philosophy — holding 10-30 high-conviction stocks rather than diversifying across hundreds. It helps you stay disciplined by:

- Warning when a company fails your checklist criteria
- Highlighting when a "Dream Team" stock finally hits your target price after a market correction
- Tracking position sizes and ensuring no single holding becomes too large

## Who Uses It

- **Individual investors** who want to apply Buffett-style rigor without Bloomberg Terminal costs
- **Small investment clubs** that want a shared workflow for researching ideas
- **Professional advisors** who need a reproducible process for documenting investment decisions
- **Anyone** who wants to move from "picking tickers" to "buying businesses"

## How It Works

1. **Run an analysis** — `alphatrace analyze AAPL`
2. **AlphaTrace fetches** — Financial data via `yfinance`, business description from public filings
3. **AI generates** — Moat assessment, Pre-Mortem, Thesis, and Kill-Switch conditions
4. **You decide** — Compare the Margin of Safety to your threshold, add to watchlist or skip
5. **Track over time** — `alphatrace track` shows your watchlist with live prices and valuation gaps

## Future Possibilities

- **Web dashboard** — Visual portfolio tracking, charts, and alerts
- **Backtesting** — Test your thesis against historical data to see how valuation would have performed
- **Multi-source data** — Integrate SEC EDGAR, Morningstar, or other premium data providers
- **Local AI option** — Run models like Llama locally for complete privacy (no data leaves your machine)
- **Collaboration** — Share analysis files with others, export thesis documents to PDF

---

## The Psychological Defense Layer

AlphaTrace doesn't just analyze stocks — it analyzes *your thinking*. Every investment recommendation includes a **Bias Audit** that identifies which cognitive biases might be distorting your decision:

- **Social Proof Warning** — "You want to buy this because it's trending, not because the fundamentals support it"
- **Anchoring Alert** — "You're treating $300 as a 'discount' from $150, but the real question is: is $150 expensive for this business?"
- **Liking/Loving Trap** — "You're valuing the CEO's 'vision' at a 30% premium. Let's strip that out and value the business on fundamentals"
- **Lollapalooza Detection** — When multiple biases converge (e.g., high social sentiment + authority bias + loss aversion), AlphaTrace triggers a high-level warning: "Decision quality is likely compromised. Require 3 non-anecdotal data points to proceed."

### The Council of Contrarians

For high-stakes decisions, AlphaTrace runs a **multi-agent debate** between three perspectives:

1. **The Contrarian Quant** — Challenges valuation assumptions, strips out narrative
2. **The Rational Architect** — Challenges product/market fit, detects "shiny object" syndrome
3. **The Antagonistic Auditor** — Challenges execution assumptions, forces edge-case testing

Each agent scores the decision on their specific bias vulnerabilities. If all three identify overlapping psychological distortions, the system issues a **Lollapalooza Verdict: Denied**.

### Personal Bias Profile

Over time, AlphaTrace learns your psychological vulnerabilities. After 10-20 decisions, it generates a report:

> "You exhibit Sunk Cost bias in both your stock portfolio (holding losing positions 40% longer than winning ones) and your software projects (refusing to kill features after 2 sprints). Recommendation: Your 'Sell/Kill' threshold is being lowered by 20% for the next 30 days."

---

AlphaTrace turns the Buffett workflow into a repeatable, tool-assisted process — so you spend less time on data entry and more time on the hard part: thinking about whether you actually understand the business.