import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from abc import ABC, abstractmethod
from lexer.token_t import Token

class Stmt_Visitor(ABC):
    
    @abstractmethod
    def visitExpression(self, stmt):
        pass
    
    @abstractmethod
    def visitPrint(self, stmt):
        pass
        
    @abstractmethod
    def visitVar(self, stmt):
        pass
        
    @abstractmethod
    def visitBlock(self, stmt):
        pass
        
    @abstractmethod
    def visitIfStmt(self, stmt):
        pass
        
    @abstractmethod
    def visitWhileStmt(self, stmt):
        pass
        
    @abstractmethod
    def visitFunction(self, stmt):
        pass
        
    @abstractmethod
    def visitReturnStmt(self, stmt):
        pass
        
    @abstractmethod
    def visitClassStmt(self, stmt):
        pass


class Stmt(ABC):
    
    @abstractmethod
    def accept(self, visitor):
        pass


class Expression(Stmt):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitExpression(self)


class Print(Stmt):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitPrint(self)


class Var(Stmt):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer
    
    def accept(self, visitor):
        return visitor.visitVar(self)


class Block(Stmt):
    def __init__(self, statements):
        self.statements = statements
    
    def accept(self, visitor):
        return visitor.visitBlock(self)


class IfStmt(Stmt):
    def __init__(self, condition, thenBranch, elseBranch):
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch
    
    def accept(self, visitor):
        return visitor.visitIfStmt(self)


class WhileStmt(Stmt):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    
    def accept(self, visitor):
        return visitor.visitWhileStmt(self)


class Function(Stmt):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor):
        return visitor.visitFunction(self)


class ReturnStmt(Stmt):
    def __init__(self, keyword, value):
        self.keyword = keyword
        self.value = value

    def accept(self, visitor):
        return visitor.visitReturnStmt(self)


class ClassStmt(Stmt):
    def __init__(self, name, superclass, methods):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def accept(self, visitor):
        return visitor.visitClassStmt(self)
