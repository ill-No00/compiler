from errors.runtimeError import RuntimeError

class DarijaInstance:
    def __init__(self, darijaClass):
        self.darijaClass = darijaClass
        self.fields = {}

    def get(self, name):
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]

        method = self.darijaClass.findMethod(name.lexeme)
        if method is not None:
            return method.bind(self)

        raise RuntimeError(f"Undefined property '{name.lexeme}'.", name)

    def set(self, name, value):
        self.fields[name.lexeme] = value

    def __str__(self) -> str:
        return f"{self.darijaClass.name} instance"
