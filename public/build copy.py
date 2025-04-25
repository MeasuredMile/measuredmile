#!/usr/bin/env python3.11
"""
The Measured Mile - Static Site Generator
A simple static site generator for The Measured Mile website.
"""

import os
import sys
import shutil
import datetime
import re
import json
import glob
from pathlib import Path
import markdown
import yaml
import jinja2
from slugify import slugify

print("Script is starting...")
print("Python version:", sys.version)

# Configuration
import config

class MeasuredMileSite:
    def __init__(self):
        self.content_dir = Path("content")
        self.output_dir = Path("output")
        self.templates_dir = Path("templates")
        self.static_dir = Path("static")
        
        # Initialize Jinja2 environment
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.templates_dir),
            autoescape=jinja2.select_autoescape(['html', 'xml'])
        )
        
        # Site data
        self.pages = []
        self.posts = {}  # Organized by category
        self.categories = {}
        
        # Add custom Jinja2 filters
        self.jinja_env.filters['slugify'] = slugify
        self.jinja_env.filters['date_format'] = self.date_format
        self.jinja_env.filters['lstrip'] = lambda x, chars: x.lstrip(chars)
    
    def date_format(self, date, format="%B %d, %Y"):
        """Format a date for display"""
        if isinstance(date, str):
            try:
                date = datetime.datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                return date
        return date.strftime(format)
    
    def clean_output(self):
        """Clean the output directory"""
        print("Cleaning output directory...")
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def copy_static_files(self):
        """Copy static files to output directory"""
        print("Copying static files...")
        if self.static_dir.exists():
            shutil.copytree(
                self.static_dir, 
                self.output_dir / "static", 
                dirs_exist_ok=True
            )
    
    def parse_content_file(self, file_path):
        """Parse a content file with YAML front matter and Markdown content"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split the file into front matter and content
        if content.startswith('---'):
            _, front_matter, content = content.split('---', 2)
            metadata = yaml.safe_load(front_matter)
        else:
            metadata = {}
        
        # Convert Markdown to HTML
        html_content = markdown.markdown(
            content, 
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
                'markdown.extensions.meta',
                'markdown.extensions.smarty'
            ]
        )
        
        # Add default values for important metadata
        if 'title' not in metadata:
            metadata['title'] = "Untitled"
        
        if 'date' not in metadata:
            # Use file modification time if no date specified
            mtime = file_path.stat().st_mtime
            metadata['date'] = datetime.datetime.fromtimestamp(mtime)
        elif isinstance(metadata['date'], str):
            # Convert date string to datetime object
            metadata['date'] = datetime.datetime.strptime(metadata['date'], "%Y-%m-%d")
            
        if 'updated' not in metadata:
            metadata['updated'] = metadata['date']
        
        # Generate slug from filename if not specified
        if 'slug' not in metadata:
            metadata['slug'] = file_path.stem
        
        # Determine URL based on file location
        rel_path = file_path.relative_to(self.content_dir)
        if rel_path.stem == 'index':
            # For index.md files, URL is the directory
            url = '/' + '/'.join(rel_path.parts[:-1]) + '/'
        else:
            # For regular files, URL is the directory + filename
            url = '/' + '/'.join(rel_path.parts[:-1]) + '/' + metadata['slug'] + '/'
        
        # Clean up URLs
        url = url.replace('//', '/')
        if not url.startswith('/'):
            url = '/' + url
        if not url.endswith('/'):
            url = url + '/'
            
        metadata['url'] = url
        
        # Determine template
        if 'template' not in metadata:
            if rel_path.parts[0] in config.CATEGORIES and rel_path.stem == 'index':
                metadata['template'] = 'category.html'
            elif len(rel_path.parts) == 1 and rel_path.stem == 'index':
                metadata['template'] = 'home.html'
            elif len(rel_path.parts) == 1:
                metadata['template'] = 'page.html'
            else:
                metadata['template'] = 'post.html'
                
        # Determine category for posts
        if len(rel_path.parts) > 1 and rel_path.stem != 'index':
            metadata['category'] = rel_path.parts[0]
        
        return {
            'metadata': metadata,
            'content': html_content,
            'url': url,
            'file_path': file_path,
            'rel_path': rel_path
        }
    
    def load_content(self):
        """Load all content from the content directory"""
        print("Loading content...")
        
        # First, load all posts and category index pages
        for category in config.CATEGORIES:
            cat_dir = self.content_dir / category
            if not cat_dir.exists():
                continue
                
            self.posts[category] = []
            
            # Load category index
            cat_index = cat_dir / "index.md"
            if cat_index.exists():
                data = self.parse_content_file(cat_index)
                self.categories[category] = data
            
            # Load posts in this category
            for post_file in cat_dir.glob("*.md"):
                if post_file.stem == "index":
                    continue
                
                data = self.parse_content_file(post_file)
                self.posts[category].append(data)
        
        # Sort posts by date (newest first)
        for category in self.posts:
            self.posts[category].sort(key=lambda x: x['metadata']['date'], reverse=True)
        
        # Load standalone pages
        for page_file in self.content_dir.glob("*.md"):
            if page_file.stem == "index":
                # Home page is handled separately
                data = self.parse_content_file(page_file)
                self.home_page = data
            else:
                data = self.parse_content_file(page_file)
                self.pages.append(data)
    
    def generate_site(self):
        """Generate the site from content and templates"""
        print("Generating site...")
        
        # Create site data for templates
        site_data = {
            'title': config.SITE_TITLE,
            'subtitle': getattr(config, 'SITE_SUBTITLE', ''),
            'description': config.SITE_DESCRIPTION,
            'url': config.SITE_URL,
            'categories': config.CATEGORIES,
            'navigation': config.NAVIGATION,
            'current_year': datetime.datetime.now().year,
            'all_posts': {category: self.posts[category] for category in self.posts},
            'recent_posts': self.get_recent_posts(10),
            'build_time': datetime.datetime.now(),
            'featured_posts': getattr(config, 'FEATURED_POSTS', []),
            # Add these default values
            'analytics': getattr(config, 'ANALYTICS', {'enabled': False}),
            'newsletter': getattr(config, 'NEWSLETTER', {'enabled': False}),
            'features': getattr(config, 'FEATURES', {
                'enable_search': False,
                'enable_dark_mode': False,
                'enable_comments': False
            }),
            'category_meta': getattr(config, 'CATEGORY_META', {})
        }
        
        # Generate home page
        self.generate_page(self.home_page, site_data)
        
        # Generate standalone pages
        for page in self.pages:
            self.generate_page(page, site_data)
        
        # Generate category pages
        for category, data in self.categories.items():
            # Add posts to category data
            if category in self.posts:
                data['metadata']['posts'] = self.posts[category]
            self.generate_page(data, site_data)
        
        # Generate post pages
        for category in self.posts:
            for post in self.posts[category]:
                self.generate_page(post, site_data)
        
        # Generate sitemap.xml
        self.generate_sitemap()
        
        # Generate RSS feed
        self.generate_rss()
    
    def generate_page(self, page_data, site_data):
        """Generate a single page"""
        # Ensure output directory exists
        output_path = self.output_dir / page_data['url'].lstrip('/')
        if not output_path.exists():
            output_path.mkdir(parents=True, exist_ok=True)
        
        # Create a copy of the page data
        page_metadata = dict(page_data['metadata'])
        
        # Ensure URL is set correctly
        if 'url' not in page_metadata:
            page_metadata['url'] = page_data['url']
        
        # Prepare template data
        template_data = {
            'site': site_data,
            'page': page_metadata,
            'content': page_data['content']
        }
        
        # Render template
        template = self.jinja_env.get_template(page_data['metadata']['template'])
        output_html = template.render(**template_data)
        
        # Write output file
        with open(output_path / "index.html", 'w', encoding='utf-8') as f:
            f.write(output_html)
            
        print(f"Generated: {page_data['url']}")
    
    def get_recent_posts(self, count=5):
        """Get the most recent posts across all categories"""
        all_posts = []
        for category in self.posts:
            all_posts.extend(self.posts[category])
        
        # Sort by date
        all_posts.sort(key=lambda x: x['metadata']['date'], reverse=True)
        
        return all_posts[:count]
    
    def generate_sitemap(self):
        """Generate sitemap.xml"""
        print("Generating sitemap.xml...")
        
        template = self.jinja_env.get_template('sitemap.xml')
        
        # Collect all URLs
        urls = []
        
        # Home page
        urls.append({
            'loc': config.SITE_URL + self.home_page['url'],
            'lastmod': datetime.datetime.now().strftime('%Y-%m-%d'),
            'priority': '1.0'
        })
        
        # Standalone pages
        for page in self.pages:
            urls.append({
                'loc': config.SITE_URL + page['url'],
                'lastmod': page['metadata'].get('updated', page['metadata']['date']).strftime('%Y-%m-%d'),
                'priority': '0.8'
            })
        
        # Category pages
        for category, data in self.categories.items():
            urls.append({
                'loc': config.SITE_URL + data['url'],
                'lastmod': data['metadata'].get('updated', data['metadata']['date']).strftime('%Y-%m-%d'),
                'priority': '0.8'
            })
        
        # Post pages
        for category in self.posts:
            for post in self.posts[category]:
                urls.append({
                    'loc': config.SITE_URL + post['url'],
                    'lastmod': post['metadata'].get('updated', post['metadata']['date']).strftime('%Y-%m-%d'),
                    'priority': '0.6'
                })
        
        # Render sitemap
        sitemap_xml = template.render(urls=urls)
        
        # Write sitemap
        with open(self.output_dir / "sitemap.xml", 'w', encoding='utf-8') as f:
            f.write(sitemap_xml)
    
    def generate_rss(self):
        """Generate RSS feed"""
        print("Generating RSS feed...")
        
        template = self.jinja_env.get_template('rss.xml')
        
        # Get recent posts for the feed
        feed_posts = self.get_recent_posts(20)
        
        # Render RSS feed
        rss_xml = template.render(
            site_title=config.SITE_TITLE,
            site_description=config.SITE_DESCRIPTION,
            site_url=config.SITE_URL,
            build_date=datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z'),
            posts=feed_posts
        )
        
        # Write RSS feed
        with open(self.output_dir / "feed.xml", 'w', encoding='utf-8') as f:
            f.write(rss_xml)
    
    def build(self):
        """Build the entire site"""
        start_time = datetime.datetime.now()
        print(f"Building site: {config.SITE_TITLE}")
        
        self.clean_output()
        self.copy_static_files()
        self.load_content()
        self.generate_site()
        
        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()
        print(f"Build completed in {duration:.2f} seconds")

if __name__ == "__main__":
    site = MeasuredMileSite()
    site.build()
    print("Build process completed.")