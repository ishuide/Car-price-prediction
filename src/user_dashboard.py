from db_manager import query_all
from tabulate import tabulate
from joblib import load
import pandas as pd

MODEL_PATH = "models/price_linear_pipeline.joblib"

def display_menu():
    print("\n🚗 Toyota Corolla Used Car Analyzer")
    print("1. View all cars")
    print("2. Search cars by fuel type")
    print("3. Search cars by year range")
    print("4. Search cars by KM range")
    print("5. Show basic statistics")
    print("6. Exit")
    print("7. Predict car price")   # New option


def view_all_cars():
    df = query_all()
    print(tabulate(df.head(10), headers='keys', tablefmt='fancy_grid'))  


def search_by_fuel():
    df = query_all()
    fuel = input("Enter fuel type (e.g., Petrol, Diesel, CNG): ").strip().capitalize()
    results = df[df['fuel_type'] == fuel]
    print(tabulate(results.head(10), headers='keys', tablefmt='fancy_grid'))


def search_by_year():
    df = query_all()
    min_year = int(input("Enter minimum year (e.g., 2000): "))
    max_year = int(input("Enter maximum year (e.g., 2004): "))
    results = df[(df['mfg_year'] >= min_year) & (df['mfg_year'] <= max_year)]
    print(tabulate(results.head(10), headers='keys', tablefmt='fancy_grid'))


def search_by_km():
    df = query_all()
    min_km = int(input("Enter minimum KM: "))
    max_km = int(input("Enter maximum KM: "))
    results = df[(df['km'] >= min_km) & (df['km'] <= max_km)]
    print(tabulate(results.head(10), headers='keys', tablefmt='fancy_grid'))


def show_statistics():
    df = query_all()
    print("\n📊 Dataset Statistics:")
    
    print("\n📊 Numerical Features Summary:")
    print(df.describe(include=['number']).transpose())

    print("\n🗂️ Categorical Features Summary:")
    print(df.describe(include=['object']).transpose())


# 🔮 NEW FUNCTION – Predict Car Price
def predict_price():
    try:
        model = load(MODEL_PATH)
    except FileNotFoundError:
        print("❌ Trained model not found. Please run model training first.")
        return

    print("\n🔮 Enter car details for price prediction:")

    year = int(input("Manufacturing Year (e.g., 2002): "))
    km = int(input("Kilometers driven: "))
    hp = int(input("Horsepower: "))
    doors = int(input("Number of doors (e.g., 3, 4, 5): "))
    fuel = input("Fuel type (Petrol/Diesel/CNG): ").strip().capitalize()
    auto = int(input("Automatic? (1 = Yes, 0 = No): "))

    # Build sample input
    sample = pd.DataFrame([{
        "mfg_year": year,
        "km": km,
        "hp": hp,
        "doors": doors,
        "fuel_type": fuel,
        "automatic": auto
    }])

    pred = model.predict(sample)[0]
    print(f"\n💰 Estimated Price: $ {pred:.2f}")


def run_interface():
    while True:
        display_menu()
        choice = input("Choose an option (1-7): ").strip()
        
        if choice == '1':
            view_all_cars()
        elif choice == '2':
            search_by_fuel()
        elif choice == '3':
            search_by_year()
        elif choice == '4':
            search_by_km()
        elif choice == '5':
            show_statistics()
        elif choice == '6':
            print("Exiting. Thank you! 👋")
            break
        elif choice == '7':
            predict_price()
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    run_interface()
