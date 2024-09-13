# Copyright (c) 2013-2015, 2020 The Linux Foundation. All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 and
# only version 2 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import os
import platform
import glob
import re
import string
import sys

_parsers = []


class ParserConfig(object):

    """Class to encapsulate a RamParser its desired setup (command-line
    options, etc)."""

    def __init__(self, cls, longopt, desc, shortopt, optional):
        self.cls = cls
        self.longopt = longopt
        self.desc = desc
        self.shortopt = shortopt
        self.optional = optional


def cleanupString(unclean_str):
    if unclean_str is None:
        return unclean_str
    else:
        return ''.join([c for c in unclean_str if c in string.printable])


def import_all_by_path(path):
    """Imports everyone under the given directory. It is expected that
    the modules under the given directory will register themselves with
    one of the decorators below.

    Note that the import is effectively a noop if the module has already
    been imported, so there's no harm in calling with the same path
    multiple times"""

    dir = os.path.join(os.path.dirname(__file__), path)
    if not os.path.isdir(dir):
        return

    package = path.replace(os.sep, '.')
    for f in sorted(glob.glob(os.path.join(dir, '*.py'))):
        modname_ext = os.path.basename(f)
        if modname_ext == '__init__.py':
            continue

        modname = os.path.splitext(modname_ext)[0]
        __import__(package + '.' + modname)


def register_parser(longopt, desc, shortopt=None, optional=False):
    """Decorator for registering a parser class.

    By using this decorator your parser will automatically be hooked
    up to the command-line parsing code.

    This makes it very easy and clean to add a new parser:

      1. Drop a new file in the ``parsers/`` directory
      2. Decorate your class with ``@register_parser``
      3. Define a ``parse`` method for your class

    All the command line argument handling and invoking the parse
    method of your parser will then be handled automatically.

    Example::

       # file: parsers/my_banner.py
       @register_parser('--banner', 'Print the kernel banner')
       class BannerParser(Parser):

    :param longopt: The longopt command line switch for this parser
    :param desc: A short description of the parser (also shown in the
        help-text associated with the longopt)
    :param shortopt: The shortopt command line switch for this parser.
        This should only be used for maintaining backwards compatibility
        with legacy parsers.  Otherwise shortopts are reserved for core
        parser options.
    :param optional: Indicates the parser is optional and should not be run
        with ``--everything``
    """
    def wrapper(cls):
        if cls in [p.cls for p in _parsers]:
            raise Exception(cls + ' is already registered!')
        _parsers.append(ParserConfig(cls, longopt, desc, shortopt, optional))
        return cls
    return wrapper


def get_parsers():
    """Imports everyone under the ``parsers`` directory. It is expected that
    the parsers under the parsers directory will be a collection of
    classes that subclass RamParser and use the register_parser
    decorator to register themselves with the parser
    framework. Therefore, importing all the modules under ``parsers``
    should have the side-effect of populating the (internal to
    parser_util) _parsers list with the discovered parsers.

    Returns the list of ParserConfig instances built as a side-effect
    of the importing.

    """

    import_all_by_path('parsers')
    import_all_by_path(os.path.join('extensions', 'parsers'))
    return _parsers


class OnemoreParser(object):

    """Base class for implementing onemore parsers. New parsers should inherit
    from this class and define a ``parse`` method.

    Interesting properties that will be set for usage in derived
    classes:

    - onemore:: The Onemore instance being parsed

    """

    def __init__(self):
        self.onemore = None

    def parse(self):
        raise NotImplementedError


def which(program):
    """Just like which(1).

    Searches the PATH environment variable for a directory containing
    program.

    """
    for path in os.environ['PATH'].split(os.pathsep):
        exe_file = os.path.join(path, program)
        if os.access(exe_file, os.X_OK):
            return exe_file

    return None


def get_system_type():
    """Returns a "normalized" version of platform.system (transforming CYGWIN
    to Windows, for example).

    Returns None if not a supported platform.

    """
    plat = platform.system()
    if plat == 'Windows':
        return 'Windows'
    if re.search('CYGWIN', plat) is not None:
        # On certain installs, the default Windows shell
        # runs cygwin. Treat cygwin as windows for this
        # purpose
        return 'Windows'
    if plat == 'Linux':
        return 'Linux'
    if plat == 'Darwin':
        return 'Darwin'


if __name__ == "__main__":
    import doctest
    doctest.testmod()
