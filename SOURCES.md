# Sources, Assumptions, and Inspirations

## Purpose
This document records the practical references and assumptions used to shape ingestion mappings, workflow behavior, and deployment architecture for the ESG platform.

## ESG Data Assumptions
Assumptions used in this implementation:

- source files represent activity data rather than finalized emissions calculations,
- one uploaded CSV corresponds to one ingestion batch (`DataSource`),
- scope mapping can be inferred from source type in the MVP (`SAP` -> Scope 1, `UTILITY` -> Scope 2, `TRAVEL` -> Scope 3),
- suspicious values can be flagged using deterministic thresholds before analyst review.

These assumptions intentionally optimize for workflow clarity and can be replaced by richer source-level semantics later.

## SAP Export Inspirations
Ingestion logic is inspired by typical ERP material/fuel extraction shapes where:

- quantity-style fields are present (`MENGE`),
- units are represented separately (`MEINS`),
- rows represent operational events requiring normalization before ESG reporting.

Current mapping:
- `MENGE` -> `activity_amount`
- `MEINS` -> `unit`
- normalized category/scope defaults to Fuel/Scope 1 for this source type.

## Utility CSV Inspirations
Utility ingestion reflects common electricity usage exports:

- meter or billing-period level records,
- kWh consumption as principal activity metric,
- direct mapping to Scope 2 activity reporting context.

Current mapping:
- `Usage_kWh` -> `activity_amount`
- unit fixed as `kWh`
- category/scope set to Electricity/Scope 2.

## Travel Report Inspirations
Travel ingestion follows simplified travel-log abstractions:

- each row treated as one trip event,
- no distance/fuel-class detail in current schema,
- normalized into Scope 3 travel activity.

Current mapping:
- each row -> amount `1`, unit `trip`
- category/scope set to Business Travel/Scope 3.

## Normalization Assumptions
Normalization model assumptions:

- source heterogeneity is resolved through source-type adapters,
- normalized records should remain minimal and review-friendly,
- raw payload preservation is required to support correction and replay.

Validation assumptions:
- negative amounts are invalid and auto-rejected,
- exceptionally high values are suspicious and require review.

## Workflow Inspirations
Operational workflow pattern is inspired by internal data quality pipelines:

- ingest -> normalize -> validate -> analyst decision,
- lock reviewed records to reduce accidental workflow churn,
- track decision events for governance and accountability.

This mirrors practical control gates used in finance, compliance, and sustainability reporting operations.

## Documentation References
Primary implementation references:

- Django project/app architecture conventions,
- Django REST Framework serializer/view patterns,
- pandas CSV ingestion patterns,
- React component-driven dashboard patterns,
- Tailwind utility styling conventions.

These were used as implementation guidance rather than copied templates.

## Deployment References
Deployment approach is informed by:

- Render managed Python service + PostgreSQL workflow,
- Vercel static frontend hosting model,
- environment variable-based cross-service configuration,
- CORS/CSRF origin whitelisting for split frontend/backend deployments.

## Architecture Inspirations
Architecture follows a practical internal platform pattern:

- transactional backend with strong relational lineage,
- immutable-ish raw capture + normalized working layer,
- analyst decision state machine,
- auditable change history.

This pattern balances explainability and speed, making it suitable for ESG operations where data trust is as important as throughput.

## Limitations of Source Assumptions
These references are intentionally pragmatic and not a complete ESG standard implementation. In production, expected enhancements include:

- source-specific emission factor integration,
- richer controlled vocabularies and ontology alignment,
- jurisdiction-specific reporting schemas and evidence retention controls.

