# AlphaTrace

AlphaTrace is a Python-based investment analysis tool that combines quantitative Buffett-style metrics (ROE, Owner Earnings, Margin of Safety, $1 Test via `yfinance`) with LLM-powered qualitative analysis (moat assessment, pre-mortem scenarios, investment thesis generation).

It serves as a developer-focused showcase for **agentic development** — demonstrating how AI agents can handle both the "hard" math (data fetching, financial calculations) and the "soft" reasoning (competitive analysis, risk scenarios) that characterize real investment work.

The core product is a CLI tool that automates the Focused Portfolio workflow: company screening, intrinsic value calculation, thesis generation, and ongoing Margin of Safety tracking with configurable alerts.

The architecture is built for extensibility — a FastAPI layer and web UI can be layered on top for portfolio visualization and dashboarding as needs evolve.