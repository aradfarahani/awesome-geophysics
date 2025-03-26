import json

def process_resource(resource, indent_level=0):
    """Helper function to process a resource with proper indentation"""
    indent = '  ' * indent_level
    name = resource['name']
    lines = []
    
    # Handle resources that have both description and sub-resources
    if 'description' in resource:
        description = resource['description']
        if description.strip().startswith('```'):
            lines.append(f"{indent}- **`{name}`**  \n{indent}{description}\n")
        else:
            url = resource.get('url', '#')
            if url and url != '#':
                lines.append(f"{indent}- **[`{name}`]({url})**  \n{indent}  {description}\n")
            else:
                lines.append(f"{indent}- **`{name}`**  \n{indent}  {description}\n")
    
    # Handle sub-resources if they exist
    if 'resources' in resource:
        if 'description' not in resource:  # Only add name if no description exists
            lines.append(f"{indent}- **{name}**")
        for sub_resource in resource['resources']:
            lines.extend(process_resource(sub_resource, indent_level + 1))
    
    return lines

def generate_markdown_from_json(json_file, output_file):
    # Load the JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Start building the markdown content
    md_content = []
    
    # Add header with badges
    md_content.append('[![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)')
    md_content.append('<a href="https://github.com/aradfarahani/awesome-geophysics">')
    md_content.append('    <img src="https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=flat&color=BC4E99" alt="Star Badge"/>')
    md_content.append('</a>')
    md_content.append('<a href="https://github.com/aradfarahani/awesome-geophysics/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/aradfarahani/awesome-geophysics?color=2b9348"></a>')
    md_content.append('[![License](https://img.shields.io/github/license/aradfarahani/awesome-geophysics.svg)](https://github.com/aradfarahani/awesome-geophysics/blob/master/LICENSE)')
    md_content.append('[![Commits](https://img.shields.io/github/last-commit/aradfarahani/awesome-geophysics.svg?label=last%20contribution)](https://github.com/aradfarahani/awesome-geophysics/commits/main) [![GitHub stars](https://img.shields.io/github/stars/aradfarahani/awesome-geophysics?style=social)](https://github.com/aradfarahani/awesome-geophysics/stargazers) [![GitHub Forks](https://img.shields.io/github/forks/aradfarahani/awesome-geophysics?style=social)](https://github.com/aradfarahani/awesome-geophysics/forks)')
    md_content.append('')
    
    # Add title and cover image
    md_content.append('# Awesome Geophysics')
    md_content.append('')
    md_content.append('# [<img src="https://cdn.rawgit.com/aradfarahani/awesome-geophysics/master/cover.png">](https://github.com/aradfarahani/awesome-geophysics)')
    md_content.append('')
    
    # Add introduction paragraph
    md_content.append('<p align="justify">')
    md_content.append('Welcome to <strong>Awesome Geophysics</strong> – a community-curated, ever-evolving collection of resources that spans the full spectrum of geophysical sciences. Whether you\'re a student just beginning your journey, a researcher pushing the boundaries of the field, or a professional applying cutting-edge methods, this guide is your one-stop destination for software, datasets, educational materials, and much more. Let\'s explore the Earth\'s hidden depths and stay connected with the vibrant global geophysics community!')
    md_content.append('</p>')
    md_content.append('')
    md_content.append('---')
    md_content.append('')
    
    # Generate Table of Contents
    md_content.append('## Table of Contents')
    toc = []
    for category in data['AwesomeGeophysics']['categories']:
        name = category['name']
        anchor = name.lower().replace(' ', '-').replace('&', '').replace(',', '').replace('/', '')
        toc.append(f'- [{name}](#{anchor})')
        
        if 'subcategories' in category:
            for subcategory in category['subcategories']:
                sub_name = subcategory['name']
                sub_anchor = sub_name.lower().replace(' ', '-').replace('&', '').replace(',', '').replace('/', '')
                toc.append(f'  - [{sub_name}](#{sub_anchor})')

    
    # Add the footer sections to TOC
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
    for category in data['AwesomeGeophysics']['categories']:
        name = category['name']
        md_content.append(f'## {name}')
        md_content.append('')
        
        if 'description' in category:
            md_content.append(category['description'])
            md_content.append('')
        
        # Special handling for Software and Tools (table format)
        if name == "Software and Tools":
            md_content.append('| **Name** | **Description** |')
            md_content.append('|----------|-----------------|')
            for resource in category['resources']:
                name = resource['name']
                description = resource.get('description', 'No description available')
                url = resource['url']
                md_content.append(f'| **[`{name}`]({url})** | {description} |')
            md_content.append('')
        else:
            # Handle regular sections (non-table format)
            if 'resources' in category:
                for resource in category['resources']:
                    md_content.extend(process_resource(resource))
            
            if 'subcategories' in category:
                for subcategory in category['subcategories']:
                    sub_name = subcategory['name']
                    md_content.append(f"\n### {sub_name}")
                    md_content.append('')
                    
                    if 'description' in subcategory:
                        md_content.append(subcategory['description'])
                        md_content.append('')
                    
                    if 'resources' in subcategory:
                        for resource in subcategory['resources']:
                            md_content.extend(process_resource(resource))
        
        # Add back to top link ONLY after main category sections
        md_content.append('')
        md_content.append('| ▲ [Top](#awesome-geophysics) |')
        md_content.append('| --- |')
        md_content.append('---')
        md_content.append('')
    
    # Add contributors section
    md_content.append('## Contributors')
    md_content.append('')
    md_content.append('Thanks to our many contributors!')
    md_content.append('')
    md_content.append('[![Contributors](https://contrib.rocks/image?repo=aradfarahani/awesome-geophysics&t=1742885103)](https://github.com/aradfarahani/awesome-geophysics/graphs/contributors)')
    md_content.append('')
    md_content.append('| ▲ [Top](#awesome-geophysics) |')
    md_content.append('| --- |')
    md_content.append('')
    md_content.append('---')
    md_content.append('')

    # Add How to Contribute section
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
    md_content.append('> **For more detailed guidelines, please check the [CONTRIBUTING.md](https://github.com/aradfarahani/awesome-geophysics/blob/master/CONTRIBUTING.md) file.**')
    md_content.append('')
    md_content.append('')
    md_content.append('| ▲ [Top](#awesome-geophysics) |')
    md_content.append('| --- |')
    md_content.append('')
    md_content.append('---')
    md_content.append('')

    # Add License section
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

    # Add closing paragraph
    md_content.append('*Whether you\'re diving into seismic data processing, modeling Earth\'s subsurface, or simply looking for inspiration, we invite you to explore, share, and contribute. Let\'s push the boundaries of geophysical exploration and understanding—together!*')
    md_content.append('')

    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_content))

if __name__ == '__main__':
    input_json = 'awesome_geophysics.json'
    output_md = 'README.md'
    generate_markdown_from_json(input_json, output_md)
    print(f"Markdown file generated: {output_md}")