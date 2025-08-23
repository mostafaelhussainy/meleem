from typing import List
from pathlib import Path
from .database import DatabaseConnectionFactory

class MigrationRunner:
    def __init__(self, migrations_path: str = "app/migrations"):
        self.migrations_path = Path(migrations_path) # Convert the migrations path to a Path object
        
    def get_migration_files(self) -> List[Path]:
        """Get all SQL migration files sorted by name."""
        if not self.migrations_path.exists():
            raise FileNotFoundError(f"Migrations directory not found: {self.migrations_path}") # Raise an error if the migrations directory does not exist
        
        # Get all SQL migration files sorted by name
        return sorted(
            [f for f in self.migrations_path.glob("*.sql")], # Get all files with the .sql extension
            key=lambda x: x.name # Sort the files by name
        )
    
    def run_migrations(self) -> None:
        """Run all migrations in order."""
        migration_files = self.get_migration_files() # Get all migration files sorted by name
        
        with DatabaseConnectionFactory.get_connection() as conn: # Get a database connection
            # Create migrations table if it doesn't exist
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS applied_migrations (
                        migration_name TEXT PRIMARY KEY,
                        applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            
            # Get applied migrations
            with conn.cursor() as cur:
                cur.execute("SELECT migration_name FROM applied_migrations")
                applied_migrations = {row[0] for row in cur.fetchall()} # Get all applied migrations
            
            # Apply new migrations
            for migration_file in migration_files:
                if migration_file.name not in applied_migrations:
                    print(f"Applying migration: {migration_file.name}") # Print the migration name
                    
                    # Read and execute migration
                    sql = migration_file.read_text() # Read the migration file
                    with conn.cursor() as cur:
                        cur.execute(sql) # Execute the migration
                        
                    # Mark migration as applied
                    with conn.cursor() as cur:
                        cur.execute(
                            "INSERT INTO applied_migrations (migration_name) VALUES (%s)",
                            (migration_file.name,)
                        )
                    
                    print(f"Successfully applied migration: {migration_file.name}") # Print the migration name
                else:
                    print(f"Skipping already applied migration: {migration_file.name}") # Print the migration name
