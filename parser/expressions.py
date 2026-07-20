import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from abc import ABC, abstractmethod
from lexer.token_t import Token

class Expr_Visitor(ABC):
    
    @abstractmethod
    def visitLiteral(self, expr):
        pass
    
    @abstractmethod
    def visitBinary(self, expr):
        pass
        
    @abstractmethod
    def visitCall(self, expr):
        pass
        
    @abstractmethod
    def visitUnary(self, expr):
        pass
        
    @abstractmethod
    def visitGrouping(self, expr):
        pass

    @abstractmethod
    def visitVariableExpr(self, expr):
        pass

    @abstractmethod
    def visitAssign(self, expr):
        pass

    @abstractmethod
    def visitLogical(self, expr):
        pass

    @abstractmethod
    def visitGet(self, expr):
        pass

    @abstractmethod
    def visitSet(self, expr):
        pass

    @abstractmethod
    def visitThis(self, expr):
        pass

    @abstractmethod
    def visitSuper(self, expr):
        pass


class Exp(ABC):
    
    @abstractmethod
    def accept(self, visitor):
        pass


class AstPrinter(Expr_Visitor):
    
    def parenthesize(self, name, *exps):
        builder = f"({name}"
        for exp in exps: 
            builder += " "
            added = exp.accept(self)
            if added is not None: 
                builder += added
        builder += ")"
        return builder
    
    def print(self, exp):
        return exp.accept(self)
    
    def visitLiteral(self, exp):
        if exp.value is None: 
            return 'nil'
        return str(exp.value)

    def visitUnary(self, exp):
        return self.parenthesize(exp.operator.lexeme, exp.right)
    
    def visitBinary(self, exp):
        return self.parenthesize(exp.operator.lexeme, exp.left, exp.right)
    
    def visitGrouping(self, exp):
        return self.parenthesize("group", exp.expression)

    def visitVariableExpr(self, exp):
        return exp.content.lexeme

    def visitAssign(self, exp):
        return self.parenthesize(f"= {exp.name.lexeme}", exp.value)

    def visitLogical(self, exp):
        return self.parenthesize(exp.operator.lexeme, exp.left, exp.right)

    def visitCall(self, exp):
        return self.parenthesize("call", exp.callee, *exp.args)

    def visitGet(self, exp):
        return self.parenthesize(f". {exp.name.lexeme}", exp.object)

    def visitSet(self, exp):
        return self.parenthesize(f"= . {exp.name.lexeme}", exp.object, exp.value)

    def visitThis(self, exp):
        return "this"

    def visitSuper(self, exp):
        return f"super.{exp.method.lexeme}"


class Literal(Exp):
    def __init__(self, value):
        self.value = value
    
    def accept(self, visitor):
        return visitor.visitLiteral(self)


class Binary(Exp): 
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
        
    def accept(self, visitor):
        return visitor.visitBinary(self)


class Unary(Exp):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right
        
    def accept(self, visitor):
        return visitor.visitUnary(self)


class Call(Exp):
    def __init__(self, callee, paren, args):
        self.callee = callee
        self.paren = paren
        self.args = args
        
    def accept(self, visitor):
        return visitor.visitCall(self)


class Grouping(Exp): 
    def __init__(self, exp):
        self.expression = exp
    
    def accept(self, visitor):
        return visitor.visitGrouping(self)


class Variable(Exp):
    def __init__(self, cont):
        self.content = cont
        
    def accept(self, visitor):
        return visitor.visitVariableExpr(self)


class Assign(Exp):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visitAssign(self)


class Logical(Exp):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
        
    def accept(self, visitor):
        return visitor.visitLogical(self)


class Get(Exp):
    def __init__(self, obj, name):
        self.object = obj
        self.name = name

    def accept(self, visitor):
        return visitor.visitGet(self)


class Set(Exp):
    def __init__(self, obj, name, value):
        self.object = obj
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visitSet(self)


class This(Exp):
    def __init__(self, keyword):
        self.keyword = keyword

    def accept(self, visitor):
        return visitor.visitThis(self)


class Super(Exp):
    def __init__(self, keyword, method):
        self.keyword = keyword
        self.method = method

    def accept(self, visitor):
        return visitor.visitSuper(self)
