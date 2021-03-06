

from loxCallable import LoxCallable
from loxInstance import LoxInstance


class LoxClass(LoxCallable):
  def __init__(self, name, superclass, methods):
    self.name = name
    self.methods = methods
    self.superclass = superclass

  def toString(self):
    return self.name

  def call(self, interpreter, arguments):
    instance = LoxInstance(self)
    initializer = self.findMethod("init")
    if (initializer != None):
      initializer.bind(instance).call(interpreter, arguments)

    return instance


  def findMethod(self, name):
    if (name in self.methods):
      return self.methods.get(name)

    if (self.superclass != None):
      return self.superclass.findMethod(name)

    return None

  def arity(self):
    initializer = self.findMethod("init")
    if (initializer != None):
      return initializer.arity()
    return 0