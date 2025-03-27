import json
import sys
import requests
from collections import defaultdict

def get_resources(json_data):
    """Extract all resources from JSON data with their paths"""
    resources = []
    
    def traverse(node, path):
        if 'resources' in node:
            for resource in node['resources']:
                resources.append({
                    "key": (resource['name'].lower(), resource['url']),
                    "resource": resource,
                    "path": path.copy()
                })
        for key in ['categories', 'subcategories']:
            if key in node:
                for child in node[key]:
                    traverse(child, path + [child.get('name', 'Unnamed Category')])
    
    traverse(json_data.get('AwesomeGeophysics', {}), [])
    return resources

def main(old_file, new_file):
    # Load both versions
    try:
        with open(old_file) as f:
            old_data = json.load(f)
        with open(new_file) as f:
            new_data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON files: {e}")
        sys.exit(1)

    # Get resources from both versions
    old_resources = {r['key']: r for r in get_resources(old_data)}
    new_resources = get_resources(new_data)

    # Identify new entries
    added_resources = [
        r for r in new_resources 
        if r['key'] not in old_resources
    ]

    # Combined resources for duplicate checking
    all_resources = list(old_resources.values()) + new_resources
    name_lookup = defaultdict(list)
    url_lookup = defaultdict(list)
    
    for r in all_resources:
        name_lookup[r['resource']['name'].lower()].append(r)
        url_lookup[r['resource']['url']].append(r)

    has_errors = False

    # Validate new entries only
    for new_entry in added_resources:
        resource = new_entry['resource']
        path = new_entry['path']
        
        # Check name conflicts
        name_entries = name_lookup[resource['name'].lower()]
        if len(name_entries) > 1:
            print(f"Name conflict: {resource['name']}")
            print(f"  - New entry in: {' -> '.join(path)}")
            for entry in name_entries:
                if entry['key'] != new_entry['key']:
                    print(f"  - Conflicts with: {' -> '.join(entry['path'])}")
            has_errors = True

        # Check URL conflicts
        url_entries = url_lookup[resource['url']]
        if len(url_entries) > 1:
            print(f"URL conflict: {resource['url']}")
            print(f"  - New entry: {resource['name']} in {' -> '.join(path)}")
            for entry in url_entries:
                if entry['key'] != new_entry['key']:
                    print(f"  - Conflicts with: {entry['resource']['name']} in {' -> '.join(entry['path'])}")
            has_errors = True

        # Validate URL
        try:
            response = requests.head(resource['url'], timeout=10, allow_redirects=True)
            if response.status_code >= 400:
                print(f"Bad URL ({response.status_code}): {resource['url']}")
                print(f"  - New entry: {resource['name']} in {' -> '.join(path)}")
                has_errors = True
        except Exception as e:
            print(f"URL Error: {resource['url']}")
            print(f"  - New entry: {resource['name']} in {' -> '.join(path)}")
            print(f"  - Error: {str(e)}")
            has_errors = True

    if has_errors:
        sys.exit(1)
    else:
        print("All new entries validated successfully!")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python validate_new_entries.py <old_file> <new_file>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])