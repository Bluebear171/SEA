#!/usr/bin/python2

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

import sys
import argparse

from src.Prelude            import mkTrace
from src.Common             import getPathConditions
from src.JumpConditions     import getJumpConditions
from src.PathGeneration     import generatePaths
from src.Lifting            import mkPath, mkProgram

parser = argparse.ArgumentParser(description='Symbolic Exploit Assistant.')
parser.add_argument('trace_filename', metavar='trace', type=str,
                    help='a sequence of REIL instruction in a trace')

parser.add_argument('-first', dest='first', action='store', type=str,
                   default=str(0), help='first instruction to process')

parser.add_argument('-last', dest='last', action='store', type=str,
                   default=str(sys.maxint-1), help='last instruction to process')

parser.add_argument('-type', dest='type', action='store', type=str,
                   default="debug", help='exploit type')

parser.add_argument('-address', dest='address', action='store', type=str,
                   default=None, help='which address to jump in jump mode')

parser.add_argument('iconditions', metavar='operator,value', type=str, nargs='*',
                   help='initial conditions for the trace')

args = parser.parse_args()

# mode  = args.type
# valid_modes = ["jump", "path", "debug", "selection", "generation"]
#
# if not (mode in valid_modes):
#   print "\""+mode+"\" is an invalid type of operation for SEA"
#   exit(1)
#
# if (mode == 'debug'):
#
#   first = int(args.first)
#   last  = int(args.last)
#   path = mkPath(args.trace_filename, first, last)
#   trace = mkTrace(path, args.iconditions, debug = True)
#
# if (mode == "jump"):
#
#   first = int(args.first)
#   last  = int(args.last)
#
#   address = args.address
#   path = mkPath(args.trace_filename, first, last)
#
#   trace = mkTrace(path, args.iconditions, debug = True)
#
#   if (address == None):
#     print "An address to jump to should be specified!"
#   else:
#     (fvars, sol) = getJumpConditions(trace, address)
#
#     if sol <> None:
#       print "SAT!"
#       for var in fvars:
#         print "sol["+str(var)+"] =", sol[var]
#     else:
#       print "UNSAT!"
#
#
# elif (mode == 'path'):
#
#   first = int(args.first)
#   last  = int(args.last)
#
#   address = args.address
#   path = mkPath(args.trace_filename, first, last)
#   trace = mkTrace(path, args.iconditions, debug = True)
#   fvars, sol = getPathConditions(trace, False)
#
#   if sol <> None:
#     print "SAT!"
#     for var in fvars:
#       print "sol["+str(var)+"] =", sol[var]
#   else:
#     print "UNSAT!"
#
# elif (mode == 'generation'):

program = mkProgram(args.trace_filename)
generatePaths(program,args.first, args.last, 2000)
    

