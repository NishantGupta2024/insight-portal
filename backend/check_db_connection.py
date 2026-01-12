import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the database URL
database_url = os.getenv("DATABASE_URL")
print(f"Testing connection to: {database_url.split('@')[1]}") # Print only host to avoid exposing password

try:
    # Create engine
    engine = create_engine(database_url)
    
    # Try to connect
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("\nSUCCESS: Successfully connected to Supabase PostgreSQL Database!")
        
except Exception as e:
    print(f"\nERROR: Connection failed.\nDetails: {e}")
