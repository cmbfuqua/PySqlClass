"""
Data Cleaning and Visualization - Practice

Examples:
df.fillna(0) # Fill missing values with 0
df.drop_duplicates() # Remove duplicate rows
"""
import pandas as pd

def clean_customer_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the given customer DataFrame by:
    1. Dropping rows with missing 'email' addresses.
    2. Filling missing 'age' values with the median age.
    3. Removing duplicate rows based on the 'customer_id' column, keeping the first occurrence.
    
    Returns the cleaned DataFrame.
    
    Starter code is incomplete.
    """
    # TODO: Drop rows where 'email' is NA
    # TODO: Calculate median age and fill NA 'age' values
    # TODO: Drop duplicates using subset=['customer_id'], keep='first'
    # TODO: Return the cleaned DataFrame
    pass
