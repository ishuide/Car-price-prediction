import os 
from data_loader import load_and_clean_data
from db_manager import insert_data
from user_interface import run_interface

def banner():
    print("\n🚗 Welcome to Toyota Corolla Used Car Analyzer")
    print("🔍 Built with Python, SQLite, Matplotlib, and Pandas")
    print("------------------------------------------------------")

def main():
    banner()

    data_path = "data/ToyotaCorolla.csv"

    if not os.path.exists(data_path):
        print(f"❌ Dataset not found at '{data_path}'. Please make sure it exists.")
        return

    print("📦 Loading and cleaning dataset...")
    df = load_and_clean_data(data_path)

    print("💾 Inserting data into local SQLite database...")
    insert_data(df)

    print("✅ Setup complete. Launching interface...\n")
    run_interface()

if __name__ == "__main__":
    main()
