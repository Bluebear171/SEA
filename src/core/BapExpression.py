
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

from Z3 import mkConst, mkByteVar, Extract, RShift, If, BTrue, BFalse


class SingleExp:
  def __init__(self, op):
    self.op = op

  def iss(self, c):
    isinstance(self, c)

  def getCond(self,md):

    if str(self.op) in md:
       op = md[str(self.op)]
    else:
      op = self.op

    size_in_bits  = op.getSizeInBits()
    size_in_bytes = op.getSizeInBytes()

    if self.op.isVar():
      c =  mkByteVar(op)
    else:
      c = mkConst(op)

    if size_in_bits == 1:
      c = Extract(0,0, c)

    return c

  def __str__(self):
    return str(self.op)

  def getOp(self):
    return self.op

class BinExp:
  def __init__(self, name, op1, op2):
    self.name = name
    self.op1 = op1
    self.op2 = op2

  def getCond(self, md):
    if self.name == "eq":
      #print "types", self.op1.getCond().sort(), self.op2.getCond().sort()
      #print "sizes:", self.op1.getCond().size(), self.op2.getCond().size()
      return self.op1.getCond(md) == self.op2.getCond(md)
      return If(self.op1.getCond(md) == self.op2.getCond(md), BTrue, BFalse)
    if self.name == "lt":
      return If(self.op1.getCond(md) < self.op2.getCond(md), BTrue, BFalse)
    elif self.name == "plus":
      return self.op1.getCond(md) + self.op2.getCond(md)
    elif self.name == "minus":
      return self.op1.getCond(md) - self.op2.getCond(md)
    elif self.name == "andbop":
      return self.op1.getCond(md) & self.op2.getCond(md)
    elif self.name == "xor":
      return self.op1.getCond(md) ^ self.op2.getCond(md)
    elif self.name == "rshift":
      n = self.op2.getCond()
      return RShift(self.op1.getCond(md),n)
    else:
      print self.__str__()
      assert(0)

  def __str__(self):
    return str(self.name)+"("+str(self.op1)+","+str(self.op2)+")"


class UnExp:
  def __init__(self, name, op):
    self.name = name
    self.op = op

  def getCond(self, md):
    if self.name == "not":
      return (~ self.op.getCond())
    elif "cast_low" in self.name:
      n = int(self.name.split(":")[1])-1
      return Extract(n,0, self.op.getCond(md))

    elif "cast_high" in self.name:
      n = int(self.name.split(":")[1])
      h = self.op.getCond().size()-1
      return Extract(h,h-n+1, self.op.getCond(md))

    else:
      print self.__str__()
      assert(0)

  def __str__(self):
    return str(self.name)+"("+str(self.op)+")"

def flatten(exp):
  if isinstance(exp, BinExp):
    return flatten(exp.op1)+flatten(exp.op2)
  elif isinstance(exp, UnExp):
    return flatten(exp.op)
  elif isinstance(exp, SingleExp):
    return [exp]
  else:
    assert(0)

#def replace(exp, md):
#  if exp.iss(BinExp):
#    return BinExp(replace(exp,md)

