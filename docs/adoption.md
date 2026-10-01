# OpenTAF Adoption & Experimentation Guide

## Purpose

OpenTAF is an open-source reference architecture for designing, governing and scaling Agentic AI-enabled digital transformation in regulated enterprises.

This guide provides a practical path for teams and individuals who want to **explore, experiment with or extend OpenTAF**.

OpenTAF is currently an early-stage project. It is intended for experimentation, architectural exploration and reference implementations rather than production deployment without appropriate engineering, security and governance assessment.

---

## Who Can Experiment with OpenTAF?

OpenTAF can be explored by:

* Enterprise architects
* Solution architects
* AI engineers
* Software engineers
* Technology leaders
* Digital transformation teams
* AI governance professionals
* Risk and compliance teams
* Researchers and students
* Teams working in regulated industries

No specific industry or technology provider is required.

---

## Getting Started

The simplest way to explore OpenTAF is to:

1. Clone the repository.
2. Review the architecture and principles.
3. Follow the Getting Started documentation.
4. Run the reference examples.
5. Review the automated tests.
6. Experiment with a small use case.
7. Provide feedback or contribute an improvement.

See the [Getting Started Guide](getting-started.md).

---

## Suggested Experimentation Path

OpenTAF experimentation can follow five stages.

```text
Understand
    ↓
Run
    ↓
Experiment
    ↓
Evaluate
    ↓
Contribute
```

### 1. Understand

Start by reviewing:

* OpenTAF architecture
* Architecture principles
* Agentic AI architecture
* Governance model
* Responsible AI principles
* Transformation maturity model

The [Technical Review Guide](review.md) can be used to understand the areas where architectural feedback is encouraged.

---

### 2. Run

Run the existing examples and reference implementations.

The objective is to understand how the architectural concepts translate into working code.

Experimenters should use synthetic or non-sensitive data.

---

### 3. Experiment

Choose a small business or technology scenario.

Examples include:

* Customer onboarding
* Document processing
* Knowledge assistance
* Compliance analysis
* Service request processing
* Risk assessment support
* Policy analysis
* Enterprise workflow automation

The recommended approach is to begin with a **bounded use case** rather than attempting to automate an entire business process.

---

## Designing an Experiment

An OpenTAF experiment can be documented using the following structure:

```text
Business Problem
      ↓
Process
      ↓
AI Opportunity
      ↓
Agent Capability
      ↓
Tools / Data
      ↓
Governance Controls
      ↓
Human Oversight
      ↓
Expected Outcome
```

### Example

**Business Problem**

Manual review of customer onboarding documents.

**AI Opportunity**

Identify and extract information from submitted documents.

**Agent Capability**

Document analysis agent.

**Tools / Data**

Document parser, OCR service and validation API.

**Governance Controls**

* Restricted document access
* Defined tool permissions
* Confidence thresholds
* Audit logging

**Human Oversight**

Human review for low-confidence or high-risk cases.

**Expected Outcome**

Reduced manual effort while retaining appropriate human control.

---

## Bounded Autonomy

OpenTAF encourages experimentation with **bounded autonomy**.

An agent should not automatically receive unrestricted access to enterprise systems.

Experimenters should consider:

* What the agent is allowed to do
* Which data it can access
* Which tools it can use
* Which actions require approval
* What happens when confidence is low
* How actions are recorded
* How the agent should fail safely

A useful experiment should therefore define explicit boundaries before enabling autonomous execution.

---

## Experiment Classification

Experiments can be classified according to the level of autonomy involved.

| Level | Description         | Example                                   |
| ----- | ------------------- | ----------------------------------------- |
| 0     | Informational       | Generate an explanation                   |
| 1     | Assistive           | Recommend an action                       |
| 2     | Agent-assisted      | Prepare an action for human approval      |
| 3     | Agent-orchestrated  | Execute predefined workflow steps         |
| 4     | Governed autonomous | Execute within explicit policy boundaries |

