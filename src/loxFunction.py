from loxCallable import LoxCallable
from environment import Environment
from returnException import ReturnException

class LoxFunction(LoxCallable):
  def __init__(self, declaration):
    self.declaration = declaration

  def call(self, interpreter, arguments):
    environment = Environment(interpreter.globals)

    for i in range(0, len(self.declaration.params)):
      environment.define(self.declaration.params[i].lexeme, arguments[i])

    try:
      interpreter.executeBlock(self.declaration.body, environment)
    except ReturnException as returnC:
      return returnC.value

    return None

  def arity(self):
    return len(self.declaration.params)

  def toString(self):
    return f"<fn {self.declaration.name.lexeme} >"