

class LoxInstance():
  def __init__(self, klass):
    self.klass = klass
    self.fields = {}

  def toString(self):
    return f"{self.klass.name} instance" 

  def get(self, name):
    if (name.lexeme in self.fields):
      return self.fields.get(name.lexeme)

    method = self.klass.findMethod(name.lexeme)
    if (method != None):
      return method.bind(self)
    
    raise RuntimeError(name, f"Undefined property {name.lexeme}.")

  def set(self, name, value):
    self.fields[name.lexeme] = value
