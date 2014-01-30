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

from json import *
from Operand import *
from Instruction import *
from BapExpression import *

class BapInstruction(Instruction):
  
  def __readAttributes__(self, d):
    if 'attributes' in d:
      atts = d['attributes']
      for att in atts:
        if 'strattr' in att:
          self.isCallV = ('call' == att['strattr'])
        if 'strattr' in att:
          self.isRetV = ('ret' == att['strattr'])
  
  def __getBinOp__(self, d):
    
    name = d["binop_type"]
    op1  = self.__getExp__(d["lexp"])
    op2  = self.__getExp__(d["rexp"])
    
    return BinExp(name, op1, op2)

  def __getUnOp__(self, d):

    name = d["unop_type"]
    op  = self.__getExp__(d["exp"])

    return UnExp(name, op)

  def __getStore__(self, d):
    address = self.__getExp__(d['address'])
    value = self.__getExp__(d['value'])
    return address,value
 
    #print address, "->", value
    #endian = d['endian']
    #assert(0)

  def __getCast__(self, d):
    #if 'type'
    #print d['type']
    #assert(0)
    return UnExp(d['cast_type']+":"+str(d['new_type']["reg"]), self.__getExp__(d['exp']))

  def __getExp__(self, d):
    
    if 'var' in d:
      return self.__getVar__(d['var'])
    if 'inte' in d:
      return self.__getInt__(d['inte'])
    elif 'binop' in d:
      return self.__getBinOp__(d['binop'])
    elif 'unop' in d:
      return self.__getUnOp__(d['unop'])
    elif 'cast' in d:
      return self.__getCast__(d['cast'])
    elif 'unknown' in d:
       return SingleExp(UndefinedOp("", 1))
    #  return self.__getStore__(d['store'])
    else:
      #pass
      print "exp:"
      print d
      assert(0)
  
  def __getInt__(self, d):

    size = d['typ']["reg"]
    return SingleExp(ImmOp(d['int'], size))

  def __getVar__(self, d):
    
    if ('reg' in d['typ']):
      return SingleExp(RegOp(d['name'], d['typ']['reg']))
    else:
      #pass
      print d['name'], d['typ']
      assert(False)

  def __getLoad__(self, d):
    return self.__getExp__(d['address'])

  def __getBranch__(self, d):
    size = "DWORD"
    if 'inte' in d:
      name = hex(self.__getInt__(d['inte']).getOp().getValue())
      return AddrOp(name, size)
    elif 'lab' in d:
      name = d['lab']
      return AddrOp(name, size)
    elif 'load' in d:
      name = hex(self.__getLoad__(d['load']).getOp().getValue())
      return pAddrOp(name, size)
    elif 'var' in d:
      return self.__getVar__(d['var'])
    else:
      print d
      assert(False)
      
  def __init__(self, dins):
    
    self.read_operands = []
    self.write_operands = []
    self.branchs = []
    
    # # for memory instructions
    self.mem_reg = None
    
    # # for call instructions
    self.called_function = None
    self.instruction = None
    self.raw = str(dins)
    self.isCallV = False
    self.isRetV  = False

    self.var = None
    #self.isJmp = False

    #print self.raw
    
    if ('label_stmt' in dins):
      assert(False)
    elif ('move' in dins):
        #pass
        self.instruction = 'move'
        
        #print "moving to:", self.__getVar__(dins['move']['var'])
        if  'store' in dins['move']['exp']:
          address, value = self.__getStore__(dins['move']['exp']['store'])

          self.exp = value
          self.read_operands = map(lambda v: v.getOp(), flatten(value))
          self.write_operands = []
          self.mem_reg = address
        elif 'load' in dins['move']['exp']:
          self.read_operands = []
          self.write_operands = map(lambda v: v.getOp(), flatten(self.__getVar__(dins['move']['var'])))
          address = self.__getLoad__(dins['move']['exp']['load'])
          self.mem_reg = address

        else:
          self.var = self.__getVar__(dins['move']['var'])
          self.exp = self.__getExp__(dins['move']['exp'])
          self.read_operands  = map(lambda v: v.getOp(), flatten(self.exp))
          self.write_operands = map(lambda v: v.getOp(), flatten(self.var))
        
        #print self.write_operands[0], "=", self.read_operands[0]
        #var = dins['move']['var']
        #exp = dins['move']['exp']
        #print 'dst', var['name']
        #print 'src', exp
    elif ('jmp' in dins):
        self.instruction = 'jmp'
        #self.isJmp = True
        self.__readAttributes__(dins['jmp'])
        
        if 'exp' in dins['jmp']:
          self.branchs = [self.__getBranch__(dins['jmp']['exp'])]
            
        #print 'jmp:', dins['jmp']
    elif ('cjmp' in dins):
        self.instruction = 'cjmp'
        self.__readAttributes__(dins['cjmp'])
        self.exp =  self.__getExp__(dins['cjmp']['cond'])
        
        if 'iftrue' in dins['cjmp']:
          d = dins['cjmp']['iftrue']
          self.branchs = [self.__getBranch__(d)]
        
        if 'iffalse' in dins['cjmp']:
          d = dins['cjmp']['iffalse']
          self.branchs.append(self.__getBranch__(d))
                  
         
    else:
        #self.instruction = "xxx"
        print dins
        assert(False)

    #print "read operands:", map(str, self.getReadOperands())
    #print "write operands", map(str, self.getWriteOperands())
        
  def isCall(self):
    return self.isCallV
  def isRet(self):
    return self.isRetV
    
  def isJmp(self):
    return self.instruction == "jmp"
    
  def isCJmp(self):
    return self.instruction == "cjmp"

  def getCond(self):

    print "getCond"
    for op in self.read_operands:
      print op,
    print "\n",
    for op in self.write_operands:
      print op,

    md = dict()
    read_ops = self.getReadVarOperands()

    for op in read_ops:
      md[str(op)] = self.__renameReadOperand__(op)

    if self.isJmp():
      return [] # true
    elif self.isCJmp():
      #print "exp:", self.exp
      return [self.exp.getCond(md)]
    else:
      #if (self.exp is None):
      #  return []
      #elif UndefinedOp("",1) in self.getOperands():
      #  return []
      #else:
        #if self.var <> None:
      #for (x,y) in md.items():
      #    print x,str(y)

      exp_cond = self.exp.getCond(md)
      write_op = self.getReadVarOperands()[0]
      md[str(write_op)] = self.__renameWriteOperand__(write_op)

      #for (x,y) in md.items():
      #    print x,str(y)

      var_cond = self.var.getCond(md)
      return [exp_cond == var_cond]
      #  else:
      #    return []

  def getMemReg(self):
    ops =  filter(lambda v: v.isVar(), map(lambda v: v.getOp(), flatten(self.mem_reg)))
    return ops[0]

    for op in ops:
      print op

    assert(0)


    

def BapParser(filename):
    openf = open(filename)
    size = "DWORD" #size of address
    last_addr = None
    r = []
    
    for dins in load(openf):
      if ('label_stmt' in dins):
        if 'label' in dins['label_stmt']:
          label = dins['label_stmt']['label']
          if 'name' in label:
            x = label['name'].replace("pc_", "")
            last_addr = AddrOp(x, size)
            r.append(last_addr)
          else:
            last_addr = AddrOp(hex(int(label['addr'])), size)
            r.append(last_addr)
      else:
        ins = BapInstruction(dins)
        ins.address = last_addr.copy()
        r.append(ins)
        #assert(0)

    call_ins = BapInstruction(dict(jmp=dict(attributes=[dict(strattr='call')])))
    return r[0:2]+[call_ins]+r[3:]

