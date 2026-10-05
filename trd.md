# TRD — Fulfillment Hub

## Stack (LOCKED — do not substitute)
Frontend: Python + Streamlit 1.x, Pandas, Plotly, native Streamlit components, lightweight dashboard UI
Backend: Python 3.11+, SQLite database, SQL queries and data processing in Python
Database: SQLite 3.x with direct SQL schema and seed data
Auth: Internal demo access only; no external auth provider in v1
Hosting: Local development with optional Streamlit-hosted deployment later; no containerization required

## Third-party services
| Service | Purpose | Free tier limit |
|---------|---------|-----------------|
| SQLite | Local operational data store | Included |
| Plotly | Charts and status visualization | Open-source |
| Pandas | Data shaping and dashboard calculations | Open-source |
| Streamlit | Frontend dashboard and workflow UI | Free for internal prototype |

## Constraints (HARD RULES)
- Budget: this must run on a local developer setup and free/open-source tools only
- Skill: keep implementation simple; no complex microservices or Docker setup
- Performance: dashboard must remain responsive with a 250+ order demo dataset
- Scope: focus on fulfillment operations, not a broad commerce platform
- DO NOT USE: heavy JavaScript frameworks, React, GraphQL, Kafka, Kubernetes, enterprise ERPs, external payment systems, or paid APIs

## Conventions
- Naming: snake_case for Python variables, SQL table names in lowercase, clear operational names like `inventory_mismatch` and `pickup_window`
- Folders: keep app entry at root level, database scripts under `database/`, dashboard logic under `pages/`, and data access in `services/`
- API shape: use simple REST-style endpoints in Python where needed, but keep within the single-app structure
- Error format: return consistent JSON-like error objects with code and message in server interactions; in UI, use clear status banners and inline validation

## Design and implementation constraints for AI
- Keep the workflow operational and practical rather than over-engineered
- Prefer incremental phases and small local feature additions
- Do not invent a new stack mid-build
- Do not create enterprise-level infrastructure when the prototype only needs local workflow logic
- Single-app architecture must remain the default unless a clear operational need emerges
