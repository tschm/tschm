# Thomas Schmelzer

I build optimization algorithms and research tooling for quantitative finance, from Palo Alto and Abu Dhabi.

I left continental Europe in 2004 to become a Rhodes Scholar at Balliol College, Oxford.
I wrote my DPhil — Oxford's PhD — on fast matrix functions, supervised by Nick Trefethen. Shadows of this past include

* [nncg](https://github.com/jebel-quant/nncg) — non-negative conjugate gradients: bound-constrained SPD quadratics solved by a guarded active-set loop, the reference implementation for Schmelzer & Stoll
* [mean_variance_solvers](https://github.com/jebel-quant/mean_variance_solvers) — two companion working papers on fast matrix-free and direct solvers for long-only mean-variance portfolios

In 2007 I jumped head first into quantitative hedge funds, where I became interested in higher-dimensional convex problems

* [linalg](https://github.com/jebel-quant/linalg) — the linear algebra underneath portfolio optimization
* [cvxcla](https://github.com/cvxgrp/cvxcla) — the critical line algorithm: exact efficient frontiers rather than sampled ones
* [pyhrp](https://github.com/tschm/pyhrp) — cluster-based allocation: hierarchical risk parity, Schur complement risk parity, 1/N

I have released utilities such as

* [jquantstats](https://github.com/jebel-quant/jquantstats) — time series and portfolio analytics
* [basanos](https://github.com/jebel-quant/basanos) — a first hurdle for expected returns

Entire strategies are discussed in

* [cs](https://github.com/tschm/cs) — the 10-line CTA: a trend-following strategy in ten lines of code, and what convex programming reveals about its Sharpe ratio, kurtosis and trading costs. Written for a talk at Credit Suisse, on a challenge from a young CEO. The engine underneath it is [TinyCTA](https://github.com/tschm/TinyCTA)

In 2023 I was a visiting scholar at Stanford, working with Stephen Boyd. That is where the [cvxgrp](https://github.com/cvxgrp) work comes from: `cvxcla` above, and alongside it [simulator](https://github.com/cvxgrp/simulator) for backtests small enough to read, [cvxrisk](https://github.com/cvxgrp/cvxrisk) for risk models you can compose, and [cvxball](https://github.com/cvxgrp/cvxball) for the smallest enclosing sphere.

In 2025 I launched — together with HE Omar Saif Ghobash — [Jebel Quant Research](https://github.com/jebel-quant).
Jebel Quant Research offers help with data, strategies and trading. We also continue the tradition of publishing open source software. We have released

* [rhiza](https://github.com/jebel-quant/rhiza) — one template repository that owns the boring parts of a Python project: CI workflows, the Makefile, linting, typing, test and coverage gates, and the docs build. A repo pins a template release and syncs; every project then shares one configuration instead of drifting into its own.
* [rhiza-claude](https://github.com/jebel-quant/rhiza-claude) — the same workflow as slash commands for Claude Code: `/init` to adopt rhiza, `/update` to move to a newer template release, `/quality` to score a repo against the gates, `/release` to cut a version.

The point of both is leverage. Configuration is written once, reviewed once, and then inherited — so the time goes into the research and not into the plumbing.

I have had exposure to ADIA's Team Q. That experience became my manifesto:

**[A Technology Vision for Quantitative Trading](https://jebel-quant.github.io/platform/vision.pdf)** — fourteen pages arguing that the industry's problems are organisational rather than technical. The handover model, in which research is written in Python and reimplemented in C++, produces diffuse accountability, dozens of reinvented wheels, and reconciliation as an organising principle; what replaces it is a single environment for research and production, a checkerboard team instead of an upstream and a downstream one, and quality at every stage instead of inspection at the end. Before any of the quant work I trained as a mechanic at AUDI, so the factory analogies come from the shop floor rather than a business book: the industry adopted Ford's assembly line, which manufacturing itself had largely abandoned by the 1980s, when Toyota's line is the better model and a professional kitchen — calm, deliberate, every station visible to every other — is better still. A chef buys the oven and does not cook from a packet. Knowing which is which is the whole of build-or-buy.

I am a firm believer in good and detailed documentation

* [rhiza-education](https://github.com/jebel-quant/rhiza-education) — training for and with rhiza
* [An introduction to rhiza-claude](https://jebel-quant.github.io/rhiza-claude/paper/rhiza-claude-intro.pdf) — a paper on what the plugin is for, before what it contains: the two-repository boundary a sync respects, what "rhiza-managed" means on disk, the order the commands are meant to be run in, and why a tool that sells determinism keeps half of itself in prose

A good part of my work lands in other people's repositories — nearly 400 merged pull requests outside my own projects. The ones I keep returning to

* [chebpy](https://github.com/chebpy/chebpy) — a Python implementation of Chebfun, and so the most direct continuation of the DPhil I could have hoped for
* [loman](https://github.com/janushendersonassetallocation/loman) — computation graphs for quantitative research and trading
* [investment-funnel](https://github.com/VanekPetr/investment-funnel) — an open platform for developing and backtesting investment strategies
* [pycharting](https://github.com/alihaskar/pycharting) — high-performance charting for financial data

And smaller fixes, usually filed where a tool got in my way: [scipy](https://github.com/scipy/scipy), [cvxpy](https://github.com/cvxpy/cvxpy), [marimo](https://github.com/marimo-team/marimo), [PyPortfolioOpt](https://github.com/PyPortfolio/PyPortfolioOpt), [Clarabel](https://github.com/oxfordcontrol/Clarabel.rs), [Kaleido](https://github.com/plotly/Kaleido), [finmarketpy](https://github.com/cuemacro/finmarketpy), [connector-x](https://github.com/sfu-db/connector-x), [ISLP labs](https://github.com/intro-stat-learning/ISLP_labs).

I am currently one of the most active GitHub users in the UAE:

[![committers.top badge](https://user-badge.committers.top/uae_private/tschm.svg?cache_bust=1)](https://user-badge.committers.top/uae_private/tschm)

Though that is a measure of volume, and volume was never the point. Or maybe it was?

A more useful measure is what is still open. Every count below is live, and every count is a link to the thing behind it — so the state of the work is as visible to you as it is to me.

| | issues | pull requests | latest release | last commit |
|---|---|---|---|---|
| [nncg](https://github.com/jebel-quant/nncg) | [![open issues](https://img.shields.io/github/issues/jebel-quant/nncg?label=)](https://github.com/jebel-quant/nncg/issues) | [![open pull requests](https://img.shields.io/github/issues-pr/jebel-quant/nncg?label=)](https://github.com/jebel-quant/nncg/pulls) | [![latest release](https://img.shields.io/github/v/release/jebel-quant/nncg?label=&sort=semver)](https://github.com/jebel-quant/nncg/releases) | [![last commit](https://img.shields.io/github/last-commit/jebel-quant/nncg?label=)](https://github.com/jebel-quant/nncg/commits) |
| [mean_variance_solvers](https://github.com/jebel-quant/mean_variance_solvers) | [![open issues](https://img.shields.io/github/issues/jebel-quant/mean_variance_solvers?label=)](https://github.com/jebel-quant/mean_variance_solvers/issues) | [![open pull requests](https://img.shields.io/github/issues-pr/jebel-quant/mean_variance_solvers?label=)](https://github.com/jebel-quant/mean_variance_solvers/pulls) | [![latest release](https://img.shields.io/github/v/release/jebel-quant/mean_variance_solvers?label=&sort=semver)](https://github.com/jebel-quant/mean_variance_solvers/releases) | [![last commit](https://img.shields.io/github/last-commit/jebel-quant/mean_variance_solvers?label=)](https://github.com/jebel-quant/mean_variance_solvers/commits) |
| [linalg](https://github.com/jebel-quant/linalg) | [![open issues](https://img.shields.io/github/issues/jebel-quant/linalg?label=)](https://github.com/jebel-quant/linalg/issues) | [![open pull requests](https://img.shields.io/github/issues-pr/jebel-quant/linalg?label=)](https://github.com/jebel-quant/linalg/pulls) | [![latest release](https://img.shields.io/github/v/release/jebel-quant/linalg?label=&sort=semver)](https://github.com/jebel-quant/linalg/releases) | [![last commit](https://img.shields.io/github/last-commit/jebel-quant/linalg?label=)](https://github.com/jebel-quant/linalg/commits) |
| [pyhrp](https://github.com/tschm/pyhrp) | [![open issues](https://img.shields.io/github/issues/tschm/pyhrp?label=)](https://github.com/tschm/pyhrp/issues) | [![open pull requests](https://img.shields.io/github/issues-pr/tschm/pyhrp?label=)](https://github.com/tschm/pyhrp/pulls) | [![latest release](https://img.shields.io/github/v/release/tschm/pyhrp?label=&sort=semver)](https://github.com/tschm/pyhrp/releases) | [![last commit](https://img.shields.io/github/last-commit/tschm/pyhrp?label=)](https://github.com/tschm/pyhrp/commits) |
| [jquantstats](https://github.com/jebel-quant/jquantstats) | [![open issues](https://img.shields.io/github/issues/jebel-quant/jquantstats?label=)](https://github.com/jebel-quant/jquantstats/issues) | [![open pull requests](https://img.shields.io/github/issues-pr/jebel-quant/jquantstats?label=)](https://github.com/jebel-quant/jquantstats/pulls) | [![latest release](https://img.shields.io/github/v/release/jebel-quant/jquantstats?label=&sort=semver)](https://github.com/jebel-quant/jquantstats/releases) | [![last commit](https://img.shields.io/github/last-commit/jebel-quant/jquantstats?label=)](https://github.com/jebel-quant/jquantstats/commits) |
| [basanos](https://github.com/jebel-quant/basanos) | [![open issues](https://img.shields.io/github/issues/jebel-quant/basanos?label=)](https://github.com/jebel-quant/basanos/issues) | [![open pull requests](https://img.shields.io/github/issues-pr/jebel-quant/basanos?label=)](https://github.com/jebel-quant/basanos/pulls) | [![latest release](https://img.shields.io/github/v/release/jebel-quant/basanos?label=&sort=semver)](https://github.com/jebel-quant/basanos/releases) | [![last commit](https://img.shields.io/github/last-commit/jebel-quant/basanos?label=)](https://github.com/jebel-quant/basanos/commits) |
| [cs](https://github.com/tschm/cs) | [![open issues](https://img.shields.io/github/issues/tschm/cs?label=)](https://github.com/tschm/cs/issues) | [![open pull requests](https://img.shields.io/github/issues-pr/tschm/cs?label=)](https://github.com/tschm/cs/pulls) | [![latest release](https://img.shields.io/github/v/release/tschm/cs?label=&sort=semver)](https://github.com/tschm/cs/releases) | [![last commit](https://img.shields.io/github/last-commit/tschm/cs?label=)](https://github.com/tschm/cs/commits) |
| [TinyCTA](https://github.com/tschm/TinyCTA) | [![open issues](https://img.shields.io/github/issues/tschm/TinyCTA?label=)](https://github.com/tschm/TinyCTA/issues) | [![open pull requests](https://img.shields.io/github/issues-pr/tschm/TinyCTA?label=)](https://github.com/tschm/TinyCTA/pulls) | [![latest release](https://img.shields.io/github/v/release/tschm/TinyCTA?label=&sort=semver)](https://github.com/tschm/TinyCTA/releases) | [![last commit](https://img.shields.io/github/last-commit/tschm/TinyCTA?label=)](https://github.com/tschm/TinyCTA/commits) |
| [rhiza](https://github.com/jebel-quant/rhiza) | [![open issues](https://img.shields.io/github/issues/jebel-quant/rhiza?label=)](https://github.com/jebel-quant/rhiza/issues) | [![open pull requests](https://img.shields.io/github/issues-pr/jebel-quant/rhiza?label=)](https://github.com/jebel-quant/rhiza/pulls) | [![latest release](https://img.shields.io/github/v/release/jebel-quant/rhiza?label=&sort=semver)](https://github.com/jebel-quant/rhiza/releases) | [![last commit](https://img.shields.io/github/last-commit/jebel-quant/rhiza?label=)](https://github.com/jebel-quant/rhiza/commits) |
| [rhiza-claude](https://github.com/jebel-quant/rhiza-claude) | [![open issues](https://img.shields.io/github/issues/jebel-quant/rhiza-claude?label=)](https://github.com/jebel-quant/rhiza-claude/issues) | [![open pull requests](https://img.shields.io/github/issues-pr/jebel-quant/rhiza-claude?label=)](https://github.com/jebel-quant/rhiza-claude/pulls) | [![latest release](https://img.shields.io/github/v/release/jebel-quant/rhiza-claude?label=&sort=semver)](https://github.com/jebel-quant/rhiza-claude/releases) | [![last commit](https://img.shields.io/github/last-commit/jebel-quant/rhiza-claude?label=)](https://github.com/jebel-quant/rhiza-claude/commits) |
| [rhiza-education](https://github.com/jebel-quant/rhiza-education) | [![open issues](https://img.shields.io/github/issues/jebel-quant/rhiza-education?label=)](https://github.com/jebel-quant/rhiza-education/issues) | [![open pull requests](https://img.shields.io/github/issues-pr/jebel-quant/rhiza-education?label=)](https://github.com/jebel-quant/rhiza-education/pulls) | [![latest release](https://img.shields.io/github/v/release/jebel-quant/rhiza-education?label=&sort=semver)](https://github.com/jebel-quant/rhiza-education/releases) | [![last commit](https://img.shields.io/github/last-commit/jebel-quant/rhiza-education?label=)](https://github.com/jebel-quant/rhiza-education/commits) |

An issue that has been open for a year is not a backlog item, it is a decision that was never made.
