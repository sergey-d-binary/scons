#!/usr/bin/env python
#
# Copyright (c) 2001 Steven Knight
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

import os
import string
import sys
import TestSCons

python = sys.executable

if sys.platform == 'win32':
    _exe = '.exe'
else:
    _exe = ''

test = TestSCons.TestSCons()

test.write("wrapper.py",
"""import os
import string
import sys
open('%s', 'wb').write("wrapper.py\\n")
os.system(string.join(sys.argv[1:], " "))
""" % string.replace(test.workpath('wrapper.out'), '\\', '\\\\'))

test.write('SConstruct', """
foo = Environment()
link = foo.Dictionary('LINK')
bar = Environment(LINK = '', LINKFLAGS = r'%s wrapper.py ' + link)
foo.Program(target = 'foo', source = 'foo.c')
bar.Program(target = 'bar', source = 'bar.c')
""" % python)

test.write('foo.c', r"""
int
main(int argc, char *argv[])
{
	argv[argc++] = "--";
	printf("foo.c\n");
	exit (0);
}
""")

test.write('bar.c', r"""
int
main(int argc, char *argv[])
{
	argv[argc++] = "--";
	printf("foo.c\n");
	exit (0);
}
""")


test.run(arguments = 'foo' + _exe)

test.fail_test(os.path.exists(test.workpath('wrapper.out')))

test.run(arguments = 'bar' + _exe)

test.fail_test(test.read('wrapper.out') != "wrapper.py\n")

test.pass_test()
