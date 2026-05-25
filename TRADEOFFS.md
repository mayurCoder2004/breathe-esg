# Intentional Tradeoffs

## Overview
The platform intentionally favors a clear, auditable MVP over broad platform breadth. This document records non-implemented capabilities, why they were deferred, and realistic upgrade paths.

## 1) No OCR Ingestion
### Why not implemented
- current ingestion scope is structured CSV exports only,
- OCR introduces document parsing uncertainty and quality variation,
- adds significant preprocessing and verification burden.

### Production requirements
- document pipeline (PDF/image upload, OCR extraction, confidence scoring),
- field mapping UI for human correction,
- storage for original document artifacts and extraction metadata.

### Upgrade path
1. Introduce `DocumentSource` model with file metadata.
2. Add extraction service (cloud OCR or on-prem engine).
3. Route extracted fields into existing normalization + review flow.

## 2) No Live SAP Integration
### Why not implemented
- internship scope prioritized upload-based integration,
- direct ERP integration requires credentials, network controls, and enterprise approvals.

### Production requirements
- SAP connector strategy (OData/BAPI/ETL),
- secure secret management and rotation,
- incremental sync, retry, and reconciliation logic.

### Upgrade path
1. Add connector service with scheduled pulls.
2. Save pulled payloads as `RawData` with connector metadata.
3. Reuse normalization pipeline with source-specific adapters.

## 3) No Asynchronous Processing
### Why not implemented
- synchronous flow is simpler to operate for small files,
- avoids queue/worker infrastructure during MVP.

### Production requirements
- task queue (Celery + Redis/RabbitMQ),
- job status tracking and retry policies,
- idempotent ingestion with robust failure handling.

### Upgrade path
1. Replace direct processing in upload endpoint with queued job dispatch.
2. Add ingestion job model (`PENDING`, `RUNNING`, `FAILED`, `COMPLETED`).
3. Expose job status endpoint for frontend progress states.

## 4) No ML Anomaly Detection
### Why not implemented
- no curated labeled dataset at project stage,
- deterministic rules are easier to explain and validate,
- ML systems require monitoring and model lifecycle operations.

### Production requirements
- historical feature store,
- model training/validation pipeline,
- drift detection and human-in-the-loop override controls.

### Upgrade path
1. Keep rule engine as baseline.
2. Add optional ML score alongside rule outcome.
3. Route high-risk mismatches into analyst escalation queue.

## 5) No Role-Based Authentication
### Why not implemented
- current demo assumes trusted analyst context,
- auth and role boundaries were not primary learning objective.

### Production requirements
- authentication provider integration (OIDC/SAML/JWT),
- role model (`admin`, `analyst`, `viewer`),
- endpoint-level permission classes and UI-level action guards.

### Upgrade path
1. Enable Django auth and token-based API auth.
2. Introduce role claims and policy checks for review endpoints.
3. Replace hardcoded actor values in audit logs with authenticated identity.

## 6) Simplified ESG Schema
### Why not implemented
- MVP centers on activity ingestion and review mechanics,
- full ESG taxonomy coverage is large and evolving.

### Production requirements
- expanded schema for factors, geographies, facility/unit hierarchies,
- versioned mapping dictionaries and controlled vocabularies,
- data quality constraints by category and unit family.

### Upgrade path
1. Extend `NormalizedRecord` with optional metadata fields.
2. Externalize schema/rules into configuration tables.
3. Add schema version tagging for backward compatibility.

## 7) Free-Tier Deployment Limitations
### Why accepted
- cost-efficient for internship demonstration,
- sufficient for low-volume testing and review scenarios.

### Impacts
- cold starts,
- limited compute and storage,
- lower throughput and less predictable latency.

### Production requirements
- paid instances with autoscaling,
- persistent monitoring, alerting, and backup policies,
- load/performance testing and capacity planning.

### Upgrade path
1. Move to paid tiers with fixed compute guarantees.
2. Add observability stack (metrics, logs, traces).
3. Introduce staged environments (dev/staging/prod) with release controls.

## 8) Scalability Constraints
### Current limitation
- row-by-row pandas iteration inside request-response cycle,
- no pagination/filtering optimization for large datasets.

### Production requirements
- bulk insert strategies,
- asynchronous worker pools,
- indexed query patterns and pagination contracts.

### Upgrade path
1. Batch processing and `bulk_create` where safe.
2. Server-side pagination/filtering for record endpoints.
3. Parallel ingestion workers with bounded concurrency.

## 9) Simplicity vs Extensibility
### Tradeoff made
- simpler explicit service logic now, less dynamic configuration.

### Why reasonable
- easier code comprehension and faster onboarding,
- deterministic behavior for review and demos.

### Extensibility requirements
- pluggable source adapters,
- declarative normalization rules,
- policy registry for suspicious detection.

### Upgrade path
1. Extract per-source mappers into strategy classes.
2. Add source onboarding checklist and config-driven mapping.
3. Version normalization logic and migrate with replay support.

## 10) Startup/Internship Prioritization
### Prioritization principle
- demonstrate complete business workflow over edge-case completeness.

### What was prioritized
- ingestion + normalization + review + audit loop,
- production deployment and end-to-end usability.

### What was intentionally deferred
- enterprise-grade auth, integrations, and ML sophistication.

### Production progression
1. Strengthen access control and compliance posture.
2. Expand integration coverage and throughput.
3. Add decision intelligence while preserving auditability.

