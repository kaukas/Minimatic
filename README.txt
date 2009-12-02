What is MinificationWebHelpers?
===============================

Consider the MinificationWebHelpers_ as an extension to WebHelpers_.

Basicly it adds two more options to the WebHelpers_ javascript_link_
and stylesheet_link_ functions:

* **minified** (bool): Minifies, ie, reduces as much as possible each of the files
  passed to it's minimum size to reduce page load times.
* **combined** (bool): Joins all files passed into a single one to reduce server
  requests which in turn reduces page load times.
* **beaker_kwargs** (dict): override default arguments that will be passed to `beaker_cache`.  `beaker_kwargs.update()` is issued on default arguments.
* **combined_filename** (string): Name of the filename that will be used in conjunction with combined=True
* **timestamp** append `time.time` timestamp to file, eg. test.js?t=123012343

For an up-to-date read of the documentation, please `read the documentation
page on site`__.

Mercurial repository is located at bitbucket.org_.

.. _MinificationWebHelpers: http://docs.fubar.si/minwebhelpers/
.. _WebHelpers: http://pylonshq.com/docs/en/0.9.7/thirdparty/webhelpers/
.. _javascript_link: http://pylonshq.com/docs/en/0.9.7/thirdparty/webhelpers/html/html/#webhelpers.html.tags.javascript_link
.. _stylesheet_link: http://pylonshq.com/docs/en/0.9.7/thirdparty/webhelpers/html/html/#webhelpers.html.tags.stylesheet_link
.. _bitbucket.org: http://bitbucket.org/iElectric/minificationwebhelpers/
.. __: http://docs.fubar.si/minwebhelpers/
