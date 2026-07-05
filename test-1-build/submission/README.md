# Lead-Scoring Agent (Test 1 Submission)

A deployed FastAPI service designed to score and route inbound B2B wholesale beverage leads using Google Gemini.

---

## 1. Model Choice & Rationale
We chose **`gemini-2.5-flash`** via the modern `google-genai` Python SDK:
*   **Structured Outputs**: Gemini natively supports Pydantic validation schemas. Passing `response_schema` guarantees that the LLM response is 100% compliant with our output structure, eliminating parsing/formatting errors.
*   **Latency & Cost**: Crucial for real-time webhooks, Flash operates with sub-second latencies and has a highly generous free tier for developer iteration.

---

## 2. Architectural Design
The codebase is structured under **Clean Architecture** principles to separate concerns and ensure maintainability:
*   `app/core/`: Configuration via Pydantic settings.
*   `app/models/`: Data Transfer Objects (DTOs) for incoming payloads and responses using Pydantic.
*   `app/repositories/`: Abstract interface and LLM data adapter for Gemini client calling.
*   `app/services/`: Main business logic. Handles default fallback calculations if Gemini goes offline or has invalid keys.
*   `app/controllers/`: Handles FastAPI HTTP endpoints (`/score` and `/api/v1/score`).

---

## 3. Lead-Scoring Logic & Weights
We evaluate leads based on a **0-100 score** allocated across four pillars:
1.  **Volume (30 pts)**: High volume (>= 1 FCL/month) earns full marks. Retail/office use earns 0.
2.  **Import License (30 pts)**: Established active licenses get 30. In-process gets 15. None gets 0.
3.  **Product Fit (20 pts)**: Brand alignment (Coke, Red Bull, Monster) gets 20. Other goods get 0.
4.  **Credibility (20 pts)**: Established retail network, years of experience gets 20.

### Tiers & Routing:
*   **Hot** (Score >= 80) &rarr; `kam_handoff` (Fast-track to Sales)
*   **Warm** (Score 40-79) &rarr; `nurture_pool` (Automatic drip marketing)
*   **Cold** (Score < 40) &rarr; `auto_archive` (Spam/Retail filter)

---

## 4. Run & Test Instructions

### Setup
1. Move to the directory: `cd test-1-build/submission`
2. Create your `.env` file: `cp .env.example .env`
3. Configure `GEMINI_API_KEY` in `.env` (optional, fallback logic will run if empty)
4. Activate the virtual environment: `source venv/bin/activate`

### Run Local Tests
Run our unit test suite utilizing FastAPI's `TestClient`:
```bash
python3 test_payloads.py
```

### Start Server
Run the local FastAPI server:
```bash
python3 main.py
```
The server will run on `http://localhost:8000`. You can POST JSON payloads to `http://localhost:8000/score`.

---

## 5. What We'd Do With More Time
1.  **Observability & Tracing**: Integrate LangSmith or OpenTelemetry to monitor LLM latencies, prompt drift, and token consumption.
2.  **CDP Database Logging**: Persist all inbound conversation logs and scores directly to a local SQL/NoSQL database for audit trails.
3.  **Queue-Based Processing**: Use Celery/Redis background jobs to handle scoring asynchronously if requests scale beyond thousands of parallel calls.

This is my URL deployed : https://northern-coast-takehome.vercel.app/

This is my URL Repo Github : https://github.com/Yohannes-Alexander/northern-coast-takehome.git
