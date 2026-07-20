import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from callable.darijaCallable import DarijaCallable
from callable.darijaFunction import DarijaFunction
from callable.darijaClass import DarijaClass
from callable.darijaInstance import DarijaInstance
from errors.return_exception import ReturnException

from parser.expressions import Expr_Visitor
from parser.statements import Stmt_Visitor
from errors.runtimeError import RuntimeError
from lexer.token_t import Token
from lexer.token_type import TokenType
from parser.environment import Environment


class Interpreter(Expr_Visitor, Stmt_Visitor):
    
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals
        self.hadRuntimeError = False
        
    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as error:
            print(error)
            self.hadRuntimeError = True

    def execute(self, stmt):
        stmt.accept(self)
    
    def visitBlock(self, stmt):
        self.executeBlock(stmt.statements, Environment(self.environment))
        return None
        
    def executeBlock(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous
    
    def visitAssign(self, expr):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value
        
    def visitVar(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        
        self.environment.add(stmt.name, value)
        return None
    
    def visitVariableExpr(self, expr):
        return self.environment.get(expr.content)
    
    def visitExpression(self, stmt):
        self.evaluate(stmt.expression)
        return None
    
    def evaluate(self, expr):
        return expr.accept(self)
    
    def stringify(self, value):
        if value is None:
            return "nil"
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, float):
            text = str(value)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        return str(value)
    
    def checkNumberOperand(self, operator, operand):
        if isinstance(operand, (int, float)):
            return
        raise RuntimeError("Operand must be a number.", operator)

    def checkNumberOperands(self, operator, left, right):
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return
        raise RuntimeError("Operands must be numbers.", operator)
    
    def visitPrint(self, stmt):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None
    
    def visitLogical(self, expr):
        left = self.evaluate(expr.left)
        
        if expr.operator.type == TokenType.OR:
            if self.isTruthy(left):
                return left
        else:
            if not self.isTruthy(left):
                return left
        
        return self.evaluate(expr.right)
    
    def visitIfStmt(self, stmt):
        if self.isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch is not None:
            self.execute(stmt.elseBranch)
        return None

    def visitWhileStmt(self, stmt):
        while self.isTruthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        return None
    
    def visitFunction(self, stmt):
        function = DarijaFunction(stmt, self.environment, is_initializer=False)
        self.environment.add(stmt.name, function)
        return None

    def visitReturnStmt(self, stmt):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        raise ReturnException(value)

    def visitClassStmt(self, stmt):
        superclass = None
        if stmt.superclass is not None:
            superclass = self.evaluate(stmt.superclass)
            if not isinstance(superclass, DarijaClass):
                raise RuntimeError("Superclass must be a class.", stmt.superclass.content)

        self.environment.add(stmt.name, None)

        if stmt.superclass is not None:
            self.environment = Environment(self.environment)
            waled_token = Token(TokenType.SUPER, "waled", None, 0)
            self.environment.add(waled_token, superclass)

        methods = {}
        for method in stmt.methods:
            is_initializer = method.name.lexeme == "init"
            function = DarijaFunction(method, self.environment, is_initializer)
            methods[method.name.lexeme] = function

        klass = DarijaClass(stmt.name.lexeme, superclass, methods)

        if superclass is not None:
            self.environment = self.environment.enclosing

        self.environment.assign(stmt.name, klass)
        return None

    def visitCall(self, expr):
        callee = self.evaluate(expr.callee)
        
        arguments = []
        for argument in expr.args:
            arguments.append(self.evaluate(argument))
        
        if not isinstance(callee, DarijaCallable):
            raise RuntimeError("Can only call functions and classes.", expr.paren)
        
        if len(arguments) != callee.arity():
            raise RuntimeError(f"Expected {callee.arity()} arguments but got {len(arguments)}.", expr.paren)
        
        return callee.call(self, arguments)

    def visitGet(self, expr):
        obj = self.evaluate(expr.object)
        if isinstance(obj, DarijaInstance):
            return obj.get(expr.name)
        raise RuntimeError("Only instances have properties.", expr.name)

    def visitSet(self, expr):
        obj = self.evaluate(expr.object)
        if not isinstance(obj, DarijaInstance):
            raise RuntimeError("Only instances have fields.", expr.name)
        value = self.evaluate(expr.value)
        obj.set(expr.name, value)
        return value

    def visitThis(self, expr):
        return self.environment.get(expr.keyword)

    def visitSuper(self, expr):
        waled_token = Token(TokenType.SUPER, "waled", None, 0)
        superclass = self.environment.get(waled_token)
        
        ana_token = Token(TokenType.THIS, "ana", None, 0)
        instance = self.environment.get(ana_token)
        
        method = superclass.findMethod(expr.method.lexeme)
        if method is None:
            raise RuntimeError(f"Undefined property '{expr.method.lexeme}'.", expr.method)
        return method.bind(instance)

    def visitLiteral(self, exp):
        return exp.value

    def visitUnary(self, exp):
        right = exp.right.accept(self)
        
        if exp.operator.type == TokenType.MINUS:
            self.checkNumberOperand(exp.operator, right)
            return -right
        elif exp.operator.type == TokenType.BANG:
            return not self.isTruthy(right)
        return None
        
    def visitBinary(self, exp):
        left = exp.left.accept(self)
        right = exp.right.accept(self)
        
        if exp.operator.type == TokenType.PLUS:
            if isinstance(left, str) and isinstance(right, str): 
                return left + right
            elif isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left + right
            else:
                raise RuntimeError("Operands must be two numbers or two strings.", exp.operator)
            
        elif exp.operator.type == TokenType.MINUS:
            self.checkNumberOperands(exp.operator, left, right)
            return left - right
        elif exp.operator.type == TokenType.STAR:
            self.checkNumberOperands(exp.operator, left, right)
            return left * right
        elif exp.operator.type == TokenType.SLASH:
            self.checkNumberOperands(exp.operator, left, right)
            if right == 0:
                raise RuntimeError("Division by zero.", exp.operator)
            return left / right
        elif exp.operator.type == TokenType.GREATER:
            self.checkNumberOperands(exp.operator, left, right)
            return left > right
        elif exp.operator.type == TokenType.GREATER_EQUAL:
            self.checkNumberOperands(exp.operator, left, right)
            return left >= right
        elif exp.operator.type == TokenType.LESS:
            self.checkNumberOperands(exp.operator, left, right)
            return left < right
        elif exp.operator.type == TokenType.LESS_EQUAL:
            self.checkNumberOperands(exp.operator, left, right)
            return left <= right
        elif exp.operator.type == TokenType.EQUAL_EQUAL:
            return left == right
        elif exp.operator.type == TokenType.BANG_EQUAL:
            return left != right
        return None
        
    def visitGrouping(self, exp):
        return exp.expression.accept(self)
    
    def isTruthy(self, value):
        if value is None: 
            return False
        if isinstance(value, bool): 
            return value
        return True