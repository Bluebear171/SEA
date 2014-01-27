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
from Memory      import MemAccess
from Parameters  import FuncParameters
from Callstack   import Callstack
from Allocation  import Allocation
from Lifting     import *


def mkTrace(path, raw_inputs, debug = True):
    
    if debug:
      print "Loading trace.."
    
    inputs = parse_inputs(raw_inputs)
    
    #if (raw_inputs <> []):
    #  print "Using these inputs.."
    
    #  for op in Inputs:
    #    print op,"=", Inputs[op]
    if debug:
      print "Detecting callstack layout..."
    callstack = Callstack(path)#, Inputs) #TODO: it should recieve inputs also!
    
    #if debug:
    print callstack
    #assert(0)
    
    allocationLog = Allocation()
    memAccess = MemAccess()
    funcParameters = FuncParameters()
    
    path_size = len(path)
    
    # we reset path iterator and callstack
    path.reset()
    callstack.reset()
    
    #print "Detecting memory accesses and function parameters.."
  
    for ins in path:
      
      counter = ins.getCounter()
      callstack.nextInstruction(ins)
      #print ins,counter
      if ins.isReadWrite():
        memAccess.detectMemAccess(path[0:counter+1], callstack, inputs, counter)
        #AllocationLog.check(MemAccess.getAccess(end), end)
        
      elif ins.isCall() and ins.called_function <> None:
        funcParameters.detectFuncParameters(path[0:counter+1], memAccess, callstack, inputs, counter)
        #if (ins.called_function == "malloc"):
          
          #try:
            #size = int(FuncParameters.getParameters(end)[0][1].name)
          #except ValueError:
            #size = None
          #AllocationLog.alloc(ins.address, end, size)
        #elif (ins.called_function == "free"):
          #ptr = (FuncParameters.getParameters(end)[0][1].mem_source)
          #AllocationLog.free(ptr, end)
    
    if debug:      
      print memAccess
      print funcParameters
      allocationLog.report()
    
    callstack.reset()
    path.reset()
    
    # trace definition
    trace = dict()
    trace["code"] = path
    trace["initial_conditions"] = inputs
    trace["final_conditions"] = dict()
    trace["callstack"] = callstack
    trace["mem_access"] = memAccess
    trace["func_parameters"] = funcParameters
    
    return trace

    
