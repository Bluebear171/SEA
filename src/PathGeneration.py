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

import random
import csv

from core import *

from Lifting import *
from Prelude import *
from Common import getPathConditions

"""
class PathInfo:
  def __init__(self, ilabels):
    self.E_viw = dict()
    
    self.vi = dict()
    labels = list(ilabels)
    labels.insert(0,"start")
    labels.append("end")
    
    for label in labels:
      self.vi[label] = 0
    
    for (i, label) in enumerate(labels[:-1]):
      self.vi[label] = self.vi[label] + 1 
      self.E_viw[(label, self.vi[label], labels[i+1])] = True
      
  def E(self, v,i, w, j):
    
    return ((v, i, w) in self.E_viw) and j <= self.vi[w] 


class EXISTPathGenerator(PathGenerator):
  
  def __init__(self, program, start, ends, epsilon):
    self.program = program
    self.start = start
    self.epsilon = epsilon
    
    ## for all possible labels
    #self.max_counts = dict()
    
    ## label population
    #for (s, y) in self.epsilon:
      #for label in s:
        #self.max_counts[label] = 0
        
    self.train()
    
  def count(self, seq, labels):
    pass
    #res = dict()
    
    #for label in labels:
      #res[label] = seq.count(label)
	
    #return res
  
  def train(self):
    
    self.pathinfos = []
    
    for (i, (labels, y)) in enumerate(self.epsilon):
      if y:
	pi = PathInfo(labels)
	self.pathinfos.append(pi)
	#print pi.E_viw
  
  def prob(self, v,i, w,j):
    
    count = 0
    for pi in self.pathinfos:
      
      if pi.E(v,i, w, j):
        count = count + 1
    
    if count == 0:
      return 1.0
    
    return float(count)/float(len(self.pathinfos))
    #if self.max_counts[k] == 0: 
      #return 0
    #return float(self.max_counts[k] - res[k])/float(self.max_counts[k])
  
  def select(self, seq, states):
    
    v = seq[-1]
    
    probs = map(lambda w: self.prob(v, seq.count(v) ,w , seq.count(w)+1), states) 
    m = max(probs)
    
    #if (m == 0.0):
    #  return None
    
    indexes = [i for i, j in enumerate(probs) if j == m]
    
    return random.choice(indexes)
    
  
  def next(self):
    self.program.reset(self.start)
    seq = ["start"]
    count = 0
    max_count = 20
    
    for ins in self.program:
      ##print str(ins.raw)
      ##print ins.ins
      if count == max_count:
        break
      
      ##if branches_taken <> []:
        ##print "last:", branches_taken[-1]
  
      if ins.isCall():
	pass
        ##if str(ins.branchs[0]) == "0x8048890":
          ##branches_taken.append("exit")
          ##break
      
        ##if str(ins.branchs[0]) == "0x8048800":
          ##branches_taken.append("__stack_chk_fail")
          ##break
    
      elif ins.isCJmp():
        count = count + 1
        i = self.select(seq, map(str, ins.branchs))
        
        #print i,
        
        if i == None:
	  return seq
        
        if i == 0:
          seq.append(str(self.program.selectFalseBranch()))
        elif i == 1:
          seq.append(str(self.program.selectTrueBranch()))
        else:
	  assert(False)
	
	if seq[-1] == "end":
	  break
        
    
    return seq
    #return branches_taken
"""


def generatePaths(program, start, end, n):

  random_paths = ManualPathGenerator(program, start, set([end]))
  epsilon = dict()#list()
  rand_count = 0
  gen_count = 0
  path_set = set()
  #csv_writer = csv.writer(open('loop_bad_impos.csv', 'wb'))

  for (i,(path, labels)) in enumerate(random_paths):
    
    path.reset()
    trace = mkTrace(path, [], False)
    #path.reset()
    #fvars, sol = getPathConditions(trace, False)

    #if sol <> None:
    #  print "SAT!"
    #  for var in fvars:
    #    print "sol["+str(var)+"] =", sol[var]
    #else:
    #  print "UNSAT!"
      #if not (str(labels) in path_set):
      #  path_set.add(str(labels))
      #  csv_writer.writerow(labels)
      #  print labels
        
    #if (i==1000):
    #  break
  """
  assert(0) 
  print float(rand_count)/10000
  
  #print epsilon
  
  gen_paths = EXISTPathGenerator(program, start, set(), epsilon.values())
  paths = []
  
  
  
  for (i,path) in enumerate(gen_paths):
    
    
    (x,y,z) = detectFeasible(path)
    
    
    #paths.append((path,(x > 0 and 2*x == y and z == 1)))
    
    
    if ((x > 0 and 2*x == y and z == 1)):
      gen_count = gen_count + 1
    
    #print paths[-1]
    #if :
      
    
    
    if (i==10000):
      break
  
  #print paths
  print float(gen_count)/10000
  """
      

