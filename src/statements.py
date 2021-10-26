from abc import ABC, abstractmethod

from expressions import Expr
from tokenC import TokenC

class StmtVisitor(ABC):
    @abstractmethod
    def visitExpressionStmt(self, expr: 'Stmt'):
        pass

    @abstractmethod
    def visitPrintStmt(self, expr: 'Stmt'):
        pass

    @abstractmethod
    def visitVarStmt(self, expr: 'Stmt'):
        pass
    
    @abstractmethod
    def visitBlockStmt(self, expr: 'Stmt'):
        pass


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: StmtVisitor):
        pass


class Expression(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor):
        return visitor.visitExpressionStmt(self)


class Print(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor):
        return visitor.visitPrintStmt(self)

class Var(Stmt):
    def __init__(self, name: TokenC, initializer):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: StmtVisitor):
        return visitor.visitVarStmt(self)

class Block(Stmt):
    def __init__(self, statements):
        self.statements = statements
    
    def accept(self, visitor: StmtVisitor):
        return visitor.visitBlockStmt(self)