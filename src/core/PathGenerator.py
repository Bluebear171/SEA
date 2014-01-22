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

from __init__ import *

class PathInfo:
  def __init__(self, ilabels):
    pass

class PathGenerator:
  def __init__(program, start, ends, max_count):
    pass
  
  def __iter__(self):
    return self 
    
  def next(self):
    pass
  
  
import random  

class RandomPathGenerator(PathGenerator):
  
  def __init__(self, program, start, ends, max_count = 1000):
    self.program = program
    self.start = start
    self.ends = ends
    self.max_count = max_count
  
  def next(self):
  
    self.program.reset(self.start)
    branches_taken = []
    code = []
    count = 0
    for ins in self.program:
      #print str(ins.ins_raw)
      #print ins.address
      code.append(ins)
      if count == self.max_count:
        break
      
      #if branches_taken <> []:
      #  if branches_taken[-1] in self.ends:
      #    break
         #print "last:", branches_taken[-1]
  
      if ins.isJmp():
	#print ins.branchs[0]
        pass
        #if str(ins.branchs[0]) == "0x8048890":
          #branches_taken.append("exit")
          #break
      
        #if str(ins.branchs[0]) == "0x8048800":
          #branches_taken.append("__stack_chk_fail")
          #break
    
      elif ins.isCJmp():
        count = count + 1
        i = bool(random.randint(0,1))
        #print ins.branchs[0], ins.branchs[1]  
        if i == False:
          branches_taken.append(self.program.selectFalseBranch())
          ins.setBranchTaken(0)
        elif i == True:
          branches_taken.append(self.program.selectTrueBranch())
          ins.setBranchTaken(1)

    
    path = AbsPath(0, len(code), code)

    return (path, branches_taken)

import sys

class ManualPathGenerator(PathGenerator):
  def __init__(self, program, start, ends, max_count = 1000):
    self.program = program
    self.start = start
    self.max_count = max_count
    
  def __help_path__(self):
   print "To select interactively a path in this program use:"
   print "t to continue with the true branch."
   print "f to continue with the false branch."
   print "i to step in."
   print "o to step out."
   print "e to finish recording a path."
  
  def __ask__(self, values):
  
    i = None
    prompt = ",".join(values)+">"
    
    try:
      while (not (i in values)):
        if i <> None:
          print "Invalid selection"
        i = raw_input(prompt)
    except EOFError:
      print ""
      sys.exit(0)
      

  
    return i
 

  def next(self):
  
    self.program.reset(self.start)
    branches_taken = []
    code = []
    counter = 0
    self.__help_path__()
    for ins in self.program:
      
      code.append(ins)
      print "(%.4d)" % counter, ins
      #print ins.getCond()
      # if not (UndefinedOp("",1) in ins.getOperands()):
      #   print ins.getCond()
      # else:
      #   print ""
      counter = counter + 1
      if counter == self.max_count:
        break
      
      #if ins.isCall() and False:
      #  print "call detected! (", ins.branchs[0], ")"
      #  i = ask(["i", "o", "e"])
      
      #  if (i == "e"):
      #    break
      #  elif (i == "i"):
      #    self.program.stepIn()
      #  elif (i == "o"):
      #    pass


      #elif ins.isJmp():
      #  pass
    
      if ins.isCJmp():
        i = self.__ask__(["t","f","e"])#bool(random.randint(0,1))
        if i == "f":
          branches_taken.append(self.program.selectFalseBranch())
          ins.setBranchTaken(0)
        elif i == "t":
          branches_taken.append(self.program.selectTrueBranch())
          ins.setBranchTaken(1)
        elif i == "e":
          code.pop()
          break
      else:
        pass
	#i = self.__ask__(["s","e"])
	#if i == "s":
	#  pass
	#elif i == "e":
	#  code.pop()
	#  break

    
    path = AbsPath(0, len(code), code)
    return (path, branches_taken)

class MarkovianPathGenerator(PathGenerator):
  def __init__(self, program, start, ends, train_labels, max_count = 1000):
    pass
    
    



