#!/usr/bin/env python
#
# __COPYRIGHT__
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

"""
Verify that use of SWIGPATH finds dependency files in subdirectories.
"""

import sys

import TestSCons

if sys.platform =='darwin':
    # change to make it work with stock OS X python framework
    # we can't link to static libpython because there isn't one on OS X
    # so we link to a framework version. However, testing must also
    # use the same version, or else you get interpreter errors.
    python = "/System/Library/Frameworks/Python.framework/Versions/Current/bin/python"
    _python_ = '"' + python + '"'
else:
    python = TestSCons.python
    _python_ = TestSCons._python_

test = TestSCons.TestSCons()

swig = test.where_is('swig')

if not swig:
    test.skip_test('Can not find installed "swig", skipping test.\n')



test.subdir('inc1', 'inc2')

test.write(['inc2', 'dependency.i'], """\
%module dependency
""")

test.write("dependent.i", """\
%module dependent

%include dependency.i
""")

test.write('SConstruct', """
foo = Environment(SWIGFLAGS='-python',
                  SWIGPATH=['inc1', 'inc2'])
swig = foo.Dictionary('SWIG')
bar = foo.Clone(SWIG = r'%(_python_)s wrapper.py ' + swig)
foo.CFile(target = 'dependent', source = ['dependent.i'])
""" % locals())

test.run()

test.up_to_date(arguments = "dependent_wrap.c")

test.write(['inc1', 'dependency.i'], """\
%module dependency

extern char *dependency_1();
""")

test.not_up_to_date(arguments = "dependent_wrap.c")

test.write(['inc2', 'dependency.i'], """\
%module dependency
extern char *dependency_2();
""")

test.up_to_date(arguments = "dependent_wrap.c")

test.unlink(['inc1', 'dependency.i'])

test.not_up_to_date(arguments = "dependent_wrap.c")

test.up_to_date(arguments = "dependent_wrap.c")



test.pass_test()