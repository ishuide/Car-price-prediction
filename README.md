Used Car Price Prediction — Toyota Corolla Dataset

Overview

This project builds a machine learning model to predict the resale price of used Toyota Corolla cars based on their specifications such as age, mileage, fuel type, and more.
The model learns from real historical car data to estimate fair market prices, helping buyers and sellers make informed decisions.

---
Dataset

* Source: [ToyotaCorolla.csv](https://www.kaggle.com/datasets)
* Dataset Features (used):

  * `Age_08_04` — Age of the car in months (as of 2004)
  * `KM` — Distance driven (in kilometers)
  * `Fuel_Type` — Type of fuel (Petrol, Diesel, CNG)
  * `HP` — Horsepower
  * `Met_Color` — Metallic color indicator
  * `Automatic` — Transmission type (Manual/Automatic)
  * `Doors` — Number of doors
  * `Quarterly_Tax` — Tax amount per quarter
  * `Weight` — Weight of the car
  * Target: `Price` — Resale value of the car (in Euros)

---

Workflow

1. Data Preprocessing

   * Handle missing values and remove irrelevant columns.
   * Encode categorical variables (Fuel_Type, Transmission).
   * Normalize numerical features (Age, KM, Weight, HP, etc.).

2. Model Training

   * Split data into training and testing sets (80/20).
   * Train a Linear Regression model for price prediction.
   * Save the trained model and preprocessing pipeline using joblib.

3. Model Integration

   * Build an interactive Streamlit web app.
   * Users input car details → model predicts the resale price instantly.

4. Deployment

   * Run locally or deploy on **Streamlit Cloud** for online access.


Technologies Used

| Category        | Tools                               |
| --------------- | ----------------------------------- |
| Language        | Python                              |
| Libraries       | pandas, numpy, scikit-learn, joblib |
| Web Framework   | Streamlit                           |
| IDEs            | Jupyter Notebook / VS Code          |
| Version Control | Git & GitHub                        |


Steps to Run
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Train the model (optional)
python src/model_training.py

3️⃣ Run the Streamlit app
streamlit run app.py

Example Input(In terminal)

| Feature            | Example |
| ------------------ | ------- |
| Manufacturing Year | 2002    |
| KM Driven          | 70,000  |
| Horsepower         | 110     |
| No. of doors       | 3       |
| Fuel Type          | Petrol  |
| Automatic          | 1       |

Estimated Price: $ 15982.94
