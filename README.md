# CareerLens AI

A beginner-friendly, runnable prototype of a multi-stage career guidance workflow: resume + target role → detected skills → gap analysis → roadmap → portfolio project ideas → interview practice.

## Project layout

- `frontend/` — React + Vite dashboard. The main flow talks to FastAPI directly so it can run without setting up MySQL or Spring Boot.
- `ai-service/` — Python FastAPI service with PDF text extraction and six small, deterministic agents in `app/agents.py`.
- `backend/` — Spring Boot REST API gateway with health and analysis proxy routes, BCrypt encoder configuration, CORS, and documented starter routes.
- `database/schema.sql` — normalized MySQL schema for users and career analyses.

## Run the demo

Requirements: Python 3.10+, Node.js 18+, and (optionally) Java 17/Maven and MySQL 8.

### 1. Start the AI service

```bash
cd ai-service
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

Interactive API docs: http://localhost:8001/docs

### 2. Start the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL Vite prints (usually http://localhost:5173). A sample resume and job description are preloaded. Upload a selectable-text PDF, edit/paste resume text, then analyze. The demo does not save a PDF; it sends it to the local service for extraction and discards it after the request.

### 3. Optional Spring Boot API

Run `database/schema.sql` in MySQL, then set `DB_URL`, `DB_USER`, and `DB_PASSWORD` as environment variables. From `backend/`, run `mvn spring-boot:run`. The analysis proxy is `POST http://localhost:8080/api/career/analyze`; set `AI_SERVICE_URL` to change the FastAPI URL.

## API examples

```http
POST /analyze
Content-Type: application/json
{"resume_text":"Python, SQL, Java","job_description":"Python, SQL, Java, FastAPI, Docker"}
```

Returns `match_percentage`, matched/missing/improvement skills, priorities, roadmap, project recommendations, interview questions, and interpretation notes. PDF extraction is `POST /resume/extract` with multipart field `file`.

## What the demo does and does not claim

Skill matching uses a small editable vocabulary and alias map, not an external LLM or embeddings. The agent modules are separate deterministic stages (parse/extract, normalize, compare, plan, recommend, prepare). The match percentage is matched detected skills divided by detected job skills; it is not a hiring probability. The current heuristic cannot infer skill proficiency reliably, so `improvement_skills` is empty until an evidence/rating step is added. Roadmap hours and project lengths are illustrative estimates. OCR for scanned PDFs is not installed; the service returns a clear message and users can paste text instead. No LLM key is required.

The frontend is a functional analysis dashboard. Authentication, per-user analysis history, persisted PDF records, and authenticated history endpoints are not enabled in this demo; the corresponding Spring routes return an explicit not-configured response. `BCryptPasswordEncoder` and a MySQL schema are included as foundations, not as a claim that JWT authentication is complete. Before exposing beyond localhost, implement database-backed registration/login, JWT issuance and request filtering, retention/deletion policies, rate limits, and stronger file validation. Do not store raw resume text unless the user has clearly consented.

## Extension points

- Add OCR through Tesseract or a managed OCR service in `ai-service/app/main.py`.
- Replace the skill vocabulary with an embeddings/LLM-backed extraction agent and return evidence spans/confidence.
- Add proficiency self-ratings and resume evidence so the improvement category is evidence-based.
- Persist analysis JSON and normalized skill/roadmap records using the supplied schema and protect user routes with JWT.
- Add a real curriculum source/catalog and citations rather than treating generated topics as course links.

## License

Educational prototype. Add a project license before redistribution.
