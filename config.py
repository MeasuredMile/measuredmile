#!/usr/bin/env python3.11
"""
Measured Mile - Site Configuration
Configuration settings for Measured Mile website.
"""

# Site information
SITE_TITLE = "Measured Mile"
SITE_SUBTITLE = "Technology on Your Terms"
SITE_DESCRIPTION = "My home for using tech sensibly"
SITE_URL = "https://measuredmile.com"
SITE_AUTHOR = "Michael"
SITE_EMAIL = "hello@measuredmile.com"

# Categories - these match your folder structure and URLs
CATEGORIES = [
    "reclaim-attention",
    "choose-better-tech",
    "find-balance",
    "protect-privacy",
    "offline-living"
]

# Featured content for the homepage
FEATURED_POSTS = [
    "reclaim-attention/how-to-delete-facebook",
    "choose-better-tech/best-ereaders-2025",
    "find-balance/managing-notification-anxiety"
]

# Category metadata (for display on the site)
CATEGORY_META = {
    "reclaim-attention": {
        "title": "Reclaim Your Attention",
        "description": "Practical strategies for breaking free from digital overwhelm and creating healthier relationships with your devices.",
        "icon": "fas fa-brain"
    },
    "choose-better-tech": {
        "title": "Choose Better Tech",
        "description": "Reviews and recommendations for technology that respects your attention and enhances your life without stealing your focus.",
        "icon": "fas fa-glasses"
    },
    "find-balance": {
        "title": "Find Digital Balance",
        "description": "Strategies for protecting your mental health, improving focus, and reducing anxiety in our always-connected world.",
        "icon": "fas fa-heart"
    },
    "protect-privacy": {
        "title": "Protect Your Privacy",
        "description": "Practical guides to understanding and protecting your data with straightforward steps anyone can follow.",
        "icon": "fas fa-user-shield"
    },
    "offline-living": {
        "title": "Rediscover Offline Living",
        "description": "Finding joy in analog activities, physical media, and creating a more deliberate relationship with technology.",
        "icon": "fas fa-seedling"
    }
}

# Navigation menu
NAVIGATION = [
    {"title": "Home", "url": "/"},
    {"title": "About", "url": "/about/"},
    {"title": "Start Here", "url": "/start-here/"},
    {"title": "Reclaim Your Attention", "url": "/reclaim-attention/"},
    {"title": "Choose Better Tech", "url": "/choose-better-tech/"},
    {"title": "Find Digital Balance", "url": "/find-balance/"},
    {"title": "Protect Your Privacy", "url": "/protect-privacy/"},
    {"title": "Rediscover Offline Living", "url": "/offline-living/"},
    {"title": "Newsletter", "url": "/newsletter/"},
    {"title": "Contact", "url": "/contact/"}
]

# Footer navigation
FOOTER_NAVIGATION = [
    {"title": "About", "url": "/about/"},
    {"title": "Contact", "url": "/contact/"},
    {"title": "Privacy Policy", "url": "/privacy-policy/"}
]

# Analytics configuration
ANALYTICS = {
    "enabled": False,
    "provider": "plausible",  # Options: "plausible", "goatcounter", "google"
    "site_id": "measuredmile.com"  # Your analytics site ID
}

# Newsletter configuration
# NEWSLETTER = {
#    "enabled": True,
#    "provider": "convertkit",  # Options: "convertkit", "buttondown", "mailchimp", "tinyletter"
#    "form_id": "YOUR_FORM_ID"  # Your newsletter provider's form ID
# }

# Newsletter configuration
NEWSLETTER = {
    "enabled": True,
    "provider": "buttondown",  # Changed from "convertkit" to "buttondown"
    "form_id": "measuredmile"  # Your Buttondown username
}

# Site features
FEATURES = {
    "enable_search": True,  # Enable site search
    "enable_dark_mode": True,  # Enable dark mode toggle
    "enable_comments": False,  # Enable comments (requires external service)
    "enable_pagination": True,  # Enable pagination for category pages
    "posts_per_page": 10,  # Number of posts per page in category listings
    "show_reading_time": True  # Calculate and show estimated reading time
}