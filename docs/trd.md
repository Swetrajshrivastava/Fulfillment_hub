# TRD — Fulfillment Hub

## Stack (proposed implementation decision)
Frontend: Python + Streamlit, Pandas, Plotly, lightweight dashboard UI
Backend: Python + SQLite for data processing and workflow logic
Database: SQLite with schema files and seeded demo data
Auth: Internal-only demo access; no external auth provider required for v1
Hosting: Local development using Streamlit; simple local deployment path later if needed

## Third-party services
| Service | Purpose | Free / local use |
|---------|---------|------------------|
| Streamlit | Dashboard and operational workflows | Free |
| SQLite | Local operational data store | Included |
| Pandas | Data shaping and filtering | Free |
| Plotly | Charts and operational visuals | Free |

## Constraints (HARD RULES)
- Budget: use free or bundled tools only
- Skill: keep the solution understandable and easy to maintain by a small team
- Performance: support a dataset of roughly 250–300 orders without lag
- Scope: do not build a broad commerce platform; focus on the operational workflow
- DO NOT USE: heavy enterprise platforms, Kafka, microservices, Docker-first architecture, or paid external APIs just to demonstrate the UI

## Conventions
- Naming: snake_case for Python and SQL-friendly operational names
- Folders: `app.py` for entry point, `database/` for schema and seed, `pages/` for workflow screens, `services/` for business logic if needed
- Data conventions: keep order IDs, exception IDs, and shipment IDs consistent and traceable
- Error handling: consistent in-app validation and clear status/banner messaging

## Implementation choices
- We are choosing a single-app architecture for the first build because the target users are operations staff, not engineers.
- We are prioritizing a clear operational workflow over highly abstract enterprise architecture.
- We will keep the workflow realistic and user-friendly for staff who are not comfortable with advanced software.
