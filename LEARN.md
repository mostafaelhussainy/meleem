# To activate python virtual environment

-> venv\Scripts\activate

# To run the server

-> uvicorn app.main:app --reload

---

# packages:

- fastapi → the web framework
- uvicorn → ASGI server to run FastAPI
- psycopg2-binary → connect to Postgres (raw SQL)
- python-dotenv → load environment variables from .env

# To list all the packages

-> pip list

# Run all migrations

-> python -m app.infrastructure.scripts.run_migrations
