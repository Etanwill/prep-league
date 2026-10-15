# System Design Interview Template (45 Minutes)

**Problem:** [System to design]  
**Date:** [Date]  
**Target level:** [Level]  
**Total time:** 45 minutes

## 1. Requirements — 5 minutes

### Functional requirements
- [ ] FR1:
- [ ] FR2:
- [ ] FR3:
- **Out of scope:**

### Non-functional requirements
- **Users:** [DAU/MAU/concurrent users]
- **Traffic:** [Average and peak QPS; read/write ratio]
- **Data size:** [Records, storage, growth, retention]
- **Latency:** [Target p95/p99]
- **Availability/durability:** [Targets]
- **Consistency:** [Required guarantees]

## 2. Core Entities — 2 minutes

- **Entity 1:** [Purpose and key fields]
- **Entity 2:** [Purpose and key fields]
- **Entity 3:** [Relationships]

## 3. API — 5 minutes

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/v1/...` | [Create/write] |
| GET | `/v1/...` | [Read/query] |
| PUT/PATCH | `/v1/...` | [Update, if needed] |
| DELETE | `/v1/...` | [Delete, if needed] |

- Authentication/authorization:
- Pagination/idempotency/error handling:

## 4. Data Flow — 3 minutes

**Write path:**  
[Client → API → processing → database/queue → response]

**Read path:**  
[Client → API → cache/database → response]

**Async path, if needed:**  
[Event producer → queue → consumer → destination]

## 5. High-Level Design — 12 minutes

Draw and explain the main architecture.

- **Components and responsibilities:**
- **Database and data ownership:**
- **Request flow for each core requirement:**
- **How the design meets the functional requirements:**
- **Known bottlenecks or assumptions:**

**Baseline architecture diagram:**

[Insert diagram here]

## 6. Deep Dives — 13 minutes

Choose the 2–3 highest-impact problems based on the requirements.

### Deep dive 1: [Main bottleneck]
- Problem and evidence:
- Proposed solution:
- Alternatives and trade-offs:
- Failure handling:

### Deep dive 2: [Scaling or reliability]
- Problem and evidence:
- Proposed solution:
- Alternatives and trade-offs:
- Failure handling:

### Deep dive 3: [Optional]
- Problem:
- Solution and trade-offs:

## 7. Closing Checklist — 3 minutes

- [ ] **Failures:** Single points of failure, retries, timeouts, recovery.
- [ ] **Observability:** Metrics, logs, tracing, alerts.
- [ ] **Rollout:** Gradual rollout, compatibility, rollback.
- [ ] **Cost:** Main cost drivers and optimizations.
- [ ] **10× scale:** What breaks first, and what changes?
- [ ] Summarize the biggest trade-off and remaining limitation.

## 8. Self-Score — 2 minutes

Score each area from **1 (weak) to 4 (strong)**.

| Rubric | Score (1–4) | Evidence / improvement |
|---|---:|---|
| Understanding | /4 | |
| Approach | /4 | |
| Code | /4 | |
| Testing | /4 | |
| Communication | /4 | |
| Senior signal | /4 | |

### Top 3 gaps
1. [Biggest gap and next action]
2. [Second gap and next action]
3. [Third gap and next action]

**Next practice focus:** [One specific skill to improve]