Minimatic
=========

An extension to WebHelpers_ that enables a real time JS/CSS combination and
minification in production mode.

Installation
------------

Using easy_install::

    $ easy_install minimatic

Using pip::
    
    $ pip install minimatic

Source code
-----------

Mercurial repository is located at bitbucket.org_.

Usage
-----

It extends the WebHelpers_ functions javascript_link_ and stylesheet_link_ to
take a modified set of parameters:

* **sources** (list): JS/CSS items to process. Each item is one of the following:
    * (dict) with keys:
        * file: a path to the source file relative to the static file root
        * minify: minification method. Possible values (default *False*):
            * False (bool): use the source unmodified
            * strip (str): only strip extra whitespace and comments (applicable
              to CSS only)
            * minify (str): strip whitespace and apply other possible JS/CSS
              minifications. Note that this involves source parsing and will err
              on syntax errors (CSS hacks will be removed!). In effect the
              resulting file may be logically different
        * dest: if the source list is not combined then each item must provide a
          destination filename relative to the static file root
    * (str): it will be treated as (see above)::

        {'file': (str), 'minify': False}

* **combined** (str): the combined filename relative to the static file root.
  Implies that the files need to be combined. If **combined** is None then every
  Item must have a dest key provided.
* **beaker_kwargs** (dict): override default arguments that will be passed to
  `beaker_cache`. `beaker_kwargs.update()` is issued on default arguments.
* **timestamp** append `time.time` timestamp to links to force browsers reload
  the JS/CSS assets, eg. test.js?t=123012343

The files will be combined in production mode; in development mode
(*debug=True*) they will be served unmodified separately.

Example
-------

Mix and match the sources into one big JS file::

    >>> javascript_link(
    ...     # These files are already minified; combine them only
    ...     '/js/jquery.js',
    ...     '/js/jquery-ui-custom.js',
    ...     # These are custom files which need to be minified first
    ...     dict(file='/js/base.js', minify='minify'),
    ...     dict(file='/js/page-script.js', minify='minify'),
    ...     combined='/combined/js/scripts.js',
    ...     timestamp=True)

Serve CSS files separately (uncombined)::

    >>> stylesheet_link(
    ...     # This stylesheet is valid CSS and safe to parse and minify
    ...     dict(file='/css/base.css', minify='minify',
    ...         dest='/combined/css/base.css'),
    ...     # This stylesheet is full of CSS hacks and only the extra whitespace
    ...     # and comments should be stripped
    ...     dict(file='/css/styles.ie6.css', minify='strip',
    ...         dest='/combined/css/styles.ie6.css'),
    ...     timestamp=True)

.. _WebHelpers: http://pylonshq.com/docs/en/0.9.7/thirdparty/webhelpers/
.. _javascript_link: http://pylonshq.com/docs/en/0.9.7/thirdparty/webhelpers/html/html/#webhelpers.html.tags.javascript_link
.. _stylesheet_link: http://pylonshq.com/docs/en/0.9.7/thirdparty/webhelpers/html/html/#webhelpers.html.tags.stylesheet_link
.. _bitbucket.org: https://bitbucket.org/kaukas/minimatic/
