import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from lexer.token_type import TokenType
from .expressions import *
from .statements import *
from .expressions import *


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0



    def parse(self):
        try:
            statements = []
            while not self.is_at_end():
                statements.append(self.declaration())
            return statements
        except ParseError:
            return None
    
    def declaration(self):
        try:
            if self.match(TokenType.VAR) :
                return self.varDeclaration()
            return self.statement() 
        except Exception as e:
            self.synchronize()
            return None
        
    def varDeclaration(self):
        
        name = self.consume(TokenType.IDENTIFIER , "Expect a variable name.")
        
        initializer = None

        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        
        self.consume(TokenType.SEMICOLON , "Expect a semicolon.")
        
        return Var(name,initializer)
    
    def statement(self):
        if self.match(TokenType.PRINT):
            return self.print_statement()
        elif self.match(TokenType.LEFT_BRACE):
            return Block(self.block())
        elif self.match(TokenType.IF):
            return self.ifStatement()

        return self.expression_statement()
    
    def block(self):
        statements = []
        
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())
        
        self.consume(TokenType.RIGHT_BRACE , "Expect '}' after block.")
        return statements
    
    def ifStatement(self):
        self.consume(TokenType.LEFT_PAREN , "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN , "Expect ')' after if condition.")
        
        thenBranch = self.statement()
        elseBranch = None
        
        if self.match(TokenType.ELSE):
            elseBranch = self.statement()
        
        return IfStmt(condition,thenBranch,elseBranch)
    
    def declaration(self):
        try:
            if self.match(TokenType.VAR):
                return self.varDeclaration()
            return self.statement()
        except ParseError:
            self.synchronize()
            return None
    
    def print_statement(self): 
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)
    
    def expression_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Expression(expr)
    
    def expression(self):
        return self.assignment()
    
    def assignment(self):
        expr = self.equality()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)

            self.error(equals, "Invalid assignment target.")

        return expr

    def equality(self):
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL,
                         TokenType.EQUAL_EQUAL):

            operator = self.previous()
            right = self.comparison()

            expr = Binary(expr, operator, right)
            
            

        return expr

    def comparison(self):
        expr = self.term()

        while self.match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):

            operator = self.previous()
            right = self.term()

            expr = Binary(expr, operator, right)

        return expr

    def term(self):
        expr = self.factor()

        while self.match(TokenType.PLUS,
                         TokenType.MINUS):

            operator = self.previous()
            right = self.factor()

            expr = Binary(expr, operator, right)

        return expr

    def factor(self):
        expr = self.unary()

        while self.match(TokenType.STAR,
                         TokenType.SLASH):

            operator = self.previous()
            right = self.unary()

            expr = Binary(expr, operator, right)

        return expr

    def unary(self):
        if self.match(TokenType.BANG,
                      TokenType.MINUS):

            operator = self.previous()
            right = self.unary()

            return Unary(operator, right)

        return self.primary()

    def primary(self):
        
        
        if self.match(TokenType.FALSE):
            return Literal(False)

        if self.match(TokenType.TRUE):
            return Literal(True)

        if self.match(TokenType.NIL):
            return Literal(None)
        
        if self.match(TokenType.IDENTIFIER):
            
            return Variable(self.previous())

        if self.match(TokenType.NUMBER,
                      TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            
            expr = self.expression()

            self.consume(
                TokenType.RIGHT_PAREN,
                "Expect ')' after expression."
            )

            return Grouping(expr)

        raise self.error(
            self.peek(),
            "Expect expression."
        )



    def match(self, *types):
        
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True

        return False

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()

        raise self.error(self.peek(), message)

    def check(self, token_type):
        
        if self.is_at_end():
            return False

        return self.peek().type == token_type

    def advance(self):
        if not self.is_at_end():
            self.current += 1

        return self.previous()

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]


    def error(self, token, message):
        if token.type == TokenType.EOF:
            self.report(token.line,
                         " at end",
                         message)
        else:
            self.report(token.line,
                         f" at '{token.lexeme}'",
                         message)

        return ParseError()

    def report(self, line, where, message):
        print(
            f"[line {line}] Error{where}: {message}"
        )

    def synchronize(self):
        self.advance()

        while not self.is_at_end():

            if self.previous().type == TokenType.SEMICOLON:
                return

            if self.peek().type in (
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            ):
                return

            self.advance()