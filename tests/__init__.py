#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from unittest import TestCase

import minwebhelpers
from minwebhelpers import javascript_link, stylesheet_link, beaker_kwargs

from fixtures import config, beaker_cache, fixture_path
minwebhelpers.config = config
minwebhelpers.beaker_cache = beaker_cache


class MinificationTestCase(TestCase):

    def purge_files(self, *files):
        for file_ in files:
            path = os.path.join(fixture_path, file_)
            os.remove(path)

    def test_paths(self):
        """Testing if paths are constructed correctly"""
        # minify and combine
        js_source = javascript_link('/deep/a.js', '/b.js', combined=True, minified=True)
        css_source = stylesheet_link('/deep/a.css', '/b.css', combined=True, minified=True)
        self.assert_('"/a.b.COMBINED.min.css"' in css_source)
        self.assert_('"/a.b.COMBINED.min.js"' in js_source)
        
        # combine
        js_source = javascript_link('/deep/a.js', '/b.js', combined=True)
        css_source = stylesheet_link('/deep/a.css', '/b.css', combined=True)
        self.assert_('"/a.b.COMBINED.css"' in css_source)
        self.assert_('"/a.b.COMBINED.js"' in js_source)

        # minify
        js_source = javascript_link('/deep/a.js', '/b.js', minified=True)
        css_source = stylesheet_link('/deep/a.css', '/b.css', minified=True)
        self.assert_('"/deep/a.min.css"' in css_source)
        self.assert_('"/b.min.css"' in css_source)
        self.assert_('"/deep/a.min.js"' in js_source)
        self.assert_('"/b.min.js"' in js_source)

        # root minify and combined
        js_source = javascript_link('/c.js', '/b.js', combined=True, minified=True)
        css_source = stylesheet_link('/c.css', '/b.css', combined=True, minified=True)
        self.assert_('"/c.b.COMBINED.min.css"' in css_source)
        self.assert_('"/c.b.COMBINED.min.js"' in js_source)

        # root minify
        js_source = javascript_link('/c.js', '/b.js', minified=True)
        css_source = stylesheet_link('/c.css', '/b.css', minified=True)
        self.assert_('"/b.min.css"' in css_source)
        self.assert_('"/b.min.js"' in js_source)
        self.assert_('"/c.min.js"' in js_source)
        self.assert_('"/c.min.js"' in js_source)

        # both root minify and combined
        js_source = javascript_link('/deep/a.js', '/deep/d.js', combined=True, minified=True)
        css_source = stylesheet_link('/deep/a.css', '/deep/d.css', combined=True, minified=True)
        self.assert_('"/deep/a.d.COMBINED.min.css"' in css_source)
        self.assert_('"/deep/a.d.COMBINED.min.js"' in js_source)

        # Cleanup
        self.purge_files('a.b.COMBINED.min.js', 'a.b.COMBINED.min.css')
        self.purge_files('a.b.COMBINED.js', 'a.b.COMBINED.css')
        self.purge_files('deep/a.min.css', 'deep/a.min.js', 'b.min.js', 'b.min.css')
        self.purge_files('c.b.COMBINED.min.js', 'c.b.COMBINED.min.css')
        #self.purge_files('b.min.js', 'b.min.css', 'c.min.js', 'c.min.css')
        self.purge_files('deep/a.d.COMBINED.min.js', 'deep/a.d.COMBINED.min.css')

    def test_beaker_kwargs(self):
        """Testing for proper beaker kwargs usage"""
        css_source = stylesheet_link('/deep/a.css', '/b.css', combined=True, minified=True)
        from fixtures import beaker_container
        self.assertEqual(beaker_container, beaker_kwargs)

        css_source = stylesheet_link('/deep/a.css', '/b.css', combined=True, minified=True, beaker_kwargs={'foo': 'bar'})
        from fixtures import beaker_container
        beaker_kwargs.update({'foo': 'bar'})
        self.assertEqual(beaker_container, beaker_kwargs)
