from ..config.database import DatabaseConfig
from ..persistence.database import DatabaseConnectionFactory
from ..persistence.migration_runner import MigrationRunner

def main():
    # Load configuration from environment
    config = DatabaseConfig.from_env()
    
    # Initialize database connection pool
    DatabaseConnectionFactory.initialize(config)
    
    try:
        # Run migrations
        runner = MigrationRunner()
        runner.run_migrations()
    finally:
        # Clean up connections
        DatabaseConnectionFactory.close_all()

if __name__ == "__main__":
    main()
