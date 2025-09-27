# src/process_data.py

import pandas as pd
import os
import numpy as np

def process_data(input_csv_path, output_csv_path):
    """
    Ingests raw data from an existing CSV, performs unit standardization,
    feature engineering, and categorical encoding, then saves the processed data.

    Args:
        input_csv_path (str): Path to the existing raw CSV file.
        output_csv_path (str): Path to save the processed CSV file.
    """
    # Ingest Stage
    print(f"Loading raw data from {input_csv_path}...")
    try:
        df = pd.read_csv(input_csv_path)
    except FileNotFoundError:
        print(f"Error: Raw data file not found at {input_csv_path}. Please ensure it exists.")
        return

    # a. Unit standardization
    df['Height_m'] = df['Height'] * 0.0254
    df['Weight_kg'] = df['Weight'] * 0.45359237
    
    # Reorder the columns
    df = df[['Height_m', 'Weight_kg', 'Age', 'Grip strength', 'Frailty']]

    # b_i Feature engineering
    df['BMI'] = (df['Weight_kg'] / (df['Height_m'] ** 2)).round(2)

    # b_ii AgeGroup (categorical)
    bins = [0, 29, 45, 60, float('inf')]
    labels = ["<30", "30-45", "46-60", ">60"]
    df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels, right=True)


    # c_i Binary encoding for Frailty
    frailty_mapping = {'Y': 1, 'N': 0}
    df['Frailty_binary'] = df['Frailty'].str.strip().map(frailty_mapping)
    df['Frailty_binary'] = df['Frailty_binary'].fillna(0).astype('int8')


    # c_ii One-hot encode AgeGroup
    age_group_dummies = pd.get_dummies(df['AgeGroup'], prefix='AgeGroup', dtype=int)

    # Add the one-hot encoded columns to the DataFrame
    df = pd.concat([df, age_group_dummies], axis=1)

    # Clean up the DataFrame by dropping the original categorical columns
    df = df.drop(columns=['Frailty', 'AgeGroup'])


    # Save the processed data
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    df.to_csv(output_csv_path, index=False)
    print(f"Processed data saved to {output_csv_path}")

if __name__ == "__main__":
    assignment_base_path = r"C:\Users\18325\Desktop\CS5530\Assignment 11"

    raw_data_file = os.path.join(assignment_base_path, "data_raw", "raw_data.csv")
    processed_data_file = os.path.join(assignment_base_path, "data_processed", "processed_data.csv")

    process_data(raw_data_file, processed_data_file)
    print("Data processing complete.")
