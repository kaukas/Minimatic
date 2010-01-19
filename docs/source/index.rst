.. MinificationWebHelpers documentation master file, created by
   sphinx-quickstart on Thu Apr 16 00:02:24 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

:mod:`minwebhelpers` -- Welcome to MinificationWebHelpers's documentation!
==========================================================================

.. module:: minwebhelpers
	 :synopsis: Extension to WebHelpers

.. moduleauthor:: Pedro Algarvio

:Author: Pedro Algarvio <ufs_REMOVE@ME_ufsoft.org>
:Maintainer: Domen Kozar <domen_REMOVE@ME_dev.si>
:Version: |release|
:Source: bitbucket.org_
:Bug tracker: `bitbucket.org/issues <http://bitbucket.org/iElectric/minificationwebhelpers/issues/>`_

Consider the MinificationWebHelpers_ as an extension to WebHelpers_.

Basicly it adds these options to the WebHelpers_ javascript_link_
and stylesheet_link_ functions:

* **minified** (bool): Minifies, ie, reduces as much as possible each of the files
  passed to it's minimum size to reduce page load times.
* **combined** (bool): Joins all files passed into a single one to reduce server
  requests which in turn reduces page load times.
* **beaker_kwargs** (dict): override default arguments that will be passed to `beaker_cache`.  `beaker_kwargs.update()` is issued on default arguments.
* **combined_filename** (string): Name of the filename that will be used in conjunction with combined=True

.. code-block:: python

	# default args
	beaker_kwargs = dict(key='sources', expire='never', type='memory')

For an up-to-date read of the documentation, please `read the documentation
page on site`__.


.. note::
	 
	 Running Pylons/TG application in debug mode will force minfied and combined options off.



Terminology
-----------

MinificationWebHelpers_ cache your javascript and css files through Beaker_'s
``@beaker.cache`` decorator.

Javascript minification is achieved through Python port of jsmin_.

Usage
-----

On your own Pylons_ application, inside ``<app>/lib/helpers.py`` you add:

.. sourcecode:: python

  from minwebhelpers import *


Then, inside a template you could have:

.. sourcecode:: html+mako

  <head>
    ${ h.javascript_link('/js/file1.js',
                         '/js/file2.js',
                         minified=True,
                         combined=True,
												 combined_filename='all_javascript_files') }
    ${ h.stylesheet_link('/css/style1.css',
                         '/css/style2.css',
                         minified=True,
                         combined=True,
                         beaker_kwargs=dict(invalidate_on_startup=False)) }
  </head>

The above would mean ``file1.js`` and ``file2.js`` would be combined and then
minimized (same story for css files).

Instalation
-----------

It's as easy as::

  sudo easy_install MinificationWebHelpers


Or if you wish to install current trunk::

  sudo easy_install http://bitbucket.org/iElectric/minificationwebhelpers/get/tip.zip


.. _MinificationWebHelpers: http://docs.fubar.si/minwebhelpers/
.. _WebHelpers: http://pylonshq.com/docs/en/0.9.7/thirdparty/webhelpers/
.. _javascript_link: http://pylonshq.com/docs/en/0.9.7/thirdparty/webhelpers/html/html/#webhelpers.html.tags.javascript_link
.. _stylesheet_link: http://pylonshq.com/docs/en/0.9.7/thirdparty/webhelpers/html/html/#webhelpers.html.tags.stylesheet_link
.. _Pylons: http://pylonshq.com
.. _Beaker: http://pylonshq.com/docs/en/0.9.7/thirdparty/beaker
.. _bitbucket.org: http://bitbucket.org/iElectric/minificationwebhelpers/
.. _jsmin: http://www.crockford.com/javascript/jsmin.html
.. __: http://docs.fubar.si/minwebhelpers/


API
---

.. autofunction:: minwebhelpers.javascript_link

.. autofunction:: minwebhelpers.stylesheet_link

.. autofunction:: minwebhelpers.base_link

.. autofunction:: minwebhelpers.minify_sources

.. autofunction:: minwebhelpers.combine_sources


Changelog
---------

.. toctree::
   :maxdepth: 2

   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

