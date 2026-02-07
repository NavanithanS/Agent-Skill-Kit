# PDF Processing

A skill for handling PDF text extraction, form filling, and merging operations using `pypdf` and `pdfplumber`.

## Purpose

To enable AI agents to work with PDF documents effectively, including:
- **Text Extraction**: Extract text content from PDFs with layout awareness
- **Form Filling**: Populate PDF form fields programmatically
- **Merging**: Combine multiple PDFs into a single document

## Prerequisites

Install required dependencies:

```bash
pip install pypdf pdfplumber
```

## Tool Restrictions

When using this skill, agents should restrict their actions to:

| Allowed | Tools |
|---------|-------|
| ✅ Reading | `view_file`, `grep_search`, `list_dir`, `find_by_name` |
| ✅ Execution | `run_command` (only for running provided scripts) |
| ❌ Prohibited | Direct file writes outside script outputs |

> [!IMPORTANT]
> Only execute the provided Python scripts. Do not run arbitrary code that modifies PDFs without using the controlled scripts.

---

## Usage

### 1. Text Extraction

Use `pdfplumber` for layout-aware text extraction:

```bash
python scripts/extract_text.py input.pdf --output extracted.txt
```

**Python API**:
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

#### Extract Tables

```python
with pdfplumber.open("document.pdf") as pdf:
    page = pdf.pages[0]
    tables = page.extract_tables()
    for table in tables:
        for row in table:
            print(row)
```

---

### 2. Form Filling

Use `pypdf` to fill PDF form fields:

```bash
python scripts/fill_form.py template.pdf --data form_data.json --output filled.pdf
```

**Python API**:
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("form_template.pdf")
writer = PdfWriter()

# Clone the template
writer.append(reader)

# Fill form fields
writer.update_page_form_field_values(
    writer.pages[0],
    {
        "name": "John Doe",
        "email": "john@example.com",
        "date": "2026-01-18"
    }
)

with open("filled_form.pdf", "wb") as output:
    writer.write(output)
```

#### Discovering Form Fields

```python
from pypdf import PdfReader

reader = PdfReader("form.pdf")
fields = reader.get_fields()

for field_name, field_info in fields.items():
    print(f"Field: {field_name}")
    print(f"  Type: {field_info.get('/FT', 'Unknown')}")
    print(f"  Value: {field_info.get('/V', 'Empty')}")
```

---

### 3. PDF Merging

Use `pypdf` to combine multiple PDFs:

```bash
python scripts/merge_pdfs.py file1.pdf file2.pdf file3.pdf --output merged.pdf
```

**Python API**:
```python
from pypdf import PdfWriter

writer = PdfWriter()

# Add PDFs in order
for pdf_path in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    writer.append(pdf_path)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

#### Merge Specific Pages

```python
from pypdf import PdfReader, PdfWriter

writer = PdfWriter()

# Add pages 1-3 from first PDF
reader1 = PdfReader("doc1.pdf")
for page in reader1.pages[0:3]:
    writer.add_page(page)

# Add all pages from second PDF
writer.append("doc2.pdf")

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

---

## Examples

### Example 1: Extract Text from Invoice

```python
import pdfplumber

def extract_invoice_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
        
        # Parse invoice fields
        lines = text.split("\n")
        data = {}
        for line in lines:
            if "Invoice #" in line:
                data["invoice_number"] = line.split("#")[-1].strip()
            if "Total:" in line:
                data["total"] = line.split(":")[-1].strip()
        
        return data

result = extract_invoice_data("invoice.pdf")
print(result)
```

### Example 2: Batch Fill Forms

```python
import json
from pypdf import PdfReader, PdfWriter

def fill_form_batch(template_path, data_list, output_dir):
    for i, data in enumerate(data_list):
        reader = PdfReader(template_path)
        writer = PdfWriter()
        writer.append(reader)
        
        writer.update_page_form_field_values(
            writer.pages[0],
            data
        )
        
        output_path = f"{output_dir}/filled_{i+1}.pdf"
        with open(output_path, "wb") as f:
            writer.write(f)
        print(f"Created: {output_path}")

# Load data from JSON
with open("applicants.json") as f:
    applicants = json.load(f)

fill_form_batch("application.pdf", applicants, "./output")
```

### Example 3: Merge with Table of Contents

```python
from pypdf import PdfWriter

def merge_with_bookmarks(pdf_list, output_path):
    writer = PdfWriter()
    current_page = 0
    
    for pdf_info in pdf_list:
        path = pdf_info["path"]
        title = pdf_info["title"]
        
        # Add bookmark at current page
        writer.add_outline_item(title, current_page)
        
        # Append the PDF
        writer.append(path)
        
        # Update page counter
        from pypdf import PdfReader
        reader = PdfReader(path)
        current_page += len(reader.pages)
    
    with open(output_path, "wb") as f:
        writer.write(f)

pdfs = [
    {"path": "chapter1.pdf", "title": "Introduction"},
    {"path": "chapter2.pdf", "title": "Methods"},
    {"path": "chapter3.pdf", "title": "Results"},
]

merge_with_bookmarks(pdfs, "book.pdf")
```

---

## Best Practices

### Do's ✅

- **Validate PDFs before processing** — Check if files exist and are valid PDFs
- **Handle encrypted PDFs** — Use `pypdf`'s decryption if needed
- **Use context managers** — Always open PDFs with `with` statements
- **Process in batches** — For large operations, process files in chunks
- **Preserve metadata** — Copy document metadata when merging

### Don'ts ❌

- Don't load extremely large PDFs entirely into memory
- Don't ignore encoding issues in extracted text
- Don't overwrite original files without backup
- Don't assume all PDFs have extractable text (some are image-based)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No text extracted | PDF may be image-based; use OCR tools instead |
| Form fields not filling | Check field names with `get_fields()` |
| Merged PDF too large | Use `writer.compress_identical_objects()` |
| Unicode errors | Specify encoding or handle with error replacement |

---

## Notes

- **Image-based PDFs**: `pdfplumber` cannot extract text from scanned documents. Use OCR tools like `pytesseract` for those.
- **Encrypted PDFs**: `pypdf` can handle password-protected PDFs if you provide the password.
- **Form Flattening**: To make form fields non-editable after filling, flatten the PDF.

## Related Skills

- Document processing workflows
- Data extraction patterns
- Automation scripts

## Trigger Phrases

Activate this skill when the user says things like:
- "Extract text from this PDF"
- "Fill out this form"
- "Merge these PDF files"
- "Read data from this document"
