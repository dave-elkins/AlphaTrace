# AlphaTrace

Command-line investment analysis tool combining Buffett-style quantitative metrics with AI-powered qualitative reasoning.

## What is AlphaTrace?

AlphaTrace automates Warren Buffett-style investment analysis. It combines quantitative financial metrics (ROE, Owner Earnings, Margin of Safety, DCF valuation) with AI-powered qualitative reasoning (moat assessment, pre-mortem risk scenarios, investment thesis generation).

Designed for focused portfolios of 10-30 high-conviction stocks. AlphaTrace helps you move from "picking tickers" to "buying businesses."

## Features

- **Company Research** — Fetch ROE, Owner Earnings, Debt-to-Equity, and cash flow metrics from public data
- **DCF Valuation** — Calculate intrinsic value using customizable growth rate, discount rate, and terminal growth assumptions
- **Margin of Safety** — Compare fair value to market price and track when stocks hit your target buy price
- **AI Analysis** — Generate investment theses, pre-mortem risk assessments, and checklist audits
- **Watchlist Tracking** — Monitor companies with live price updates and valuation alerts
- **Portfolio Management** — Track positions, position sizes, and enforce focused portfolio limits

## Installation

```bash
# Clone and enter project
git clone https://github.com/dave-elkins/AlphaTrace.git
cd AlphaTrace

# Create virtual environment and install
uv venv
uv pip install -e .

# Verify installation
alphatrace --help
```

## Quick Start

```bash
# Analyze a company
alphatrace analyze AAPL

# Calculate intrinsic value with custom assumptions
alphatrace dcf AAPL --growth-rate 0.10 --discount-rate 0.09 --terminal-growth 0.03

# Add to watchlist
alphatrace watch AAPL

# View watchlist with Margin of Safety
alphatrace track

# Generate investment documents
alphatrace thesis AAPL
```

## Architecture

AlphaTrace follows the WYSIWID (What You See Is What It Does) concept design pattern. See [docs/003-candidate-concepts.md](./docs/003-candidate-concepts.md) for the candidate concept definitions.

## License

MIT