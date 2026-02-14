#!/usr/bin/env python3
import sys
import os

def validate_report():
    """
    Validates that the security report was generated and follows basic format.
    """
    report_file = "security_report.md"
    
    if not os.path.exists(report_file):
        print(f"❌ Error: {report_file} not found. You must generate the report.")
        sys.exit(1)
        
    content = ""
    with open(report_file, 'r') as f:
        content = f.read()
        
    if not content.strip():
        print(f"❌ Error: {report_file} is empty.")
        sys.exit(1)
        
    if "| Vulnerability |" not in content:
        print("❌ Error: Report missing standard vulnerability table.")
        sys.exit(1)
        
    print("✅ Validation Passed: Security report format is correct.")
    sys.exit(0)

if __name__ == "__main__":
    validate_report()
