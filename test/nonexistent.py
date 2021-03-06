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

"""
This test verifies that we fail gracefully and provide informative
messages if someone tries to build a target that hasn't been defined
or uses a nonexistent source file.
"""

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

import os.path
import TestSCons

test = TestSCons.TestSCons()

foo_bar = os.path.join('foo', 'bar')

test.write('SConstruct', """
env = Environment()
env.Command("aaa.out", "aaa.in", "should never get executed")
env.Command("bbb.out", "bbb.in", "should never get executed")
File('xxx')
Dir('ddd')
""")

test.run(arguments = 'foo',
         stderr = "scons: *** Do not know how to make target `foo'.  Stop.\n",
         status = 2)

test.run(arguments = '-k foo/bar foo',
         stderr = "scons: *** Do not know how to make target `%s'.\n" % foo_bar,
         status = 2)

test.run(arguments = "aaa.out",
         stderr = "scons: *** Source `aaa.in' not found, needed by target `aaa.out'.  Stop.\n",
         status = 2)

test.run(arguments = "-k bbb.out aaa.out",
         stderr = """scons: *** Source `bbb.in' not found, needed by target `bbb.out'.
scons: *** Source `aaa.in' not found, needed by target `aaa.out'.
""",
         status = 2)

test.run(arguments = '-k aaa.in bbb.in',
         stderr = """scons: *** Do not know how to make target `aaa.in'.
scons: *** Do not know how to make target `bbb.in'.
""",
         status = 2)


test.run(arguments = 'xxx',
         stderr = "scons: *** Do not know how to make target `xxx'.  Stop.\n",
         status = 2)

test.run(arguments = 'ddd')


# Make sure that SCons doesn't print up-to-date messages for non-derived files that exist:
test.write('SConstruct', """
File('xxx')
""")

test.write('xxx', "xxx")

test.run(arguments='xxx', stdout=test.wrap_stdout("""\
scons: Nothing to be done for `xxx'.
"""))
         
test.run(arguments='xxx', stdout=test.wrap_stdout("""\
scons: Nothing to be done for `xxx'.
"""))

test.pass_test()
