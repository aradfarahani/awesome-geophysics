import json
from urllib.parse import urlparse

def process_resource(resource, indent_level=0):
    """Process a resource and return Markdown lines with proper indentation.

    Args:
        resource (dict): The resource dictionary containing name, description, url, etc.
        indent_level (int): The indentation level for nested items (default is 0).

    Returns:
        list: A list of Markdown-formatted lines.
    """
    indent = ' ' * indent_level
    name = resource.get('name', 'Unnamed Resource')
    description = resource.get('description', '')
    url = resource.get('url', '')
    lines = []
    if url:
        lines.append(f"{indent}- **[`{name}`]({url})**")
    else:
        lines.append(f"{indent}- **`{name}`**")
    if description:
        # Split description into lines and indent each line
        desc_lines = description.split('\n')
        for desc_line in desc_lines:
            lines.append(f"{indent}  {desc_line}")
    if 'resources' in resource:
        for sub_resource in sorted(resource['resources'], key=lambda x: x['name'].lower()):
            lines.extend(process_resource(sub_resource, indent_level + 1))
    return lines

def process_subcategory(subcategory, indent_level=1):
    """Process a subcategory recursively and return Markdown lines.

    Args:
        subcategory (dict): The subcategory dictionary containing name, description, resources, etc.
        indent_level (int): The heading level for subcategories (default is 1, resulting in ###).

    Returns:
        list: A list of Markdown-formatted lines.
    """
    lines = []
    name = subcategory.get('name', 'Unnamed Subcategory')
    # Add subcategory heading (e.g., ### for indent_level=1, #### for indent_level=2)
    lines.append(f"\n{'#' * (indent_level + 2)} {name}\n")
    if 'description' in subcategory:
        lines.append(f"{subcategory['description']}\n")
    if 'resources' in subcategory:
        for resource in sorted(subcategory['resources'], key=lambda x: x['name'].lower()):
            lines.extend(process_resource(resource, indent_level))
    if 'subcategories' in subcategory:
        for sub_subcategory in subcategory['subcategories']:
            lines.extend(process_subcategory(sub_subcategory, indent_level + 1))
    return lines

def generate_toc(categories, indent=0):
    """Generate table of contents recursively for all categories and subcategories.

    Args:
        categories (list): List of category dictionaries.
        indent (int): Indentation level for TOC items (default is 0).

    Returns:
        list: A list of TOC entries with Markdown links.
    """
    toc = []
    for category in categories:
        name = category['name']
        anchor = name.lower().replace(' ', '-').replace('&', '').replace(',', '').replace('/', '')
        toc.append(f"{'  ' * indent}- [{name}](#{anchor})")
        if 'subcategories' in category:
            toc.extend(generate_toc(category['subcategories'], indent + 1))
    return toc

def github_star_count(url):
    """Generate GitHub star badge if URL is a GitHub repository."""
    github_stars = ""
    if "github.com" not in url.lower():
        return github_stars

    parsed = urlparse(url)
    # Remove any empty parts (e.g. from leading '/')
    path_parts = [part for part in parsed.path.split('/') if part]

    if len(path_parts) >= 2:
        github_username = path_parts[0]
        github_repo = path_parts[1]
        github_stars = (
            f"[![GitHub stars](https://img.shields.io/github/stars/{github_username}/{github_repo}?style=social)]"
            f"(https://github.com/{github_username}/{github_repo}/stargazers)"
        )
    return github_stars

