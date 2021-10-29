from os import stat
from clock import Clock
from environment import Environment
import expressions
from loxCallable import LoxCallable
from loxFunction import LoxFunction
from returnException import ReturnException
import statements
from tokenType import TokenType
from parserC import ParserError

class Interpreter(expressions.ExprVisitor, statements.StmtVisitor):
  def __init__(self):
    self.globals = Environment()
    self.environment = self.globals
    self.locals = {}

    self.globals.define("clock", Clock())

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
        try:
          leftFloat = float(left)
          rightFloat = float(right)
          return leftFloat + rightFloat
        except:
          return str(left) + str(right)

      if (isinstance(left, str) and isinstance(right, float)):
        return float(left) + float(right)

      if (isinstance(left, float) and isinstance(right, str)):
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
    except:
      raise RuntimeError("error")

  def execute(self, stmt: statements.Stmt):
    stmt.accept(self)

  def resolve(self, expr, depth):
    self.locals[expr] = depth

  def stringify(self, object):
    if (object == None):
      return "nil"

    if (isinstance(object, float)):
      text = str(object)

      if (text.endswith(".0")):
        text = text[0:len(text) - 2]
      
      return text

    return str(object)     

  def executeBlock(self, statements, environment):
    previous = self.environment

    try:
      self.environment = environment
      for statement in statements:
        self.execute(statement)
    finally:
      self.environment = previous

  def visitAssignExpr(self, expr: expressions.Assign):
    value = self.evaluate(expr.value)

    distance = self.locals.get(expr)

    if (distance != None):
      self.environment.assignAt(distance, expr.name, value)
    else:
      self.globals.assign(expr.name, value)

    return value
  
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
    return self.lookUpVariable(expr.name, expr)

  def lookUpVariable(self, name, expr):
    distance = self.locals.get(expr)

    if (distance != None):
      return self.environment.getAt(distance, name.lexeme)
    else:
      return self.globals.get(name)

  def visitVarStmt(self, stmt: statements.Var):
    value = None

    if (stmt.initializer != None):
      value = self.evaluate(stmt.initializer)
    
    self.environment.define(stmt.name.lexeme, value)
    return None

  def visitExpressionStmt(self, stmt: statements.Expression):
    self.evaluate(stmt.expression)
    return None

  def visitPrintStmt(self, stmt: statements.Print):
    value = self.evaluate(stmt.expression)
    print(self.stringify(value))
    return None

  def visitBlockStmt(self, stmt: statements.Block):
    self.executeBlock(stmt.statements, Environment(self.environment))

  def visitIfStmt(self, stmt: statements.If):

    if (self.isTruthy(self.evaluate(stmt.condition))):
      self.execute(stmt.thenBranch)
    elif (stmt.elseBranch != None) :
      self.execute(stmt.elseBranch)

    return None

  def visitLogicalExpr(self, expr: expressions.Logical):
    left = self.evaluate(expr.left)

    if (expr.operator.type == TokenType.OR):
      if (self.isTruthy(left)):
        return left
      else:
        if (not self.isTruthy(left)):
          return left
        
    return self.evaluate(expr.right)

  def visitWhileStmt(self, stmt: statements.While):
    while (self.isTruthy(self.evaluate(stmt.condition))):
      self.execute(stmt.body)
    
    return None

  def visitCallExpr(self, expr: expressions.Call):
    function = self.evaluate(expr.callee)

    arguments = []

    for argument in expr.arguments:
      arguments.append(self.evaluate(argument)) 

    if (not isinstance(function, LoxCallable)):
      raise RuntimeError("Can only call functions and classes.")

    # function: LoxCallable = callee

    if (len(arguments) != function.arity()):
      raise RuntimeError(f"Expected {function.arity()} arguments but got {arguments.size}.")

    return function.call(self, arguments)

  def visitFunctionStmt(self, stmt: statements.Function):
    function = LoxFunction(stmt, self.environment)

    self.environment.define(stmt.name.lexeme, function)
    return None

  def visitReturnStmt(self, stmt: statements.Return):
    value = None

    if (stmt.value != None):
      value = self.evaluate(stmt.value)

    raise ReturnException(value)