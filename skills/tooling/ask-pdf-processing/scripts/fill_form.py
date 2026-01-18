#!/usr/bin/env python3
"""
Fill PDF form fields using pypdf.

Usage:
    python fill_form.py template.pdf --data data.json --output filled.pdf
    python fill_form.py template.pdf --list-fields

Examples:
    # List all form fields in a PDF
    python fill_form.py form.pdf --list-fields
    
    # Fill form with JSON data
    python fill_form.py form.pdf --data input.json --output completed.pdf
    
    # Fill form with inline data
    python fill_form.py form.pdf --field "name=John Doe" --field "email=john@example.com" -o filled.pdf
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    print("Error: pypdf not installed. Run: pip install pypdf")
    sys.exit(1)


def list_form_fields(pdf_path: str) -> dict:
    """
    List all form fields in a PDF.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Dictionary of field names and their info
    """
    reader = PdfReader(pdf_path)
    fields = reader.get_fields()
    
    if not fields:
        return {}
    
    result = {}
    for name, info in fields.items():
        result[name] = {
            "type": str(info.get("/FT", "Unknown")),
            "value": str(info.get("/V", "")),
            "options": info.get("/Opt", [])
        }
    
    return result


def fill_form(
    template_path: str,
    output_path: str,
    field_data: dict,
    flatten: bool = False
) -> None:
    """
    Fill PDF form fields with provided data.
    
    Args:
        template_path: Path to the template PDF
        output_path: Path for the filled PDF
        field_data: Dictionary of field names and values
        flatten: Whether to flatten the form (make fields non-editable)
    """
    reader = PdfReader(template_path)
    writer = PdfWriter()
    
    # Clone the template
    writer.append(reader)
    
    # Fill fields on each page
    for page in writer.pages:
        writer.update_page_form_field_values(page, field_data)
    
    # Optionally flatten
    if flatten:
        for page in writer.pages:
            page.annotations = None
    
    with open(output_path, "wb") as f:
        writer.write(f)


def parse_field_args(field_args: list[str]) -> dict:
    """Parse --field arguments into a dictionary."""
    data = {}
    for field in field_args:
        if "=" not in field:
            print(f"Warning: Invalid field format '{field}', expected 'name=value'")
            continue
        name, value = field.split("=", 1)
        data[name.strip()] = value.strip()
    return data


def main():
    parser = argparse.ArgumentParser(
        description="Fill PDF form fields",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("input", help="Input PDF file (template)")
    parser.add_argument("--output", "-o", help="Output PDF file")
    parser.add_argument("--data", "-d", help="JSON file with field data")
    parser.add_argument(
        "--field", "-f",
        action="append",
        default=[],
        help="Field value in 'name=value' format (can be repeated)"
    )
    parser.add_argument(
        "--list-fields", "-l",
        action="store_true",
        help="List all form fields in the PDF"
    )
    parser.add_argument(
        "--flatten",
        action="store_true",
        help="Flatten form after filling (make non-editable)"
    )
    
    args = parser.parse_args()
    
    # Validate input
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    # List fields mode
    if args.list_fields:
        fields = list_form_fields(str(input_path))
        if not fields:
            print("No form fields found in this PDF.")
        else:
            print(f"Found {len(fields)} form field(s):\n")
            for name, info in fields.items():
                print(f"  Field: {name}")
                print(f"    Type:  {info['type']}")
                print(f"    Value: {info['value'] or '(empty)'}")
                if info['options']:
                    print(f"    Options: {info['options']}")
                print()
        return
    
    # Fill mode requires output
    if not args.output:
        print("Error: --output is required when filling forms", file=sys.stderr)
        sys.exit(1)
    
    # Gather field data
    field_data = {}
    
    if args.data:
        data_path = Path(args.data)
        if not data_path.exists():
            print(f"Error: Data file not found: {args.data}", file=sys.stderr)
            sys.exit(1)
        with open(data_path, encoding="utf-8") as f:
            field_data = json.load(f)
    
    # Command-line fields override JSON
    field_data.update(parse_field_args(args.field))
    
    if not field_data:
        print("Error: No field data provided (use --data or --field)", file=sys.stderr)
        sys.exit(1)
    
    # Fill the form
    fill_form(str(input_path), args.output, field_data, args.flatten)
    print(f"Filled form saved to: {args.output}")
    print(f"  Fields updated: {len(field_data)}")


if __name__ == "__main__":
    main()
