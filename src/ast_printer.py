import expressions
from tokenC import TokenC
from tokenType import TokenType

class AstPrinter(expressions.ExprVisitor):
    def print(self, expr: expressions.Expr):
        return expr.accept(self)

    def parenthesize(self, name: str, *exprs: expressions.Expr):
        content = ' '.join(expr.accept(self) for expr in exprs)

        return f'({name} {content})'

    def visit_assign_expr(self, expr: expressions.Assign):
        return self.parenthesize('=', expr.name.lexeme, expr.value)

    def visit_binary_expr(self, expr: expressions.Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_call_expr(self, expr: expressions.Call):
        return self.parenthesize('call', expr.callee, expr.arguments)

    def visit_get_expr(self, expr: expressions.Get):
        return self.parenthesize('.', expr.obj, expr.name.lexeme)

    def visit_grouping_expr(self, expr: expressions.Grouping):
        return self.parenthesize('group', expr.expression)

    def visit_literal_expr(self, expr: expressions.Literal):
        return str(expr.value)

    def visit_logical_expr(self, expr: expressions.Logical):
        name = f'logical {expr.operator.lexeme}'
        return self.parenthesize(name, expr.left, expr.right)

    def visit_this_expr(self, expr: expressions.This):
        return 'this'

    def visit_set_expr(self, expr: expressions.Set):
        return self.parenthesize('=', expr.obj, expr.name.lexeme, expr.value)

    def visit_super_expr(self, expr: expressions.Super):
        return self.parenthesize('super', expr.method)

    def visit_unary_expr(self, expr: expressions.Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def visit_variable_expr(self, expr: expressions.Variable):
        return expr.name.lexeme
