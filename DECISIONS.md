# Engineering Decisions

## Decision Philosophy
This project optimizes for a reliable, auditable ingestion and review workflow that can be implemented quickly, demonstrated clearly, and evolved safely. Decisions prioritized:

- deterministic behavior over hidden automation,
- clear data lineage over short-term convenience,
- operational simplicity for startup/internship constraints.

## Why Django
Decision:
- Use Django as the backend framework with modular apps.

Rationale:
- mature ORM for relationship-heavy domain modeling,
- predictable project structure for rapid feature delivery,
- built-in admin and migration system improves operational control,
- strong ecosystem compatibility with REST, PostgreSQL, and deployment tooling.

Alternatives considered:
- FastAPI: faster endpoint prototyping but more assembly required for admin, auth, and conventions.
- Node/Express: flexible, but requires more custom architecture to reach equivalent governance patterns.

## Why Django REST Framework
Decision:
- Use DRF `APIView` for explicit API control.

Rationale:
- serializer-based validation for structured ingestion payloads,
- consistent response/status management,
- straightforward path to permissions/throttling/versioning later.

Alternative rejected:
- raw Django views with manual validation would increase boilerplate and risk inconsistency.

## Why PostgreSQL
Decision:
- Use PostgreSQL as system of record.

Rationale:
- strong relational integrity for foreign-key lineage,
- reliable JSON support for `RawData.raw_json` and audit payloads,
- production-grade durability with hosted managed options.

Alternatives considered:
- SQLite: suitable for prototypes, limited for production concurrency/governance.
- NoSQL-only store: less ideal for strongly relational workflow states and joins.

## Why React + Vite
Decision:
- Use React for UI composition and Vite for development/build performance.

Rationale:
- component model fits dashboard + review surfaces,
- Vite provides fast feedback loop during iterative UI work,
- broad ecosystem support for API-driven applications.

Alternative rejected:
- server-rendered Django templates reduce frontend complexity but limit richer client interactions and deployment separation.

## Why Tailwind CSS
Decision:
- Use Tailwind utility classes for styling.

Rationale:
- high delivery speed with consistent design tokens,
- avoids custom CSS sprawl for dashboard UIs,
- easy responsive and state styling in component code.

Alternative rejected:
- heavy component libraries can constrain visual control and add dependency weight.

## Why a Normalization Layer
Decision:
- Normalize source-specific rows into a unified `NormalizedRecord` schema.

Rationale:
- source files expose incompatible column conventions,
- review, metrics, and downstream analytics require a shared contract,
- isolates source mapping logic from review UX and API consumers.

Alternative rejected:
- direct reporting from raw source schemas would duplicate logic per source and produce brittle analytics.

## Why RawData Storage
Decision:
- Persist every incoming row in `RawData` JSON.

Rationale:
- preserves forensic traceability and replay capability,
- prevents irreversible information loss during transformation,
- supports future normalization reprocessing without re-upload.

Alternative rejected:
- storing only normalized output sacrifices audit confidence and source reconciliation.

## Why Audit Logs
Decision:
- Persist review transitions to `AuditLog`.

Rationale:
- creates accountability for decision actions,
- captures history needed for governance and stakeholder trust,
- supports debugging and compliance evidence.

Alternative rejected:
- relying only on current status state loses history and actor attribution.

## Why Analyst Review Workflow
Decision:
- Introduce explicit approve/reject lifecycle before data is treated as final.

Rationale:
- ESG data quality often requires domain review and contextual judgment,
- separates ingestion success from reporting acceptance,
- enables a controlled gate for suspicious/outlier records.

Alternative rejected:
- automatic acceptance of all normalized records risks propagating bad data.

## Why Synchronous Ingestion
Decision:
- Perform ingestion within request cycle.

Rationale:
- low operational overhead for MVP,
- immediate user feedback for small-to-medium files,
- fewer moving parts than queue infrastructure.

Alternative rejected:
- background workers (Celery/RQ) add scalability but increase architecture complexity.

## Why Rule-Based Suspicious Detection
Decision:
- Use deterministic threshold-based suspicious flagging.

Rationale:
- explainable and auditable logic,
- fast implementation and low compute cost,
- predictable behavior suitable for internship-stage platform.

Alternative rejected:
- ML anomaly detection requires labeled data, monitoring, and drift management not yet justified.

## Why Render + Vercel
Decision:
- Deploy backend/database on Render and frontend on Vercel.

Rationale:
- low-friction deployment for Python API + managed Postgres + React static app,
- free-tier accessibility for demo and review workflows,
- clear separation of concerns between API and UI hosting.

Alternatives considered:
- all-in-one cloud stack (AWS/GCP/Azure) offers scale, but raises setup/ops burden for project phase.

## Additional Alternatives Rejected
### Single Database Table for All Data
Rejected because:
- mixes raw, normalized, and workflow concerns,
- weakens lineage clarity and makes policy evolution harder.

### Full Microservices Split
Rejected because:
- premature decomposition for current scope,
- unnecessary operational overhead relative to domain complexity.

### Event-Sourcing From Day One
Rejected because:
- stronger historical guarantees but higher implementation complexity,
- current audit logs provide sufficient traceability for project stage.

