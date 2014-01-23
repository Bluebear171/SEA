"""
    This file is part of SEA.

    SEA is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    SEA is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with SEA.  If not, see <http://www.gnu.org/licenses/>.

    Copyright 2013 by neuromancer
"""

from src.core import *

def mkPath(pathf, first, last):
  if (".reil" in pathf):
    return ReilPath(pathf, first, last)
  else:
    print "I don't know how to read "+pathf+"."
    assert(0)

def mkProgram(pathf, program):
  if (".reil" in pathf):
     return ReilProgram(pathf)
  elif (".json" in pathf):
    return BapProgram(pathf, program)
  else:
    print "I don't know how to lift "+pathf+"."
    assert(0)


