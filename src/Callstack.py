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


from core import *

#from SSA import SSA
from Condition   import *
from SMT         import SMT

def getValueFromCode(inss, initial_values, op):
  assert(len(inss) > 0)
  
  # code should be copied and reversed
  inss.reverse()
  
  ssa = None#SSA()
  smt_conds  = SMT()
 
  # we will track op
  mvars = set([op])    
  #ssa.getMap(mvars, set(), set())

  for ins in inss:

    #counter = ins.getCounter() 
    ins_write_vars = set(ins.getWriteVarOperands())
    ins_read_vars = set(ins.getReadVarOperands())

    print "write vars:"
    for v in ins_write_vars:
      print v,
    print "\nread vars:"
    for v in ins_read_vars:
      print v,
    print "\nmvars:"
    for v in mvars:
      print v,
    print ""


    if len(ins_write_vars.intersection(mvars)) > 0: 
      
      #ssa_map = ssa.getMap(ins_read_vars.difference(mvars), ins_write_vars, ins_read_vars.intersection(mvars))

      #print ssa_map
      #print ins.getCond()
      #assert(0)

      #cons = ins.getCond()
      #condition = cons(ins, ssa_map)
     
      mvars = mvars.difference(ins_write_vars) 
      mvars = ins_read_vars.union(mvars)

      #mvars = set(filter(lambda o: o.name <> "ebp", mvars))
      conds = ins.getCond()
      #print conds
   
      smt_conds.add(conds)
      
  #for iop in initial_values.keys():
  #  if not (iop in ssa):
  #    del initial_values[iop]
    
  #ssa_map = ssa.getMap(set(), set(), set(initial_values.keys()))
  #eq = Eq(None, None)
    
  #for iop in initial_values:
  #  smt_conds.add(eq.getEq(ssa_map[iop.name],initial_values[iop]))
    
  #op.name = op.name+"_0"
  smt_conds.solve()
  
  renamed_name = op.getName()+"_0"
  renamed_size = op.getSizeInBits()
  renamed_offset = op.getOffset()
  renamed_op = op.__class__(renamed_name, renamed_size, renamed_offset)
    
  return smt_conds.getValue(renamed_op)


class Callstack:
  def __init__(self, code):
    
    # The first instruction should be a call
    self.callstack = [None]
    self.stack_diff = []
    
    self.index = 0
    
    # aditional information need to compute the callstack
    self.calls = [None]
    self.esp_diffs = [None]
    self.code = code
    code_size = len(code)
    start = 0  
  
    #for (end,ins) in enumerate(self.code):
    #  if (ins.isCall() and ins.called_function == None) or ins.isRet():
    #    print str(ins), "is call!"
    #    self.__getStackDiff__(ins, code[start:end])
    #    start = end
        
    if (start <> code_size-1):
      ins = code[start]
      self.__getStackDiff__(ins, code[start:code_size-1])
      
    self.index = len(self.callstack) - 1
  
  def __str__(self):
    ret = ""
    for (addr, sdiff) in zip(self.callstack, self.stack_diff):
      if (addr <> None):
        ret = ret + " " + hex(addr) + "[" +str(sdiff)+"]"
    
    return ret
  
  def reset(self):
    self.index = 0
  
  def nextInstruction(self, ins):
    if (ins.isCall() and ins.called_function == None) or ins.isRet():
      self.index = self.index + 1
  
  
  def prevInstruction(self, ins):
    if (ins.isCall() and ins.called_function == None) or ins.isRet():
      self.index = self.index - 1
  
  def currentCall(self):
    return self.callstack[self.index]
    
  def currentStackDiff(self):
    return self.stack_diff[self.index]
  
  def currentCounter(self):
    return 1 # TODO!
  
  def firstCall(self):
    return self.index == 1
  
  #def convertStackMemLoc(self, loc):
    #self.index = self.index - 1
    
    #if self.index == 1:
      #index = (loc.index)+self.currentStackDiff()-4
    #else:
      #index = (loc.index)+self.currentStackDiff()
    
    #new_loc = MemLoc(loc.name,index)  
    
    #einfo = dict()
    #einfo["source.name"] = self.currentCall()
    #new_loc.type = Type(loc.type.name, loc.type.index, loc.type.getInfo())
    
    #print loc.type.getInfo()
    #assert(0)
    #new_loc.type = Type(loc.type.name, loc.type.index, loc.type.getInfo())
    
    ##mem_source =  "s."+hex(self.currentCall())+"."+str(self.currentCounter())
    ##if self.index == 1:
    ##  mem_offset = (op.mem_offset)+self.currentStackDiff()-4#+16
    ##else:
    ##  mem_offset = (op.mem_offset)+self.currentStackDiff()#+16
    ##name = mem_source+"@"+str(mem_offset)
    
    #self.index = self.index + 1
    #return new_loc
    
    #return Operand(name,"BYTE", mem_source, mem_offset)
  
  
  def convertStackMemOp(self, op):
    self.index = self.index - 1
    
    mem_source =  "s."+hex(self.currentCall())+"."+str(self.currentCounter())
    if self.index == 1:
      mem_offset = (op.mem_offset)+self.currentStackDiff()-4#+16
    else:
      mem_offset = (op.mem_offset)+self.currentStackDiff()#+16
    name = mem_source+"@"+str(mem_offset)
    
    self.index = self.index + 1
    
    return Operand(name,"BYTE", mem_source, mem_offset)
  
  def __getStackDiff__(self, ins, reil_code):
    addr = ins.address.getValue()
    if ins.isCall() or reil_code.current == 0:
      call = addr
      esp_diff = self.__getESPdifference__(reil_code, 0) 
        
      self.calls.append(call)
      self.callstack.append(call)
        
      self.stack_diff.append(esp_diff)
      self.esp_diffs.append(esp_diff)
      
    elif ins.isRet():
        
      if (reil_code[0].isCall()):
        self.stack_diff.append(self.__getESPdifference__(reil_code, 0))
      else:
        self.calls.pop()
        self.esp_diffs.pop()
          
        call = self.calls[-1]
        esp_diff = self.esp_diffs[-1]
          
        self.stack_diff.append(self.__getESPdifference__(reil_code, esp_diff)) 
        self.callstack.append(call)
    else:
      assert(False)
  
  def __getESPdifference__(self, reil_code, initial_esp):
    if len(reil_code) == 0:
      return initial_esp
    esp_op = RegOp("R_ESP","DWORD")
    initial_values = dict([ (esp_op, ImmOp(str(0), "DWORD"))])
    return getValueFromCode(reil_code, initial_values, esp_op)+ initial_esp
