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

from Instruction import *

class Path:
  """An abstract path class"""
  def __init__(self, first, last, code = None, filename = None, parser = None, is_reversed = False):
        
    if (filename <> None and parser <> None):
        
      self.init_type = "file"
      self.filename = filename
      self.parser   = parser
      self.code = self.parser(self.filename)
        
    elif (code <> None):
      self.init_type = "code"
      self.code = list(code)
        
    self.code = filter(lambda i: i |iss| Instruction, self.code)
    self.first = first
    if last <> first:
      self.last = min(first + len(self.code), last) - 1
    else:
      self.last = last

    assert(self.last >= self.first)
    self.len = self.last - self.first 

    self.is_reversed = is_reversed

    # add reset and remove following code
    self.reset()
    #if (self.is_reversed):
    #  self.current = self.last
    #else:
    #  self.current = first

  def __iter__(self):
    """Returns the iterator of the path"""
    return self
    
  def __len__(self):
    """Returns the size of the path"""
    return self.len

  def next(self):
    """Returns the next instruction or the previous, depending if the path is reversed"""

    #print self.current, self.is_reversed, self.len
    if (self.is_reversed):
      if self.current < self.first:
        raise StopIteration
      else:
        ins = self.code[self.current]
        ins.setCounter(self.current)
          
        self.current -= 1
        return ins
    else:
       if self.current >= self.last:
         raise StopIteration
       else:
         ins = self.code[self.current]
         ins.setCounter(self.current)
          
         self.current += 1
         return ins        
    
  def reverse(self):
    """Reverse the path, changing the order of the instructions"""

    self.is_reversed = not (self.is_reversed)
    if (self.is_reversed):
      self.current = self.last
    else:
      self.current = self.first
        
  def reset(self):
    """Resets the path to the first or the last instruction, depending if the path is reversed"""

    self.var_map = dict()

    for ins in self.code:
      ins.setVarMap(self.var_map)

    if (self.is_reversed):
      self.current = self.last
    else:
      self.current = self.first
        
  def __getitem__(self, i):
    """Returns an instruction of the path or an slice of the path"""
        
    if (type(i) == slice):
     (first, last, stride) = i.indices(self.len)
          
     if self.init_type == "file":    
       # slice of reversed path not supported!
       assert(not self.is_reversed)		    
       return Path(first, last, filename = self.filename, parser = self.parser, is_reversed = self.is_reversed) 

     elif self.init_type == "code":
       return Path(first, last, code = self.code)

    else: 
      if (i<0):
        i = self.last + 1 + i
      return self.code[i]
