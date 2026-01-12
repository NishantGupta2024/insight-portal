from app.database import engine, Base
# Import all models to ensure they are registered with Base
from app.models import User, Upload, Report, Notification
from sqlalchemy import inspect

print("Attempting to create tables in Supabase...")
try:
    Base.metadata.create_all(bind=engine)
    print("create_all() executed.")

    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Tables in database: {tables}")

    required_tables = ["users", "uploads", "reports", "notifications"]
    missing = [t for t in required_tables if t not in tables]

    if not missing:
        print("\nSUCCESS: All required tables exist!")
    else:
        print(f"\nWARNING: Missing tables: {missing}")

except Exception as e:
    print(f"\nERROR during table creation: {e}")
