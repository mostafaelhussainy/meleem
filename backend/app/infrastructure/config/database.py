from dataclasses import dataclass
from dotenv import load_dotenv
import os

@dataclass
class DatabaseConfig:
    host: str                  # Database server address
    port: int                  # Port number
    database: str              # Database name
    user: str                  # Username
    password: str              # Password
    min_connections: int = 1    # Minimum number of connections in the pool
    max_connections: int = 10   # Maximum number of connections in the pool

    @classmethod
    def from_env(cls) -> 'DatabaseConfig':
        load_dotenv()
        # Get environment variables with defaults
        
        return cls(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', '5432')),
            database=os.getenv('DB_NAME', ''),
            user=os.getenv('DB_USER', ''),
            password=os.getenv('DB_PASSWORD', ''),
            min_connections=int(os.getenv('DB_MIN_CONNECTIONS', '1')),
            max_connections=int(os.getenv('DB_MAX_CONNECTIONS', '10'))
        )