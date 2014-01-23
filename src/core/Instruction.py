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

from Operand import *
from copy    import copy

class Instruction:
  """An abstract instruction class"""

  exp = None

  def __init__(self, raw_ins):
    """Creates a new instruction from raw data"""
    pass
  
  def setMemoryAccess(self, mem_access):
    """Set the memory address accessed by the instruction updating its read/write operands"""
    pass

  def setBranchTaken(self, branch):
    """Set the branch taken in a jmp instruction"""  
    pass

  def getBranchTaken(self):
    """Get the branch taken in a jmp instruction"""  
    pass

  def setCalledFunction(self, fname):
    self.called_function = str(fname)
 
  def getCounter(self):
    """Returns the counter set by an instruction path"""
    return self.counter

  def setCounter(self, counter):
    """Sets the instructions counter in a path"""
    self.counter = counter

  def setVarMap(self, d):
    self.var_map = d

  def __renameWriteOperand__(self, op):

    if not (str(op) in self.var_map):
      self.var_map[str(op)] = -1

    self.var_map[str(op)] = self.var_map[str(op)] + 1
    op_ren = op.copy()
    op_ren.name = str(op)+"_"+str(self.var_map[str(op)])
    return op_ren

  def __renameReadOperand__(self, op):

    if not (str(op) in self.var_map):
      self.var_map[str(op)] = 0

    op_ren = op.copy()
    op_ren.name = str(op)+"_"+str(self.var_map[str(op)])

    return op_ren

  def getOperands(self):
    """Returns the list of all operands"""
    return list(self.read_operands + self.write_operands)
  
  def getReadOperands(self):
    """Returns the list of read operands"""
    return list(self.read_operands)

  def getWriteOperands(self):
    """Returns the list of written operands"""
    return list(self.write_operands)

  def getReadRegOperands(self):
    """Returns the list of operand that are read registers"""
    return filter(lambda o: o |iss| RegOp, self.read_operands)

  def getWriteRegOperands(self):
    """Returns the list of operands that are written registers"""
    return filter(lambda o: o |iss| RegOp, self.write_operands)
  
  def getReadVarOperands(self):
    """Returns the list of read operands that are not constant"""
    return filter(lambda o: o.isVar(), self.read_operands)

  def getWriteVarOperands(self):
    """Returns the list of written operand that are not constants""" 
    return filter(lambda o: o.isVar(), self.write_operands)
  
  def getReadMemOperands(self):
    return filter(lambda o: o.isMem(), self.read_operands)

  def getWriteMemOperands(self):
    return filter(lambda o: o.isMem(), self.write_operands)
  
  def getMemReg(self):
    """Returns the register operand used for memory addressing (or None)"""
    return self.mem_reg 
  
  def isReadWrite(self):
    """Returns if the instruction is reading or writing the memory"""
    return self.mem_reg <> None
  
  def isCall(self):
    """Returns if the instruction is a call"""
    pass

  def isRet(self):
    """Returns if the instruction is a ret"""
    pass
    
  def isJmp(self):
    """Returns if the instruction is an unconditional jmp"""
    pass
    
  def isCJmp(self):
    """Returns if the instruction is a conditional jmp"""
    pass

  def getCond(self):
    """Returns the conditions, using the dictionary md to replace variables"""
    pass

  def copy(self):
    """Returns a copy of current instance of Instruction"""
    return copy(self)

  def __str__(self):

    if self.isJmp() or self.isCJmp():
        return "jmp to: "+" ".join(map(str, self.branchs))
    else:
      return " ".join(map(str, self.getWriteOperands()))+ " := "+ str (self.exp)

