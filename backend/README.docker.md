# Meleem Backend Docker Setup

## Prerequisites

- Docker
- Docker Compose

## Setup Instructions

1. Clone the repository

```bash
git clone <your-repository-url>
cd meleem-backend
```

2. Create environment file

```bash
cp .env.example .env
```

Then edit `.env` and set secure values for passwords and keys.

3. Start the services

```bash
docker-compose up -d
```

4. Check if services are running

```bash
docker-compose ps
```

5. View logs

```bash
docker-compose logs -f app
```

## Environment Variables

Required environment variables in `.env`:

- DB_USER: Database username
- DB_PASSWORD: Database password
- DB_NAME: Database name
- JWT_SECRET_KEY: Secret key for JWT token generation

## Available Endpoints

The API will be available at: http://localhost:8000

## Troubleshooting

If you encounter any issues:

1. Check logs: `docker-compose logs`
2. Ensure all environment variables are set correctly
3. Try rebuilding: `docker-compose up -d --build`
4. Make sure ports 8000 and 5432 are not in use

## Stopping the Services

```bash
docker-compose down
```

To remove volumes (will delete database data):

```bash
docker-compose down -v
```

