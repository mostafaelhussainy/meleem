# # 1. Use a lightweight Python base image
# FROM python:3.12-slim

# # 2. Set a working directory inside the container
# WORKDIR /app

# # 3. Copy requirements and install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # 4. Copy the FastAPI app code
# COPY . .

# # 5. Run FastAPI with uvicorn when container starts
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

######################################################################################################################

# Uses a lightweight Python 3.12 image.
# Keeps the container small but still flexible.
FROM python:3.12-slim

# Set environment variables
# PYTHONDONTWRITEBYTECODE=1 → don’t create .pyc files from being created (saves disk, cleaner).
# PYTHONUNBUFFERED=1 → ensures logs are output immediately (important for Docker logs).
# PYTHONPATH=/app → makes sure /app is in Python’s import path (so app.main works properly) | makes Python look inside /app for your code..
ENV PYTHONDONTWRITEBYTECODE=1 \ 
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app


# Set working directory
# All commands (COPY, RUN, etc.) now happen inside /app in the container.
# Keeps the container’s filesystem tidy.
WORKDIR /app

# Installs extra Linux tools the app might need:
    # gcc → a compiler, needed if some Python packages (like psycopg2) need to compile code.
    # postgresql-client → lets you use psql (Postgres command line).
# --no-install-recommends → installs only what’s strictly necessary.
# rm -rf /var/lib/apt/lists/* → cleans up leftover files to keep the image smaller.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copies only requirements.txt first (so Docker caching works).
# Upgrades pip.
# Installs Python dependencies.

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# After dependencies are installed, copies your actual FastAPI code into the container.
COPY . .

# By default, containers run as root (super admin). That’s risky.
# Here, we:
# Create a user called appuser.
# Give them permission to the /app folder.
# Switch to that user.
# ➡️ Like saying: “Don’t let the head chef (root) cook; let the assistant (appuser) handle it — safer.”
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app
USER appuser

# Tells Docker: “This app will be available on port 8000.”
# Doesn’t actually open it — but it’s documentation + hint for when you run docker run -p 8000:8000.
# ➡️ Like putting a sign: “Kitchen door is here.”
EXPOSE 8000

# Run FastAPI with uvicorn when container starts
# Starts FastAPI with Uvicorn.
# Runs on 0.0.0.0 so Docker can forward traffic from your host.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
