import os

# Set test environment variables before any imports
# This ensures Settings class can initialize during test collection
# Allows override via environment variable (useful for CI/CD)
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql://test:test@localhost:5432/test_db"
)
