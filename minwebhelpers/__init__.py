#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8

import re
import os
import logging
import StringIO

import cssutils
from jsmin import JavascriptMinify
from cssutils.serialize import CSSSerializer
from pylons import config
from pylons.decorators.cache import beaker_cache

from webhelpers.html.tags import javascript_link as __javascript_link
from webhelpers.html.tags import stylesheet_link as __stylesheet_link


__all__ = ['javascript_link', 'stylesheet_link']
log = logging.getLogger(__name__)
beaker_kwargs = dict(key='sources',
                     expire='never',
                     type='memory')

def combine_sources(sources, ext, fs_root):
    if len(sources) < 2:
        return sources

    names = list()
    js_buffer = StringIO.StringIO()
    base = os.path.commonprefix([os.path.dirname(s) for s in sources])

    for source in sources:
        # get a list of all filenames without extensions
        js_file = os.path.basename(source)
        js_file_name = os.path.splitext(js_file)[0]
        names.append(js_file_name)

        # build a master file with all contents
        full_source = os.path.join(fs_root, source.lstrip('/'))
        f = open(full_source, 'r')
        js_buffer.write(f.read())
        js_buffer.write('\n')
        f.close()

    # glue a new name and generate path to it
    fname = '.'.join(names + ['COMBINED', ext])
    fpath = os.path.join(fs_root, base.strip('/'), fname)

    # write the combined file
    f = open(fpath, 'w')
    f.write(js_buffer.getvalue())
    f.close()

    return [os.path.join(base, fname)]

def minify_sources(sources, ext, fs_root=''):
    if 'js' in ext:
        js_minify = JavascriptMinify()
    minified_sources = []

    for source in sources:
        # generate full path to source
        no_ext_source = os.path.splitext(source)[0]
        full_source = os.path.join(fs_root, (no_ext_source + ext).lstrip('/'))

        # generate minified source path
        full_source = os.path.join(fs_root, (source).lstrip('/'))
        no_ext_full_source = os.path.splitext(full_source)[0]
        minified = no_ext_full_source + ext

        f_minified_source = open(minified, 'w')

        # minify js source (read stream is auto-closed inside)
        if 'js' in ext:
            js_minify.minify(open(full_source, 'r'), f_minified_source)
        # minify css source
        if 'css' in ext:
            sheet = cssutils.parseFile(full_source)
            sheet.setSerializer(CSSUtilsMinificationSerializer())
            cssutils.ser.prefs.useMinified()
            f_minified_source.write(sheet.cssText)

        f_minified_source.close()
        minified_sources.append(no_ext_source + ext)

    return minified_sources

def base_link(ext, *sources, **options):
    combined = options.pop('combined', False)
    minified = options.pop('minified', False)
    beaker_options = options.pop('beaker_kwargs', False)
    fs_root = config.get('pylons.paths').get('static_files')

    if not (config.get('debug', False) or options.get('builtins', False)):
        if beaker_options:
            beaker_kwargs.update(beaker_options)

        if combined:
            sources = beaker_cache(**beaker_kwargs)(combine_sources)(list(sources), ext, fs_root)

        if minified:
            sources = beaker_cache(**beaker_kwargs)(minify_sources)(list(sources), '.min.' + ext, fs_root)

    if 'js' in ext:
        return __javascript_link(*sources, **options)
    if 'css' in ext:
        return __stylesheet_link(*sources, **options)

def javascript_link(*sources, **options):
    return base_link('js', *sources, **options)

def stylesheet_link(*sources, **options):
    return base_link('css', *sources, **options)


class CSSUtilsMinificationSerializer(CSSSerializer):
    def __init__(self, prefs=None):
        CSSSerializer.__init__(self, prefs)

    def do_css_CSSStyleDeclaration(self, style, separator=None):
        try:
            color = style.getPropertyValue('color')
            if color and color is not u'':
                color = self.change_colors(color)
                style.setProperty('color', color)
        except:
            pass
        return re.sub(r'0\.([\d])+', r'.\1',
                      re.sub(r'(([^\d][0])+(px|em)+)+', r'\2',
                      CSSSerializer.do_css_CSSStyleDeclaration(self, style,
                                                               separator)))

    def change_colors(self, color):
        colours = {
            'black': '#000000',
            'fuchia': '#ff00ff',
            'yellow': '#ffff00',
            '#808080': 'gray',
            '#008000': 'green',
            '#800000': 'maroon',
            '#000800': 'navy',
            '#808000': 'olive',
            '#800080': 'purple',
            '#ff0000': 'red',
            '#c0c0c0': 'silver',
            '#008080': 'teal'
        }
        if color.lower() in colours:
            color = colours[color.lower()]

        if color.startswith('#') and len(color) == 7:
            if color[1]==color[2] and color[3]==color[4] and color[5]==color[6]:
                color = '#%s%s%s' % (color[1], color[3], color[5])
        return color
