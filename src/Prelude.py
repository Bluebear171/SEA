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
from Inputs      import parse_inputs
from Memory      import MemAccessREIL
from Parameters  import FuncParametersREIL
from Callstack   import Callstack as CS
from Allocation  import Allocation

def mkTrace(trace_filename, first, last, raw_inputs):
    
    print "Loading trace.."
    reil_code = ReilPath(trace_filename, first, last)
    
    Inputs = parse_inputs(raw_inputs)
    
    if (raw_inputs <> []):
      print "Using these inputs.."
    
      for op in Inputs:
        print op,"=", Inputs[op]
    
    print "Detecting callstack layout..."
    Callstack = CS(reil_code)#, Inputs) #TODO: it should recieve inputs also!
    
    reil_code.reset()
    
    print Callstack
    
    AllocationLog = Allocation()
    MemAccess = MemAccessREIL()
    FuncParameters = FuncParametersREIL()
    
    reil_size = len(reil_code)
    start = 0  
  
    Callstack.reset()
    
    print "Detecting memory accesses and function parameters.."
  
    for (end,ins) in enumerate(reil_code):
      
      Callstack.nextInstruction(ins)
      
      if ins.instruction in ["stm", "ldm"]:
	
        MemAccess.detectMemAccess(reil_code[start:end+1], Callstack, Inputs, end)
        #AllocationLog.check(MemAccess.getAccess(end), end)
        
      elif ins.isCall() and ins.called_function <> None:
        ##print "detect parameters of", ins.called_function, "at", ins_str
        FuncParameters.detectFuncParameters(reil_code[start:end+1], MemAccess, Callstack, Inputs, end)
        if (ins.called_function == "malloc"):
          
          try:
            size = int(FuncParameters.getParameters(end)[0][1].name)
          except ValueError:
            size = None
          AllocationLog.alloc(ins.address, end, size)
        elif (ins.called_function == "free"):
          ptr = (FuncParameters.getParameters(end)[0][1].mem_source)
          AllocationLog.free(ptr, end)
    
    
    print MemAccess
    print FuncParameters
    AllocationLog.report()
    
    
    Callstack.reset()
    reil_code.reset()
    
    # trace definition
    trace = dict()
    trace["code"] = reil_code
    trace["initial_conditions"] = Inputs
    trace["final_conditions"] = dict()
    trace["callstack"] = Callstack
    trace["mem_access"] = MemAccess
    trace["func_parameters"] = FuncParameters
    
    return trace

    
