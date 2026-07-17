import os
import tempfile
import pytest
from ..assignment import generate_markdown_report

def test_generate_markdown_report():
    activities = [
        {'user': 'alice', 'action': 'login', 'timestamp': '2023-10-01 10:00:00'},
        {'user': 'bob', 'action': 'logout', 'timestamp': '2023-10-01 10:05:00'}
    ]
    
    fd, path = tempfile.mkstemp()
    os.close(fd)
    
    try:
        generate_markdown_report(activities, path)
        
        with open(path, 'r') as f:
            content = f.read()
            
        assert "# User Activity Report" in content
        assert "| User | Action | Timestamp |" in content
        assert "| --- | --- | --- |" in content
        assert "| alice | login | 2023-10-01 10:00:00 |" in content
        assert "| bob | logout | 2023-10-01 10:05:00 |" in content
    finally:
        os.remove(path)
