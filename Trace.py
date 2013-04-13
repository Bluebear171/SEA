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

class IR_Trace:
    def __init__(self, filename, first, last):
        pass
    
    def __iter__(self):
        return self

    def next(self):
        pass
    
    # more functions
    
    def reset(self):
        pass
    
    def __getitem__(self, i):
        pass
    
    
class REIL_Trace(IR_Trace):
    def __init__(self, filename, first, last, is_reversed = False):
        
        self.filename = filename
        self.reilf = open(filename)
        self.reil_code = self.reilf.readlines()[first:last+1]
        
        #print self.reil_code
        
        self.len = len(self.reil_code)
        
        self.first = first
        self.last = first + self.len
        #self.len = self.last - self.first
        
        self.is_reversed = is_reversed
        
        if (self.is_reversed):
          self.current = self.len - 1
        else:
          self.current = 0

    def __iter__(self):
        return self
    
    def __len__(self):
        return self.len

    def next(self):
        #print self.current, self.is_reversed, self.len
        if (self.is_reversed):
          if self.current < 0:
            raise StopIteration
          else:
            self.current -= 1
            return self.reil_code[self.current + 1]
        else:
          if self.current >= self.len:
            raise StopIteration
          else:
            self.current += 1
            return self.reil_code[self.current - 1]  
          
    
    def reverse(self):
        self.is_reversed = not (self.is_reversed)
        if (self.is_reversed):
          self.current = self.len - 1
        else:
          self.current = 0
        #return REIL_Trace(self.filename, self.first, self.last, is_reversed = not (self.is_reversed))
        
    def reset(self):
        if (self.is_reversed):
          self.current = self.len - 1
        else:
          self.current = 0
        
    def __getitem__(self, i):
        
        if (type(i) == slice):
          (first, last, stride) = i.indices(self.len)
          #print (first, last, stride), self.is_reversed
          return REIL_Trace(self.filename, first, last-1) #self.__init__(self.filename, first, last)
        else:
           return self.reil_code[i]
