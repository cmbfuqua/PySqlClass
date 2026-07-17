"""
Automation and Reporting - Practice

Examples:
with open('output.csv', 'w') as f:
    f.write("id,value\n")
    f.write("1,100\n")
"""
import os

def export_to_csv(data: list[dict], filepath: str) -> None:
    """
    Takes a list of dictionaries and exports them to a CSV file.
    The keys of the first dictionary should be used as the CSV headers.
    
    Assume all dictionaries in the list have the same keys.
    Assume data is not empty.
    
    Starter code is incomplete.
    """
    # TODO: Open filepath in write mode ('w')
    # TODO: Extract headers from the keys of the first dictionary
    # TODO: Write the headers to the file (comma separated, followed by a newline)
    # TODO: Loop through the data and write each row's values (comma separated, followed by a newline)
    pass
