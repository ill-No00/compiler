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


class Expr_Visitor(ABC):
    
    @abstractmethod
    def visitLiteral(self):
        pass
    
    @abstractmethod
    def visitBinary(self):
        pass
        
    @abstractmethod
    def visitUnary(self):
        pass
        
    @abstractmethod
    def visitGrouping(self):
        pass
        

    
        
    

class Exp(ABC):
    
    @abstractmethod
    def accept(self , visitor):
        pass
    
class AstPrinter(Expr_Visitor):
    
    def parenthesize(self , name ,*exps ):
        
        builder = f"({name}"
    
        for exp in exps : 
            print(f"exp :{exp}")
            builder+= " "
            added = exp.accept(self)
            if added != None : 
                builder+= added
            
            
        builder += ")"
        
        return builder
    
    def print(self,exp):
        return exp.accept(self)
    
    def visitLiteral(self,exp):
        
        if exp.value == None : 
            return 'nil'
        else:
            return str(exp.value)

    def visitUnary(self,exp):
        
        return self.parenthesize(exp.operator.lexeme , exp.right)
    
    def visitBinary(self,exp):
        return self.parenthesize(exp.operator.lexeme ,exp.left, exp.right)
    
    def visitGrouping(self,exp):
        
        return self.parenthesize("group" , exp.expression)

class Literal(Exp):
    
    def __init__(self,value):
        self.value = value
    
    def accept(self, visitor):
        return visitor.visitLiteral(self)
    


class Binary(Exp): 
    
    def __init__(self,left,operator,right):
        self.left = left
        self.operator = operator
        self.right = right
        
    def accept(self, visitor):
        return visitor.visitBinary(self)
    
    
    
class Unary(Exp):
    
    def __init__(self,operator,right):
        self.operator = operator
        self.right = right
        
    def accept(self, visitor):
        return visitor.visitUnary(self)
    
    
    
class Grouping(Exp): 
    
    def __init__(self,exp):
        self.expression = exp
    
    def accept(self, visitor):
        return visitor.visitGrouping(self)
    
class Variable(Exp):
    def __init__(self,cont):
        self.content = cont


class Assign(Exp):
    def __init__(self,name,value):
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visitAssign(self)