def generate_markdown_from_json(json_file, output_file):
    """Generate a README.md file from the JSON data.

    Args:
        json_file (str): Path to the input JSON file (e.g., 'awesome_geophysics.json').
        output_file (str): Path to the output Markdown file (e.g., 'README.md').
    """
    # Load JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    md_content = []
    
    # Header with badges
    md_content.append('[![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)')
    md_content.append('<a href="https://github.com/aradfarahani/awesome-geophysics">')
    md_content.append('    <img src="https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=flat&color=BC4E99" alt="Star Badge"/>')
    md_content.append('</a>')
    md_content.append('<a href="https://github.com/aradfarahani/awesome-geophysics/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/aradfarahani/awesome-geophysics?color=2b9348"></a>')
    md_content.append('[![License](https://img.shields.io/github/license/aradfarahani/awesome-geophysics.svg)](https://github.com/aradfarahani/awesome-geophysics/blob/master/LICENSE)')
    md_content.append('[![Commits](https://img.shields.io/github/last-commit/aradfarahani/awesome-geophysics.svg?label=last%20contribution)](https://github.com/aradfarahani/awesome-geophysics/commits/main) [![GitHub stars](https://img.shields.io/github/stars/aradfarahani/awesome-geophysics?style=social)](https://github.com/aradfarahani/awesome-geophysics/stargazers) [![GitHub Forks](https://img.shields.io/github/forks/aradfarahani/awesome-geophysics?style=social)](https://github.com/aradfarahani/awesome-geophysics/forks)')
    md_content.append('')
    
    # Title and cover image
    md_content.append('# Awesome Geophysics')
    md_content.append('')
    md_content.append('# [<img src="https://cdn.rawgit.com/aradfarahani/awesome-geophysics/master/cover.png">](https://github.com/aradfarahani/awesome-geophysics)')
    md_content.append('')
    
    # Introduction
    metadata = data['AwesomeGeophysics']['metadata']
    md_content.append('<p align="justify">')
    md_content.append(f"Welcome to <strong>{metadata['title']}</strong> – {metadata['description']} Whether you're a student just beginning your journey, a researcher pushing the boundaries of the field, or a professional applying cutting-edge methods, this guide is your one-stop destination for software, datasets, educational materials, and much more. Let's explore the Earth's hidden depths and stay connected with the vibrant global geophysics community!")
    md_content.append('</p>')
    md_content.append('')
    md_content.append('---')
    md_content.append('')
    
    # Table of Contents
    md_content.append('## Table of Contents')
    toc = generate_toc(data['AwesomeGeophysics']['categories'])
    # Add footer sections
    toc.append('- [Contributors](#contributors)')
    toc.append('- [How to Contribute](#how-to-contribute)')
    toc.append('- [License](#license)')
    md_content.extend(toc)
    md_content.append('')
    md_content.append('| ▲ [Top](#awesome-geophysics) |')
    md_content.append('| --- |')
    md_content.append('---')
    md_content.append('')
    
    # Process each category
    for category in data['AwesomeGeophysics']['categories']:  # Remove sorting
        name = category['name']
        md_content.append(f"## {name}")
        md_content.append('')
        if 'description' in category:
            md_content.append(category['description'])
            md_content.append('')
        if name == "Software and Tools":
            # Table format for Software and Tools
            md_content.append('| **Name** | **Description** | **GitHub Stars** |')
            md_content.append('|----------|-----------------| -----------------|')
            # Sort only resources
            sorted_resources = sorted(category['resources'], key=lambda x: x['name'].lower())
            for resource in sorted_resources:
                res_name = resource.get('name', 'Unnamed Resource')
                desc = resource.get('description', 'No description available')
                url = resource.get('url', '#')
                github_stars = github_star_count(url)
                md_content.append(f"| **[`{res_name}`]({url})** | {desc} | {github_stars} |")
            md_content.append('')
        else:
            # List format for other categories
            if 'resources' in category:
                sorted_resources = sorted(category['resources'], key=lambda x: x['name'].lower())
                for resource in sorted_resources:
                    md_content.extend(process_resource(resource))
            
            if 'subcategories' in category:
                for subcategory in category['subcategories']:
                    md_content.extend(process_subcategory(subcategory))
        
        md_content.append('')
        md_content.append('| ▲ [Top](#awesome-geophysics) |')
        md_content.append('| --- |')
        md_content.append('---')
        md_content.append('')
    
    # Contributors section
    md_content.append('## Contributors')
    md_content.append('')
    md_content.append('Thanks to our many contributors!')
    md_content.append('')
    md_content.append('[![Contributors](https://contrib.rocks/image?repo=aradfarahani/awesome-geophysics)](https://github.com/aradfarahani/awesome-geophysics/graphs/contributors)')
    md_content.append('')
    md_content.append('| ▲ [Top](#awesome-geophysics) |')
    md_content.append('| --- |')
    md_content.append('')
    md_content.append('---')
    md_content.append('')
    
    # How to Contribute section
    md_content.append('## How to Contribute')
    md_content.append('')
    md_content.append('This list is a community effort and grows with your contributions!  ')
    md_content.append('Have a tool, dataset, blog, or resource to add? Here\'s how you can help:')
    md_content.append('')
    md_content.append('1. **Submit a Suggestion:**  ')
    md_content.append('   Open an issue or pull request on our [GitHub repository](https://github.com/aradfarahani/awesome-geophysics) to add or update resources.')
    md_content.append('')
    md_content.append('2. **Share Your Expertise:**  ')
    md_content.append('   Contribute by writing tutorials, guides, or blog posts that explain complex geophysical concepts in an accessible way.')
    md_content.append('')
    md_content.append('Together, we can continue to make Awesome Geophysics the definitive resource for the global geophysical community.')
    md_content.append('')
    md_content.append('> **For more detailed guidelines, please check the [CONTRIBUTING.md](https://github.com/aradfarahani/awesome-geophysics/blob/main/CONTRIBUTING.md) file.**')
    md_content.append('')
    md_content.append('| ▲ [Top](#awesome-geophysics) |')
    md_content.append('| --- |')
    md_content.append('')
    md_content.append('---')
    md_content.append('')
    
    # License section
    md_content.append('## License')
    md_content.append('')
    md_content.append('[![CC0](http://mirrors.creativecommons.org/presskit/buttons/88x31/svg/cc-zero.svg)](https://creativecommons.org/publicdomain/zero/1.0)')
    md_content.append('')
    md_content.append('To the extent possible under law, all contributors have waived all copyright and')
    md_content.append('related or neighboring rights to this work. ')
    md_content.append('')
    md_content.append('| ▲ [Top](#awesome-geophysics) |')
    md_content.append('| --- |')
    md_content.append('')
    md_content.append('---')
    md_content.append('')
    
    # Closing paragraph
    md_content.append('*Whether you\'re diving into seismic data processing, modeling Earth\'s subsurface, or simply looking for inspiration, we invite you to explore, share, and contribute. Let\'s push the boundaries of geophysical exploration and understanding—together!*')
    md_content.append('')
    
    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_content))

if __name__ == '__main__':
    generate_markdown_from_json('awesome_geophysics.json', 'README.md')
