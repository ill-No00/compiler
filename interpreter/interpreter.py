
import sys
import os
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)


from parser.expressions import Expr_Visitor
from parser.statements import Stmt_Visitor
from errors.runtimeError import RuntimeError
from lexer.token_t import Token
from lexer.token_type import TokenType
from parser.environment import Evironment






class Interpreter(Expr_Visitor, Stmt_Visitor):
    
    def __init__(self):
        self.environment = Evironment()
        hadRuntimeError = False
        
    
    def interpret(self,statements):
        try:
            
            for statement in statements:
                self.execute(statement)
            
        except RuntimeError as error:
            print(error)
            self.hadRuntimeError = True

    def execute(self,stmt):
        stmt.accept(self)
        
    def visitVar(self,stmt):
        value = None
        if stmt.initializer != None:
            value = self.evaluate(stmt.initializer)
        
        self.environment.add(stmt.name,value)
        return None
    
    def visitVariableExpr(self,expr):
        return self.environment.get(expr.name)
    
    def visitExpression(self,stmt):
        value = self.evaluate(stmt.expression)
        return None
    
    def visitPrint(self , stmt):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None
    
    def evaluate(self,expr):
        return expr.accept(self)
    
    def stringify(self, value):
        if value == None:
            return "nil"
        if isinstance(value,bool):
            return "true" if value else "false"
        if isinstance(value,float):
            text = str(value)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        return str(value)
    
    def checkNumberOperand(self,operand):
        if isinstance(operand,(int,float)):
            return
        raise RuntimeError("Operand must be a number.", operand.token)

    def checkStringOperand(self,operand):
        if isinstance(operand,str):
            return
        raise RuntimeError("Operand must be a string.", operand.token)
    

    def visitLiteral(self,exp):
        return exp.value

    def visitUnary(self,exp):
        
        right = exp.right.accept(self)
        
        if exp.operator.type == TokenType.MINUS:
            self.checkNumberOperand(right)
            return -right
        elif exp.operator.type == TokenType.BANG:
            return not self.isTruthy(right)
        
    def visitBinary(self,exp):
        
        left = exp.left.accept(self)
        right = exp.right.accept(self)
        
        if exp.operator.type == TokenType.PLUS:
            if isinstance(left,str) and isinstance(right,str) : 
                self.checkStringOperand(left)
                self.checkStringOperand(right)
                return left + right
            elif isinstance(left,(int,float)) and isinstance(right,(int,float)) :
                self.checkNumberOperand(left)
                self.checkNumberOperand(right)
                return left + right
            else :
                raise RuntimeError("Operands must be two numbers or two strings.", exp.token)
            
        elif exp.operator.type == TokenType.MINUS:
            self.checkNumberOperand(left)
            self.checkNumberOperand(right)
            return left - right
        elif exp.operator.type == TokenType.STAR:
            self.checkNumberOperand(left)
            self.checkNumberOperand(right)
            return left * right
        elif exp.operator.type == TokenType.SLASH:
            self.checkNumberOperand(left)
            self.checkNumberOperand(right)
            return left / right
        elif exp.operator.type == TokenType.GREATER:
            return left > right
        elif exp.operator.type == TokenType.GREATER_EQUAL:
            return left >= right
        elif exp.operator.type == TokenType.LESS:
            return left < right
        elif exp.operator.type == TokenType.LESS_EQUAL:
            return left <= right
        elif exp.operator.type == TokenType.EQUAL_EQUAL:
            return left == right
        elif exp.operator.type == TokenType.BANG_EQUAL:
            return left != right
        
    def visitGrouping(self,exp):
        
        return exp.expression.accept(self)
    
    def isTruthy(self,value):
        if value == None : 
            return False
        if isinstance(value,bool) : 
            return value
        return True