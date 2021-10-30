from collections import deque
from enum import Enum
from os import stat

import expressions
import statements

class FunctionType(Enum):
  NONE = 1
  FUNCTION = 2
  METHOD = 3
  INITIALIZER = 4

class ClassType(Enum):
  NONE = 1
  CLASS = 2

class Resolver(expressions.ExprVisitor, statements.StmtVisitor):
  def __init__(self, interpreter):
    self.interpreter = interpreter
    self.scopes = deque()
    self.currentFunction = FunctionType.NONE
    self.currentClass = ClassType.NONE

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

    self.resolveStatements(function.body)
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

    if (self.currentFunction == FunctionType.INITIALIZER):
      RuntimeError(f"{stmt.keyword} Can't return a value from an initializer.")

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

  def visitGetExpr(self, expr: expressions.Expr):
    self.resolveExpression(expr.obj)

  def visitSetExpr(self, expr: expressions.Set):
    self.resolveExpression(expr.value)
    self.resolveExpression(expr.obj)

    return None

  def visitSuperExpr(self, expr: 'expressions.Expr'):
    pass

  def visitThisExpr(self, expr: expressions.This):
    if (self.currentClass == ClassType.NONE):
      RuntimeError(expr.keyword, "Can't use 'this' outside of a class.")

    self.resolveLocal(expr, expr.keyword)
    return None

  def visitClassStmt(self, stmt: statements.Class):
    enclosingClass = self.currentClass
    self.currentClass = ClassType.CLASS

    self.declare(stmt.name)
    self.define(stmt.name)

    self.beginScope()
    self.scopes[-1]["this"] = True

    for method in stmt.methods:
      declaration = FunctionType.METHOD
      if (method.name.lexeme == "init"):
        declaration = FunctionType.INITIALIZER
      self.resolveFunction(method, declaration)

    self.endScope()

    self.currentClass = enclosingClass
    return None