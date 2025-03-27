import json
import sys
from collections import defaultdict
import requests

"""
This script validates the structure of the AwesomeGeophysics JSON file.
It checks for the following:
1. Each resource must have 'name', 'url', and 'description' fields.
2. No duplicate names (case-insensitive) across all resources.
3. No duplicate URLs across all resources.
4. Each URL must be accessible (HTTP status code < 400).
"""

def traverse(node, path, resources):
    """Recursively collect all resources from categories and subcategories."""
    if 'resources' in node:
        for resource in node['resources']:
            resources.append((resource, path.copy()))
    for key in ['categories', 'subcategories']:
        if key in node:
            for child in node[key]:
                child_name = child.get('name', 'Unnamed Category')
                traverse(child, path + [child_name], resources)

def main():
    try:
        with open('awesome_geophysics.json') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        sys.exit(1)

    awesome_geophysics = data.get('AwesomeGeophysics', {})
    resources = []
    traverse(awesome_geophysics, [], resources)

    # Check for required fields
    names = defaultdict(list)
    urls = defaultdict(list)
    for resource, path in resources:
        name = resource.get('name')
        url = resource.get('url', '').strip()
        description = resource.get('description', '').strip()
        
        if not name:
            print(f"Resource missing 'name' in category: {' -> '.join(path)}")
            sys.exit(1)
        if not url:
            print(f"Resource '{name}' missing URL in category: {' -> '.join(path)}")
            sys.exit(1)
        if not description:
            print(f"Resource '{name}' missing description in category: {' -> '.join(path)}")
            sys.exit(1)
            
        names[name.lower()].append((name, path))
        urls[url].append((name, path))

    has_errors = False

    # Check duplicate names (case-insensitive)
    for _, entries in names.items():
        if len(entries) > 1:
            print(f"Duplicate name found: {entries[0][0]}")
            for entry in entries:
                print(f"  - Location: {' -> '.join(entry[1])}")
            has_errors = True

    # Check duplicate URLs
    for url, entries in urls.items():
        if len(entries) > 1:
            print(f"Duplicate URL found: {url}")
            for entry in entries:
                print(f"  - Resource '{entry[0]}' in {' -> '.join(entry[1])}")
            has_errors = True

    # Validate URLs
    for resource, path in resources:
        url = resource.get('url', '').strip()
        try:
            response = requests.head(url, allow_redirects=True, timeout=10)
            if response.status_code >= 400:
                print(f"URL returned status {response.status_code}: {url}")
                print(f"  - Resource '{resource['name']}' in {' -> '.join(path)}")
                has_errors = True
        except requests.exceptions.RequestException as e:
            print(f"Error accessing URL: {url}")
            print(f"  - Resource '{resource['name']}' in {' -> '.join(path)}")
            print(f"  - Error: {e}")
            has_errors = True

    if has_errors:
        sys.exit(1)
    else:
        print("All checks passed successfully!")

if __name__ == "__main__":
    main()