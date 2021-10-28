from loxCallable import LoxCallable
from environment import Environment
from returnException import ReturnException

class LoxFunction(LoxCallable):
  def __init__(self, declaration, closure):
    self.declaration = declaration
    self.closure = closure

  def call(self, interpreter, arguments):
    environment = Environment(self.closure)

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