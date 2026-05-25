# Data Model Design

## Overview
The data model is designed for controlled ESG ingestion from multiple operational sources, with three non-negotiable properties:

- traceability from normalized records back to original source rows,
- review-state management for analyst decisions,
- auditable state transitions for governance and compliance evidence.

Core entities:
- `Company`
- `DataSource`
- `RawData`
- `NormalizedRecord`
- `AuditLog`

## Company Model
Represents a legal entity or operating unit whose ESG activity is being tracked.

Key fields:
- `name`
- `industry`
- `created_at`

Why it exists:
- anchors all ingestion and review records to an accountable business entity,
- supports future multi-tenant or multi-subsidiary expansions,
- allows ESG records to be partitioned by organization.

## DataSource Model
Represents an ingestion batch and metadata for an uploaded file.

Key fields:
- `company` (FK -> `Company`)
- `source_type` (`SAP`, `UTILITY`, `TRAVEL`)
- `file_name`
- `uploaded_at`
- `uploaded_by`

Why it exists:
- preserves ingestion lineage at file level,
- distinguishes record origin by source system/type,
- allows investigation and rollback strategy by batch.

## RawData Model
Stores immutable source rows exactly as uploaded.

Key fields:
- `data_source` (FK -> `DataSource`)
- `raw_json` (JSON payload of source row)
- `row_number`
- `created_at`

Why raw preservation is mandatory:
- supports reconciliation when normalization logic changes,
- enables source-of-truth verification during audits,
- prevents data loss from schema assumptions during transformation.

## NormalizedRecord Model
Represents a standardized ESG activity record for review and downstream reporting.

Key fields:
- `company` (FK -> `Company`)
- `data_source` (FK -> `DataSource`)
- `category` (e.g., Fuel, Electricity, Business Travel)
- `scope` (Scope 1/2/3)
- `activity_amount`
- `unit`
- `status` (`PENDING`, `APPROVED`, `REJECTED`, `SUSPICIOUS`)
- `is_locked`
- `created_at`

Why normalization exists:
- different source systems expose incompatible column names and semantics,
- analytics/review requires a stable schema across sources,
- normalized shape decouples downstream logic from source-specific formats.

## AuditLog Model
Captures review actions and record-level state transitions.

Key fields:
- `record` (FK -> `NormalizedRecord`)
- `action`
- `old_value` (JSON)
- `new_value` (JSON)
- `changed_by`
- `changed_at`

Auditability considerations:
- status transitions are recorded with before/after snapshots,
- actor and timestamp provide accountability,
- JSON payloads allow incremental enrichment without schema churn.

## Relationships
```text
Company 1 ────< DataSource 1 ────< RawData
   |               |
   |               └────< NormalizedRecord 1 ────< AuditLog
   |
   └────────────────────< NormalizedRecord
```

Relationship intent:
- `Company` groups all operational ESG data.
- `DataSource` groups rows by ingestion event/source.
- `RawData` keeps immutable source evidence per row.
- `NormalizedRecord` enables standardized review flow.
- `AuditLog` preserves decision history.

## Review Workflow Lifecycle
Lifecycle state machine for `NormalizedRecord.status`:

1. `PENDING`  
   Default state after successful normalization when no rule is triggered.

2. `SUSPICIOUS`  
   Assigned automatically when deterministic threshold checks detect outliers.

3. `APPROVED`  
   Analyst confirms validity; record is locked (`is_locked=true`) to prevent further action in current workflow.

4. `REJECTED`  
   Analyst or validation rejects record due to invalid/undesired data.

## Immutable Approved Records
Design intent:
- Approved records represent reviewed reporting artifacts and should be stable.
- `is_locked` signals workflow immutability after approval.

Current implementation behavior:
- UI hides review buttons for locked records.
- API currently allows updates via action endpoints unless additional guards are added.

Production hardening recommendation:
- enforce lock check in approve/reject endpoints,
- optionally enforce DB-level guard via constraint or service policy,
- capture attempted post-lock mutation in `AuditLog` as denied action.

## Multi-Source ESG Ingestion Design
The model separates source metadata (`DataSource`) from row evidence (`RawData`) and review entities (`NormalizedRecord`) to support:

- onboarding additional sources without redesigning review tables,
- source-wise validation and anomaly policies,
- future replay/re-normalization from preserved raw payloads.

## Suspicious Detection Workflow
Current rule:
- if normalized `activity_amount > 100000`, mark as `SUSPICIOUS`.

Why this is modeled at normalized level:
- threshold logic should operate on harmonized fields,
- avoids duplicating source-specific threshold checks,
- supports future rule composition (per category, per company, per unit).

Production path:
- configurable rule thresholds by source/category,
- rule versioning and explainability metadata,
- optional escalation queue for suspicious records.

