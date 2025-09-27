# Exploratory Data Analysis Findings

## 1. Summary Statistics for Numeric Columns

The following table provides the mean, median, and standard deviation for all numeric columns.

|                | Mean   | Median   | Standard Deviation   |
|:---------------|:-------|:---------|:---------------------|
| Height_m       | 1.74   | 1.74     | 0.04                 |
| Weight_kg      | 59.83  | 61.69    | 6.46                 |
| Age            | 32.50  | 29.50    | 12.86                |
| Grip strength  | 26.00  | 27.00    | 4.52                 |
| BMI            | 19.68  | 19.19    | 1.78                 |
| Frailty_binary | 0.40   | 0.00     | 0.52                 |
| AgeGroup_<30   | 0.50   | 0.50     | 0.53                 |
| AgeGroup_30-45 | 0.30   | 0.00     | 0.48                 |
| AgeGroup_46-60 | 0.20   | 0.00     | 0.42                 |
| AgeGroup_>60   | 0.00   | 0.00     | 0.00                 |

## 2. Correlation of Grip Strength and Frailty

### Pearson Correlation Coefficient

The Pearson correlation between Grip strength and Frailty (binary) is: **-0.48**.

### Interpretation

Positive correlation (close to 1): As grip strength increases, the probability of being frail also increases.
Negative correlation (close to -1): As grip strength increases, the probability of being frail decreases.
No correlation (close to 0): There is no linear relationship between grip strength and frailty.

