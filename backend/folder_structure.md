backend/
│── alembic/ # For migrations (when you switch to ORM)
│── app/
│ │── **init**.py
│ │── main.py # FastAPI entrypoint
│ │── api/ # Presentation Layer (routes/controllers)
│ │ │── **init**.py
│ │ │── v1/ # Versioned APIs
│ │ │ │── **init**.py
│ │ │ │── auth_routes.py
│ │ │ │── user_routes.py
│ │ │ │── transaction_routes.py
│ │
│ │── core/ # Cross-cutting concerns
│ │ │── **init**.py
│ │ │── config.py # Settings (using pydantic-settings)
│ │ │── security.py # JWT handling, password hashing, etc.
│ │ │── exceptions.py # Global app exceptions
│ │ │── logging.py # Custom logging setup
│ │
│ │── domain/ # Domain Layer (business rules/entities)
│ │ │── **init**.py
│ │ │── models/ # Pydantic domain models (not DB models)
│ │ │ │── **init**.py
│ │ │ │── user_model.py
│ │ │ │── auth_model.py
│ │ │ │── transaction_model.py
│ │
│ │── services/ # Application Layer (use cases/business logic)
│ │ │── **init**.py
│ │ │── auth_service.py
│ │ │── user_service.py
│ │ │── transaction_service.py
│ │
│ │── infrastructure/ # Data access, external services
│ │ │── **init**.py
│ │ │── db/ # Database
│ │ │ │── **init**.py
│ │ │ │── connection.py # asyncpg connection pool setup
│ │ │ │── migrations/ # If you start raw SQL migrations manually
│ │ │ │── repositories/ # Raw SQL Repos (later switch to ORM repos)
│ │ │ │ │── **init**.py
│ │ │ │ │── user_repository.py
│ │ │ │ │── transaction_repository.py
│ │ │
│ │ │── external/ # For third-party integrations (email, payment APIs etc.)
│ │ │ │── **init**.py
│ │ │ │── email_client.py
│ │
│ │── schemas/ # Request/Response Schemas (pydantic)
│ │ │── **init**.py
│ │ │── auth_schema.py
│ │ │── user_schema.py
│ │ │── transaction_schema.py
│ │
│ │── utils/ # Small helpers/utilities
│ │ │── **init**.py
│ │ │── time_utils.py
│ │ │── validation.py
│
│── tests/ # Testing suite
│ │── **init**.py
│ │── test_auth.py
│ │── test_user.py
│
│── .env # Environment variables
│── pyproject.toml # poetry config
│── taskipy.toml # for task runner (you already use it)
│── README.md
