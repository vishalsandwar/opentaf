
# Getting Started with OpenTAF

OpenTAF is an open-source reference framework for enterprise transformation, Agentic AI architecture, governance, and responsible AI.

This guide explains how to install the project, run the examples, and execute the test suite.

## 1. Prerequisites

- Python 3.10 or later
- Git
- pip

## 2. Clone the repository

```bash
git clone https://github.com/vishalsandwar/opentaf.git
cd opentaf
```

## 3. Set up a virtual environment

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## 4. Install OpenTAF

```bash
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install pytest
```

## 5. Run the multi-agent KYC example

From the repository root:

```bash
python examples/multi_agent_kyc_demo.py
```

Other examples are available in the `examples/` directory.

## 6. Run the tests

```bash
python -m pytest -q
```

## 7. Explore the architecture

| Document | Description |
| --- | --- |
| [Architecture Principles](01-architecture-principles.md) | Foundational design principles |
| [Reference Architecture](02-reference-architecture.md) | Overall framework architecture |
| [Agentic AI Architecture](03-agentic-ai-architecture.md) | Agent design and interactions |
| [Agent Governance](04-agent-governance.md) | Governance and control concepts |
| [Responsible AI](05-responsible-ai.md) | Responsible AI considerations |
| [Transformation Maturity Model](06-transformation-maturity-model.md) | Transformation maturity framework |

## 8. Important disclaimer

OpenTAF is an open-source reference architecture and educational project. It is not certified for production use, regulatory compliance, or any specific business purpose.

Organisations should conduct their own security, privacy, legal, risk, and regulatory assessments before adapting components for real-world environments.

The examples are not intended to make actual lending, credit, KYC, or compliance decisions. Use synthetic data only.
