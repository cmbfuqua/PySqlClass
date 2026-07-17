"""
Data Cleaning and Visualization - Assignment

Problem: Sales Data Visualization Prep
You are given a messy pandas DataFrame containing sales data. You need to clean it and prepare an aggregated summary suitable for visualization.

Function Signature:
def summarize_sales(df: pd.DataFrame) -> pd.DataFrame:

Requirements:
1. The DataFrame has columns: 'date', 'category', 'revenue', and 'units_sold'.
2. Remove any rows with missing 'category' or 'revenue'.
3. Convert the 'revenue' column to numeric (it might contain string values that can be parsed as float, errors should be coerced to NaN and then those rows dropped).
4. Group by 'category' and calculate the sum of 'revenue'.
5. Return a new DataFrame with 'category' as a column (reset the index) and the total revenue for each category.
"""
import pandas as pd

def summarize_sales(df: pd.DataFrame) -> pd.DataFrame:
    pass
