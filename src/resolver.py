from collections import deque
from enum import Enum

import expressions
import statements

class FunctionType(Enum):
  # Single-character tokens.
  NONE = 1
  FUNCTION = 2

class Resolver(expressions.ExprVisitor, statements.StmtVisitor):
  def __init__(self, interpreter):
    self.interpreter = interpreter
    self.scopes = deque()
    self.currentFunction = FunctionType.NONE

  def resolve(self, statements):
    self.resolveStatements(statements)

  def resolveStatements(self, statements):
    for statement in statements:
      self.resolveStatement(statement)
  
  def resolveStatement(self, statement):
    statement.accept(self)

  def resolveExpression(self, expressions):
    expressions.accept(self)

  def visitBlockStmt(self, stmt: statements.Block):
    self.beginScope()
    self.resolve(stmt.statements)
    self.endScope()
    return None

  def beginScope(self):
    self.scopes.append({})

  def endScope(self):
    self.scopes.pop()

  def declare(self, name):
    if (len(self.scopes) == 0):
      return
    
    scope = self.scopes[-1]

    if (name.lexeme in scope):
      RuntimeError(f"{name} Already variable with this name in this scope.")

    scope[name.lexeme] = False

  def define(self, name):
    if (len(self.scopes) == 0):
      return

    scope = self.scopes[-1]
    scope[name.lexeme] = True

  def visitVarStmt(self, stmt: statements.Var):
    self.declare(stmt.name)

    if (stmt.initializer != None):
      self.resolveExpression(stmt.initializer)

    self.define(stmt.name)
    return None

  def visitVariableExpr(self, expr: expressions.Variable):
    if (len(self.scopes) != 0 and self.scopes[-1].get(expr.name.lexeme) == False):
      RuntimeError(f"{expr.name} Can't read local variable in its own initializer.")

    self.resolveLocal(expr, expr.name)
    return None

  def resolveLocal(self, expr, name):
    for i, s in enumerate(reversed(self.scopes)):
      if (name.lexeme in s):
        self.interpreter.resolve(expr, i)
        return 

  def visitAssignExpr(self, expr: expressions.Assign):
    self.resolveExpression(expr.value)
    self.resolveLocal(expr, expr.name)
    return None

  def visitFunctionStmt(self, stmt: statements.Function):
    self.declare(stmt.name)
    self.define(stmt.name)

    self.resolveFunction(stmt, FunctionType.FUNCTION)
    return None

  def resolveFunction(self, function: statements.Function, type):
    enclosingFunction = self.currentFunction
    self.currentFunction = type
    self.beginScope()

    for param in function.params:
      self.declare(param)
      self.define(param)

    self.resolve(function.body)
    self.endScope()

    self.currentFunction = enclosingFunction 

  def visitExpressionStmt(self, stmt: statements.Expression):
    self.resolveExpression(stmt.expression)
    return None

  def visitIfStmt(self, stmt: statements.If):
    self.resolveExpression(stmt.condition)
    self.resolveStatement(stmt.thenBranch)

    if (stmt.elseBranch != None):
      self.resolveStatement(stmt.elseBranch)

    return None

  def visitPrintStmt(self, stmt: statements.Print):
    self.resolveExpression(stmt.expression)
    return None

  def visitReturnStmt(self, stmt: statements.Return):
    if (self.currentFunction == FunctionType.NONE):
      RuntimeError(f"{stmt.keyword} Can't return from top-level code.")

    if (stmt.value != None):
      self.resolveExpression(stmt.value)

    return None

  def visitWhileStmt(self, stmt: statements.While):
    self.resolveExpression(stmt.condition)
    self.resolveStatement(stmt.body)

    return None

  def visitBinaryExpr(self, expr: expressions.Binary):
    self.resolveExpression(expr.left)
    self.resolveExpression(expr.right)

    return None

  def visitCallExpr(self, expr: expressions.Call):
    self.resolveExpression(expr.callee)
    
    for argument in expr.arguments:
      self.resolveExpression(argument)

    return None

  def visitGroupingExpr(self, expr: expressions.Grouping):
    self.resolveStatement(expr.expression)

    return None

  def visitLiteralExpr(self, expr: expressions.Literal):
    return None

  def visitLogicalExpr(self, expr: expressions.Logical):
    self.resolveExpression(expr.left)
    self.resolveExpression(expr.right)
    
    return None

  def visitUnaryExpr(self, expr: expressions.Unary):
    self.resolveExpression(expr.right)

    return None

  def visitGetExpr(self, expr: 'expressions.Expr'):
    pass

  def visitSetExpr(self, expr):
    pass

  def visitSuperExpr(self, expr: 'expressions.Expr'):
    pass

  def visitThisExpr(self, expr):
    pass