import os
from anyio import Path
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

def get_engine():
    host     = os.getenv("DB_HOST")
    user     = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")
    return create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

def run_query(sql, params=None):
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn, params=params)
    