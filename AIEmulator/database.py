# Initialize pathlib, sqlalchemy, and langchain imports
from pathlib import Path
from sqlalchemy import create_engine, text
from langchain_community.utilities import SQLDatabase

# Set up database paths and create directory if needed
DB_PATH = Path(__file__).parent / "data" / "sample.db"
DB_PATH.parent.mkdir(exist_ok=True)
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create definition for database
def database():

    # Creates object 'engine' responsible for communicating with the database
    engine = create_engine(DATABASE_URL)

    # Create Try block to catch exceptions when connecting to database
    try:
        # Use 'With' statement to connect engine object to database, automatically closing file once finished
        with engine.connect() as conn:
            # Execute the connection test with simple query
            conn.execute(text("SELECT 1"))
        print(f"✅ Connected successfully to {DB_PATH}")
        return engine

    # Catch if failed to connect to database
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        raise e

def get_langchain_db():
    # Take database connection URI and create a LangChain SQLDat6abase
    return SQLDatabase.from_uri(DATABASE_URL)