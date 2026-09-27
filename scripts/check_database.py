from sqlalchemy import text

from backend.app.db.database import SessionLocal


def main() -> None:
    db = SessionLocal()

    try:
        result = db.execute(
            text("SELECT current_database(), current_user, version();")
        )

        database_name, username, version = result.fetchone()

        print(f"Database: {database_name}")
        print(f"User: {username}")
        print(f"PostgreSQL: {version}")

        result = db.execute(
            text(
                """
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = 'public'
                """
            )
        )

        table_count = result.scalar_one()

        print(f"Public tables: {table_count}")

    finally:
        db.close()


if __name__ == "__main__":
    main()