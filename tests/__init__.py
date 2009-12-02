#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from tempfile import mkdtemp
from shutil import rmtree
from unittest import TestCase

import minwebhelpers
from minwebhelpers import javascript_link, stylesheet_link, beaker_kwargs

from fixtures import config, beaker_cache, fixture_path, memoize
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
        js_source = javascript_link(
            dict(file='/deep/a.js', minify='minify'),
            '/b.js', combined='ab.combined.js')
        self.assert_('"/ab.combined.js"' in js_source)

        css_source = stylesheet_link(
            dict(file='/deep/a.css', minify='minify'),
            '/b.css', combined='ab.combined.css')
        self.assert_('"/ab.combined.css"' in css_source)
        
        # combine
        js_source = javascript_link('/deep/a.js', '/b.js', combined='ab.js')
        self.assert_('"/ab.js"' in js_source)

        css_source = stylesheet_link('/deep/a.css', '/b.css', combined='ab.css')
        self.assert_('"/ab.css"' in css_source)

        # minify
        js_source = javascript_link(
            dict(file='/deep/a.js', minify='minify', dest='/deep/a.m.js'),
            dict(file='/b.js', minify='minify', dest='/b.m.js'))
        self.assert_('"/deep/a.m.js"' in js_source)
        self.assert_('"/b.m.js"' in js_source)

        css_source = stylesheet_link(
            dict(file='/deep/a.css', minify='minify', dest='/deep/a.m.css'),
            dict(file='/b.css', minify='minify', dest='/b.m.css'))
        self.assert_('"/deep/a.m.css"' in css_source)
        self.assert_('"/b.m.css"' in css_source)

        # root minify and combined
        js_source = javascript_link(
            dict(file='/c.js', minify='minify'),
            dict(file='/b.js', minify='minify'),
            combined='cb.mc.js')
        self.assert_('"/cb.mc.js"' in js_source)

        css_source = stylesheet_link(
            dict(file='/c.css', minify='minify'),
            dict(file='/b.css', minify='minify'),
            combined='cb.mc.css')
        self.assert_('"/cb.mc.css"' in css_source)

        # root minify
        js_source = javascript_link(
            dict(file='/b.js', minify='minify', dest='b.min.js'),
            dict(file='/c.js', minify='minify', dest='c.min.js'))
        self.assert_('"/b.min.js"' in js_source)
        self.assert_('"/c.min.js"' in js_source)

        css_source = stylesheet_link(
            dict(file='/b.css', minify='minify', dest='b.min.css'),
            dict(file='/c.css', minify='minify', dest='c.min.css'))
        self.assert_('"/b.min.css"' in css_source)
        self.assert_('"/c.min.css"' in css_source)

        # both deep minify and combined
        js_source = javascript_link(
            dict(file='/deep/a.js', minify='minify'),
            dict(file='/deep/d.js', minify='minify'),
            combined='/deep/ad.js')
        self.assert_('"/deep/ad.js"' in js_source)

        css_source = stylesheet_link(
            dict(file='/deep/a.css', minify='minify'),
            dict(file='/deep/d.css', minify='minify'),
            combined='/deep/ad.css')
        self.assert_('"/deep/ad.css"' in css_source)

    def test_two_deep_paths(self):
        js_source = javascript_link(
            dict(file='/js/1.js', minify='minify'),
            dict(file='/jquery/2.js', minify='minify'),
            combined='/js/1.2.js')
        self.assert_('"/js/1.2.js"' in js_source)

        css_source = stylesheet_link(
            dict(file='/js/1.css', minify='minify'),
            dict(file='/jquery/2.css', minify='minify'),
            combined='/js/1.2.css')
        self.assert_('"/js/1.2.css"' in css_source)
    
    #def test_specified_filename(self):
    #    js_source = javascript_link('/js/1.js', '/jquery/2.js', combined=True, minified=True, combined_filename="w00t_1")
    #    css_source = stylesheet_link('/js/1.css', '/jquery/2.css', combined=True, minified=True, combined_filename="foobar")
    #    self.assert_('"/w00t_1.COMBINED.min.js"' in js_source)
    #    self.assert_('"/foobar.COMBINED.min.css"' in css_source)

    #    # When the filename begins with ./ treat it as an exact filename (don't
    #    # add anything else)
    #    js_source = javascript_link('/js/1.js', '/jquery/2.js', combined=True,
    #        minified=True, combined_filename="./js/combined.js")
    #    css_source = stylesheet_link('/js/1.css', '/jquery/2.css',
    #        combined=True, minified=True, combined_filename="./foobar.css")
    #    self.assert_('"/js/combined.min.js"' in js_source)
    #    self.assert_('"/foobar.min.css"' in css_source)

    def test_beaker_kwargs(self):
        """Testing for proper beaker kwargs usage"""
        css_source = stylesheet_link(
            dict(file='/deep/a.css', minify='minify'),
            dict(file='/b.css', minify='minify'),
            combined='ab.css')
        from fixtures import beaker_container
        self.assertEqual(beaker_container, beaker_kwargs)

        css_source = stylesheet_link(
            dict(file='/deep/a.css', minify='minify'),
            dict(file='/b.css', minify='minify'),
            combined='ab.css', beaker_kwargs={'foo': 'bar'})
        from fixtures import beaker_container
        beaker_kwargs.update({'foo': 'bar'})
        self.assertEqual(beaker_container, beaker_kwargs)

    def test_timestamp(self):
        """test that timestamp is really remembered"""
        # apply real memoize to do proper testing
        minwebhelpers.beaker_cache = memoize

        css_source_1 = stylesheet_link(
            dict(file='/deep/a.css', minify='minify'),
            dict(file='/b.css', minify='minify'),
            combined='ab.css',
            timestamp=True)
        time.sleep(1)
        css_source_2 = stylesheet_link(
            dict(file='/deep/a.css', minify='minify'),
            dict(file='/b.css', minify='minify'),
            combined='ab.css',
            timestamp=True)
        self.assertEqual(css_source_1, css_source_2)
        self.assert_('?t=' in css_source_1)

        js_source_1 = stylesheet_link(
            dict(file='/deep/a.js', minify='minify'),
            dict(file='/b.js', minify='minify'),
            combined='ab.css',
            timestamp=True)
        time.sleep(1)
        js_source_2 = stylesheet_link(
            dict(file='/deep/a.js', minify='minify'),
            dict(file='/b.js', minify='minify'),
            combined='ab.css',
            timestamp=True)
        self.assertEqual(js_source_1, js_source_2)
        self.assert_('?t=' in js_source_1)

        # cleanup 
        minwebhelpers.beaker_cache = beaker_cache

