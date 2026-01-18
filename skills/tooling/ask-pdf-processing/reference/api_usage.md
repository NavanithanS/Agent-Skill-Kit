# pypdf & pdfplumber API Reference

Quick reference for common PDF operations.

---

## pdfplumber

### Opening PDFs

```python
import pdfplumber

# Basic open
with pdfplumber.open("document.pdf") as pdf:
    pass

# With password
with pdfplumber.open("encrypted.pdf", password="secret") as pdf:
    pass
```

### PDF Object Properties

```python
pdf.metadata        # Document metadata (title, author, etc.)
pdf.pages          # List of Page objects
len(pdf.pages)     # Total page count
```

### Page Object Methods

```python
page = pdf.pages[0]

# Text extraction
page.extract_text()                    # All text as string
page.extract_text(layout=True)         # Preserve layout
page.extract_words()                   # List of word dicts

# Table extraction
page.extract_tables()                  # All tables as lists
page.extract_table()                   # First/largest table
page.find_tables()                     # Table objects with metadata

# Visual debugging
page.to_image()                        # PIL Image for debugging
page.to_image().draw_rects(rects)      # Draw rectangles
```

### Table Extraction Settings

```python
table_settings = {
    "vertical_strategy": "lines",    # or "text", "explicit"
    "horizontal_strategy": "lines",
    "snap_tolerance": 3,
    "join_tolerance": 3,
    "edge_min_length": 3,
    "min_words_vertical": 3,
    "min_words_horizontal": 1,
}

page.extract_tables(table_settings)
```

### Character-Level Access

```python
page.chars      # List of character dicts with position info
page.lines      # Line segment objects
page.rects      # Rectangle objects
page.curves     # Curve objects
```

---

## pypdf

### Reading PDFs

```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")

# With password
reader = PdfReader("encrypted.pdf", password="secret")

# Properties
reader.metadata         # Document info
len(reader.pages)       # Page count
reader.is_encrypted     # Encryption status
```

### Page Operations

```python
page = reader.pages[0]

# Text extraction
page.extract_text()                    # Extract text
page.extract_text(extraction_mode="layout")  # With layout

# Page properties
page.mediabox           # Page dimensions
page.rotation           # Page rotation
```

### Writing PDFs

```python
from pypdf import PdfWriter

writer = PdfWriter()

# Add pages
writer.add_page(page)                  # Add single page
writer.append("document.pdf")          # Add all pages from PDF
writer.append("doc.pdf", pages=(0, 3)) # Add pages 0-2

# Save
with open("output.pdf", "wb") as f:
    writer.write(f)
```

### Form Operations

```python
# List fields
reader.get_fields()                    # Dict of all fields

# Fill fields
writer.update_page_form_field_values(
    writer.pages[0],
    {"field_name": "value"}
)

# Flatten form (make non-editable)
for page in writer.pages:
    for annot in page.annotations or []:
        annot.update({"/Ff": 1})       # Read-only flag
```

### Merging

```python
writer = PdfWriter()

# Simple merge
writer.append("doc1.pdf")
writer.append("doc2.pdf")

# With page selection
writer.append("doc.pdf", pages=(0, 5))     # Pages 0-4
writer.append("doc.pdf", pages=[0, 2, 4])  # Specific pages

# Add bookmarks
writer.add_outline_item("Chapter 1", 0)    # Bookmark at page 0
```

### Page Manipulation

```python
# Rotate
page.rotate(90)             # Rotate 90 degrees clockwise

# Scale
page.scale(0.5, 0.5)        # Scale to 50%
page.scale_by(2)            # Scale by factor

# Crop
page.cropbox = (0, 0, 300, 400)

# Merge pages (overlay)
page.merge_page(overlay_page)
```

### Compression

```python
writer.compress_identical_objects()    # Deduplicate objects
writer.add_metadata({"/Producer": ""}) # Remove producer info
```

### Encryption

```python
# Add password
writer.encrypt(
    user_password="user",
    owner_password="owner",
    permissions_flag=-1        # All permissions
)

# Remove password (requires correct password first)
reader = PdfReader("encrypted.pdf", password="secret")
writer = PdfWriter()
writer.append(reader)
writer.write("decrypted.pdf")
```

---

## Common Patterns

### Extract Text from All Pages

```python
def extract_all_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join(
            page.extract_text() or ""
            for page in pdf.pages
        )
```

### Batch Form Filling

```python
def fill_forms(template, data_list, output_dir):
    from pathlib import Path
    
    for i, data in enumerate(data_list):
        reader = PdfReader(template)
        writer = PdfWriter()
        writer.append(reader)
        
        for page in writer.pages:
            writer.update_page_form_field_values(page, data)
        
        output = Path(output_dir) / f"filled_{i+1}.pdf"
        with open(output, "wb") as f:
            writer.write(f)
```

### Split PDF by Pages

```python
def split_pdf(input_path, output_dir):
    from pathlib import Path
    
    reader = PdfReader(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        
        output = output_dir / f"page_{i+1}.pdf"
        with open(output, "wb") as f:
            writer.write(f)
```

### Extract Images

```python
def extract_images(pdf_path):
    reader = PdfReader(pdf_path)
    images = []
    
    for page in reader.pages:
        for image in page.images:
            images.append({
                "name": image.name,
                "data": image.data,
                "width": image.image.width,
                "height": image.image.height
            })
    
    return images
```

---

## Error Handling

```python
from pypdf.errors import PdfReadError, FileNotDecryptedError

try:
    reader = PdfReader("document.pdf")
except PdfReadError:
    print("Invalid or corrupted PDF")
except FileNotDecryptedError:
    print("PDF is encrypted, provide password")
```
