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

from core        import *

#from SSA         import SSA
from Function    import *
from Condition   import *
from SMT         import SMT, Solution
from Typing      import *

concatSet = lambda l: reduce(set.union, l, set())

def getValueFromCode(inss, callstack, initial_values, memory, op, debug = False):
  
  # Initialization
  
  # we reverse the code order
  inss.reverse()
  
  # we reset the used memory variables
  Memvars.reset()
  
  # we save the current callstack
  last_index = callstack.index  # TODO: create a better interface
  
  # we set the instruction counter
  #counter = len(inss)-1
  
  # ssa and smt objects
  ssa = None #SSA()
  smt_conds  = SMT()
  
  mvars = set()
  mlocs = set()
 
  if (op |iss| ImmOp or op |iss| AddrOp):
    return op.getValue()
  
  mvars.add(op)
  mlocs = set(op.getLocations())
  
  # we start without free variables
  fvars = set()
  
  ssa.getMap(mvars, set(), set())

  for ins in inss:
    
    counter = ins.getCounter()
    
    if debug:
      print str(counter) + ":", ins.instruction

    if memory.getAccess(counter) <> None:
      ins.setMemoryAccess(memory.getAccess(counter))
  
    ins_write_vars = set(ins.getWriteVarOperands())
    ins_read_vars = set(ins.getReadVarOperands())
    
    write_locs = concatSet(map(lambda op: set(op.getLocations()), ins.getWriteVarOperands()))
    read_locs  = concatSet(map(lambda op: set(op.getLocations()), ins.getReadVarOperands() ))
    
    if len(write_locs.intersection(mlocs)) > 0: 
    #if len(ins_write_vars.intersection(mvars)) > 0: 
      
      ssa_map = ssa.getMap(ins_read_vars.difference(mvars), ins_write_vars, ins_read_vars.intersection(mvars))

      cons = conds.get(ins.instruction, Condition)
      condition = cons(ins, ssa_map)
      
      mlocs = mlocs.difference(write_locs) 
      mlocs = read_locs.union(mlocs) 
       
      mvars = mvars.difference(ins_write_vars) 
      mvars = ins_read_vars.union(mvars)
   
      smt_conds.add(condition.getEq())

    
    # additional conditions
    mvars = addAditionalConditions(mvars, mlocs, ins, ssa, callstack, smt_conds)

    # we update the current call for next instruction
    callstack.prevInstruction(ins) 
    
  for v in mvars:
    if not (v in initial_values):
      print "#Warning__", str(v), "is free!" 
  
  #setInitialConditions(ssa, initial_values, smt_conds)
  smt_conds.solve(debug)
  
  renamed_name = op.getName()+"_0"
  renamed_size = op.getSizeInBits()
  renamed_offset = op.getOffset()
  renamed_op = op.__class__(renamed_name, renamed_size, renamed_offset)
    
  callstack.index = last_index  # TODO: create a better interface
  return smt_conds.getValue(renamed_op)

      
