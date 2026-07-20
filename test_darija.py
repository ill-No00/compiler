import io
import sys
from lexer.scanner import Scanner
from parser.parser import Parser
from interpreter.interpreter import Interpreter

def run_darija(code):
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    try:
        scanner = Scanner(code)
        tokens = scanner.scanTokens()
        parser = Parser(tokens)
        statements = parser.parse()
        if statements is None:
            return "Parsing error"
        interpreter = Interpreter()
        interpreter.interpret(statements)
    except Exception as e:
        sys.stdout = old_stdout
        return f"Error: {e}"
    finally:
        sys.stdout = old_stdout
    return new_stdout.getvalue().strip()

def test_simple_function():
    print("Running test_simple_function...")
    code = """
    khedma jma3(a, b) {
        rod a + b;
    }
    akteb jma3(12, 18);
    """
    output = run_darija(code)
    assert output == "30", f"Expected '30', got {repr(output)}"
    print("test_simple_function passed!")

def test_recursion():
    print("Running test_recursion...")
    # Fibonacci recursion
    code = """
    khedma fib(n) {
        yla (n <= 1) {
            rod n;
        }
        rod fib(n - 1) + fib(n - 2);
    }
    akteb fib(7);
    """
    output = run_darija(code)
    assert output == "13", f"Expected '13', got {repr(output)}"
    print("test_recursion passed!")

def test_closures():
    print("Running test_closures...")
    code = """
    khedma dir_counter() {
        khali i = 0;
        khedma counter() {
            i = i + 1;
            rod i;
        }
        rod counter;
    }
    khali c1 = dir_counter();
    akteb c1();
    akteb c1();
    """
    output = run_darija(code).split("\n")
    assert output == ["1", "2"], f"Expected ['1', '2'], got {repr(output)}"
    print("test_closures passed!")

def test_basic_class():
    print("Running test_basic_class...")
    code = """
    class Tomobil {}
    khali t = Tomobil();
    t.marka = "Dacia";
    akteb t.marka;
    """
    output = run_darija(code)
    assert output == "Dacia", f"Expected 'Dacia', got {repr(output)}"
    print("test_basic_class passed!")

def test_class_methods():
    print("Running test_class_methods...")
    code = """
    class Kelb {
        init(smiya) {
            ana.smiya = smiya;
        }
        skwet() {
            akteb ana.smiya + " kaynabah!";
        }
    }
    khali k = Kelb("Rex");
    k.skwet();
    """
    output = run_darija(code)
    assert output == "Rex kaynabah!", f"Expected 'Rex kaynabah!', got {repr(output)}"
    print("test_class_methods passed!")

def test_class_inheritance():
    print("Running test_class_inheritance...")
    code = """
    class Hayawan {
        init(smiya) {
            ana.smiya = smiya;
        }
        smiya_dyalha() {
            rod ana.smiya;
        }
    }
    class Mech < Hayawan {
        init(smiya, lon) {
            waled.init(smiya);
            ana.lon = lon;
        }
        details() {
            akteb waled.smiya_dyalha() + " lonha " + ana.lon;
        }
    }
    khali m = Mech("Mimi", "k7al");
    m.details();
    """

    output = run_darija(code)
    assert output == "Mimi lonha k7al", f"Expected 'Mimi lonha k7al', got {repr(output)}"
    print("test_class_inheritance passed!")

if __name__ == "__main__":
    test_simple_function()
    test_recursion()
    test_closures()
    test_basic_class()
    test_class_methods()
    test_class_inheritance()
    print("\nAll tests passed successfully!")
