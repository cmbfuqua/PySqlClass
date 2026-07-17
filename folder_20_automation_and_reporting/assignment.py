"""
Automation and Reporting - Assignment

Problem: Generate Markdown Summary Report
You need to generate a Markdown report summarizing a list of user activities.

Function Signature:
def generate_markdown_report(activities: list[dict], filepath: str) -> None:

Requirements:
1. `activities` is a list of dictionaries like: 
   [{'user': 'alice', 'action': 'login', 'timestamp': '2023-10-01 10:00:00'}, ...]
2. Write a Markdown file to `filepath`.
3. The report should start with a heading 1: "# User Activity Report".
4. Below the heading, create a Markdown table with columns: User, Action, Timestamp.
5. The table header in Markdown looks like this:
   | User | Action | Timestamp |
   | --- | --- | --- |
6. Add a row in the table for each dictionary in the list.
"""
def generate_markdown_report(activities: list[dict], filepath: str) -> None:
    pass
