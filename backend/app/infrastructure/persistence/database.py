from contextlib import contextmanager
from typing import Generator, Optional
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extensions import connection as Connection
from ..config.database import DatabaseConfig

class DatabaseConnectionFactory:
    _pool: Optional[SimpleConnectionPool] = None # The connection pool
    
    @classmethod
    def initialize(cls, config: DatabaseConfig) -> None:
        """Initialize the connection pool with the given configuration."""
        if cls._pool is not None: # If the connection pool is not None
            cls._pool.closeall() # Close all connections in the pool
        
        cls._pool = SimpleConnectionPool(
            minconn=config.min_connections, # Minimum number of connections in the pool
            maxconn=config.max_connections, # Maximum number of connections in the pool
            host=config.host, # Database server address
            port=config.port, # Port number
            database=config.database, # Database name
            user=config.user, # Username
            password=config.password # Password
        )
    
    @classmethod
    @contextmanager
    def get_connection(cls) -> Generator[Connection, None, None]:
        """Get a database connection from the pool."""
        if cls._pool is None: # If the connection pool is None
            raise RuntimeError("Database connection pool not initialized") # Raise an error
        
        conn: Connection = cls._pool.getconn() # Get a connection from the pool
        try:
            yield conn              # Yield the connection
            conn.commit()           # Commit the transaction
        except Exception:           # If an error occurs
            conn.rollback()         # Rollback the transaction
            raise                   # Raise the error
        finally:
            cls._pool.putconn(conn) # Put the connection back in the pool
    
    @classmethod
    def close_all(cls) -> None:
        """Close all connections in the pool."""
        if cls._pool is not None: # If the connection pool is not None
            cls._pool.closeall() # Close all connections in the pool
            cls._pool = None # Set the connection pool to None


