#!/usr/bin/env python3
"""
Merge multiple PDF files into one using pypdf.

Usage:
    python merge_pdfs.py file1.pdf file2.pdf file3.pdf --output merged.pdf

Examples:
    # Basic merge
    python merge_pdfs.py doc1.pdf doc2.pdf -o combined.pdf
    
    # Merge with bookmarks
    python merge_pdfs.py doc1.pdf doc2.pdf --bookmarks -o combined.pdf
    
    # Merge specific pages
    python merge_pdfs.py "doc1.pdf:1-3" "doc2.pdf:5" -o partial.pdf
"""

import argparse
import sys
from pathlib import Path

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    print("Error: pypdf not installed. Run: pip install pypdf")
    sys.exit(1)


def parse_page_spec(spec: str) -> tuple[str, list[int] | None]:
    """
    Parse a page specification like 'file.pdf:1-3,5'.
    
    Args:
        spec: File path with optional page range
        
    Returns:
        Tuple of (file_path, page_list or None for all pages)
    """
    if ":" not in spec:
        return spec, None
    
    path, pages_str = spec.rsplit(":", 1)
    
    # Check if this is actually a Windows path (C:\...)
    if len(pages_str) > 0 and not pages_str[0].isdigit():
        return spec, None
    
    pages = []
    for part in pages_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-")
            pages.extend(range(int(start), int(end) + 1))
        else:
            pages.append(int(part))
    
    return path, pages


def merge_pdfs(
    pdf_specs: list[str],
    output_path: str,
    add_bookmarks: bool = False,
    compress: bool = True
) -> int:
    """
    Merge multiple PDFs into one.
    
    Args:
        pdf_specs: List of PDF paths (with optional page ranges)
        output_path: Path for the merged PDF
        add_bookmarks: Add bookmarks for each source PDF
        compress: Compress identical objects
        
    Returns:
        Total number of pages in merged PDF
    """
    writer = PdfWriter()
    total_pages = 0
    
    for spec in pdf_specs:
        path, pages = parse_page_spec(spec)
        
        if not Path(path).exists():
            print(f"Warning: File not found, skipping: {path}", file=sys.stderr)
            continue
        
        reader = PdfReader(path)
        file_name = Path(path).stem
        
        if add_bookmarks:
            writer.add_outline_item(file_name, total_pages)
        
        if pages:
            # Add specific pages (convert to 0-indexed)
            for page_num in pages:
                if 0 < page_num <= len(reader.pages):
                    writer.add_page(reader.pages[page_num - 1])
                    total_pages += 1
        else:
            # Add all pages
            for page in reader.pages:
                writer.add_page(page)
                total_pages += 1
    
    if compress:
        writer.compress_identical_objects()
    
    with open(output_path, "wb") as f:
        writer.write(f)
    
    return total_pages


def main():
    parser = argparse.ArgumentParser(
        description="Merge multiple PDF files into one",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="Input PDF files (use 'file.pdf:1-3,5' for specific pages)"
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Output PDF file"
    )
    parser.add_argument(
        "--bookmarks", "-b",
        action="store_true",
        help="Add bookmarks for each source PDF"
    )
    parser.add_argument(
        "--no-compress",
        action="store_true",
        help="Disable compression (faster but larger file)"
    )
    
    args = parser.parse_args()
    
    # Validate at least 2 inputs for merge
    if len(args.inputs) < 2:
        print("Error: Need at least 2 PDF files to merge", file=sys.stderr)
        sys.exit(1)
    
    # Merge
    total = merge_pdfs(
        args.inputs,
        args.output,
        add_bookmarks=args.bookmarks,
        compress=not args.no_compress
    )
    
    print(f"Merged PDF saved to: {args.output}")
    print(f"  Source files: {len(args.inputs)}")
    print(f"  Total pages: {total}")


if __name__ == "__main__":
    main()
