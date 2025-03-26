# Contributing to Awesome Geophysics

Thank you for your interest in contributing to **Awesome Geophysics**! This is a community-curated collection of geophysical resources, including software, datasets, educational materials, and more. We welcome contributions from geophysicists, students, developers, and enthusiasts to keep this resource comprehensive and up-to-date.

By contributing, you help build a valuable toolkit for the geophysics community under the [CC0 license](https://creativecommons.org/publicdomain/zero/1.0/), meaning all contributions are freely available to the public.

## How to Contribute

Follow these steps to contribute:

### 1. Fork and Clone the Repository
- Fork the repository on GitHub: [aradfarahani/awesome-geophysics](https://github.com/aradfarahani/awesome-geophysics).
- Clone your fork to your local machine:
  ```bash
  git clone https://github.com/YOUR_USERNAME/awesome-geophysics.git
  cd awesome-geophysics
  ```

### 2. Make Your Changes
- Open the `awesome_geophysics.json` file in a text editor or IDE.
- Add your resource(s) to the appropriate category (e.g., "Software and Tools," "Datasets and Databases," "Textbooks").
- Follow the existing JSON structure (see [Formatting Guidelines](#formatting-guidelines) below).
- Ensure your addition is relevant to geophysics and provides value to the community.

  **⚠️ Alert: Do not update the `README.md` file yet.** The primary data lives in `awesome_geophysics.json`, and we’re still working on syncing updates between the JSON and README. For now, focus on editing the JSON file only.

- **Can’t work with JSON?** If you’re not comfortable editing JSON directly, please try your best to follow the format. If that’s not possible, open an [issue](https://github.com/aradfarahani/awesome-geophysics/issues) with your suggested update (e.g., resource name, description, and URL), and we’ll help integrate it.

### 3. Test Your Changes
- Validate your JSON syntax using a tool like [JSONLint](https://jsonlint.com/) to ensure it’s error-free.
- If possible, test any URLs you add to confirm they’re active and lead to the intended resource.

### 4. Commit and Push
- Commit your changes with a clear message:
  ```bash
  git add awesome_geophysics.json
  git commit -m "Add [resource name] to [category name]"
  git push origin main
  ```
- Replace `[resource name]` and `[category name]` with specifics (e.g., "Add ObsPy to Software and Tools").

### 5. Submit a Pull Request
- Go to your fork on GitHub and click "New Pull Request."
- Compare your branch to the `main` branch of the original repository.
- Provide a brief description of your contribution in the PR (e.g., why this resource is useful).
- Submit the pull request for review.

## Contribution Guidelines

### What to Contribute
We’re looking for high-quality resources in these areas:
- **Software and Tools**: Open-source or widely-used geophysical software (e.g., seismic processing, inversion tools).
- **Datasets and Databases**: Publicly accessible geophysical data (e.g., seismic, gravity, magnetic).
- **Educational Resources**: Textbooks, online courses, tutorials, or workshops.
- **Research Papers and Journals**: Key publications or preprint servers.
- **Organizations and Events**: Societies, conferences, or professional networks.
- **Miscellaneous**: Visualization tools, blogs, podcasts, or career resources.

### Formatting Guidelines
To maintain consistency, please adhere to the JSON structure:
- Each resource should have:
  - `name`: The name of the resource.
  - `description`: A concise, informative summary (1-2 sentences).
  - `url`: A direct link to the resource (if applicable).
- Example:
  ```json
  {
    "name": "ObsPy",
    "description": "A comprehensive Python library for seismology, perfect for waveform analysis, data handling, and visualization.",
    "url": "https://github.com/obspy/obspy"
  }
  ```
- Add your resource under the appropriate `categories` or `subcategories` section.
- Use proper indentation (2 spaces) to match the existing file.

### Quality Standards
- Ensure resources are relevant to geophysics.
- Provide accurate, working URLs.
- Avoid self-promotion unless the resource is widely recognized and beneficial to the community.
- If adding proprietary software or paid resources, note any licensing or cost details in the description.

## Code of Conduct
- Be respectful and inclusive in all interactions.
- Provide constructive feedback during reviews.
- Avoid duplicate entries—check if a resource already exists before adding it.

## Questions?
If you’re unsure about anything:
- Open an [issue](https://github.com/aradfarahani/awesome-geophysics/issues) to discuss your idea or suggest a resource if you can’t edit JSON.
- Reach out to the maintainers listed in the [contributors](https://github.com/aradfarahani/awesome-geophysics/graphs/contributors) section.

## Attribution
All contributions are credited via GitHub’s contributor graph. By submitting, you agree to release your work under the CC0 license, making it freely available to all.

Thank you for helping make **Awesome Geophysics** even more awesome!
