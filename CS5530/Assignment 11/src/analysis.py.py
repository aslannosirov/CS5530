# src/analysis.py

import pandas as pd
import os

def analyze_data(input_processed_csv_path, reports_dir):
    """
    Loads processed data, performs EDA and analysis, and generates a findings report.

    Args:
        input_processed_csv_path (str): Path to the processed CSV file.
        reports_dir (str): Directory where the findings.md report will be saved.
    """
    # --- Load Processed Data ---
    print(f"Loading processed data from {input_processed_csv_path}...")
    try:
        df_processed = pd.read_csv(input_processed_csv_path)
    except FileNotFoundError:
        print(f"Error: Processed data file not found at {input_processed_csv_path}. "
              "Please ensure 'data_processing.py' has been run successfully.")
        return # Exit if the file doesn't exist

    print("Processed data loaded successfully.")

    # Ensure the reports directory exists
    os.makedirs(reports_dir, exist_ok=True)
    findings_report_path = os.path.join(reports_dir, "findings.md")
    
    # --- I. Compute summary table ---
    # Select only numeric columns for summary statistics
    numeric_cols = df_processed.select_dtypes(include=['number']).columns
    summary_table = df_processed[numeric_cols].agg(['mean', 'median', 'std']).T

    # Rename columns for clarity in the report
    summary_table.columns = ['Mean', 'Median', 'Standard Deviation']

    # Convert the summary table to a Markdown format
    summary_markdown = summary_table.to_markdown(numalign="left", stralign="left", floatfmt=".2f")


    try:
        correlation = df_processed['Grip strength'].corr(df_processed['Frailty_binary'])
    except KeyError as e:
        print(f"Error: Missing column {e}. Please ensure 'Grip strength' and 'Frailty_binary' exist.")
        exit()

    
    # --- Analysis Stage ---

    with open(findings_report_path, 'w') as f:
        f.write("# Exploratory Data Analysis Findings\n\n")

        f.write("## 1. Summary Statistics for Numeric Columns\n\n")
        f.write("The following table provides the mean, median, and standard deviation for all numeric columns.\n\n")
        f.write(summary_markdown)
        f.write("\n\n")

        f.write("## 2. Correlation of Grip Strength and Frailty\n\n")
        f.write("### Pearson Correlation Coefficient\n\n")
        f.write(f"The Pearson correlation between Grip strength and Frailty (binary) is: **{correlation:.2f}**.\n\n")
        f.write("### Interpretation\n\n")
        f.write(
            "Positive correlation (close to 1): As grip strength increases, the probability of being frail also increases.\n"
            "Negative correlation (close to -1): As grip strength increases, the probability of being frail decreases.\n"
            "No correlation (close to 0): There is no linear relationship between grip strength and frailty.\n"
        )
        f.write("\n")

        

    print(f"Analysis complete. Findings reported in {findings_report_path}")


if __name__ == "__main__":
    # Define your paths - adjust based on your project_root location
    assignment_base_path = r"C:\Users\18325\Desktop\CS5530\Assignment 11"

    # Construct the full paths for processed data file and reports directory
    processed_data_file = os.path.join(assignment_base_path, "data_processed", "processed_data.csv")
    reports_directory = os.path.join(assignment_base_path, "reports")

    # Make sure processed_data.csv exists before running analysis, or run data_processing.py first
    if not os.path.exists(processed_data_file):
        print(f"Error: Processed data file '{processed_data_file}' not found.")
        print("Please run 'data_processing.py' first to generate the processed data.")
    else:
        analyze_data(processed_data_file, reports_directory)
        print("Analysis script finished.")

