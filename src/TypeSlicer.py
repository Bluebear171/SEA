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

concatSet = lambda l: reduce(set.union, l, set())
concatList = lambda l: reduce(lambda a,b: a+b, l, [])

from core        import *
from Common      import getValueFromCode


def typeLocs(ins, callstack, tlocs):
  
  def detectStackChange(loc, sloc):
    
    i = ins.getCounter()
    
    print loc,loc.type
    
    #if (loc.type <> None):
    #  print loc.type.index
   
    if i > 0 and ins.instruction == "call" and ins.called_function == None and \
       ("SPtr32" in str(loc.type)) and loc.index >= 8:
      #assert(0)
      callstack.prevInstruction(ins)
      
      einfo = dict()
      einfo["source.name"] = hex(callstack.currentCall())
      einfo["source.index"] = callstack.currentCounter()
      
      index = (loc.index)+callstack.currentStackDiff()
      cloc = MemLoc(loc.name,index) 
      cloc.type = Type("SPtr32", loc.type.index, einfo)
      
      sloc.discard(loc)
      sloc.add(cloc)
      
      callstack.nextInstruction(ins)
      
  def detectMainParameters(loc, sloc):
    
    #i = ins.getCounter()
    #if i > 0:
    #  return
    


    if ("argv" in str(loc)):
      #print "ENTRE", str(loc)
      #assert(0) 
      #einfo = dict()
      #einfo["source.name"] = "argc"
      #einfo["source.index"] = 0
      sloc.discard(loc)
      sloc.add(loc.getType())

    #elif ("SPtr32" in str(loc.type)) and \
    #   loc.index >= 12 and loc.index < 16:
      
    #  einfo = dict()
    #  einfo["source.name"] = "argv[]"
    #  einfo["source.index"] = 0
    #  sloc.discard(loc)
    #  sloc.add(Type("Ptr32", loc.index-12, einfo))

    #elif ("Ptr32" in str(loc.type)) and \
    #   "argv[]" in str(loc):
      
      #print loc
      #print loc.index % 4
      #assert(0)

    #  einfo = dict()
    #  einfo["source.name"] = "argv[" +str(loc.index / 4)+"]"
    #  einfo["source.index"] = 0
    #  sloc.discard(loc)
    #  sloc.add(Type("Ptr32", loc.index % 4, einfo))

      #print "ENTRE:", Type("Ptr32", loc.index-12, einfo)

  
  def detectStackPtr(loc, sloc):
    
    if loc.name in ["R_ESP","R_EBP"] and \
       ins.instruction == "call" and ins.called_function == None:
      
      einfo = dict()
      einfo["source.name"] = hex(callstack.currentCall())
      einfo["source.index"] = callstack.currentCounter()
      sloc.discard(loc)
      sloc.add(Type("SPtr32", loc.index, einfo))
  
  def detectHeapPtr(loc, sloc):
    #print loc.name
    if loc.name in ["eax"] and \
       ins.instruction == "call" and ins.called_function == "malloc":
     
      #assert(0)
      einfo = dict()
      einfo["source.name"] = ins.address
      einfo["source.index"] = ins.getCounter()
      sloc.discard(loc)
      sloc.add(Type("HPtr32", loc.index, einfo))
  
  
  def detectImm(loc, sloc):
    
    if loc |iss| ImmLoc:
      sloc.discard(loc)
      sloc.add(Type("Data32", loc.index))
    
  
  for sloc in tlocs:
    
    for loc in list(sloc):
      
      if (loc |iss| Location):
        
        detectMainParameters(loc, sloc)
        detectImm(loc, sloc)
        #detectStackChange(loc, sloc)
        detectStackPtr(loc, sloc)
        detectHeapPtr(loc, sloc)
         
def checkType(tlocs):
  pt_name = tlocs[0].name
  einfo  = tlocs[0].einfo
  
  #FIXME: improve type detection
  if (all(map(lambda pt: pt.name == pt_name, tlocs))):
    return Type(pt_name, None, einfo)
    
  assert(False)
    
  
def trackLocs(ins, tlocs, read_ops, write_ops):
  
  if len(write_ops) > 1:
    assert(0)
  else:
    write_locs = write_ops[0].getLocations()
  
  for sloc in tlocs:
    
    for (i,wloc) in enumerate(write_locs):
      if (wloc in sloc):
	sloc.discard(wloc)
	
	for op in read_ops:  
	  read_locs = op.getLocations()
	  sloc.add(read_locs[i])

def getType(inss, callstack, memory, op, initial_type):
  
  #print inss.first, inss.last
  #print inss[-2] 
  #print "-----------------------------------------------------------"
  assert(len(inss) > 0)
  
  if (op |iss| ImmOp):
    return Type("Data32", None)
  
  if (op |iss| AddrOp):
    return Type("Ptr32", None)
  
  #print "hola"
  # code should be copied and reversed
  inss.reverse()
  
  index = callstack.index

  # we will track op
  mlocs = set(op.getLocations())
  
  tlocs = range(op.getSizeInBytes())
  for (i,loc) in enumerate(op.getLocations()):
    
    pt = Type(initial_type.name, i)
    tlocs[i] = set([loc, pt])
  
  for ins in inss:
       
    counter = ins.getCounter()
    
    if memory.getAccess(counter) <> None:
      ins.setMemoryAccess(memory.getAccess(counter))

    #print ins.getCounter(), str(ins)

    ins_write_vars = map(lambda op: set(op.getLocations()), ins.getWriteVarOperands())
    write_locs = concatSet(ins_write_vars)
    
    ins_read_vars  = map(lambda op: set(op.getLocations()), ins.getReadVarOperands())
    read_locs  = concatSet(ins_read_vars)
    
    for loc in mlocs:
      print loc, "::", loc.type, "--",
    
    if (len(mlocs) > 0):
      print "\n"

     
    #for loc in write_locs:
    #  print loc, "::", loc.type, "--",
    
    #if (len(mlocs) > 0):
    #  print "\n"
 
    typeLocs(ins, callstack, tlocs)
    
    if len(write_locs.intersection(mlocs)) > 0: 
      
      trackLocs(ins, tlocs, ins.getReadOperands(), ins.getWriteOperands())
      
      
      mlocs = mlocs.difference(write_locs) 
      mlocs = read_locs.union(mlocs)
    
    callstack.prevInstruction(ins)
  
  callstack.index = index
  #print "finally:"
  for (i,s) in enumerate(tlocs):
    
    #for loc in tlocs[i]:
    #  print loc, "-",
    #print "xxx"
    tlocs[i] = joinset(s)
    
  return checkType(tlocs)

def getTypedValue(inss, callstack, memory, op, initial_type):
  
  rtype = getType(inss, callstack, memory, op, initial_type)
  
  # we reset the path
  inss.reverse()
  inss.reset()
    
  val = getValueFromCode(inss, callstack, dict(), memory, op)

  if ("SPtr32" in str(rtype)) and val >= 12:
   
    einfo = dict()
    einfo["source.name"] = "argv[]"
    einfo["source.index"] = 0
    rtype.setInfo(einfo)
    val = val - 12

  elif ("argv[]" in str(rtype)):
    
    einfo = dict()
    einfo["source.name"] = "argv["+str(val/4)+"]"
    einfo["source.index"] = 0
    rtype.setInfo(einfo)
    val = val % 4

  elif "Ptr32" == str(rtype):
    rtype = Type("GPtr32", None)
    
    einfo = dict()
    einfo["source.name"] = "0x00000000"
    einfo["source.index"] = 0
    rtype.setInfo(einfo)

  return (val, rtype)

