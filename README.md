# Jen

Static site generator and prototyping tool based on [Jinja2](http://jinja.pocoo.org/docs/2.9/).


## Install

Jen is available in the Python Package Index:

    pip install jen


## Overview

Create some Jinja templates in a directory, alongside the desired static content.
Example:

```
site/
    _base.html
    index.html
    about.html
    robots.txt
    css/
        theme.css
```

Run the development server while you create your content:

    jen run site

The content will be accessible in your browser on `localhost:8000`. Try some pretty urls:

    /
    /about
    /css/theme.css

A few points to notice:

* HTML templates are accessed without the `.html` extension.
* `/` maps to `index.html`. Any sub-directory with an `index.html` can also be accessed like this.
* `_base.html` is accessible in the Jinja environment but will not be exposed because it starts with underscore `_`.

After you're done, build your static site with:

    jen build site dist

The static content will be generated in the specified `dist` directory.

You can now serve the build with your favorite web server (if well configured). An easy one for testing (zero-configuration) is `http-server` from the `npm` package manager:

    npm install -g http-server
    http-server dist
