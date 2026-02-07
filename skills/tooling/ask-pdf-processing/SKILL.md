---
name: ask-pdf-processing
description: PDF text extraction, form filling, and merging using pypdf and pdfplumber.
triggers: ["extract text from pdf", "fill pdf form", "merge pdfs", "read pdf"]
---

<critical_constraints>
❌ NO arbitrary file writes → use provided scripts only
❌ NO loading huge PDFs into memory → process in chunks
❌ NO overwriting originals → backup first
✅ MUST use context managers (`with` statements)
✅ MUST validate PDFs before processing
✅ MUST handle encrypted PDFs with password
</critical_constraints>

<dependencies>
pip install pypdf pdfplumber
</dependencies>

<operations>
## Text Extraction (pdfplumber)
```python
with pdfplumber.open("doc.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        tables = page.extract_tables()
```

## Form Filling (pypdf)
```python
from pypdf import PdfReader, PdfWriter
writer = PdfWriter()
writer.append(PdfReader("template.pdf"))
writer.update_page_form_field_values(writer.pages[0], {"name": "John"})
writer.write(open("filled.pdf", "wb"))
```

## Discover Fields
```python
fields = PdfReader("form.pdf").get_fields()
```

## Merge PDFs
```python
writer = PdfWriter()
for pdf in ["a.pdf", "b.pdf"]:
    writer.append(pdf)
writer.write(open("merged.pdf", "wb"))
```
</operations>

<troubleshooting>
| Issue | Solution |
|-------|----------|
| No text extracted | Image-based PDF → use OCR (pytesseract) |
| Fields not filling | Check names with get_fields() |
| Large output | Use writer.compress_identical_objects() |
</troubleshooting>

<heuristics>
- Scanned document → recommend OCR instead
- Form fields unknown → run get_fields() first
- Many PDFs → batch process with chunks
</heuristics>
