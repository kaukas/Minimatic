#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8

import re
import os
import logging
import StringIO
# URLs are always with / separators
import posixpath as path
import shutil
import time

import cssutils
from cssutils.serialize import CSSSerializer
from pylons import config
from pylons.decorators.cache import beaker_cache

from webhelpers.html.tags import javascript_link as __javascript_link
from webhelpers.html.tags import stylesheet_link as __stylesheet_link

from minwebhelpers.jsmin import JavascriptMinify


__all__ = ['javascript_link', 'stylesheet_link']
log = logging.getLogger(__name__)
beaker_kwargs = dict(key='sources',
                     expire='never',
                     type='memory')

js_minify = JavascriptMinify()

def generate_timestamp(timestamp):
    if timestamp:
        return '?t=' + str(int(time.time()))
    else:
        return ''

def combine_sources(sources, ext, fs_root, filename=False, timestamp=False):
    """Use utilities to combine two or more files together.
    
    :param sources: Paths of source files
    :param ext: Type of files
    :param fs_root: Root of file (normally public dir)
    :param filename: Filename of the combined file
    :type sources: string
    :type ext: js or css
    :type fs_root: string
    :type filename: string

    :returns: List of path to minified source
    """

    if len(sources) < 2:
        return sources

    names = list()
    js_buffer = StringIO.StringIO()
    base = path.dirname(os.path.commonprefix(sources))

    for source in sources:
        # get a list of all filenames without extensions
        js_file = path.basename(source)
        js_file_name = path.splitext(js_file)[0]
        names.append(js_file_name)

        # build a master file with all contents
        full_source = path.join(fs_root, (source).lstrip('/'))
        f = open(full_source, 'r')
        js_buffer.write(f.read())
        js_buffer.write('\n')
        f.close()

    fpath = None
    if filename:
        # if name starts with ./ then we want this specific name
        if filename.startswith('./'):
            filename = filename[2:]
            fname = filename
            fpath = path.join(fs_root, filename)
        else:
            names = [filename]
    if not fpath:
        # otherwise glue a new name and generate path to it
        fname = '.'.join(names + ['COMBINED', ext])
        fpath = path.join(fs_root, (base).lstrip('/'), fname)

    # write the combined file
    f = open(fpath, 'w')
    f.write(js_buffer.getvalue())
    f.close()

    link = path.join(base, fname)
    if timestamp:
        timestamp = int(path.getmtime(fpath))
        link = '%s?t=%s' % (link, timestamp)

    return [link]

def minify_sources(sources, ext, fs_root='', timestamp=False):
    """Use utilities to minify javascript or css.
    
    :param sources: Paths of source files
    :param ext: Type of files
    :param fs_root: root of file (normally public dir)
    :type sources: string
    :type ext: js or css
    :type fs_root: string

    :returns: List of paths to minified sources
    """
    if 'js' in ext:
        js_minify = JavascriptMinify()
    minified_sources = []

    for source in sources:
        # generate full path to source
        no_ext_source = path.splitext(source)[0]
        full_source = path.join(fs_root, (no_ext_source + ext).lstrip('/'))

        # generate minified source path
        full_source = path.join(fs_root, (source).lstrip('/'))
        no_ext_full_source = path.splitext(full_source)[0]
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


def process_sources(sources, ext, fs_root, combined=False, timestamp=False):
    """Use utilities to combine two or more files together.
    
    :param sources: Paths of source files (strings or dicts)
    :param ext: Type of files
    :param fs_root: Root of file (normally public dir)
    :param combined: Filename of the combined file
    :param timestamp: Should the timestamp be added to the link
    :type sources: string
    :type ext: js or css
    :type fs_root: string
    :type filename: string
    :type timestamp: bool

    :returns: List of paths to processed sources
    """

    if not sources:
        return []
    if len(sources) == 1 and isinstance(sources, (str, unicode)):
        # We have a single file which doesn't even have to be minified
        return sources

    base = '/'

    # Get the file names and modification dates first
    for i in range(len(sources)):
        source = sources[i]
        # if it's a bare string then we don't want this file to be minified
        if isinstance(source, (str, unicode)):
            source = sources[i] = dict(file=source)
        if not combined and source.get('minify') and not source.get('dest'):
            raise ValueError(
                'Either "combined" must be specified or "dest" for every file')
        source['file_path'] = path.join(fs_root, source['file'].lstrip('/'))
        if source.get('dest'):
            source['dest_path'] = path.join(fs_root, source['dest'].lstrip('/'))
            source['dest_link'] = path.join(base, source['dest'].lstrip('/'))
        source['modts'] = path.getmtime(source['file_path'])

    if combined:
        fname = combined.lstrip('/')
        fpath = path.join(fs_root, fname)

        refresh_needed = False
        if path.exists(fpath):
            last_mod = path.getmtime(fpath)
            refresh_needed = last_mod < max([s['modts'] for s in sources])
        else:
            refresh_needed = True
        buffer = StringIO.StringIO()
    else:
        refresh_needed = True
        buffer = None

    if refresh_needed:
        for source in sources:
            # build a master file with all contents
            dest = buffer
            if not dest:
                dest = source['dest_path']
                if path.exists(dest) and source['modts'] <= path.getmtime(dest):
                    # The file was not modified since the last processing. Skip
                    continue
                dirs = path.dirname(dest)
                try:
                    os.makedirs(dirs, 0700)
                except OSError:
                    pass
                dest = open(dest, 'w')

            if 'js' in ext:
                f = open(source['file_path'], 'r')
                if source.get('minify'):
                    # stream is auto-closed inside
                    js_minify.minify(f, dest)
                else:
                    dest.write(f.read())
                    f.close()
            elif 'css' in ext:
                if source.get('minify'):
                    sheet = cssutils.parseFile(source['file_path'])
                    sheet.setSerializer(CSSUtilsMinificationSerializer())
                    cssutils.ser.prefs.useMinified()
                    dest.write(sheet.cssText)
                else:
                    f = open(source['file_path'], 'r')
                    dest.write(f.read())
                    f.close()
            else:
                raise ValueError('Source type unknown: %s' % ext)
            if buffer:
                buffer.write('\n')
            else:
                dest.close()

        if buffer:
            dirs = path.dirname(fpath)
            try:
                os.makedirs(dirs, 0700)
            except OSError:
                pass
            # write the combined file
            f = open(fpath, 'w')
            f.write(buffer.getvalue())
            f.close()

    if buffer:
        last_mod = path.getmtime(fpath)

        link = path.join(base, fname)
        if timestamp:
            timestamp = int(last_mod)
            link = '%s?t=%s' % (link, timestamp)
        return [link]
    else:
        links = []
        for s in sources:
            last_mod = path.getmtime(s['dest_path'])
            link = s['dest_link']
            if timestamp:
                timestamp = int(last_mod)
                link = '%s?t=%s' % (link, timestamp)
            links.append(link)
        return links


