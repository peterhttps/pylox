

from runtimeError import RuntimeErrorC


class ReturnException(RuntimeErrorC):
  def __init__(self, value):
    super().__init__(None, None)
    self.value = value