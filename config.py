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
    "attention-focus",
    "mindful-technology-use",
    "privacy-digital-independence",
    "healthy-digital-culture",
    "analog-offline-life",
    "ai-emerging-technologies",
    "preservation-legacy",
    "personal-reflections-experiments"
]

# Featured content for the homepage
FEATURED_POSTS = [
    "healthy-digital-culture/the-false-promise-of-convergence",
]

# Category metadata (for display on the site)
CATEGORY_META = {
    "attention-focus": {
        "title": "Attention & Focus",
        "description": "Reclaim your mental bandwidth in a world of constant pings.",
        "icon": "fas fa-brain"
    },
    "mindful-technology-use": {
        "title": "Mindful Technology Use",
        "description": "Use tech on your terms: find sustainable, low-stress ways to live with your devices.",
        "icon": "fas fa-mobile-alt"
    },
    "privacy-digital-independence": {
        "title": "Privacy & Digital Independence",
        "description": "Take control of your data with practical privacy guides and open-source alternatives.",
        "icon": "fas fa-shield-alt"
    },
    "healthy-digital-culture": {
        "title": "Healthy Digital Culture",
        "description": "Build real connections and ethical digital habits for social media, gaming, and communication.",
        "icon": "fas fa-users"
    },
    "analog-offline-life": {
        "title": "Analog & Offline Life",
        "description": "Rediscover presence and creativity with physical media, handwriting, and screen-free hobbies.",
        "icon": "fas fa-book-open"
    },
    "ai-emerging-technologies": {
        "title": "AI & Emerging Technologies",
        "description": "Harness AI and emerging tech intentionally to offload busywork and enhance your life.",
        "icon": "fas fa-robot"
    },
    "preservation-legacy": {
        "title": "Preservation & Legacy",
        "description": "Preserve your digital memories and plan your digital estate with archiving and legacy tips.",
        "icon": "fas fa-archive"
    },
    "personal-reflections-experiments": {
        "title": "Personal Reflections & Experiments",
        "description": "Join personal challenges, monthly experiments, and reflections on digital wellbeing journeys.",
        "icon": "fas fa-lightbulb"
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