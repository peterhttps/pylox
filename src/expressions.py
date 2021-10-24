from abc import ABC, abstractmethod
from typing import Any, List
from tokenC import TokenC

class ExprVisitor(ABC):
    @abstractmethod
    def visitAssignExpr(self, expr: 'Expr'):
        pass
    
    @abstractmethod
    def visitBinaryExpr(self, expr: 'Expr'):
        pass

    @abstractmethod
    def visitCallExpr(self, expr: 'Expr'):
        pass

    @abstractmethod
    def visitGetExpr(self, expr: 'Expr'):
        pass

    @abstractmethod
    def visitGroupingExpr(self, expr: 'Expr'):
        pass

    @abstractmethod
    def visitLiteralExpr(self, expr: 'Expr'):
        pass

    @abstractmethod
    def visitLogicalExpr(self, expr: 'Expr'):
        pass

    @abstractmethod
    def visitSetExpr(self, expr: 'Expr'):
        pass

    @abstractmethod
    def visitSuperExpr(self, expr: 'Expr'):
        pass

    @abstractmethod
    def visitThisExpr(self, expr: 'Expr'):
        pass

    @abstractmethod
    def visitUnaryExpr(self, expr: 'Expr'):
        pass

    @abstractmethod
    def visitVariableExpr(self, expr: 'Expr'):
        pass


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: ExprVisitor):
        pass


class Assign(Expr):
    def __init__(self, name: TokenC, value: Expr):
        self.name = name
        self.value = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visitAssignExpr(self)


class Binary(Expr):
    def __init__(self, left: Expr, operator: TokenC, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visitBinaryExpr(self)


class Call(Expr):
    def __init__(self, callee: Expr, paren: TokenC, arguments: List[Expr]):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor: ExprVisitor):
        return visitor.visitCallExpr(self)


class Get(Expr):
    def __init__(self, obj: Expr, name: TokenC):
        self.obj = obj
        self.name = name

    def accept(self, visitor: ExprVisitor):
        return visitor.visitGetExpr(self)


class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: ExprVisitor):
        return visitor.visitGroupingExpr(self)


class Literal(Expr):
    def __init__(self, value: Any):
        self.value = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visitLiteralExpr(self)


class Logical(Expr):
    def __init__(self, left: Expr, operator: TokenC, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visitLogicalExpr(self)


class Set(Expr):
    def __init__(self, obj: Expr, name: TokenC, value: Expr):
        self.obj = obj
        self.name = name
        self.value = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visitSetExpr(self)


class Super(Expr):
    def __init__(self, keyword: TokenC, method: TokenC):
        self.keyword = keyword
        self.method = method

    def accept(self, visitor: ExprVisitor):
        return visitor.visitSuperExpr(self)


class This(Expr):
    def __init__(self, keyword: TokenC):
        self.keyword = keyword

    def accept(self, visitor: ExprVisitor):
        return visitor.visitThisExpr(self)


class Unary(Expr):
    def __init__(self, operator: TokenC, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visitUnaryExpr(self)


class Variable(Expr):
    def __init__(self, name: TokenC):
        self.name = name

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_variable_expr(self)