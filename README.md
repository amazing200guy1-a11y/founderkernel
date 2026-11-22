# FounderKernel: Autonomous Runway Sentry & Microservice Expense Circuit-Breaker

[![Tests](https://img.shields.io/badge/Tests-10%2F10%20Passing-brightgreen.svg)](test_founder_kernel.py)
[![Latency](https://img.shields.io/badge/Latency-0.022ms%2Ftx-blue.svg)](test_founder_kernel.py)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **FounderKernel** is an autonomous zero-cashflow runway sentry, token burn throttler, and microservice expense circuit-breaker for solo founders. It applies staged Hoare-invariant circuit breakers to block runaway LLM API loops, enforce four-tier degradation, and produce cryptographic solvency attestations — all in **0.022 milliseconds per evaluation**.

---

## ⚡ Key Features
- **4-Tier Circuit Breaker:** Auto-degrades from OPTIMAL → THROTTLED → DOWNGRADED → HARD HALT based on live runway calculation.
- **Runaway Burn Detection:** Intercepts sudden API cost acceleration spikes (>3.5× recent rate) caused by infinite agentic loops.
- **Hard Solvency Invariant:** `{P: Cash - cost >= 0} Dispatch {Q: Insolvent = False}` guaranteed atomically.
- **Cryptographic Solvency Certificate:** SHA-256 Merkle spend root attestation for investor or compliance reporting.
- **Aerospace Titanium Cockpit:** Live interactive burn velocity chart, audit log, and dispatch simulator (`index.html`).

---

## 🚀 Quick Start

```bash
python test_founder_kernel.py
```

Expected Output:
```
..........
----------------------------------------------------------------------
Ran 10 tests in 0.003s

OK

[BENCHMARK] 100 FounderKernel Evaluations: 0.0022s | Avg Latency: 0.0218 ms/tx
```

Open `index.html` in any browser to run the interactive runway simulation.

---

## 📂 Repository Structure
- `founder_kernel_engine.py` — Core circuit-breaker, runway engine, and solvency attestation.
- `test_founder_kernel.py` — Formal test suite (10 unit & benchmark tests).
- `index.html` — Obsidian titanium operations cockpit.
- `SUBMISSION_DOSSIER.md` — Full hackathon submission documentation.

---

## 🛡️ License
MIT License. Built by Usman Bamidele for open-source developer financial governance.
