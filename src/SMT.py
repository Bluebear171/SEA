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
import z3

class SMT:

  def __init__(self):
    self.solver = z3.Solver()
    self.solver.set(unsat_core=True)
    self.m = None
  
  def add(self, cs):
    for c in cs:
      c = z3.simplify(c)
      #print c
      #if (self.c <= self.max_c):
      #self.solver.assert_and_track(c, str(c))
      self.solver.add(c)

      #self.c = self.c + 1

  def solve(self, debug = False):

    print self.solver

    #if debug:
    #  print self.solver
    
    if (self.solver.check() == z3.sat):
      self.m = self.solver.model()
    elif debug:
      print "unsat core:"
      print self.solver.unsat_core()
  
  def is_sat(self):

    #if not (self.solver.check() == z3.sat):
    #  print self.solver.unsat_core()

    return (self.solver.check() == z3.sat)
      
  def getValue(self, op):
    assert(self.m <> None)
    
    if (op |iss| RegOp):
      var = map(lambda b: z3.BitVec(str(b),8), op.getLocations())
      var = map(lambda b: self.m[b], var)
      if (len(var) > 1):
        return z3.simplify(z3.Concat(var)).as_signed_long()
      else:
        x = z3.simplify(var[0]).as_signed_long()
        print x
        return x
    elif (op.isMem()):
      array = z3.Array(op.name, z3.BitVecSort(16), z3.BitVecSort(8))
      f = self.m[array]
      
      #print self.m
      
      es = f.as_list()[:-1]

      var = []
      
      for loc in op.getLocations():
        byte = None
        for entry in es:
          #print entry
          if loc.getIndex() == entry[0].as_signed_long():
            byte = entry[1]#.as_signed_long()
            break
        
        if (byte == None):
          byte = f.else_value()
          
        var.append(byte)
        
      var.reverse()
      
      if (len(var) > 1):  
        return z3.simplify(z3.Concat(var)).as_signed_long()
      else:
        return z3.simplify(var[0]).as_signed_long()
    else:
      assert(0)


  def write_sol_file(self,filename):
    solf = open(filename, 'w')
    if (self.solver.check() == z3.sat):
      self.m = self.solver.model()
      for d in self.m.decls():
        solf.write("%s = %s\n" % (d.name(), self.m[d])) 
    else:
      solf.write("unsat")
      uc = self.solver.unsat_core()
      for c in uc:
        solf.write(c.sexpr())
      
    solf.close()

  def write_smtlib_file(self,filename):
    smtlibf = open(filename, 'w')
    smtlibf.write(self.solver.sexpr())
    smtlibf.close()
    
    
class Solution:
  def __init__(self, model):
    self.m = model
    #self.vars = dict()
    #self.fvars = set(fvars)
    #for d in self.m.decls():
    #  self.vars[d.name()] = d

  def __getitem__(self, op):
    
    if (op |iss| InputOp):
      r = ""
      for loc in op.getLocations():
        var = z3.BitVec(str(loc),8)
        var = self.m[var]
	r = r +("\\x%.2x" % var.as_long())
      return r

    if (op |iss| RegOp):
      var = map(lambda b: z3.BitVec(str(b),8), op.getLocations())
      var = map(lambda b: self.m[b], var)
      if (len(var) > 1):
        return z3.simplify(z3.Concat(var)).as_signed_long()
      else:
        return z3.simplify(var[0]).as_signed_long()
    elif (op.isMem()):
      array = z3.Array(op.name, z3.BitVecSort(16), z3.BitVecSort(8))
      f = self.m[array]
      
      #print self.m
      
      es = f.as_list()[:-1]

      var = []
      
      for loc in op.getLocations():
        byte = None
        for entry in es:
          #print entry
          if loc.getIndex() == entry[0].as_signed_long():
            byte = entry[1]#.as_signed_long()
            break
        
        if (byte == None):
          byte = f.else_value()
          
        var.append(byte)
      r = "" 
      for v in var:
	r = r +("\\x%.2x" % v.as_long())

      return r


      #var.reverse()
      
      #if (len(var) > 1):  
      #  return z3.simplify(z3.Concat(var)).as_signed_long()
      #else:
      #  return z3.simplify(var[0]).as_signed_long()
    else:
      assert(0)



    r = []
    for loc in i.getLocations():
      r.append(self.vars[str(loc)])
    return r
  """
  def __contains__(self, var):
    #print var
    #print filter(lambda v: var in v, self.vars.keys())
    return filter(lambda v: var in v, self.vars.keys()) <> []
  
  def getString(self, var, escape = False):
    
    if ":" in var:
      r = ""
      i = 0
      while ((var + str(i)+"(0)") in self.vars.keys()):
        d = self.vars[var + str(i)+"(0)"]
        if (escape):
          r = r+"\\"+str(int(self.m[d].as_long()))
        else:
          r = r+chr(int(self.m[d].as_long()))
        i = i + 1
      return r
    
  def dump(self, name, input_vars):
    dumped = []
    for var in input_vars:
      if var in self:
        filename = (var+"."+name+".out").replace(":", "")
        out = open(filename, 'w')
        out.write(self.getString(var))
        dumped.append(filename)
    return dumped
  """
