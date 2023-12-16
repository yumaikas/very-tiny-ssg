# Very Tiny SSG

This is meant to be the minimum viable SSG template in python that has a little personality.

It's currently built to assume that it's loading from folders that contain Obsidian Notes.


## Up and running

You'll need to install Python 3, this code has been tested against Python 3.11.6
You'll also need to install marko: `pip install marko`, ideally in a venv
Then, you can run python3 site.py after customizing `example_blog`, see below


## Customization

`example_blog` contains an example of what can be done to set up a very basic blog
The main thing to be changed would be the path given to `main_articles.load_articles`


