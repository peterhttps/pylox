from parserC import ParserError

class Environment:
  def __init__(self):
    self.values = {}

  def define(self, name, value):
    self.values[name] = value

  def get(self, name):
    if (name.lexeme in self.values):
      return self.values.get(name.lexeme)

    raise ParserError(name, f"Undefined variable {name.lexeme}.")

  