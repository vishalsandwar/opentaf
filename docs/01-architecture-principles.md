# OpenTAF Architecture Principles

## 1. Purpose

The Open Transformation & Agentic AI Framework (OpenTAF) provides a reference architecture for organisations seeking to introduce Agentic AI into enterprise transformation in a controlled, scalable and responsible manner.

These principles provide the architectural foundation for OpenTAF.

They are intended to guide:

* Enterprise architecture decisions
* Agent design
* AI orchestration
* Integration architecture
* Data access
* Security controls
* Human oversight
* AI governance
* Transformation design

---

# 2. Architecture Principles

## Principle 1 — Business Value Before AI

AI should be introduced to address a clearly understood business or transformation problem.

The presence of an AI capability is not, by itself, a justification for transformation.

### Implication

Every AI initiative should establish:

**Business Objective → Process Problem → AI Opportunity → Expected Outcome**

---

## Principle 2 — Architecture Before Automation

Automation should follow an understanding of the business process, information flow, existing technology landscape and control environment.

OpenTAF therefore considers:

**Business → Process → Information → Application → Technology → AI**

before defining agent behaviour.

### Implication

An agent should not be designed in isolation from the enterprise architecture in which it operates.

---

## Principle 3 — Agents Are Enterprise Components

An AI agent should be treated as an enterprise technology component rather than an isolated chatbot.

An agent may have:

* Identity
* Purpose
* Instructions
* Tools
* Permissions
* Context
* Memory
* Policies
* Monitoring
* Auditability

### Implication

Agent architecture should be subject to appropriate enterprise architecture and technology governance.

---

## Principle 4 — Human Oversight for Consequential Decisions

Agents may analyse, recommend, coordinate and execute defined activities.

However, decisions with significant business, financial, regulatory, legal or customer impact should have appropriate human oversight.

### Implication

OpenTAF supports **Human-in-the-Loop (HITL)** and **Human-on-the-Loop (HOTL)** patterns.

The level of human involvement should correspond to the risk and consequence of the activity.

---

## Principle 5 — Least-Privilege Agent Access

An agent should receive only the minimum access required to perform its authorised function.

Access should be controlled across:

* Data
* APIs
* Applications
* Tools
* Actions
* Business processes

### Implication

Agent permissions should be explicit rather than implicitly inherited.

---

## Principle 6 — Explicit Tool Permissions

Agents should interact with enterprise systems through explicitly defined and governed tools.

Examples include:

* API calls
* Database queries
* Search services
* Document services
* Workflow services
* Enterprise applications

### Implication

Every tool available to an agent should have:

**Purpose → Permission → Input → Output → Validation → Audit**

---

## Principle 7 — Traceable Agent Actions

Important agent decisions and actions should be traceable.

The architecture should support recording:

* Agent identity
* User/request identity
* Input context
* Tools invoked
* Actions performed
* Outputs generated
* Approvals
* Exceptions
* Final outcome

### Implication

Agentic workflows should support audit and investigation where required.

---

## Principle 8 — Security and Privacy by Design

Security and privacy should be architectural considerations from the beginning of an AI initiative.

OpenTAF considers:

* Identity
* Authentication
* Authorisation
* Data classification
* Data minimisation
* Encryption
* Secrets management
* Prompt and context security
* Tool security
* Monitoring

### Implication

Security controls should not be treated as a post-implementation activity.

---

## Principle 9 — Model and Provider Independence

The framework should avoid unnecessary architectural dependency on a single AI model or provider.

The architecture should allow different model providers or deployment patterns where appropriate.

For example:

```text
                Agent
                  |
             AI Gateway
                  |
        +---------+---------+
        |         |         |
     Cloud LLM  Private   Local LLM
               Model
```

### Implication

Business logic, agent policies and enterprise controls should remain as independent as practical from the underlying model provider.

---

## Principle 10 — Composable Agents

Agents should be designed as specialised, reusable capabilities rather than a single monolithic intelligence layer.

For example:

```text
                Orchestrator
                     |
       +-------------+-------------+
       |             |             |
    Data Agent    Risk Agent   Process Agent
       |             |             |
       +-------------+-------------+
                     |
                Human Review
```

### Implication

Specialised agents can be independently developed, governed, tested and replaced.

---

## Principle 11 — Governance Must Scale With Autonomy

The greater the autonomy granted to an agent, the greater the need for appropriate controls.

OpenTAF therefore considers autonomy as an architectural dimension.

```text
Assistance
    ↓
Recommendation
    ↓
Human-approved Action
    ↓
Controlled Execution
    ↓
Multi-agent Orchestration
    ↓
Bounded Autonomous Execution
```

### Implication

Controls, monitoring and approval mechanisms should increase as agent autonomy increases.

---

## Principle 12 — Design for Responsible Scale

An AI solution should be designed not only for the initial use case but also for its potential evolution across the enterprise.

The architecture should consider:

* Reusability
* Scalability
* Observability
* Governance
* Security
* Cost
* Model evolution
* Operational support
* Change management

### Implication

A successful AI experiment should have a credible path toward enterprise adoption without requiring an entirely new architecture.

---

# 3. Principle Summary

| #  | Principle                                   | Primary Focus             |
| -- | ------------------------------------------- | ------------------------- |
| 1  | Business Value Before AI                    | Transformation            |
| 2  | Architecture Before Automation              | Enterprise Architecture   |
| 3  | Agents Are Enterprise Components            | Agent Architecture        |
| 4  | Human Oversight for Consequential Decisions | Responsible AI            |
| 5  | Least-Privilege Agent Access                | Security                  |
| 6  | Explicit Tool Permissions                   | Integration               |
| 7  | Traceable Agent Actions                     | Governance                |
| 8  | Security and Privacy by Design              | Security & Privacy        |
| 9  | Model and Provider Independence             | Technology Strategy       |
| 10 | Composable Agents                           | Agent Architecture        |
| 11 | Governance Must Scale With Autonomy         | AI Governance             |
| 12 | Design for Responsible Scale                | Enterprise Transformation |

---

# 4. OpenTAF Architectural Position

OpenTAF does not propose that Agentic AI should replace enterprise architecture or human decision-making.

Instead, it treats Agentic AI as a new architectural capability that must operate within an appropriate:

**Business + Data + Application + Technology + Security + Governance + Human** context.

The objective is to enable organisations to move from isolated AI experimentation toward **governed, composable and scalable Agentic AI-enabled transformation**.
