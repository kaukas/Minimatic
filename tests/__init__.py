#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tempfile import mkdtemp
from shutil import rmtree
from unittest import TestCase

import minwebhelpers
from minwebhelpers import javascript_link, stylesheet_link, beaker_kwargs

from fixtures import config, beaker_cache, fixture_path
minwebhelpers.config = config
minwebhelpers.beaker_cache = beaker_cache


class MinificationTestCase(TestCase):

    def setUp(self):
        self.fixture_path = mkdtemp()
        minwebhelpers.config['pylons.paths']['static_files'] = self.fixture_path

        self.touch_file('b.js')
        self.touch_file('b.css')
        self.touch_file('c.css')
        self.touch_file('c.js')
        os.mkdir(os.path.join(self.fixture_path, 'deep'))
        self.touch_file('deep/a.css')
        self.touch_file('deep/a.js')
        self.touch_file('deep/d.css')
        self.touch_file('deep/d.js')
        os.mkdir(os.path.join(self.fixture_path, 'js'))
        os.mkdir(os.path.join(self.fixture_path, 'jquery'))
        self.touch_file('js/1.css')
        self.touch_file('js/1.js')
        self.touch_file('jquery/2.css')
        self.touch_file('jquery/2.js')

    def tearDown(self):
        rmtree(self.fixture_path)

    def touch_file(self, path):
        open(os.path.join(self.fixture_path, path), 'w').close()

    def write_file(self, path, contents):
        f = open(os.path.join(self.fixture_path, path), 'w')
        f.write(contents)
        f.close()

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

    def test_two_deep_paths(self):
        js_source = javascript_link('/js/1.js', '/jquery/2.js', combined=True, minified=True)
        css_source = stylesheet_link('/js/1.css', '/jquery/2.css', combined=True, minified=True)
        self.assert_('"/1.2.COMBINED.min.css"' in css_source)
        self.assert_('"/1.2.COMBINED.min.js"' in js_source)
    
    def test_specified_filename(self):
        js_source = javascript_link('/js/1.js', '/jquery/2.js', combined=True, minified=True, combined_filename="w00t_1")
        css_source = stylesheet_link('/js/1.css', '/jquery/2.css', combined=True, minified=True, combined_filename="foobar")
        self.assert_('"/w00t_1.COMBINED.min.js"' in js_source)
        self.assert_('"/foobar.COMBINED.min.css"' in css_source)

    def test_beaker_kwargs(self):
        """Testing for proper beaker kwargs usage"""
        css_source = stylesheet_link('/deep/a.css', '/b.css', combined=True, minified=True)
        from fixtures import beaker_container
        self.assertEqual(beaker_container, beaker_kwargs)

        css_source = stylesheet_link('/deep/a.css', '/b.css', combined=True, minified=True, beaker_kwargs={'foo': 'bar'})
        from fixtures import beaker_container
        beaker_kwargs.update({'foo': 'bar'})
        self.assertEqual(beaker_container, beaker_kwargs)

    def test_css_leading_zero(self):
        self.write_file('js/1.css', """
        p{
            font-size:0.83em !important;
        }""")

        css_source = stylesheet_link('/js/1.css', minified=True)

        self.assertEqual(open(os.path.join(self.fixture_path, 'js/1.min.css')).read(), 'p{font-size:.83em !important}')

    def test_css_no_leading_zero(self):
        self.write_file('js/1.css', """
        p{
            font-size: 10.83em !important;
        }""")

        css_source = stylesheet_link('/js/1.css', minified=True)

        self.assertEqual(open(os.path.join(self.fixture_path, 'js/1.min.css')).read(), 'p{font-size:10.83em !important}')

    def test_zero_px(self):
        self.write_file('js/1.css', """
        p{
            border:0px 1pt 0px 0em;
            border:1px 0em 2em 0pt;
        }""")

        css_source = stylesheet_link('/js/1.css', minified=True)

        self.assertEqual(open(os.path.join(self.fixture_path, 'js/1.min.css')).read(),
            'p{border:0 1pt 0 0;border:1px 0 2em 0}')