Higher levels require stronger controls, monitoring and evaluation.

---

## Evaluating an Experiment

Experimenters should consider both technical and business outcomes.

### Technical Evaluation

Consider:

* Accuracy
* Reliability
* Latency
* Failure rate
* Tool usage
* Security
* Auditability
* Policy compliance
* Human intervention rate

### Business Evaluation

Consider:

* Time saved
* Manual effort reduced
* Process cycle time
* User acceptance
* Operational risk
* Cost impact
* Quality improvement

Not every experiment needs to demonstrate production-level results.

Early experiments may primarily be used to test architectural assumptions.

---

## Responsible Experimentation

Experiments should avoid using:

* Confidential organisational information
* Personal data without appropriate controls
* Production credentials
* Unauthorised enterprise systems
* Sensitive customer information

Use synthetic, anonymised or publicly available data wherever possible.

Experiments involving consequential decisions should retain appropriate human oversight.

---

## Sharing an Experiment

Experimenters are encouraged to share useful findings with the OpenTAF community.

A contribution may include:

* A new reference implementation
* An architecture pattern
* A reusable agent
* A governance pattern
* A test case
* Documentation
* An experiment report
* An Architecture Decision Record
* A technical improvement

A useful experiment does not need to be large.

Small, reproducible examples can provide valuable architectural insight.

---

## Suggested Experiment Report

When sharing an experiment, the following structure is recommended:

```text
Experiment Name:

Business Problem:

Use Case:

OpenTAF Components Used:

Agent Capabilities:

Tools / Data Sources:

Governance Controls:

Human Oversight:

Architecture:

Results:

Limitations:

Lessons Learned:

Potential Improvements:
```

Where possible, include diagrams, sample inputs, outputs and reproducible steps.

---

## Contributing Findings

If an experiment identifies an architectural improvement, consider contributing it through:

### GitHub Issue

Use an Issue for:

* Problems
* Gaps
* Improvement proposals
* Questions

### GitHub Discussion

Use a Discussion for:

* Architectural ideas
* Alternative approaches
* Research topics
* Broader community discussion

### Pull Request

Use a Pull Request for:

* Code
* Tests
* Documentation
* Reference implementations
* Architecture examples

See [CONTRIBUTING.md](../CONTRIBUTING.md) before submitting a Pull Request.

---

## Adoption Without Production Deployment

Using OpenTAF does not require deploying it into a production environment.

Teams can experiment through:

* Local development
* Sandboxed environments
* Synthetic datasets
* Proof-of-concept implementations
* Architecture workshops
* Technical evaluations
* Educational projects

The objective is to allow teams to evaluate the architectural concepts before considering broader adoption.

---

## Security and Governance

OpenTAF experiments should follow appropriate organisational security and governance requirements.

Before connecting an experiment to real enterprise systems, consider:

* Identity and access management
* Data classification
* Secrets management
* Network controls
* Tool permissions
* Logging and monitoring
* Human approval
* Incident handling
* Regulatory requirements

Potential security vulnerabilities should be reported according to the process described in [SECURITY.md](../SECURITY.md).

---

## Community Feedback

OpenTAF is expected to evolve through experimentation and technical feedback.

Feedback can influence:

* Architecture
* Reference implementations
* Tests
* Documentation
* Governance patterns
* Roadmap priorities

Experimenters are encouraged to share both **successful and unsuccessful results**.

Understanding where an architectural pattern does not work can be as valuable as demonstrating where it does.

---

## Project Status

OpenTAF is an early-stage open-source project.

The adoption guidance will evolve as additional experiments, reference implementations and community contributions become available.

Any examples of adoption or implementation should represent genuine experimentation or use and should not be interpreted as production certification or endorsement.

---

## Related Documentation

* [README](../README.md)
* [Getting Started](getting-started.md)
* [Technical Review Guide](review.md)
* [Contributing Guide](../CONTRIBUTING.md)
* [Security Policy](../SECURITY.md)
