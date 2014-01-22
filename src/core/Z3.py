
"""
   Copyright (c) 2013 neuromancer
   All rights reserved.

   Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions
   are met:
   1. Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
   2. Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
   3. The name of the author may not be used to endorse or promote products
      derived from this software without specific prior written permission.

   THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
   IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
   OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
   IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
   INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
   NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
   DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
   THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
   THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import sys
from Operand import *

try:

    sys.path.append("z3py/build/")
    import z3

except:
    sys.exit("You should run bootstrap.sh to download and compile z3 support")

def mkArray(name):
    return z3.Array(name, z3.BitVecSort(16), z3.BitVecSort(8))

def mkByteList(op):
    locs = op.getLocations()

    if (len(locs) > 1):
        return map(lambda b: z3.BitVec(str(b),8), locs)
    else:
        return [z3.BitVec(str(locs[0]),8)]

"""
def mkByteListVar(op):
    locs = op.getLocations()

    if (len(locs) > 1):
        return (map(lambda b: z3.BitVec(str(b),8), locs))
    else:
        return [z3.BitVec(str(locs[0]),8)]
"""

def mkByteVar(op):
    locs = op.getLocations()

    if (len(locs) > 1):
        return z3.Concat(map(lambda b: z3.BitVec(str(b),8), locs))
    else:
        return z3.BitVec(str(locs[0]),8)

"""
def mkByteListConst(imm):
    locs = imm.getLocations()

    if (len(locs) > 1):
        return (map(lambda b: z3.BitVecVal(str(b),8), locs))
    else:
        return [ z3.BitVecVal(str(locs[0]),8)]
"""

def mkConst(imm):
    return z3.BitVecVal(imm.getValue(),imm.size)

Extract = z3.Extract
RShift  = z3.LShR
If      = z3.If
BTrue   = z3.BitVecVal(1,1)
BFalse  = z3.BitVecVal(0,1)