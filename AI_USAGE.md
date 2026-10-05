# AI Usage Note

**Project:** Fulfillment Hub

**Tools used:** ChatGPT for product planning and review; GitHub Copilot for in-editor implementation, debugging, and documentation support.

AI helped interpret the assignment, compare workflow ideas, draft SQLite queries and UI code, identify edge cases, and prepare project documentation. I reviewed generated changes against the warehouse workflow and tested the application rather than treating suggestions as requirements.

**Examples of my judgment**

1. I kept the product focused on warehouse operations instead of expanding it into a customer-facing commerce platform or adding an AI chatbot. Order urgency, stock risk, transfers, staging, and exceptions are the immediate operational problems in the brief.
2. A courier comparison can suggest average delay, but this database has no actual pickup timestamps. I chose to report confirmed and missed pickup outcomes instead, and to state that limitation rather than fabricate delay metrics. The order journey similarly distinguishes current-status progress from recorded event times.

The implementation remains local and SQLite-based, with synthetic data. Live integrations, interactive SKU/variant verification, and historical transition logging are outside the current scope. AI accelerated implementation and review; the final scope and claims were checked against the running application.
