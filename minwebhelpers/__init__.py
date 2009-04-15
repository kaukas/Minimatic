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


log = logging.getLogger(__name__)
__all__ = ['javascript_link', 'stylesheet_link']
beaker_kwargs = dict(key='sources',
                     expire='never',
                     type='memory',
                     invalidate_on_startup=True)

def javascript_link(*sources, **options):

    @beaker_cache(**beaker_kwargs)
    def combine_sources(sources, fs_root):
        if len(sources) < 2:
            return sources

        httpbase = os.path.commonprefix(
            ['/'.join(s.split('/')[:-1])+'/' for s in sources])
        jsbuffer = StringIO.StringIO()
        names = []
        bases = os.path.commonprefix([b.split('/')[:-1] for b in sources])
        for source in sources:
            _source = os.path.join(fs_root, *(source).split('/'))
            names.append(source.split('/')[-1:][0][:-3])
            jsbuffer.write(open(_source, 'r').read())
            jsbuffer.write('\n')
        fname = '.'.join(names+['COMBINED', 'js'])
        fpath = os.path.join(fs_root, *((httpbase+fname).split('/')))
        open(fpath, 'w').write(jsbuffer.getvalue())
        return [httpbase + fname]

    @beaker_cache(**beaker_kwargs)
    def get_sources(sources, fs_root=''):
        jsm = JavascriptMinify()
        _sources = []

        for source in sources:
            _source = os.path.join(fs_root, *(source[:-3]+'.min.js').split('/'))
            if os.path.exists(_source):
                _sources.append(source[:-3]+'.min.js')
            else:
                _source = os.path.join(fs_root, *source.split('/'))
                minified = _source[:-3]+'.min.js'
                jsm.minify(open(_source, 'r'), open(minified, 'w'))
                _sources.append(source[:-3]+'.min.js')
        return _sources

    combined = options.pop('combined', False)
    minified = options.pop('minified', False)

    if config.get('debug', False):
        return __javascript_link(*sources, **options)

    if options.get('builtins', False):
        return __javascript_link(*sources, **options)

    fs_root = root = config.get('pylons.paths').get('static_files')
    if combined:
        sources = combine_sources([source for source in sources], fs_root)

    if minified:
        sources = get_sources([source for source in sources], fs_root)
    return __javascript_link(*sources, **options)

def stylesheet_link(*sources, **options):

    @beaker_cache(**beaker_kwargs)
    def combine_sources(sources, fs_root):
        if len(sources) < 2:
            return sources

        httpbase = os.path.commonprefix(
            ['/'.join(s.split('/')[:-1])+'/' for s in sources])
        jsbuffer = StringIO.StringIO()
        names = []
        for source in sources:
            _source = os.path.join(fs_root, *(source).split('/'))
            names.append(source.split('/')[-1:][0][:-4])
            jsbuffer.write(open(_source, 'r').read())
            jsbuffer.write('\n')
        fname = '.'.join(names+['COMBINED', 'css'])
        fpath = os.path.join(fs_root, *((httpbase+fname).split('/')))
        open(fpath, 'w').write(jsbuffer.getvalue())
        return [httpbase + fname]

    @beaker_cache(**beaker_kwargs)
    def get_sources(sources, fs_root):
        _sources = []

        for source in sources:
            _source = os.path.join(fs_root, *(source[:-4]+'.min.css').split('/'))
            if os.path.exists(_source):
                _sources.append(source[:-4]+'.min.css')
            else:
                _source = os.path.join(fs_root, *source.split('/'))
                minified = _source[:-4]+'.min.css'
                sheet = cssutils.parse(_source)
                sheet.setSerializer(CSSUtilsMinificationSerializer())
                cssutils.ser.prefs.useMinified()
                open(minified, 'w').write(sheet.cssText)
                _sources.append(source[:-4]+'.min.css')
        return _sources

    combined = options.pop('combined', False)
    minified = options.pop('minified', False)

    if config.get('debug', False):
        return __stylesheet_link(*sources, **options)

    fs_root = root = config.get('pylons.paths').get('static_files')
    if combined:
        sources = combine_sources([source for source in sources], fs_root)

    if minified:
        sources = get_sources([source for source in sources], fs_root)
    return __stylesheet_link(*sources, **options)


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
