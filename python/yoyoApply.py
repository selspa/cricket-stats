import os
from yoyo import read_migrations
from yoyo import get_backend

def db_migrations():
        user = os.getenv("DATABASE_USERNAME")
        password = os.getenv("DATABASE_PASSWORD")
        host = os.getenv("DATABASE_HOST")
        port = os.getenv("DATABASE_PORT")
        dbname = os.getenv("DATABASE_NAME")

        backend = get_backend(f'postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}')
        migrations = read_migrations('./migrations')

        with backend.lock():
            # Apply any outstanding migrations
            backend.apply_migrations(backend.to_apply(migrations))

        print("Database migrations applied")