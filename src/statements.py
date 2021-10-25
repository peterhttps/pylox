from abc import ABC, abstractmethod

from expressions import Expr

class StmtVisitor(ABC):
    @abstractmethod
    def visitExpressionStmt(self, expr: 'Stmt'):
        pass

    @abstractmethod
    def visitPrintStmt(self, expr: 'Stmt'):
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