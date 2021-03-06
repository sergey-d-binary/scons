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
Test that the --diskcheck option and SetOption('diskcheck') correctly
control where or not we look for on-disk matches files and directories
that we look up.
"""

import string

import TestSCons

test = TestSCons.TestSCons()

test.subdir('subdir')

test.write('file', "file\n")



test.write('SConstruct', """
SetOption('diskcheck', 'none')
File('subdir')
""")

test.run()

test.run(arguments='--diskcheck=match', status=2, stderr=None)
test.fail_test(string.find(test.stderr(), "found where file expected") == -1)



test.write('SConstruct', """
SetOption('diskcheck', ['rcs', 'sccs'])
Dir('file')
""")

test.run()

test.run(arguments='--diskcheck=match', status=2, stderr=None)
test.fail_test(string.find(test.stderr(), "found where directory expected") == -1)



test.write('SConstruct', """
SetOption('diskcheck', 'rcs,sccs')
Dir('file/subdir')
""")

test.run()

test.run(arguments='--diskcheck=match', status=2, stderr=None)
test.fail_test(string.find(test.stderr(), "found where directory expected") == -1)



test.pass_test()
