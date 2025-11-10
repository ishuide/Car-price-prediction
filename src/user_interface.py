from db_manager import query_all
from tabulate import tabulate


def display_menu():
    print("\n🚗 Toyota Corolla Used Car Analyzer")
    print("1. View all cars")
    print("2. Search cars by fuel type")
    print("3. Search cars by year range")
    print("4. Search cars by KM range")
    print("5. Show basic statistics")
    print("6. Exit")


def view_all_cars():
    df = query_all()
    print(tabulate(df.head(10), headers='keys', tablefmt='fancy_grid'))  # Show first 10


def search_by_fuel():
    df = query_all()
    fuel = input("Enter fuel type (e.g., Petrol, Diesel): ").strip().capitalize()
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
    
    # Numerical columns
    print("\n📊 Numerical Features Summary:")
    print(df.describe(include=['number']).transpose())

# Categorical columns
    print("\n🗂️ Categorical Features Summary:")
    print(df.describe(include=['object']).transpose())


def run_interface():
    while True:
        display_menu()
        choice = input("Choose an option (1-6): ").strip()
        
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
        else:
            print("Invalid option. Try again.")

# Run the app directly
if __name__ == "__main__":
    run_interface()
