import os
import argparse
import re
from datetime import datetime

def slugify(text):
    """Converts a string to a filename-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text

def get_next_adr_number(adr_dir):
    """Finds the next ADR number based on existing files."""
    if not os.path.exists(adr_dir):
        return 1
    
    max_num = 0
    pattern = re.compile(r'^(\d{3,})-')
    
    for filename in os.listdir(adr_dir):
        match = pattern.match(filename)
        if match:
            num = int(match.group(1))
            if num > max_num:
                max_num = num
    
    return max_num + 1

def create_adr(title, adr_dir="docs/ADR"):
    """Creates a new ADR file."""
    # Ensure directory exists
    if not os.path.exists(adr_dir):
        os.makedirs(adr_dir)
        print(f"Created directory: {adr_dir}")

    # Determine filename
    next_num = get_next_adr_number(adr_dir)
    slug = slugify(title)
    filename = f"{next_num:03d}-{slug}.md"
    filepath = os.path.join(adr_dir, filename)

    # Content template
    content = f"""# {next_num}. {title}

Date: {datetime.now().strftime('%Y-%m-%d')}

## Context
<!-- What is the issue that we're seeing that is motivating this decision or change? -->

## Decision
<!-- What is the change that we're proposing and/or doing? -->

## Consequences
<!-- What becomes easier or more difficult to do and any risks introduced by the change that will need to be mitigated. -->
"""

    # Write file
    with open(filepath, 'w') as f:
        f.write(content)

    print(f"Created ADR: {filepath}")
    return filepath

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new Architectural Decision Record (ADR).")
    parser.add_argument("--title", required=True, help="Title of the ADR decision")
    parser.add_argument("--dir", default="docs/ADR", help="Directory to store ADRs (default: docs/ADR)")
    
    args = parser.parse_args()
    
    create_adr(args.title, args.dir)
