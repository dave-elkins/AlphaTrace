# AlphaTrace Vision

## What is AlphaTrace?

AlphaTrace is a command-line tool that automates Warren Buffett-style investment analysis. It combines quantitative financial metrics with AI-powered qualitative reasoning to help investors research companies, calculate intrinsic value, and track when stocks hit their target "Margin of Safety" price.

## What You Can Do With AlphaTrace

### Research Companies Systematically

Instead of manually pulling financial data from multiple sources, AlphaTrace fetches everything in one command. It pulls ROE, Owner Earnings, Debt-to-Equity, and cash flow metrics from public data — then feeds those numbers to an AI model that generates a structured analysis covering the business moat, competitive landscape, and risks.

### Calculate Intrinsic Value

AlphaTrace runs Discounted Cash Flow (DCF) calculations using your chosen assumptions — growth rate, discount rate, and terminal growth. You get a conservative "fair value" estimate that you can compare against the current market price to see if a stock has a Margin of Safety.

### Generate Investment Documents

For every company you analyze, AlphaTrace can generate:

- **Investment Thesis** — A one-page document with your 3 bull cases, 3 kill-switch sell conditions, and the math behind your valuation
- **Pre-Mortem** — A scenario analysis imagining how the investment could fail in 5 years, forcing you to confront risk before you buy
- **Checklist Audit** — A vet-by-checklist phase covering Circle of Competence, Moat, Management, Financials, and Valuation

### Track Your Watchlist

Add companies to your portfolio tracker and AlphaTrace monitors them. It shows live Margin of Safety percentages, flags when a stock drops to your target buy price, and alerts you when intrinsic value needs recalculation (e.g., after an earnings report).

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

AlphaTrace turns the Buffett workflow into a repeatable, tool-assisted process — so you spend less time on data entry and more time on the hard part: thinking about whether you actually understand the business.