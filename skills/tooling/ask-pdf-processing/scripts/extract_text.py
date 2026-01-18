#!/usr/bin/env python3
"""
Extract text from PDF files using pdfplumber.

Usage:
    python extract_text.py input.pdf [--output output.txt] [--pages 1,2,3]

Examples:
    python extract_text.py document.pdf
    python extract_text.py document.pdf --output extracted.txt
    python extract_text.py document.pdf --pages 1,3,5
"""

import argparse
import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("Error: pdfplumber not installed. Run: pip install pdfplumber")
    sys.exit(1)


def extract_text(pdf_path: str, pages: list[int] | None = None) -> str:
    """
    Extract text from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        pages: Optional list of page numbers (1-indexed) to extract
        
    Returns:
        Extracted text as a string
    """
    extracted = []
    
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        
        if pages:
            # Convert to 0-indexed and validate
            page_indices = [p - 1 for p in pages if 0 < p <= total_pages]
        else:
            page_indices = range(total_pages)
        
        for i in page_indices:
            page = pdf.pages[i]
            text = page.extract_text()
            if text:
                extracted.append(f"--- Page {i + 1} ---\n{text}")
    
    return "\n\n".join(extracted)


def extract_tables(pdf_path: str, page_num: int = 1) -> list[list]:
    """
    Extract tables from a specific page.
    
    Args:
        pdf_path: Path to the PDF file
        page_num: Page number (1-indexed)
        
    Returns:
        List of tables, each table is a list of rows
    """
    with pdfplumber.open(pdf_path) as pdf:
        if page_num > len(pdf.pages):
            return []
        
        page = pdf.pages[page_num - 1]
        return page.extract_tables()


def main():
    parser = argparse.ArgumentParser(
        description="Extract text from PDF files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("input", help="Input PDF file")
    parser.add_argument("--output", "-o", help="Output text file (default: stdout)")
    parser.add_argument(
        "--pages", "-p",
        help="Comma-separated page numbers to extract (e.g., 1,3,5)"
    )
    parser.add_argument(
        "--tables", "-t",
        action="store_true",
        help="Extract tables instead of text"
    )
    
    args = parser.parse_args()
    
    # Validate input
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    # Parse pages
    pages = None
    if args.pages:
        try:
            pages = [int(p.strip()) for p in args.pages.split(",")]
        except ValueError:
            print("Error: Invalid page numbers", file=sys.stderr)
            sys.exit(1)
    
    # Extract content
    if args.tables:
        tables = extract_tables(str(input_path), pages[0] if pages else 1)
        result = "\n".join(str(table) for table in tables)
    else:
        result = extract_text(str(input_path), pages)
    
    # Output
    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
        print(f"Extracted text saved to: {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
