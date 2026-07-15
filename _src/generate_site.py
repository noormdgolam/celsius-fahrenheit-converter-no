import json
import os
import random
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SRC_DIR, ".."))
DATA_DIR = os.path.join(SRC_DIR, "_data")
TPL_DIR = os.path.join(SRC_DIR, "_templates")

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    print("Loading data...")
    site = load_json(os.path.join(DATA_DIR, "site.json"))
    articles = load_json(os.path.join(DATA_DIR, "articles.json"))

    env = Environment(loader=FileSystemLoader(TPL_DIR))
    
    print("Generating articles...")
    article_tpl = env.get_template('article.html')
    
    # Extract distinct categories from articles
    categories_dict = {}
    for a in articles:
        if 'category' in a and a['category']['slug'] not in categories_dict:
            categories_dict[a['category']['slug']] = a['category']
    categories = list(categories_dict.values())
    
    for i, article in enumerate(articles):
        related = [a for a in articles if a['slug'] != article['slug']]
        random.shuffle(related)
        related = related[:5]
        
        html = article_tpl.render(site=site, article=article, articles=articles, related=related, categories=categories)
        with open(os.path.join(ROOT_DIR, f"{article['slug']}.html"), 'w', encoding='utf-8') as f:
            f.write(html)
            
    print("Generating category pages...")
    category_tpl = env.get_template('category.html')
    for cat in categories:
        cat_articles = [a for a in articles if 'category' in a and a['category']['slug'] == cat['slug']]
        html = category_tpl.render(site=site, category=cat, articles=cat_articles, categories=categories)
        with open(os.path.join(ROOT_DIR, f"{cat['slug']}.html"), 'w', encoding='utf-8') as f:
            f.write(html)

    print("Generating index.html...")
    index_tpl = env.get_template('index.html')
    html = index_tpl.render(site=site, articles=articles, categories=categories)
    with open(os.path.join(ROOT_DIR, "index.html"), 'w', encoding='utf-8') as f:
        f.write(html)

    print("Generating search.html...")
    search_tpl = env.get_template('search.html')
    html = search_tpl.render(site=site, articles=articles, categories=categories)
    with open(os.path.join(ROOT_DIR, "search.html"), 'w', encoding='utf-8') as f:
        f.write(html)

    print("Generating search_index.json...")
    search_index = []
    for a in articles:
        search_index.append({
            "title": a["title"],
            "description": a["description"],
            "slug": a["slug"]
        })
    with open(os.path.join(ROOT_DIR, "search_index.json"), 'w', encoding='utf-8') as f:
        json.dump(search_index, f, indent=2)

    print("Generating legal pages...")
    legal_tpl = env.get_template('legal.html')
    
    legal_pages = [
        {
            "slug": "privacy-policy",
            "title": "Privacy Policy",
            "description": f"Privacy Policy for {site['name']}",
            "content": f"<h2>Introduction</h2><p>At {site['name']}, accessible from {site['url']}, one of our main priorities is the privacy of our visitors. This Privacy Policy document contains types of information that is collected and recorded by {site['name']} and how we use it.</p><h2>Google AdSense</h2><p>Third party vendors, including Google, use cookies to serve ads based on a user's prior visits to your website or other websites. Google's use of advertising cookies enables it and its partners to serve ads to your users based on their visit to your sites and/or other sites on the Internet. Users may opt out of personalized advertising by visiting Ads Settings.</p>"
        },
        {
            "slug": "terms",
            "title": "Terms of Service",
            "description": f"Terms of Service for {site['name']}",
            "content": f"<h2>Terms</h2><p>By accessing this Website, accessible from {site['url']}, you are agreeing to be bound by these Website Terms and Conditions of Use and agree that you are responsible for the agreement with any applicable local laws.</p><h2>Disclaimer</h2><p>All the materials on {site['name']}'s Website are provided 'as is'. {site['name']} makes no warranties, may it be expressed or implied, therefore negates all other warranties.</p>"
        },
        {
            "slug": "disclaimer",
            "title": "Disclaimer",
            "description": f"Disclaimer for {site['name']}",
            "content": f"<h2>General Disclaimer</h2><p>The information provided by {site['name']} is for general informational purposes only. All information on the Site is provided in good faith, however we make no representation or warranty of any kind, express or implied, regarding the accuracy, adequacy, validity, reliability, availability or completeness of any information on the Site.</p>"
        },
        {
            "slug": "contact",
            "title": "Contact Us",
            "description": f"Contact {site['name']}",
            "content": f"<h2>Get in Touch</h2><p>If you have any questions or suggestions about our Privacy Policy, do not hesitate to contact us.</p><p>Email: contact@{site['url'].replace('https://', '').replace('http://', '')}</p>"
        },
        {
            "slug": "about",
            "title": "About Us",
            "description": f"About {site['name']}",
            "content": f"<h2>Our Mission</h2><p>At {site['name']}, our mission is to provide lightning-fast, mathematically precise, and easy-to-use temperature conversion tools for students, scientists, and home cooks alike.</p><h2>Who We Are</h2><p>Operated by Metric Media LLC, we are a small team of educators and developers based in Austin, Texas. We believe that everyday utility tools should be free, accessible, and not buried behind paywalls or intrusive pop-ups.</p><h2>Our Location</h2><p>Metric Media LLC<br>1234 Tech Ridge Blvd<br>Austin, TX 78753<br>United States</p>"
        }
    ]
    
    for page in legal_pages:
        html = legal_tpl.render(site=site, title=page['title'], description=page['description'], slug=page['slug'], content=page['content'], categories=categories)
        with open(os.path.join(ROOT_DIR, f"{page['slug']}.html"), 'w', encoding='utf-8') as f:
            f.write(html)

    print("Generating sitemap.xml...")
    date_str = datetime.now().strftime("%Y-%m-%d")
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    # Add home and search and legal
    for page in ["", "search.html", "privacy-policy.html", "terms.html", "disclaimer.html", "contact.html", "about.html"]:
        sitemap += f"  <url>\n    <loc>{site['url']}/{page}</loc>\n    <lastmod>{date_str}</lastmod>\n  </url>\n"
    for cat in categories:
        sitemap += f"  <url>\n    <loc>{site['url']}/{cat['slug']}.html</loc>\n    <lastmod>{date_str}</lastmod>\n  </url>\n"
    for a in articles:
        sitemap += f"  <url>\n    <loc>{site['url']}/{a['slug']}.html</loc>\n    <lastmod>{date_str}</lastmod>\n  </url>\n"
    sitemap += "</urlset>"
    with open(os.path.join(ROOT_DIR, "sitemap.xml"), 'w', encoding='utf-8') as f:
        f.write(sitemap)

    print("Generating robots.txt...")
    robots = f"User-agent: *\nAllow: /\n\nSitemap: {site['url']}/sitemap.xml\n"
    with open(os.path.join(ROOT_DIR, "robots.txt"), 'w', encoding='utf-8') as f:
        f.write(robots)
        


    print("Generating rss.xml...")
    rss = '<?xml version="1.0" encoding="UTF-8" ?>\n<rss version="2.0">\n<channel>\n'
    rss += f"  <title>{site['name']}</title>\n"
    rss += f"  <link>{site['url']}</link>\n"
    rss += f"  <description>{site['description']}</description>\n"
    for a in articles:
        rss += f"  <item>\n    <title>{a['title']}</title>\n    <link>{site['url']}/{a['slug']}.html</link>\n    <description>{a['description']}</description>\n  </item>\n"
    rss += "</channel>\n</rss>"
    with open(os.path.join(ROOT_DIR, "rss.xml"), 'w', encoding='utf-8') as f:
        f.write(rss)

    print("Generating manifest.json...")
    manifest = {
        "name": site["name"],
        "short_name": "C to F",
        "description": site["description"],
        "start_url": "/",
        "display": "standalone",
        "background_color": "#f8fafc",
        "theme_color": "#1e1e2f",
        "icons": [
            {
                "src": "/icon-192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "/icon-512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    }
    with open(os.path.join(ROOT_DIR, "manifest.json"), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

    print("Generating sw.js...")
    sw_code = """
const CACHE_NAME = 'ctof-cache-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/search.html',
  '/search_index.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response; // Cache hit
        }
        return fetch(event.request).then(
          function(response) {
            // Check if we received a valid response
            if(!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }
            var responseToCache = response.clone();
            caches.open(CACHE_NAME)
              .then(function(cache) {
                cache.put(event.request, responseToCache);
              });
            return response;
          }
        );
      })
  );
});
"""
    with open(os.path.join(ROOT_DIR, "sw.js"), 'w', encoding='utf-8') as f:
        f.write(sw_code.strip())

    print("Site generation complete!")

if __name__ == "__main__":
    main()
