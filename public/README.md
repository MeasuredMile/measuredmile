# The Measured Mile - Static Site Generator

A simple, efficient static site generator built in Python for "The Measured Mile" website - a resource for digital wellbeing and intentional technology use.

## Quick Start

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/themeasuredmile.git
   cd themeasuredmile
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Build the site:
   ```bash
   python build.py
   ```

4. View the site locally:
   ```bash
   # Using Python's built-in server
   cd output
   python -m http.server 8000
   ```

5. Deploy to GitHub Pages:
   ```bash
   # Make your content changes, then
   ./deploy.sh
   ```

## Adding Content

### Creating a New Post

1. Create a new Markdown file in the appropriate category directory:
   ```
   content/digital-detox/my-new-post.md
   ```

2. Add YAML front matter at the top of your file:
   ```yaml
   ---
   title: My New Post Title
   date: 2025-04-18
   excerpt: A brief summary of your post.
   featured_image: /static/images/my-image.jpg
   featured_image_alt: Description of the image
   tags: [tag1, tag2]
   ---
   ```

3. Write your content in Markdown format below the front matter.

4. Build and deploy the site.

### Adding Images

1. Place your images in the `static/images/` directory.
2. Reference them in your content using the path `/static/images/your-image.jpg`.

### Creating a New Category

1. Create a new directory in the `content/` folder:
   ```
   mkdir content/new-category
   ```

2. Create an `index.md` file within this directory with appropriate front matter.

3. Add the category to the `CATEGORIES` list in `config.py`.

4. Add category metadata to `CATEGORY_META` in `config.py`.

## Site Structure

```
themeasuredmile/
├── content/                  # All your content as Markdown files
│   ├── digital-detox/        # Main categories matching your site structure
│   │   ├── index.md          # Category pillar page
│   │   ├── how-to-delete-facebook.md
│   │   └── ...
├── static/                   # Static assets
│   ├── css/
│   ├── js/
│   ├── images/
│   └── fonts/
├── templates/                # HTML templates
│   ├── base.html             # Base template all others extend
│   ├── home.html             # Homepage template
│   └── ...
├── output/                   # Generated site (git-ignored)
├── build.py                  # Main build script
├── deploy.sh                 # Deployment script
├── config.py                 # Site configuration
└── requirements.txt          # Python dependencies
```

## Advanced Configuration

Edit `config.py` to modify site settings:

- Site metadata (title, description, etc.)
- Navigation menus
- Categories and their metadata 
- Analytics settings
- Newsletter integration

## Features

- Markdown content with YAML front matter
- Responsive, minimalist design with CSS
- Category-based content organization
- RSS feed generation
- Sitemap generation
- Privacy-focused analytics options
- Newsletter subscription form
- Automated deployment via GitHub Actions

## License

[MIT License](LICENSE)