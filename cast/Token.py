from cast.cParser import Parser as cParser
from cast.ppParser import Parser as ppParser

class Token:
  def __init__(self, id, resource, terminal_str, source_string, lineno, colno):
    self.__dict__.update(locals())
  
  def getString(self):
    return self.source_string
  
  def getLine(self):
    return self.lineno
  
  def getColumn(self):
    return self.colno

  def getId(self):
    return self.id

  def getTerminalStr(self):
    return self.terminal_str

  def getResource(self):
    return self.resource

  def toAst(self):
    return self
  
  def __str__( self ):
    #return "'%s'" % (self.source_string)
    #return "'%s'" % (self.terminal_str.lower())
    #return '\033[1;34m<%s (%s) %d,%d>\033[0m' % ( self.terminal_str.lower(), self.source_string, self.lineno, self.colno )
    return '[%s:%d] %s (%s) [line %d, col %d]' % ( self.type, self.id, self.terminal_str.lower(), self.source_string, self.lineno, self.colno )
    return '%s (%s)' % ( self.terminal_str.lower(), self.source_string )

  def toString( self, format = 'long' ):
    if format == 'tiny':
      return self.getString()
    elif format == 'terminal':
      return self.getTerminalStr()
    elif format == 'short':
      if len(self.getString()):
        return "%s ('%s')" % ( self.getTerminalStr(), self.getString() )
      else:
        return "%s" % ( self.getTerminalStr() )
    else:
      return '[%s:%d] %s (%s) [line %d, col %d]' % ( self.type, self.id, self.terminal_str.lower(), self.source_string, self.lineno, self.colno )

class ppToken(Token):
  type = 'pp'

# TODO: this takes ridiculous parameters.
# 1) should be able to imply terminal_str from id
# 2) lineno, colno, context should all be one Context object
class cToken(Token):
  type = 'c'
  fromPreprocessor = False

  def __init__(self, id, resource, terminal_str, source_string, lineno, colno, context):
    super().__init__(id, resource, terminal_str, source_string, lineno, colno)
    self.context = context

class TokenList(list):
  def __init__(self, arg1=[]):
    super().__init__(arg1)
    self.isIter = False
  def __iter__(self):
    if self.isIter == False:
      self.index = 0
      isIter = True
    return self
  def __next__(self):
    try:
      rval = self[self.index]
      self.index += 1
      return rval
    except:
      raise StopIteration
  def reset(self):
    self.isIter = False
  def peek(self, whereto):
    try:
      return self[self.index + int(whereto)]
    except:
      return None
  def go(self, whereto):
    whereto = int(whereto)
    if self.index + whereto < 0 or self.index + whereto + 1 > len(self):
      raise Exception()
    self.index += whereto
    return self
  def check(self, whereto, ids):
    try:
      return self[self.index + int(whereto) - 1].id in ids
    except:
      return False
  def toString(self):
    class Cursor:
      def __init__(self):
        self.string = ''
        self.lineno = 1
        self.colno = 1
        c = lambda x: cParser.terminals[x]
        self.insertSpaceAfter = {
          c('else')
        }
      def add(self, token):
        if token.lineno > self.lineno:
          self.string += ''.join('\n' for i in range(token.lineno - self.lineno))
          self.lineno = token.lineno
          self.colno = 1
        if token.colno > self.colno:
          self.string += ''.join(' ' for i in range(token.colno - self.colno))
          self.colno = token.colno
        self.string += token.source_string
        if token.fromPreprocessor or token.id in self.insertSpaceAfter:
          self.string += ' '
        self.colno += len(token.source_string)
      def __str__(self):
        return self.string
    cursor = Cursor()
    for token in self:
      cursor.add( token )
    return str(cursor)
