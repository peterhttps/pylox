
from abc import abstractmethod

from abc import ABC, abstractmethod

class LoxCallable:
  @abstractmethod
  def arity(self, interpreter, arguments):
    pass
  @abstractmethod
  def call(interpreter, arguments):
    pass