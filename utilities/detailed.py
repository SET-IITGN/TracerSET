#Generated with the assistance of Perplexity AI

import sys
import ast
import traceback
import linecache
import os
import types

COLOR = "\033[93m"
RESET = "\033[0m"

def getch():
    sys.stdin.read(1)

class VariableTracer:
    def __init__(self, script_path):
        self.script_path = script_path
        self.script_dir = os.path.dirname(self.script_path)
        self.user_vars = set()
        self.linecache_cache = {}
        
        # Setup local imports
        self.original_path = sys.path.copy()
        if self.script_dir not in sys.path:
            sys.path.insert(0, self.script_dir)
    
    def cleanup(self):
        """Restore original sys.path."""
        sys.path[:] = self.original_path
        
    def extract_user_variables(self):
        """Extract ALL user-defined variable names using comprehensive AST analysis."""
        try:
            with open(self.script_path, 'r', encoding='utf-8') as f:
                source = f.read()
        except Exception as e:
            print(f"Error reading {self.script_path}: {e}")
            sys.exit(1)
        
        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            print(f"Syntax error in {self.script_path}: {e}")
            sys.exit(1)
        
        # Comprehensive AST walker
        for node in ast.walk(tree):
            self._collect_variables(node)
        
        # Remove built-ins, Python internals, and common modules
        exclude_set = self._get_exclude_set()
        self.user_vars -= exclude_set
        
        return self.user_vars
    
    def _collect_variables(self, node):
        """Recursively collect all variable names from AST node."""
        
        # Assignments
        if isinstance(node, ast.Assign):
            for target in node.targets:
                self._collect_target_names(target)
        elif isinstance(node, ast.AnnAssign) and node.target:
            self._collect_target_names(node.target)
        elif isinstance(node, ast.AugAssign):
            self._collect_target_names(node.target)
        
        # Loop variables
        elif isinstance(node, (ast.For, ast.AsyncFor)):
            self._collect_target_names(node.target)
        elif isinstance(node, ast.While):
            pass  # No new variables
        
        # Context manager variables
        elif isinstance(node, (ast.With, ast.AsyncWith)):
            for item in node.items:
                if item.optional_vars:
                    self._collect_target_names(item.optional_vars)
        
        # Exception handlers
        elif isinstance(node, ast.ExceptHandler) and node.name:
            self._collect_target_names(node.name)
        
        # Name usages
        elif isinstance(node, ast.Name):
            self._collect_target_names(node)
        
        # Function definitions
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            self.user_vars.add(node.name)
            self._collect_function_params(node)
        
        # Class definitions
        elif isinstance(node, (ast.ClassDef, ast.AsyncFunctionDef)):
            self.user_vars.add(node.name)
        
        # Lambda parameters
        elif isinstance(node, ast.Lambda):
            self._collect_function_params(node)
        
        # Comprehension variables
        elif isinstance(node, ast.comprehension):
            self._collect_target_names(node.target)
    
    def _collect_target_names(self, node):
        """Extract names from complex targets (tuples, lists, starred)."""
        if isinstance(node, ast.Name):
            self.user_vars.add(node.id)
        elif isinstance(node, (ast.Tuple, ast.List)):
            for elt in node.elts:
                self._collect_target_names(elt)
        elif isinstance(node, ast.Starred):
            self._collect_target_names(node.value)
    
    def _collect_function_params(self, node):
        """Extract all function/lambda parameter names."""
        args = node.args if hasattr(node, 'args') else node
        for arg in args.args:
            self.user_vars.add(arg.arg)
        for arg in args.kwonlyargs:
            self.user_vars.add(arg.arg)
        if args.vararg:
            self.user_vars.add(args.vararg.arg)
        if args.kwarg:
            self.user_vars.add(args.kwarg.arg)
    
    def _get_exclude_set(self):
        """Get comprehensive set of names to exclude."""
        builtins = set(dir(__builtins__)) if isinstance(__builtins__, dict) else set(dir(__builtins__))
        
        exclude = builtins.copy()
        exclude.update([
            # Python internals
            '__name__', '__doc__', '__package__', '__loader__', '__spec__',
            '__annotations__', '__file__', '__cached__', '__builtins__',
            '__dict__', '__module__', '__qualname__', '__init__', '__str__',
            '__repr__', '__call__', '__getattr__', '__setattr__',
            
            # Keywords & constants
            'True', 'False', 'None', 'NotImplemented', 'Ellipsis',
            
            # Common conventions
            'args', 'kwargs', 'self', 'cls', 'super',
            
            # Common modules (avoid false positives)
            'sys', 'os', 'time', 'json', 're', 'math', 'random',
            'collections', 'itertools', 'functools', 'typing', 'pathlib',
            'datetime', 'decimal', 'fractions', 'statistics'
        ])
        
        return exclude
    
    def get_line_source(self, filename, line_no):
        """Safely get source line with caching."""
        key = (filename, line_no)
        if key not in self.linecache_cache:
            try:
                self.linecache_cache[key] = linecache.getline(filename, line_no).rstrip('\n\r')
            except:
                self.linecache_cache[key] = f"<line {line_no} unavailable>"
        return self.linecache_cache[key]
    
    def create_tracer(self):
        """Create the line-by-line tracer."""
        def tracer(frame, event, arg):
            if event != 'line':
                return tracer
            
            line_no = frame.f_lineno
            filename = frame.f_code.co_filename
            
            # Skip if not our main script
            if not filename.endswith(self.script_path):
                return tracer
            
            line_source = self.get_line_source(filename, line_no)
            
            # Skip empty lines, comments, and pass statements
            stripped = line_source.strip()
            if (not stripped or 
                stripped.startswith('#') or 
                stripped == 'pass' or
                stripped.startswith('pass')):
                return tracer
            
            # Get safe variable representations
            globals_dict = self._safe_repr_dict(frame.f_globals)
            locals_dict = self._safe_repr_dict(frame.f_locals)
            
            # Filter to user-defined variables only
            globals_dict = {k: v for k, v in globals_dict.items() if k in self.user_vars}
            locals_dict = {k: v for k, v in locals_dict.items() if k in self.user_vars}
            
            print(f"\n{'-'*80}")
            print(f"LINE {line_no:3d} | {COLOR}{line_source}{RESET}")
            print(f"{'-'*80}")
            print(f"GLOBAL VARIABLES ({len(globals_dict)}): {globals_dict}")
            print(f"LOCAL  VARIABLES ({len(locals_dict)}): {locals_dict}")
            print(f"{COLOR}Press Enter key to continue to next statement{RESET}")
            getch()
            return tracer
        
        return tracer
    
    def _safe_repr_dict(self, dct):
        """Safely convert dictionary values to repr strings."""
        result = {}
        for k, v in dct.items():
            try:
                result[k] = repr(v)
            except Exception:
                result[k] = f"<{type(v).__name__}: unrepresentable>"
        return result

