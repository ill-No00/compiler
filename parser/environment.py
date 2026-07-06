import sys
import os
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from errors.runtimeError import RuntimeError


class Evironment():
    
    
    def __init__(self,enclosing=None):
        self.values = {}
        self.enclosing = enclosing
    
    def add(self,name,value):
        self.values[name] = value
    
    def get(self,name):
        
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        
        if self.enclosing is not None:
            return self.enclosing.get(name)
        
        raise RuntimeError(f"Undefined variable {name.lexeme} .", name )
    
    def assign(self,name,value):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
            
        if self.enclosing is not None:
            self.enclosing.assign(name,value)
            return
        
        raise RuntimeError(f"Undefined variable {name.lexeme} .", name )