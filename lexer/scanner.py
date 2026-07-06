import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from lexer.token_t import Token
from lexer.token_type import TokenType
from parser.parser import Parser
from parser.expressions import AstPrinter

keywords = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "wela": TokenType.ELSE,
    "ghalet": TokenType.FALSE,
    "dor": TokenType.FOR,
    "khedma": TokenType.FUN,
    "yla": TokenType.IF,
    "walou": TokenType.NIL,
    "or": TokenType.OR,
    "akteb": TokenType.PRINT,
    "rod": TokenType.RETURN,
    "waled": TokenType.SUPER,
    "ana": TokenType.THIS,
    "s7i7": TokenType.TRUE,
    "khali": TokenType.VAR,
    "madam": TokenType.WHILE,
}

    
class Scanner:
    
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start= 0
        self.current = 0
        self.line = 1
        
    def scanTokens(self):
        tokens = self.scanner()
        return tokens
    
    def scanner(self):
        
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()
        
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens
    
    def isAtEnd(self):
        return self.current >= len(self.source)
    
    def scanToken(self):
        c = self.advance()
        
        match c:
            case '(':
                self.addToken(TokenType.LEFT_PAREN)
            case ')':
                self.addToken(TokenType.RIGHT_PAREN)
            case '{':
                self.addToken(TokenType.LEFT_BRACE)
            case '}':
                self.addToken(TokenType.RIGHT_BRACE)
            case ',': 
                self.addToken(TokenType.COMMA)
            case '.':
                
                self.addToken(TokenType.DOT)
            case '-':
                self.addToken(TokenType.MINUS)
            case '+':
                self.addToken(TokenType.PLUS)
            case ';':
                self.addToken(TokenType.SEMICOLON)
            case '*':
                self.addToken(TokenType.STAR)
            case '!':
                self.addToken(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
            case '=':
                self.addToken(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
            case '<':
                self.addToken(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
            case '>':
                self.addToken(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
            case '/':
                if self.match('/'):
                    while self.peek() != '\n' and not self.isAtEnd():
                        self.advance()
                else:
                    self.addToken(TokenType.SLASH)
            case ' ' | '\r' | '\t':
                pass
            case '\n':
                self.line += 1
            case '"' | "'":
                self.scanTokenstring(c)
            
            case _:
                if(self.isDegit(c)):
                    self.number()
                elif(self.isAlpha(c)):
                    self.identifier()
                else : 
               
                    print(f"Unexpected character: {c} at line {self.line}")
                
    
    def identifier(self):
        
        while self.isAlphNumeric(self.peek()):
            self.advance()
            
        text = self.source[self.start : self.current]
        
        type = keywords.get(text)
        
        if not type :
            type = TokenType.IDENTIFIER
            
        self.addToken(type)
            
    def isAlpha(self, c):
        return ('a' <= c <= 'z') or ('A' <= c <= 'Z') or c == '_'
            
        
    def isAlphNumeric(self,c):
        return self.isAlpha(c) or self.isDegit(c)
    
    def isDegit(self,num):
        return num >= '0' and num <= '9'
    
    def number(self):
        
        while self.isDegit(self.peek()):
            self.advance()
            
        if self.peek() == '.' and self.isDegit(self.nextPeek()):
            
            self.advance()
            
            while self.isDegit(self.peek()) :
                self.advance()
        
        self.addToken(TokenType.NUMBER , float(self.source[self.start : self.current]))
        
    
    def scanTokenNum(self):
        
        while not self.isAtEnd() and self.is_number(self.peek()):
            
            self.advance()
        
        if self.peek()== '.' and self.is_number(self.nextPeek()):

            self.advance()
            
            while self.is_number(self.peek()) and not self.isAtEnd() :
                self.advance()
                
        
        
    
    def nextPeek(self):
        
        if self.current + 1 > len(self.source) : 
            return '\0'
        return self.source[self.current+1]
        
            
    def scanTokenstring(self ,quote):
        
        while self.peek() != quote  and not self.isAtEnd() : 
            if self.peek() == '\n' :
                self.line+=1
            self.advance()
        
        if self.isAtEnd():
            print(f"unterminated string at line {self.line}")
        
        self.advance()
        
        value = self.source[self.start+1:self.current - 1]
        
        self.addToken(TokenType.STRING,value)


    def match(self, expected):
        if self.isAtEnd():
            return False
        if self.source[self.current] != expected:
            return False
        
        self.current += 1
        return True
    def peek(self):
        if self.isAtEnd():
            return '\0'
        return self.source[self.current]

    

    def addToken(self, type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))
        
    def advance(self):
        self.current += 1
        return self.source[self.current - 1]
    
    def printDetails(self):
        
        
        if self.tokens :
            for token in self.tokens : 
                print(f"token : {token} , type : {token.type} , literal : {token.literal} , line : {token.line}")
            
            
    
#sc = Scanner("""
#(3 + 4) * 2      
#""")

#sc.scanTokens()

#sc.printDetails()

# parser = Parser(sc.tokens)

# exp = parser.parse()

# print(f"expression {exp}")

# printer = AstPrinter()

# print(printer.print(exp))