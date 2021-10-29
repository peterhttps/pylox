from os import environ
from parserC import ParserError

class Environment:
  def __init__(self, enclosing=None):
    self.values = {}
    self.enclosing = enclosing

  def define(self, name, value):
    self.values[name] = value

  def get(self, name):
    if (name.lexeme in self.values):
      return self.values.get(name.lexeme)

    if (self.enclosing != None):
      return self.enclosing.get(name)

    raise ParserError(name, f"Undefined variable {name.lexeme}.")

  def assign(self, name, value):
    if (name.lexeme in self.values):
      self.values[name.lexeme] = value
      return

    if (self.enclosing != None):
      self.enclosing.assign(name, value)
      return

    raise ParserError(name, f"Undefined variable {name.lexeme}.")

  def getAt(self, distance, name):
    return self.ancestor(distance).values.get(name)

  def assignAt(self, distance, name, value):
    self.ancestor(distance).values[name.lexeme] = value

  def ancestor(self, distance):
    environment = self

    for i in range(0, distance):
      environment = environment.enclosing

    return environment

  
    
  