def base_link(ext, *sources, **options):
    """Base function that glues all logic together.

    It parses options and calls :func:`minify_sources` or :func:`combine_sources`
    if apropriate.

    :param ext: js or css helper
    :param sources: paths to your files
    :param combined: if True combines sources into one file
    :param minified: if True minifies javascript or css files
    :param beaker_kwargs: Beaker options to pass to caching decorators
    :param combined_filename: filename that will be used when combining files
    :param timestamp: append `time.time` timestamp to file, eg. test.js?t=123012343
    :type ext: string
    :type sources: string
    :type combined_filename: keyword arg
    :type combined: keyword arg
    :type minified: keyword arg
    :type beaker_kwargs: dict
    :type timestamp: bool
    :returns: HTML source code
    
    .. versionadded:: 0.3.1
        `beaker_kwargs` parameter

    .. versionadded:: 0.3.2
        `combined_filename` parameter

    .. versionadded:: 0.3.5
        `timestamp` parameter
    """
    #filename = options.pop('combined_filename', False)
    combined = options.pop('combined', False)
    #minified = options.pop('minified', False)
    timestamp = options.pop('timestamp', False)
    beaker_options = options.pop('beaker_kwargs', False)
    fs_root = config.get('pylons.paths').get('static_files')

    #if filename and not combined:
    #    raise ValueError("combined_filename=True specifies filename for"
    #        " combined=True parameter which is not set.")

    if not (config.get('debug', False) or options.get('builtins', False)):
        if beaker_options:
            beaker_kwargs.update(beaker_options)

        # use beaker_cache to cache the returned sources
        sources = beaker_cache(**beaker_kwargs)(process_sources)(
            list(sources), ext, fs_root, combined, timestamp)
        #if combined:
        #    # use beaker_cache decorator to cache the return value
        #    sources = beaker_cache(**beaker_kwargs)\
        #        (combine_sources)(list(sources), ext, fs_root,
        #            filename, timestamp)

        #if minified:
        #    # use beaker_cache decorator to cache the return value
        #    sources = beaker_cache(**beaker_kwargs)\
        #        (minify_sources)(list(sources), '.min.' + ext, fs_root, timestamp)

    if 'js' in ext:
        return __javascript_link(*sources, **options)
    if 'css' in ext:
        return __stylesheet_link(*sources, **options)


def javascript_link(*sources, **options):
    """Calls :func:`base_link` with first argument ``js``
    
    All other arguments are passed on.
    """
    return base_link('js', *sources, **options)

def stylesheet_link(*sources, **options):
    """Calls :func:`base_link` with first argument ``css``
    
    All other arguments are passed on.
    """
    return base_link('css', *sources, **options)


class CSSUtilsMinificationSerializer(CSSSerializer):
    
    DOT_ZERO_REGEX = re.compile(r'(?<=[^\d])0(\.\d+)')
    ZERO_PX_REGEX = re.compile(r'([^\d][0])(?:px|em|pt)')

    def do_css_CSSStyleDeclaration(self, style, separator=None):
        try:
            color = style.getPropertyValue('color')
            if color and color is not u'':
                color = self.change_colors(color)
                style.setProperty('color', color)
        except:
            pass
        output = CSSSerializer.do_css_CSSStyleDeclaration(self, style, separator)
        output = self.ZERO_PX_REGEX.sub(r'\1', output)
        return self.DOT_ZERO_REGEX.sub(r'\1', output)

    def change_colors(self, color):
        if color.startswith('#') and len(color) == 7:
            if color[1]==color[2] and color[3]==color[4] and color[5]==color[6]:
                color = '#%s%s%s' % (color[1], color[3], color[5])
        return color
