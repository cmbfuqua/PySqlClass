import sys
import os
def build_dashboard():
    report = '<html><body><h1>Financial Pipeline Dashboard</h1></body></html>'
    with open('report.html', 'w') as f:
        f.write(report)
    return True
