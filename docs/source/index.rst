.. MinificationWebHelpers documentation master file, created by
   sphinx-quickstart on Thu Apr 16 00:02:24 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

:mod:`minwebhelpers` -- Welcome to MinificationWebHelpers's documentation!
==========================================================================

.. module:: repoze.who.plugins.formcookie
.. moduleauthor:: Pedro Algarvio

:Author: Pedro Algarvio <ufs_REMOVE@ME_ufsoft.org>
:Maintainer: Domen Kozar <domen_REMOVE@ME_dev.si>
:Version: |release|
:Source: bitbucket.org_
:Bug tracker: `bitbucket.org/issues <http://bitbucket.org/iElectric/minificationwebhelpers/issues/>`_

Consider the MinificationWebHelpers_ as an extension to WebHelpers_.

Basicly it adds two more options to the WebHelpers_ javascript_link_
and stylesheet_link_ functions:

* **minified**: Minifies, ie, reduces as much as possible each of the files
  passed to it's minimum size to reduce page load times.
* **combined**: Joins all files passed into a single one to reduce server
  requests which in turn reduces page load times.

For an up-to-date read of the documentation, please `read the documentation
page on site`__.

Terminology
-----------

MinificationWebHelpers_ cache your javascript and css files through Beaker_'s
``@beaker.cache`` decorator.

Memory cache is used together with `expire=None` and `invalidate_on_startup=True`.

Javascript minification is achieved through python port of jsmin_.

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
                         combined=True ) }
    ${ h.stylesheet_link('/css/style1.css',
                         '/css/style2.css',
                         minified=True,
                         combined=True ) }
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

Changelog
=========

.. toctree::
	 :maxdepth: 2

	 changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

