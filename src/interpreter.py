from os import stat
from environment import Environment
import expressions
import statements
from tokenType import TokenType
from parserC import ParserError

class Interpreter(expressions.ExprVisitor, statements.StmtVisitor):
  def __init__(self):
    self.enviroment = Environment()

  def visitLiteralExpr(self, expr: expressions.Literal):
    return str(expr.value)

  def visitGroupingExpr(self, expr: expressions.Grouping):
      return self.evaluate(expr.expression)

  def evaluate(self, expr: expressions.Expr):
    return expr.accept(self)

  def visitUnaryExpr(self, expr: expressions.Unary):
    right = self.evaluate(expr.right)

    if (expr.operator.type == TokenType.MINUS):
      self.checkNumberOperand(expr.operator, right)
      return -float(right)
    elif (expr.operator.type == TokenType.BANG):
      return not self.isTruthy(right)
    
    return None

  def isTruthy(self, object):
    if (object == None):
      return False
    if (isinstance(object, bool)):
      return bool(object)
    
    return True

  def visitBinaryExpr(self, expr: expressions.Binary):
    left = self.evaluate(expr.left)
    right = self.evaluate(expr.right)
    
    if (expr.operator.type == TokenType.GREATER):
      self.checkNumberOperands(expr.operator, left, right)
      return float(left) > float(right)
    elif (expr.operator.type == TokenType.GREATER_EQUAL):
      self.checkNumberOperands(expr.operator, left, right)
      return float(left) >= float(right)
    elif (expr.operator.type == TokenType.LESS):
      self.checkNumberOperands(expr.operator, left, right)
      return float(left) < float(right)
    elif (expr.operator.type == TokenType.LESS_EQUAL):
      self.checkNumberOperands(expr.operator, left, right)
      return float(left) <= float(right)
    elif (expr.operator.type == TokenType.BANG_EQUAL):
      return not self.isEqual(left, right)
    elif (expr.operator.type == TokenType.EQUAL_EQUAL):
      return self.isEqual(left, right)

    elif (expr.operator.type == TokenType.MINUS):
      self.checkNumberOperands(expr.operator, left, right)
      return float(left) - float(right)
    elif (expr.operator.type == TokenType.PLUS):
      if (isinstance(left, float) and isinstance(right, float)):
        return float(left) + float(right)

      if (isinstance(left, str) and isinstance(right, str)):
        return float(left) + float(right)

      raise ParserError(expr.operator, "Operands must be two numbers or two strings.")
    elif (expr.operator.type == TokenType.SLASH):
      self.checkNumberOperands(expr.operator, left, right)
      return float(left) / float(right)
    elif (expr.operator.type == TokenType.STAR):
      self.checkNumberOperands(expr.operator, left, right)
      return float(left) * float(right)

    return None

  def isEqual(self, a, b):
    if (a == None and b == None):
      return True
    if (a == None):
      return False

    return a == b

  def checkNumberOperand(self, operator, operand):
    if (isinstance(operand, float)):
      return
    
    raise ParserError(operator, "Operand must be a number")
  
  def checkNumberOperands(self, operator, left, right):
    if (isinstance(left, float) and isinstance(right, float)):
      return
    if (isinstance(left, float) and isinstance(right, str)):
      try:
        float(right)
        return
      except:
        pass
    if (isinstance(left, str) and isinstance(right, float)):
      try:
        float(left)
        return
      except:
        pass
    if (isinstance(left, str) and isinstance(right, str)):
      try:
        float(left)
        float(right)
        return
      except:
        pass

    raise ParserError(operator, "Operand must be numbers")

  def interpret(self, statements):
    try:
      for statement in statements:
        self.execute(statement)
      # value = self.evaluate(expression)
      # print(self.stringify(value))
    except:
      raise RuntimeError("error")

  def execute(self, stmt: statements.Stmt):
    stmt.accept(self)

  def stringify(self, object):
    if (object == None):
      return "nil"

    if (isinstance(object, float)):
      text = str(object)

      if (text.endswith(".0")):
        text = text[0:len(text) - 2]
      
      return text

    return str(object)      

  def visitAssignExpr(self, expr: 'expressions.Expr'):
    pass

  def visitCallExpr(self, expr: 'expressions.Expr'):
    pass
  
  def visitGetExpr(self, expr: 'expressions.Expr'):
    pass

  def visitLogicalExpr(self, expr: 'expressions.Expr'):
    pass

  def visitSetExpr(self, expr: 'expressions.Expr'):
    pass

  def visitSuperExpr(self, expr: 'expressions.Expr'):
    pass

  def visitThisExpr(self, expr: 'expressions.Expr'):
    pass

  def visitVariableExpr(self, expr: expressions.Variable):
    return self.enviroment.get(expr.name)

  def visitVarStmt(self, stmt: statements.Var):
    value = None

    if (stmt.initializer != None):
      value = self.evaluate(stmt.initializer)
    
    self.enviroment.define(stmt.name.lexeme, value)
    return None

  def visitExpressionStmt(self, stmt: statements.Expression):
    self.evaluate(stmt.expression)
    return None

  def visitPrintStmt(self, stmt: statements.Print):
    value = self.evaluate(stmt.expression)
    print(self.stringify(value))
    return None

