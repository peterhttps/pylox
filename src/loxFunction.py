from loxCallable import LoxCallable
from environment import Environment
from returnException import ReturnException

class LoxFunction(LoxCallable):
  def __init__(self, declaration, closure, isInitializer):
    self.declaration = declaration
    self.closure = closure
    self.isInitializer = isInitializer 

  def call(self, interpreter, arguments):
    environment = Environment(self.closure)

    for i in range(0, len(self.declaration.params)):
      environment.define(self.declaration.params[i].lexeme, arguments[i])

    try:
      interpreter.executeBlock(self.declaration.body, environment)
    except ReturnException as returnC:
      if (self.isInitializer):
        return self.closure.getAt(0, "this")
      return returnC.value

    if (self.isInitializer):
      return self.closure.getAt(0, "this")

    return None

  def arity(self):
    return len(self.declaration.params)

  def toString(self):
    return f"<fn {self.declaration.name.lexeme} >"
  
  def bind(self, instance):
    environment = Environment(self.closure)
    environment.define("this", instance)

    return LoxFunction(self.declaration, environment, self.isInitializer)