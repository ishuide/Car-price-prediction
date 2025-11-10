import sqlite3
import pandas as pd
import os 

os.makedirs("database", exist_ok=True)
DB_PATH = "database/car_data.db"
TABLE_NAME = "used_cars"


def create_connection():
    return sqlite3.connect(DB_PATH)


def create_table_if_not_exists(conn: sqlite3.Connection, df: pd.DataFrame):
    cols = df.columns
    col_defs = ", ".join([f"{col} TEXT" if df[col].dtype == "object" else f"{col} REAL" for col in cols])
    create_sql = f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} ({col_defs});"
    conn.execute(create_sql)
    conn.commit()


def insert_data(df: pd.DataFrame):
    conn = create_connection()
    create_table_if_not_exists(conn, df)
    
    df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()
    print(f"Inserted {len(df)} rows into '{TABLE_NAME}'.")


def query_all():
    conn = create_connection()
    df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
    conn.close()
    return df


# Quick test
if __name__ == "__main__":
    from data_loader import load_and_clean_data
    df = load_and_clean_data("data/ToyotaCorolla.csv")
    insert_data(df)
    result = query_all()
    print(result.head())
