import os
import tempfile
import pytest
from ..practice import export_to_csv

def test_export_to_csv():
    data = [
        {'id': 1, 'name': 'Widget', 'price': 9.99},
        {'id': 2, 'name': 'Gadget', 'price': 14.50}
    ]
    
    fd, path = tempfile.mkstemp()
    os.close(fd)
    
    try:
        export_to_csv(data, path)
        
        with open(path, 'r') as f:
            lines = f.readlines()
            
        assert len(lines) == 3
        assert lines[0].strip() == "id,name,price"
        assert lines[1].strip() == "1,Widget,9.99"
        assert lines[2].strip() == "2,Gadget,14.5" or lines[2].strip() == "2,Gadget,14.50"
    finally:
        os.remove(path)
