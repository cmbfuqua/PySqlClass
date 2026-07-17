import pandas as pd
import numpy as np
import pytest
from ..practice import clean_customer_data

def test_clean_customer_data():
    data = {
        'customer_id': [1, 2, 3, 1, 4, 5],
        'email': ['a@a.com', None, 'c@c.com', 'a@a.com', 'd@d.com', 'e@e.com'],
        'age': [25, 30, np.nan, 25, 40, 50]
    }
    df = pd.DataFrame(data)
    
    cleaned_df = clean_customer_data(df)
    
    assert isinstance(cleaned_df, pd.DataFrame)
    
    # Customer 2 should be dropped (missing email)
    assert 2 not in cleaned_df['customer_id'].values
    
    # Duplicate customer 1 should be removed
    assert len(cleaned_df[cleaned_df['customer_id'] == 1]) == 1
    
    # Check there are no NA values in age
    assert not cleaned_df['age'].isna().any()
    
    # Check overall size
    assert len(cleaned_df) == 4 # 1, 3, 4, 5
