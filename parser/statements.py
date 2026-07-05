import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)


from abc import ABC , abstractmethod
from lexer.token_t import Token
from lexer.token_type import TokenType
from errors.runtimeError import RuntimeError


# program        → statement* EOF ;

# statement      → exprStmt
#                | printStmt ;

# exprStmt       → expression ";" ;
# printStmt      → "print" expression ";" ;

class Stmt_Visitor(ABC):
    
    @abstractmethod
    def visitExpression(self):
        pass
    
    @abstractmethod
    def visitPrint(self):
        pass
        
    


class Stmt(ABC):
    
    @abstractmethod
    def accept(self , visitor):
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
    
    def __init__(self , name , initializer):
        self.name = name
        self.initializer = initializer
    
    def accept(self , visitor):
        return visitor.visitVar(self)
