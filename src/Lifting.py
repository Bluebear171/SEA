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

import os
import subprocess

from src.core import *

realpath  =  os.path.dirname(os.path.realpath(__file__))+"/.."
binpath   = realpath + "/bin"
cachepath = realpath + "/cache"

def check(f):
  if not (os.access(f, os.X_OK) and os.path.isfile(f)):
    print 'Executable %s needed for readelf.py, please install binutils' % f
    exit(-1)

def lift(binary, ir, addr):

  if (ir == "bap"):
    converter = binpath + "/toil"
    cmd = converter  +" -binrecurseat "+ binary + " " + addr + " -tojson"
    outfile = cachepath + "/" + str(hash(cmd)) + ".json"
    cmd =  cmd + " -o " + outfile
    retcode = os.system(cmd)

    if retcode == 0:
      return BapProgram(outfile, binary)


