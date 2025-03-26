import json

def process_resource(resource, indent_level=0):
    """Process a resource and return Markdown lines with proper indentation."""
    indent = '  ' * indent_level
    name = resource.get('name', 'Unnamed Resource')
    lines = []
    
    # Handle resource with or without URL and description
    url = resource.get('url', '#')
    description = resource.get('description', '')
    
    if url and url != '#':
        lines.append(f"{indent}- **[`{name}`]({url})**")
    else:
        lines.append(f"{indent}- **`{name}`**")
    
    if description:
        # Ensure description is indented under the resource
        lines.append(f"{indent}  {description}")
    
    # Handle nested resources
    if 'resources' in resource and resource['resources']:
        for sub_resource in resource['resources']:
            lines.extend(process_resource(sub_resource, indent_level + 1))
    
    return lines

def process_subcategory(subcategory, indent_level=1):
    """Process a subcategory recursively and return Markdown lines."""
    lines = []
    name = subcategory.get('name', 'Unnamed Subcategory')
    # Add subcategory heading (e.g., ### or #### based on indent_level)
    lines.append(f"\n{'#' * (indent_level + 2)} {name}\n")
    
    if 'description' in subcategory:
        lines.append(f"{subcategory['description']}\n")
    
    # Process resources under this subcategory
    if 'resources' in subcategory and subcategory['resources']:
        for resource in subcategory['resources']:
            lines.extend(process_resource(resource, indent_level))
    elif 'resources' in subcategory and not subcategory['resources']:
        lines.append(f"{'  ' * indent_level}- *No resources listed yet.*\n")
    
    # Process nested subcategories
    if 'subcategories' in subcategory and subcategory['subcategories']:
        for sub_subcategory in subcategory['subcategories']:
            lines.extend(process_subcategory(sub_subcategory, indent_level + 1))
    
    return lines

def generate_markdown_from_json(json_file, output_file):
    """Generate a README.md file from the JSON data."""
    # Load JSON data
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return
    
    md_content = []
    
    # Header with badges
    md_content.append('# Awesome Geophysics')
    md_content.append('')
    md_content.append('[![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)')
    md_content.append('<a href="https://github.com/aradfarahani/awesome-geophysics">')
    md_content.append('    <img src="https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=flat&color=BC4E99" alt="Star Badge"/>')
    md_content.append('</a>')
    md_content.append('<a href="https://github.com/aradfarahani/awesome-geophysics/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/aradfarahani/awesome-geophysics?color=2b9348"></a>')
    md_content.append('[![License](https://img.shields.io/github/license/aradfarahani/awesome-geophysics.svg)](https://github.com/aradfarahani/awesome-geophysics/blob/master/LICENSE)')
    md_content.append('[![Commits](https://img.shields.io/github/last-commit/aradfarahani/awesome-geophysics.svg?label=last%20contribution)](https://github.com/aradfarahani/awesome-geophysics/commits/main)')
    md_content.append('')
    
    # Introduction from metadata
    metadata = data['AwesomeGeophysics']['metadata']
    md_content.append(f"Welcome to **{metadata['title']}** – {metadata['description']} This guide is for students, researchers, and professionals alike. Explore software, datasets, and educational resources to deepen your understanding of geophysics!")
    md_content.append('')
    
    # Table of Contents
    md_content.append('## Table of Contents')
    toc = []
    for category in data['AwesomeGeophysics']['categories']:
        name = category['name']
        anchor = name.lower().replace(' ', '-').replace('&', '').replace(',', '')
        toc.append(f"- [{name}](#{anchor})")
        if 'subcategories' in category:
            for subcategory in category['subcategories']:
                sub_name = subcategory['name']
                sub_anchor = sub_name.lower().replace(' ', '-').replace('&', '').replace(',', '')
                toc.append(f"  - [{sub_name}](#{sub_anchor})")
    md_content.extend(toc)
    md_content.append('')
    
    # Process categories
    for category in data['AwesomeGeophysics']['categories']:
        name = category['name']
        md_content.append(f"## {name}\n")
        
        if 'description' in category:
            md_content.append(f"{category['description']}\n")
        
        # Special table format for "Software and Tools"
        if name == "Software and Tools" and 'resources' in category:
            md_content.append('| **Name** | **Description** |')
            md_content.append('|----------|-----------------|')
            for resource in category['resources']:
                res_name = resource.get('name', 'Unnamed Resource')
                desc = resource.get('description', 'No description available')
                url = resource.get('url', '#')
                md_content.append(f"| **[`{res_name}`]({url})** | {desc} |")
            md_content.append('')
        else:
            # Regular list format for other categories
            if 'resources' in category and category['resources']:
                for resource in category['resources']:
                    md_content.extend(process_resource(resource))
                md_content.append('')
            if 'subcategories' in category:
                for subcategory in category['subcategories']:
                    md_content.extend(process_subcategory(subcategory))
            md_content.append('')
    
    # Footer sections
    md_content.append('## License')
    md_content.append(f"\nThis project is licensed under {metadata['license']}.\n")
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_content))
    print(f"Markdown file generated: {output_file}")

if __name__ == "__main__":
    generate_markdown_from_json('awesome_geophysics.json', 'KREADME.md')