def main():
    if len(sys.argv) != 2:
        print("Usage: python P.py <script.py>")
        print("\nComprehensive Python Variable Tracer:")
        print("• Tracks ALL user-defined local/global variables")
        print("• Handles classes, functions, comprehensions, context managers")
        print("• Shows variable states BEFORE each statement executes")
        print("• Safe repr() handling, no crashes")
        sys.exit(1)
    
    script_path = sys.argv[1]
    
    # Validate script exists
    if not os.path.exists(script_path):
        print(f"Error: File '{script_path}' not found.")
        sys.exit(1)
    
    if not script_path.endswith('.py'):
        print(f"Warning: '{script_path}' doesn't end with .py")
    
    print("Initializing comprehensive variable tracer...")
    
    # Initialize tracer
    tracer = VariableTracer(script_path)
    
    # Extract variables
    user_vars = tracer.extract_user_variables()
    
    if not user_vars:
        print("No user-defined variables found (only built-ins used)")
        print("   This is normal for scripts that only use built-in functions.")
        return
    
    print(f"Found {len(user_vars)} user-defined variable(s):")
    print(f"   {', '.join(sorted(user_vars))}")
    print(f"{'='*80}")
    
    # Setup execution environment
    exec_globals = {
        '__name__': '__main__',
        '__file__': os.path.abspath(script_path),
        '__package__': None,
        '__loader__': None,
        '__spec__': None,
        '__builtins__': __builtins__
    }
    
    # Compile and execute
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        code = compile(source, script_path, 'exec')
        
        # Install tracer
        sys.settrace(tracer.create_tracer())
        
        print("Starting execution with tracing...")
        print(f"Variable states shown BEFORE each statement executes")
        print(f"{'='*80}")
        
        exec(code, exec_globals)
        
    except SyntaxError as e:
        print(f"Syntax error: {e}")
        sys.exit(1)
    except SystemExit:
        pass  # Allow sys.exit()
    except KeyboardInterrupt:
        print("\nExecution interrupted by user")
    except Exception as e:
        print(f"\nExecution error: {type(e).__name__}: {e}")
        traceback.print_exc()
    finally:
        sys.settrace(None)
        tracer.cleanup()
    
if __name__ == "__main__":
    main()