## CSS STUFF

    def test_css_leading_zero(self):
        self.write_file('js/1.css', """
        p{
            font-size:0.83em !important;
        }""")

        css_source = stylesheet_link(
            dict(file='/js/1.css', minify='minify', dest='/js/1.min.css'))

        self.assertEqual(
            open(os.path.join(self.fixture_path, 'js/1.min.css')).read(),
            'p{font-size:.83em !important}')

    def test_css_no_leading_zero(self):
        self.write_file('js/1.css', """
        p{
            font-size: 10.83em !important;
        }""")

        css_source = stylesheet_link(
            dict(file='/js/1.css', minify='minify', dest='/js/1.min.css'))

        self.assertEqual(
            open(os.path.join(self.fixture_path, 'js/1.min.css')).read(),
            'p{font-size:10.83em !important}')

    def test_zero_px(self):
        self.write_file('js/1.css', """
        p{
            border:0px 1pt 0px 0em;
            border:1px 0em 2em 0pt;
        }""")

        css_source = stylesheet_link(
            dict(file='/js/1.css', minify='minify', dest='/js/1.min.css'))

        self.assertEqual(
            open(os.path.join(self.fixture_path, 'js/1.min.css')).read(),
            'p{border:0 1pt 0 0;border:1px 0 2em 0}')

    def text_stripping(self):
        self.write_file('js/1.css', '''
        p {
            font-size: 0.83em \t !important;
        }''')

        css_source = stylesheet_link(
            dict(file='/js/1.css', minify='strip', dest='/js/1.min.css'))

        self.assertEqual(
            open(os.path.join(self.fixture_path, 'js/1.min.css')).read(),
            'p { font-size: 0.83em !important; }')
