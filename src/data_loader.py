import pandas as pd

DROP_COLS = [
    "mfg_month", "cylinders", "guarantee_period", "radio", 
    "radio_cassette", "sport_model", "backseat_divider", "metallic_rim"
]


def load_and_clean_data(csv_path: str) -> pd.DataFrame:
    # Load dataset
    df = pd.read_csv(csv_path)
    
    # Initial shape
    print(f"Initial shape: {df.shape}")

    # Drop unnecessary columns
    df.drop(columns=DROP_COLS, inplace=True, errors='ignore')
    
    # Remove duplicates (if any)
    df.drop_duplicates(inplace=True)

    # Convert categorical binary columns to 0/1 integers (if needed)
    bool_cols = [
        'met_color', 'automatic', 'mfr_guarantee', 'bovag_guarantee',
        'abs', 'airbag_1', 'airbag_2', 'airco', 'automatic_airco',
        'boardcomputer', 'cd_player', 'central_lock', 'powered_windows',
        'power_steering', 'mistlamps', 'parking_assistant', 'tow_bar'
    ]
    for col in bool_cols:
        df[col] = df[col].fillna(0).astype(int)

    # Fill missing numerical values with median
    num_cols = df.select_dtypes(include='number').columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())

    # Fill missing categorical/text values with mode
    obj_cols = df.select_dtypes(include='object').columns
    for col in obj_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    print(f"Final shape after cleaning: {df.shape}")
    return df


# Quick test
if __name__ == "__main__":
    cleaned_df = load_and_clean_data("data/ToyotaCorolla.csv")
    print(cleaned_df.isnull().sum().sort_values(ascending=False).head(10))
    print(cleaned_df.head())
