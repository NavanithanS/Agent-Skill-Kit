import os
import argparse

def create_component(name, base_dir="."):
    """Creates a new component structure."""
    component_dir = os.path.join(base_dir, name)
    
    if os.path.exists(component_dir):
        print(f"Error: Directory {component_dir} already exists.")
        return

    os.makedirs(component_dir)
    print(f"Created directory: {component_dir}")

    # index.tsx
    index_content = f"""import React from 'react';
import styles from './styles.module.css';

interface {name}Props {{
  // Define props here
  title?: string;
}}

export const {name}: React.FC<{name}Props> = ({{ title }}) => {{
  return (
    <div className={{styles.container}}>
      {{title && <h1>{{title}}</h1>}}
      <p>{name} Component</p>
    </div>
  );
}};
"""
    with open(os.path.join(component_dir, "index.tsx"), "w") as f:
        f.write(index_content)

    # styles.module.css
    styles_content = """.container {
  display: block;
}
"""
    with open(os.path.join(component_dir, "styles.module.css"), "w") as f:
        f.write(styles_content)

    # Component.test.tsx
    test_content = f"""import React from 'react';
import {{ render, screen }} from '@testing-library/react';
import {{ {name} }} from './index';

describe('{name}', () => {{
  it('renders correctly', () => {{
    render(<{name} />);
    expect(screen.getByText('{name} Component')).toBeInTheDocument();
  }});
}});
"""
    with open(os.path.join(component_dir, "Component.test.tsx"), "w") as f:
        f.write(test_content)

    print(f"Successfully created component '{name}' in {component_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold a new UI component.")
    parser.add_argument("--name", required=True, help="Name of the component")
    parser.add_argument("--dir", default=".", help="Directory to create the component in")
    
    args = parser.parse_args()
    
    create_component(args.name, args.dir)
