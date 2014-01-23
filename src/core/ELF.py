"""
   Copyright (c) 2014 pwnies, neuromancer
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

# Code taken from: https://github.com/pwnies/pwntools (pwn/elf.py)

import re
import subprocess

_READELF = '/usr/bin/readelf'
_OBJDUMP = '/usr/bin/objdump'

def die(s):
  print s
  exit(-1)

def check(f):
  import os
  if not (os.access(f, os.X_OK) and os.path.isfile(f)):
    die('Executable %s needed for readelf.py, please install binutils' % f)

check(_READELF)
check(_OBJDUMP)

def plt_got(path):
  plt, got = dict(), dict()

  cmd = [_OBJDUMP, '-d', path]
  out = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
  got32 = '[^j]*jmp\s+\*0x(\S+)'
  got64 = '[^#]*#\s+(\S+)'
  lines = re.findall('([a-fA-F0-9]+)\s+<([^@<]+)@plt>:(%s|%s)' % (got32, got64), out)

  for addr, name, _, gotaddr32, gotaddr64 in lines:
     addr = int(addr, 16)

     try:
       gotaddr = int(gotaddr32 or gotaddr64, 16)
     except ValueError:
       gotaddr = None

     plt[name] = addr
     got[name] = gotaddr

  return plt, got

class ELF:
  '''A parsed ELF file'''

  def __init__(self, path):
    self.path = str(path)
    self.plt, self.got = plt_got(self.path)
    self.name2addr = self.plt
    self.addr2name = dict()

    for (name, addr) in self.name2addr.items():
      self.addr2name[addr] = name

    for (x,y) in self.addr2name.items():
      print hex(x),y

    self.name2func = self.got
    self.func2name = dict()

    for (name, addr) in self.name2func.items():
      self.func2name[addr] = name

  def GetFunctions(self):
    return self.name2func.keys()

  def FindFuncInPlt(self, name):

    if name in self.name2addr:
      return self.name2addr[name]
    else:
      return None

  def FindAddrInPlt(self, addr):
    #print addr
    if not isinstance(addr, int):
      addr = int(str(addr), 16)

    if addr in self.addr2name:
      return self.addr2name[addr]
    else:
      return None

  def FindFuncInGot(self, name):

    if name in self.name2addr:
      return self.name2func[name]
    else:
      return None

  def FindAddrInGot(self, addr):
    #print addr
    if addr in self.addr2name:
      return self.func2name[addr]
    else:
      return None
