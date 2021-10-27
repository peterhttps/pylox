from loxCallable import LoxCallable
import time

class Clock(LoxCallable):
  def call(self, interpreter, arguments):
    return time.time()

  def arity(self):
    return 0