def getPathConditions(trace, debug = False):
  
  # Initialization
  inss = trace["code"]
  callstack = trace["callstack"]
  
  memory = trace["mem_access"]
  parameters = trace["func_parameters"]
 
  # we reverse the code order
  inss.reverse()
  #print inss[0]
  # we reset the used memory variables
  Memvars.reset()
  
  # we save the current callstack
  last_index = callstack.index  # TODO: create a better interface
  
  # ssa and smt objects
  ssa = SSA()
  smt_conds  = SMT()
  
  mvars = set()
  mlocs = set()

  for op in trace["final_conditions"]:
    mvars.add(op)
    mlocs = mlocs.union(op.getLocations())
  
  # we start without free variables
  fvars = set()
  
  ssa.getMap(mvars, set(), set())
  setInitialConditions(ssa, trace["final_conditions"],smt_conds)
  
  #for c in smt_conds:
  #  print c
  #assert(0)   

  for ins in inss:
    
    
    counter = ins.getCounter()
    func_cons = funcs.get(ins.called_function, Function)

    if memory.getAccess(counter) <> None:
      ins.setMemoryAccess(memory.getAccess(counter))

    ins.clearMemRegs() 
    func = func_cons(None, parameters.getParameters(counter))

    if debug:
      print "(%.4d)" % counter, ins
      for v in mvars:
        print v, v.getSizeInBytes(), "--",
      print ""
     
      for l in mlocs:
        print l, "--",
      print ""
  
    ins_write_vars = set(ins.getWriteVarOperands())
    ins_read_vars = set(ins.getReadVarOperands())
   
    func_write_vars = set(func.getWriteVarOperands())
    func_read_vars = set(func.getReadVarOperands())

    ins_write_locs = concatSet(map(lambda op: set(op.getLocations()), ins.getWriteVarOperands()))
    ins_read_locs  = concatSet(map(lambda op: set(op.getLocations()), ins.getReadVarOperands()))
    
    func_write_locs = concatSet(map(lambda op: set(op.getLocations()), func.getWriteVarOperands()))
    func_read_locs  = concatSet(map(lambda op: set(op.getLocations()), func.getReadVarOperands()))
    
    #if (func_write_vars <> set()):
    #  x =  func_write_vars.pop()
    #  print x, x.getLocations()
    #  assert(0)
    #print func, parameters.getParameters(counter), func_write_vars, func_write_locs 

    if (not ins.isCall()) and (ins.isJmp() or ins.isCJmp() or len(ins_write_locs.intersection(mlocs)) > 0): 
      
      ssa_map = ssa.getMap(ins_read_vars.difference(mvars), ins_write_vars, ins_read_vars.intersection(mvars))

      cons = conds.get(ins.instruction, Condition)
      condition = cons(ins, ssa_map)
      
      mlocs = mlocs.difference(ins_write_locs) 
      mlocs = ins_read_locs.union(mlocs) 
       
      mvars = mvars.difference(ins_write_vars) 
      mvars = ins_read_vars.union(mvars)
   
      smt_conds.add(condition.getEq())
      
    elif (len(func_write_locs.intersection(mlocs)) > 0):
      # TODO: clean-up here!
      #ssa_map = ssa.getMap(func_read_vars.difference(mvars), func_write_vars, func_read_vars.intersection(mvars))
        
      cons = conds.get(ins.called_function, Condition)
      condition = cons(func, None)
        
      c = condition.getEq(func_write_locs.intersection(mlocs))
      
      mlocs = mlocs.difference(func_write_locs) 
      mlocs = func_read_locs.union(mlocs) 
  
      mvars = mvars.difference(func_write_vars) 
      mvars = func_read_vars.union(mvars)

      smt_conds.add(c)
      #print c
      #assert(0)

    
    # additional conditions
    #mvars = addAditionalConditions(mvars, mlocs, ins, ssa, callstack, smt_conds)

    # we update the current call for next instruction
    callstack.prevInstruction(ins) 
  
  fvars = set()
  ssa_map = ssa.getMap(set(), set(), mvars)

  for var in mvars:
    #print v, "--",
    #if not (v in initial_values):
    print "#Warning__", str(var), "is free!" 
    
    if (var |iss| InputOp):
      fvars.add(var)
    elif var |iss| MemOp:
      f_op = var.copy()
      f_op.name = Memvars.read(var)
      fvars.add(f_op) 
    else:
      f_op = var.copy()
      f_op.name = f_op.name+"_0"
      fvars.add(f_op)
    #else:
      #fvars.add(ssa_map[str(var)])
      # perform SSA
      #assert(0)
  
  #setInitialConditions(ssa, initial_values, smt_conds)
  #smt_conds.solve(debug)
  
  callstack.index = last_index  # TODO: create a better interface
  smt_conds.write_smtlib_file("exp.smt2")  
  smt_conds.write_sol_file("exp.sol")
  smt_conds.solve(debug)  

  if (smt_conds.is_sat()):
    #smt_conds.solve(debug)
    return (fvars, Solution(smt_conds.m))
  else: # unsat :(
    return (set(), None)
