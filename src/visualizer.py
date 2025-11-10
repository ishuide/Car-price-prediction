import sys
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from data_loader import load_and_clean_data
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# ...existing code...


def plot_price_vs_km(df: pd.DataFrame):
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x='km', y='price', hue='fuel_type')
    plt.title("Price vs KM Driven")
    plt.xlabel("Kilometers Driven")
    plt.ylabel("Price")
    plt.tight_layout()
    plt.show()


def plot_price_by_fuel_type(df: pd.DataFrame):
    plt.figure(figsize=(6, 4))
    sns.boxplot(x='fuel_type', y='price', data=df)
    plt.title("Price Distribution by Fuel Type")
    plt.tight_layout()
    plt.show()


def plot_price_trend_by_year(df: pd.DataFrame):
    plt.figure(figsize=(7, 4))
    sns.lineplot(data=df.groupby("mfg_year")["price"].mean().reset_index(),
                 x="mfg_year", y="price")
    plt.title("Average Price Trend by Manufacturing Year")
    plt.tight_layout()
    plt.show()


def plot_hp_vs_price(df: pd.DataFrame):
    plt.figure(figsize=(7, 5))
    sns.scatterplot(data=df, x='hp', y='price', hue='automatic')
    plt.title("Price vs Horsepower (Colored by Transmission)")
    plt.tight_layout()
    plt.show()


# Run if needed
if __name__ == "__main__":
    df = load_and_clean_data("data/ToyotaCorolla.csv")
    plot_price_vs_km(df)
    plot_price_by_fuel_type(df)
    plot_price_trend_by_year(df)
    plot_hp_vs_price(df)
