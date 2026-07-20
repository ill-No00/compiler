from callable.darijaCallable import DarijaCallable
from errors.return_exception import ReturnException
from lexer.token_t import Token
from lexer.token_type import TokenType

class DarijaFunction(DarijaCallable):
    def __init__(self, declaration, closure, is_initializer=False):
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer

    def arity(self) -> int:
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        from parser.environment import Environment
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.add(self.declaration.params[i], arguments[i])

        try:
            interpreter.executeBlock(self.declaration.body, environment)
        except ReturnException as returnValue:
            if self.is_initializer:
                return self.closure.get(Token(TokenType.THIS, "ana", None, 0))
            return returnValue.value

        if self.is_initializer:
            return self.closure.get(Token(TokenType.THIS, "ana", None, 0))
        return None

    def bind(self, instance):
        from parser.environment import Environment
        environment = Environment(self.closure)
        ana_token = Token(TokenType.THIS, "ana", None, 0)
        environment.add(ana_token, instance)
        return DarijaFunction(self.declaration, environment, self.is_initializer)

    def __str__(self) -> str:
        return f"<khedma {self.declaration.name.lexeme}>"
