import pandas as pd
import numpy as np
import pytest
from ..assignment import summarize_sales

def test_summarize_sales():
    data = {
        'date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
        'category': ['Electronics', 'Clothing', None, 'Electronics'],
        'revenue': ['100.50', '50.00', '20.0', 'invalid'],
        'units_sold': [1, 2, 1, 1]
    }
    df = pd.DataFrame(data)
    
    result = summarize_sales(df)
    
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ['category', 'revenue']
    
    # Row 3 (None category) is dropped.
    # Row 4 ('invalid' revenue) becomes NaN upon numeric coercion and is dropped.
    # We are left with Electronics: 100.50, Clothing: 50.00
    
    elec_revenue = result[result['category'] == 'Electronics']['revenue'].values[0]
    assert elec_revenue == 100.50
    
    cloth_revenue = result[result['category'] == 'Clothing']['revenue'].values[0]
    assert cloth_revenue == 50.00
    
    assert len(result) == 2
