import expressions

class AstPrinter(expressions.ExprVisitor):
    def print(self, expr: expressions.Expr):
        return expr.accept(self)

    def parenthesize(self, name: str, *exprs: expressions.Expr):
        content = ' '.join(expr.accept(self) for expr in exprs)

        return f'({name} {content})'

    def visitAssignExpr(self, expr: expressions.Assign):
        return self.parenthesize('=', expr.name.lexeme, expr.value)

    def visitBinaryExpr(self, expr: expressions.Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitCallExpr(self, expr: expressions.Call):
        return self.parenthesize('call', expr.callee, expr.arguments)

    def visitGetExpr(self, expr: expressions.Get):
        return self.parenthesize('.', expr.obj, expr.name.lexeme)

    def visitGroupingExpr(self, expr: expressions.Grouping):
        return self.parenthesize('group', expr.expression)

    def visitLiteralExpr(self, expr: expressions.Literal):
        return str(expr.value)

    def visitLogicalExpr(self, expr: expressions.Logical):
        name = f'logical {expr.operator.lexeme}'
        return self.parenthesize(name, expr.left, expr.right)

    def visitThisExpr(self, expr: expressions.This):
        return 'this'

    def visitSetExpr(self, expr: expressions.Set):
        return self.parenthesize('=', expr.obj, expr.name.lexeme, expr.value)

    def visitSuperExpr(self, expr: expressions.Super):
        return self.parenthesize('super', expr.method)

    def visitUnaryExpr(self, expr: expressions.Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def visitVariableExpr(self, expr: expressions.Variable):
        return expr.name.lexeme
