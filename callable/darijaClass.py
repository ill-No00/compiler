from callable.darijaCallable import DarijaCallable
from callable.darijaInstance import DarijaInstance

class DarijaClass(DarijaCallable):
    def __init__(self, name: str, superclass, methods):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def arity(self) -> int:
        initializer = self.findMethod("init")
        if initializer is not None:
            return initializer.arity()
        return 0

    def call(self, interpreter, arguments):
        instance = DarijaInstance(self)
        initializer = self.findMethod("init")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)
        return instance

    def findMethod(self, name: str):
        if name in self.methods:
            return self.methods[name]
        if self.superclass is not None:
            return self.superclass.findMethod(name)
        return None

    def __str__(self) -> str:
        return self.name
