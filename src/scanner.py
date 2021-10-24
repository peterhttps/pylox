from tokenC import *
from tokenType import TokenType

class Scanner:
  def __init__(self, source: str):
    self.source = source
    self.tokens = []
    self.start = 0
    self.current = 0
    self.line = 1
    self.keywords = {
      "and": TokenType.AND,
      "class": TokenType.CLASS,
      "else": TokenType.ELSE,
      "false": TokenType.FALSE,
      "for": TokenType.FOR,
      "fun": TokenType.FUN,
      "if": TokenType.IF,
      "nil": TokenType.NIL,
      "or": TokenType.OR,
      "print": TokenType.PRINT,
      "return": TokenType.RETURN,
      "super": TokenType.SUPER,
      "this": TokenType.THIS,
      "true": TokenType.TRUE,
      "var": TokenType.VAR,
      "while": TokenType.WHILE
    }

  def scanTokens(self):
    while (not self.isAtEnd()):
      self.start = self.current
      self.scanToken()
    
    token = TokenC(TokenType.EOF, "", "", self.line)
    self.tokens.append(token)
    return self.tokens

  def isAtEnd(self):
    return self.current >= len(self.source)

  def scanToken(self):
    c = self.advance()
    if (c == "("):
      self.addToken(TokenType.LEFT_PAREN)
    elif (c == ")"):
      self.addToken(TokenType.RIGHT_PAREN)
    elif (c == "{"):
      self.addToken(TokenType.LEFT_BRACE)
    elif (c == "}"):
      self.addToken(TokenType.RIGHT_BRACE)
    elif (c == ","):
      self.addToken(TokenType.COMMA)
    elif (c == "."):
      self.addToken(TokenType.DOT)
    elif (c == "-"):
      self.addToken(TokenType.MINUS)
    elif (c == "+"):
      self.addToken(TokenType.PLUS)
    elif (c == ";"):
      self.addToken(TokenType.SEMICOLON)
    elif (c == "*"):
      self.addToken(TokenType.STAR)
    elif (c == '!'):
      finalToken = TokenType.BANG_EQUAL

      if (not self.match("=")):
        finalToken = TokenType.BANG

      self.addToken(finalToken)
    elif (c == '='):
      finalToken = TokenType.EQUAL_EQUAL

      if (not self.match("=")):
        finalToken = TokenType.EQUAL

      self.addToken(finalToken)
    elif (c == '<'):
      finalToken = TokenType.LESS_EQUAL

      if (not self.match("=")):
        finalToken = TokenType.LESS

      self.addToken(finalToken)
    elif (c == '>'):
      finalToken = TokenType.GREATER_EQUAL

      if (not self.match("=")):
        finalToken = TokenType.GREATER

      self.addToken(finalToken)
    elif (c == '/'):
      if (self.match('/')):
        while (self.peek() != '\n' and (not self.isAtEnd())):
          self.advance()
      else:
        self.addToken(TokenType.SLASH)
    elif (c == " "):
      pass
    elif (c == "\r"):
      pass
    elif (c == "\t"):
      pass
    elif (c == '\n'):
      self.line += 1
    elif (c == '"'):
      self.string()
      pass
    else:
      if (self.isDigit(c)):
        self.number()
      elif (self.isAlpha(c)):
        self.identifier()
      else:
        raise SyntaxError(f"at {self.line} - Unexpected character.")

  def advance(self):
    self.current += 1
    return self.source[self.start:self.current]

  def addToken(self, type):
    self.addTokenFinal(type, "")

  def addTokenFinal(self, type, literal):
    text = self.source[self.start:self.current]

    token = TokenC(type, text, literal, self.line)
    self.tokens.append(token)

  def match(self, expected):
    if (self.isAtEnd()):
      return False
    if (self.source[self.current] != expected):
      return False
    
    self.current = self.current + 1
    return True
  
  def peek(self):
    if (self.isAtEnd()):
      return '\0'

    return self.source[self.current]

  def peekNext(self):
    if (self.current + 1 >= len(self.source)):
      return '\0'
    
    return self.source[self.current + 1]

  def isDigit(self, c):
    return c.isdigit()

  def isAlpha(self, c):
    return c.isalpha()

  def isAlphaNumeric(self, c):
    return c.isdigit() or c.isalpha()

  def identifier(self):
    while (self.isAlphaNumeric(self.peek())):
      self.advance()
    
    text = self.source[self.start:self.current]
    type = TokenType.IDENTIFIER
    if (text in self.keywords):
      type = self.keywords.get(text)

    self.addToken(type)
  
  def string(self):
    while (self.peek() != '"' and (not self.isAtEnd())):
      if (self.peek() == '\n'):
        self.line += 1
      self.advance()

    if (self.isAtEnd()):
      raise SyntaxError(f"at {self.line} - Unterminated string.")
      return
    
    self.advance()

    value = self.source[self.start + 1:self.current - 1]
    self.addTokenFinal(TokenType.STRING, value)

  def number(self):
    while (self.isDigit(self.peek())):
      self.advance()

    if (self.peek() == "." and self.isDigit(self.peekNext())):
      self.advance()
    
      while self.isDigit(self.peek()):
        self.advance()
    
    self.addTokenFinal(TokenType.NUMBER, float(self.source[self.start:self.current]))