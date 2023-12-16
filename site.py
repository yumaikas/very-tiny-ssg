# Outside of builtins, only depends on marko
# Which can be installed with `pip install marko` in a venv

import os
import re
import marko
from os.path import expanduser
from datetime import datetime
from random import random

def list_path(path):
    return [p for p in os.listdir(expanduser(path)) if not p.startswith(".")]

def html_header(f, metadata, site_title):
    def echo(s):
        print(s, file=f)
    title = metadata['title']
    echo("<!DOCTYPE html>")
    echo(f"""
    <head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <link rel="stylesheet" href="/site.css"/>
    <title>{title}</title>
    """)
    echo("""<style>
    body{
        display: grid;
        justify-content: center;
    }
    body,input,textarea{
        font-family: Iosevka,monospace;
        background-color: #191e2a;
        color: #21ef9f
    }
    td{margin:5px}
    a{color:#0ff}
    a:visited{color:#008b8b}
    </style>
    </head>
     """)
    echo(f'<h1><a href="/">{site_title}</a></h1>')

def article_body(f, body, metadata):
    def echo(s):
        print(s, file=f)
    echo("<body>")
    echo(f"<h2>{metadata.get('title')}</h2>")
    echo(marko.convert(body))
    echo("</body>")

def html_footer(f):
    def echo(s):
        print(s, file=f)
    echo("</header>")

class ObsidianArticle:
    def __init__(self, path):
        self.title = os.path.basename(path)
        if self.title.endswith(".md"):
            self.title = self.title[0:-3]
        self.path = path
        self.content = None

    def __str__(self):
        return "ObsidianArticle: " + self.title

    def load(self):
        content = None
        with open(self.path, "r") as f:
            content = f.read()
        print(content)
        if re.search(r"\+{6,}", content):
            sections = re.split(r"\+{6,}", content, maxsplit=1)
            frontmatter = sections[0]
            self.content = sections[1]
            metadata = { }
            # Running with scissors: #
            # Using exec would not normally be how you'd do this
            # and relies on the assumption that articles are not being crafted by
            # malicious entity.
            # It _is_ quick to code, tho
            exec(frontmatter, { 'dt': datetime }, metadata) 
            for field in ['slug', 'date']:
                if not metadata.get(field):
                    raise Exception(f'No {field} for Article "{self.title}"') 
            self.metadata = metadata
            self.metadata['title'] = self.title
        else:
            raise Exception("No Front Matter for article \""+self.title+"\"")

    def render(self, to, site_title):
        to_path = os.path.expanduser(os.path.join(to, self.metadata['slug'] + ".html"))
        with open(to_path, "w") as f:
            html_header(f, self.metadata, site_title)
            article_body(f, self.content, self.metadata)
            html_footer(f)
    
class ArticleSeries:

    def __init__(self, title):
        self.articles = []
        self.title = title

    def load_articles(self, from_dir):
        for p in list_path(from_dir):
            art = ObsidianArticle(expanduser(os.path.join(from_dir, p)))
            art.load()
            self.articles.append(art)
        self.articles.sort(key=lambda art: art.metadata['date'])


    def render_to(self, article_path):
        for a in self.articles:
            a.render(article_path, self.title)

    def index_at(self, target_path):
        with open(target_path, "w") as f:
            def echo(s):
                print(s, file=f)
            html_header(f, {"title": ""}, self.title)
            for a in self.articles:
                echo(f'<h2><a href="/posts/{a.metadata["slug"]}.html">{a.title}</a></h2>')
            html_footer(f)

def example_blog():
    # Before doing this, make sure to create publish and publish/posts directories
    main_articles = ArticleSeries("Test Blog")
    main_articles.load_articles("~/JD/30-39.Writing/30.03.Obsidian/Testing")
    main_articles.render_to("./publish/posts")
    main_articles.index_at("./publish/index.html")

# example_blog()

