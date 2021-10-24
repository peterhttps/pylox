import expressions
from tokenType import TokenType

class ParserError(RuntimeError):
  def __init__(self, token, message):
    super().__init__(message)
    self.token = token

class ParserC:
  def __init__(self, tokens):
    self.tokens = tokens
    self.current = 0

  def expression(self):
    return self.equality()

  def equality(self):
    expr = self.comparison()

    while (self.match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL])):
      operator = self.previous()
      right = self.comparison()
      expr = expressions.Binary(expr, operator, right)
    
    return expr

  def match(self, types):
    for type in types:
      if (self.check(type)):
        self.advance()
        return True
      
    return False
  
  def check(self, type):
    if (self.isAtEnd()):
      return False
    
    return self.peek().type == type

  def advance(self):
    if (not self.isAtEnd()):
      self.current += 1
    
    return self.previous()
  
  def isAtEnd(self):
    return self.peek().type == TokenType.EOF
  
  def peek(self):
    return self.tokens[self.current]
  
  def previous(self):
    return self.tokens[self.current - 1]

  def comparison(self):
    expr = self.term()

    while (self.match([TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL])):
      operator = self.previous()
      right = self.term()
      expr = expressions.Binary(expr, operator, right)
    
    return expr

  def term(self):
    expr = self.factor()

    while (self.match([TokenType.MINUS, TokenType.PLUS])):
      operator = self.previous()
      right = self.factor()
      expr = expressions.Binary(expr, operator, right)
    
    return expr

  def factor(self):
    expr = self.unary()

    while (self.match([TokenType.SLASH, TokenType.STAR])):
      operator = self.previous()
      right = self.unary()
      expr = expressions.Binary(expr, operator, right)
    
    return expr

  def unary(self):
    if (self.match([TokenType.BANG, TokenType.MINUS])):
      operator = self.previous()
      right = self.unary()
      return expressions.Unary(operator, right)

    return self.primary()

  def primary(self):
    if (self.match([TokenType.FALSE])):
      return expressions.Literal(False)
    if (self.match([TokenType.TRUE])):
      return expressions.Literal(True)
    if (self.match([TokenType.NIL])):
      return expressions.Literal(None)

    if (self.match([TokenType.NUMBER, TokenType.STRING])):
      return expressions.Literal(self.previous().literal)

    if (self.match([TokenType.LEFT_PAREN])):
      expr = self.expression()
      self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression")
      return expressions.Grouping(expr)

    raise self.error(self.peek(), "Expected expression.")

  def consume(self, type, message):
    if (self.check(type)):
      return self.advance()

    raise self.error(self.peek(), message)

  def error(self, token, message):
    return ParserError(token, message)
      
  def synchronize(self):
    self.advance()

    while (not self.isAtEnd()):
      if (self.previous().type == TokenType.SEMICOLON):
        return
      
      if (self.peek().type == TokenType.CLASS):
        return
      elif (self.peek().type == TokenType.FUN):
        return
      elif (self.peek().type == TokenType.VAR):
        return
      elif (self.peek().type == TokenType.FOR):
        return
      elif (self.peek().type == TokenType.IF):
        return
      elif (self.peek().type == TokenType.WHILE):
        return
      elif (self.peek().type == TokenType.PRINT):
        return
      elif (self.peek().type == TokenType.RETURN):
        return
      
      self.advance()
  
  def parse(self):
    try:
      return self.expression()
    except:
      return None