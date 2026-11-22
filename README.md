# AI Resume Evaluator

Team project by **CVil Society**, built during Yapay Zeka ve Teknoloji Akademisi (the name is in the site footer). Four teammates recorded the work in three Scrum sprints and used Jira for the backlog. The original Turkish sprint reports are in [docs/sprint-reports.md](docs/sprint-reports.md).

This README describes the code in the repository today.

## What it does

A user can sign up, log in, upload a CV, and reopen a saved result. The upload form accepts PDF, DOC, and DOCX. The upload route in `app/views.py` then always calls `extract_text_from_pdf` in `app/model_logic.py`, which reads PDFs with pdfplumber. A Word file is saved, and that extraction step fails on it.

`read_cv_file` in `app/views.py` can read a PDF with PyPDF2 and a DOCX with python-docx. `POST /api/analyze/<cv_id>` is the route that uses it. The upload page leaves that helper unused.

When extraction returns text, `analyze_cv` does the following:

1. Detect the language with langdetect. A result of `en` is labeled English, and the grammar check uses LanguageTool `en-US`. Every other language code is labeled Türkçe, and the grammar check uses LanguageTool `tr`.
2. Score ten CV sections. For each section the code tries, in order, a meaningful-content check (full credit), a heading-text match (score 0.4), cosine similarity with `SentenceTransformer('all-MiniLM-L6-v2')`, and zero-shot classification with `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli`. The similarity step runs when the score is still below 0.4 and keeps a similarity above 0.4. The zero-shot step runs only if the score is still below 0.4.
3. Multiply each section score by a fixed weight and sum them. The weights are experience 25, education 15, skills 15, summary 10, leadership 10, certificates 10, contact 5, portfolio 5, languages 3, and references 2 (100 in total). If no section has meaningful content, the total is set to 0.
4. Run a grammar check on the first 5,000 characters with `language_tool_python`.
5. Add rule-based recommendations when the text does not mention Python, GitHub or GitLab, a project, or English.

The function return value includes the score, strengths, weaknesses, grammar notes, and recommendations. The results page shows the score, strengths, weaknesses, and recommendation text. It leaves the grammar notes unrendered.

The routed pages are server-rendered Flask templates: home, login, sign-up, upload, results, saved CVs, and profile. Accounts live in SQLite. Passwords are hashed with Werkzeug (`pbkdf2:sha256`) and sessions use Flask-Login.

## Team

| Name | GitHub |
|------|--------|
| Yunus Emre Açıkoğlu | [yemre345561](https://github.com/yemre345561) |
| Meriç Özcan | [mericozcann](https://github.com/mericozcann) |
| Tuana Korkmazyürek | [tuana0](https://github.com/tuana0) |
| Edanur Tekçe | [edax-1](https://github.com/edax-1) |

These four accounts are the GitHub contributors on this repository. A local `git shortlog` splits some of them across display names, so those counts are a poor measure of who did what. The sprint reports list all four as active through Sprint 3 (20 July 2025 to 3 August 2025).

## Tech stack

- Backend: Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF, Flask-Migrate
- Parsing and NLP: pdfplumber, PyPDF2, python-docx, langdetect, sentence-transformers, Hugging Face transformers, language_tool_python
- Background jobs: Celery is initialized in `app/tasks.py`. The broker is `sqla+sqlite:///celery.db` and the result backend is `db+sqlite:///celery_results.db`. `analyze_cv_async` has no callers. The upload route runs the analysis inside the request.
- Database: SQLite by default (`sqlite:///cv_analyzer.db`, which Flask-SQLAlchemy places in `instance/`). `DATABASE_URL` overrides that URI.

`app/__init__.py` imports `google.generativeai` on startup and calls `genai.configure` when `GOOGLE_API_KEY` is set. `analyze_cv` does not call Gemini.

## How to run

```bash
git clone https://github.com/yemre345561/AI-grup76.git
cd AI-grup76
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Then open http://127.0.0.1:5000 and create an account.

`app/views.py` imports `app/model_logic.py` at startup. That import builds `SentenceTransformer('all-MiniLM-L6-v2')` and the zero-shot pipeline, so the first launch downloads those weights and can take a while. The first grammar check can also download LanguageTool data.

`run.py` starts the app in debug mode on `0.0.0.0:5000` and creates the SQLite tables if they do not exist. `main.py` is leftover PyCharm boilerplate and is not the entry point.

Copy `.env.example` to `.env` for local settings. The app reads `FLASK_ENV`, `SECRET_KEY`, `DATABASE_URL`, `DATA_SCIENCE_API_URL`, and `GOOGLE_API_KEY`. `DATA_SCIENCE_API_URL` is stored on the config object and no route calls it. `FLASK_APP`, `MAX_CONTENT_LENGTH`, and `REDIS_URL` were names in the old env file; the application code does not read them (`MAX_CONTENT_LENGTH` is hardcoded at 16 MB). Do not commit `.env`.

## Project status

This is an academic prototype from a fixed sprint cycle, not a production service. Known gaps:

- Some packages in `requirements.txt` are pinned and some are not.
- CSRF protection is turned off for every config (`WTF_CSRF_ENABLED = False` in `app/__init__.py`).
- `main.py` is unused. `model_logic.py` at the repo root matches `app/model_logic.py` aside from line endings and trailing blank lines. `app/templates/index.html` has no route.
- Uploaded CVs, local SQLite files, and `.env` are listed in `.gitignore` and are absent from the current tree. Older commits were left unchanged, so a full history checkout can still contain them.
