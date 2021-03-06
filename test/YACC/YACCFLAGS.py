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

import os
import os.path
import string
import sys
import TestSCons

_python_ = TestSCons._python_
_exe   = TestSCons._exe

if sys.platform == 'win32':
    compiler = 'msvc'
    linker = 'mslink'
else:
    compiler = 'gcc'
    linker = 'gnulink'

test = TestSCons.TestSCons()



test.write('myyacc.py', """
import getopt
import string
import sys
cmd_opts, args = getopt.getopt(sys.argv[1:], 'o:x', [])
output = None
opt_string = ''
for opt, arg in cmd_opts:
    if opt == '-o': output = open(arg, 'wb')
    else: opt_string = opt_string + ' ' + opt
for a in args:
    contents = open(a, 'rb').read()
    output.write(string.replace(contents, 'YACCFLAGS', opt_string))
output.close()
sys.exit(0)
""")

test.write('SConstruct', """
env = Environment(YACC = r'%(_python_)s myyacc.py',
                  YACCFLAGS = '-x',
                  tools=['yacc', '%(linker)s', '%(compiler)s'])
env.CFile(target = 'aaa', source = 'aaa.y')
""" % locals())

test.write('aaa.y',             "aaa.y\nYACCFLAGS\n")

test.run('.', stderr = None)

test.must_match('aaa.c',        "aaa.y\n -x\n")



test.pass_test()
