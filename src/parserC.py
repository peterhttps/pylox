from os import stat
import expressions
import statements
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
    return self.assignment()

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

    return self.call()

  def finishCall(self, callee):
    arguments = []

    if (not self.check(TokenType.RIGHT_PAREN)):
      arguments.append(self.expression())
      while (self.match([TokenType.COMMA])):
        if (len(arguments) >= 255):
          self.error(self.peek(), "Can't have more than 255 arguments.")

        arguments.append(self.expression())

    paren = self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")

    return expressions.Call(callee, paren, arguments)

  def call(self):
    expr = self.primary()

    while True:
      if (self.match([TokenType.LEFT_PAREN])):
        expr = self.finishCall(expr)
      elif (self.match([TokenType.DOT])):
        name = self.consume(TokenType.IDENTIFIER, "Expect property name after '.'.")
        expr = expressions.Get(expr, name)
      else:
        break

    return expr

  def primary(self):
    if (self.match([TokenType.FALSE])):
      return expressions.Literal(False)
    if (self.match([TokenType.TRUE])):
      return expressions.Literal(True)
    if (self.match([TokenType.NIL])):
      return expressions.Literal(None)
    if (self.match([TokenType.NUMBER, TokenType.STRING])):
      return expressions.Literal(self.previous().literal)
    if (self.match([TokenType.THIS])):
      return expressions.This(self.previous())
    if (self.match([TokenType.IDENTIFIER])):
      return expressions.Variable(self.previous())
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
    statements = []

    while (not self.isAtEnd()):
      statements.append(self.declaration())

    return statements

  def declaration(self):
    try:
      if (self.match([TokenType.CLASS])):
        return self.classDeclaration()
      if (self.match([TokenType.FUN])):
        return self.function("function")
      if (self.match([TokenType.VAR])):
        return self.varDeclaration()
      
      return self.statement()
    except:
      self.synchronize()
      return None

  def classDeclaration(self):
    name = self.consume(TokenType.IDENTIFIER, "Expect class name.")
    self.consume(TokenType.LEFT_BRACE, "Expect '{' before class body.")

    methods = []

    while (not self.check(TokenType.RIGHT_BRACE) and not self.isAtEnd()):
      methods.append(self.function("method"))

    self.consume(TokenType.RIGHT_BRACE, "Expect '}' after class body.")

    return statements.Class(name, methods)

  def statement(self):
    if (self.match([TokenType.FOR])):
      return self.forStatement()

    if (self.match([TokenType.IF])):
      return self.ifStatement()

    if (self.match([TokenType.PRINT])):
      return self.printStatement()
    
    if (self.match([TokenType.RETURN])):
      return self.returnStatement()
    
    if (self.match([TokenType.WHILE])):
      return self.whileStatement()
    
    if (self.match([TokenType.LEFT_BRACE])):
      return statements.Block(self.block())

    return self.expressionStatement()

  def forStatement(self):
    self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")

    initializer = None
    if (self.match([TokenType.SEMICOLON])):
      initializer = None
    elif (self.match([TokenType.VAR])):
      initializer = self.varDeclaration()
    else:
      initializer = self.expressionStatement()

    condition = None
    if (not self.check(TokenType.SEMICOLON)):    
      condition = self.expression()

    self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

    increment = None
    if (not self.check(TokenType.RIGHT_PAREN)):    
      increment = self.expression()

    self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")
    body = self.statement()

    if (increment != None):
      body = statements.Block([body, statements.Expression(increment)])

    if (condition == None):
      condition = expressions.Literal(True)

    body = statements.While(condition, body)

    if (initializer != None):
      body = statements.Block([initializer, body])

    return body

  def ifStatement(self):
    self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
    condition = self.expression()
    self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

    thenBranch = self.statement()
    elseBranch = None

    if (self.match([TokenType.ELSE])):
      elseBranch = self.statement()

    return statements.If(condition, thenBranch, elseBranch)

  def printStatement(self):
    value = self.expression()
    self.consume(TokenType.SEMICOLON, "Expect ';' after value.")

    return statements.Print(value)

  def returnStatement(self):
    keyword = self.previous()
    value = None

    if (not self.check(TokenType.SEMICOLON)):
      value = self.expression()

    self.consume(TokenType.SEMICOLON, "Expect ';' after return value.")

    return statements.Return(keyword, value)

  def whileStatement(self):
    self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
    condition = self.expression()
    self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
    body = self.statement()

    return statements.While(condition, body)

  def block(self):
    statements = []

    while ((not self.check(TokenType.RIGHT_BRACE)) and (not self.isAtEnd())):
      statements.append(self.declaration())

    self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")

    return statements

  def varDeclaration(self):
    name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")

    initializer = None
    if (self.match([TokenType.EQUAL])):
      initializer = self.expression()

    self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration")
    return statements.Var(name, initializer)

  def expressionStatement(self):
    expr = self.expression()

    self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")

    return statements.Expression(expr)

  def function(self, kind):
    name = self.consume(TokenType.IDENTIFIER, f"Expect {kind} name.")
    self.consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")
    parameters = []

    if (not self.check(TokenType.RIGHT_PAREN)):
      while True:
        if (len(parameters) >= 255):
          self.error(self.peek(), "Can't have more than 255 parameters.")

        parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name."))

        if (not self.match([TokenType.COMMA])):
          break
    
    self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")
    self.consume(TokenType.LEFT_BRACE, "Expect '{' before {kind} body.")
    body = self.block()

    return statements.Function(name, parameters, body)

  def assignment(self):
    expr = self.orOp()

    if (self.match([TokenType.EQUAL])):
      equals = self.previous()
      value = self.assignment()

      if (isinstance(expr, expressions.Variable)):
        name = expr.name
        return expressions.Assign(name, value)
      elif (isinstance(expr, expressions.Get)):
        get = expr
        return expressions.Set(get.obj, get.name, value)

      self.error(equals, "Invalid assignment target.")

    return expr

  def orOp(self):
    expr = self.andOp()

    while (self.match([TokenType.OR])):
      operator = self.previous()
      right = self.andOp()
      expr = expressions.Logical(expr, operator, right)

    return expr

  def andOp(self):
    expr = self.equality()

    while (self.match([TokenType.AND])):
      operator = self.previous()
      right = self.equality()
      expr = expressions.Logical(expr, operator, right)

    return expr
