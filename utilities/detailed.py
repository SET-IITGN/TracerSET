import sys
import ast
import traceback
import linecache
import os
import types

COLOR = "\033[93m"
CURR = "\033[92m"
RESET = "\033[0m"
flag=0 

def clear_screen():
    if sys.stdin.isatty():
        rows = os.get_terminal_size().lines
        # Natural scroll
        for _ in range(rows):
            print()
        # Reposition cursor
        print("\033[H", end="", flush=True)

def getch():
    if sys.stdin.isatty():
        sys.stdin.read(1)
        clear_screen()

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
            
        self.project_root = os.path.dirname(os.path.abspath(self.script_path))
        self.tracer_file = os.path.abspath(__file__)
    
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
        elif isinstance(node, ast.ClassDef):
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
    
    def print_code_file(self, filename, current_line):
        print("\n" + "─" * 60)
        print(f"FILE : {os.path.basename(filename)}\n")
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception:
            print("<unable to read source file>")
            print("─" * 60)
            return

        for lineno, source in enumerate(lines, start=1):
            source = source.rstrip('\n\r')
            marker = "--> " if lineno == current_line else "    "
            color = COLOR if lineno == current_line else RESET
            print(
                f"{color}"
                f"{marker}{lineno:>3} │ {source}"
                f"{RESET}"
            )
        print("\n" + "─" * 60)
    
    def create_tracer(self):
        call_depth = 0
        call_signatures = {}
        def format_args(frame):
            args = []

            argcount = frame.f_code.co_argcount
            argnames = frame.f_code.co_varnames[:argcount]

            for name in argnames:
                if name in frame.f_locals:
                    value = frame.f_locals[name]

                try:
                    value_repr = repr(value)
                except Exception:
                    value_repr = "<unrepr-able>"

                if ' object ' in value_repr:
                    xbuff = value_repr.split('__main__.')[1]
                    xbuff = xbuff.split('object')[0]
                    xbuff = '<' + xbuff + 'object>'
                    value_repr = xbuff

                args.append(f"{name}={value_repr}")

            return ", ".join(args)
        def get_filtered_vars(frame):
            globals_raw = self._safe_repr_dict(frame.f_globals)
            locals_raw = self._safe_repr_dict(frame.f_locals)

            def transform(v, k):
                if '<module' in v:
                    return '<module>'
                if '<function' in v:
                    return '<function>'
                if '<class' in v:
                    return '<class>'
                if ' object ' in v:
                    #example: <__main__.Animal object at 0x7f339319a590>
                    buff=v.split('__main__.')[1]
                    #example: <__main__.Animal object at 0x7f339319a590>
                    buff=buff.split('object')[0]
                    #'Animal '
                    buff='<'+buff+'object>'
                    return buff
                return v

            globals_dict = {
                k: transform(v, k)
                for k, v in globals_raw.items()
                if not k.startswith('__')
            }

            locals_dict = {
                k: transform(v, k)
                for k, v in locals_raw.items()
                if not k.startswith('__')
            }

            return globals_dict, locals_dict

        def get_stack(frame):

            stack = []
            current = frame
            while current:
                filename = os.path.abspath(
                current.f_code.co_filename
                )

                # Ignore tracer implementation frames
                #if os.path.basename(filename) != "detailed.py":
                basename = os.path.basename(filename)
                if (basename != "detailed.py" and "<frozen importlib" not in filename):
                    '''
                    stack.append(
                    (
                        current.f_code.co_name,
                        current.f_lineno,
                        filename
                    )                    
                )
                    '''
                    signature = call_signatures.get(id(current), "")

                    stack.append(
                        (
                            (
                                f"{current.f_code.co_name}({signature})"
                                if signature else
                                f"{current.f_code.co_name}()"
                            ),
                            current.f_lineno,
                            filename
                        )
                    ) 
                
                current = current.f_back
            stack.reverse()
            return stack  

        def print_stack(frame, active_only=False, event_type=None, switch=2):
            stack = get_stack(frame)
            print("\nRUNTIME STACK:")
            
            SCOLOR=RESET
            if switch==0:
                SCOLOR=CURR
            elif switch==1:
                SCOLOR=COLOR
            
            for depth, (func_signature, lineno, filename) in enumerate(stack):
                indent = "│   " * depth
                if depth == len(stack) - 1:
                    if event_type == "return":
                        marker = "└── RETURNING"
                    else:
                        marker = f"{SCOLOR}└── ACTIVE"
                else:
                    marker = "├──"

                if active_only and depth != len(stack) - 1:
                    continue
                
                print(
                    f"{indent}{marker} "
                    f"{func_signature} "
                    f"[{os.path.basename(filename)}:{lineno}]{RESET}"
                )
                
        def tracer(frame, event, arg):
            nonlocal call_depth
            filename = os.path.abspath(frame.f_code.co_filename)
            
            # Ignore the tracer implementation itself
            if os.path.basename(filename) == "detailed.py":
                return tracer

            # Ignore non-user code
            if not filename.startswith(self.project_root):
                return tracer

            # Ignore Python internals / virtual envs / site-packages
            exclude_dirs = (
                sys.prefix,
                sys.exec_prefix,
            )

            if filename.startswith(exclude_dirs):
                return tracer    

            func_name = frame.f_code.co_name

            # ==========================================================
            # FUNCTION CALL
            # ==========================================================
            if event == 'call':
                indent = "│   " * call_depth
                args_str = format_args(frame)
                call_signatures[id(frame)] = args_str
                globals_dict, locals_dict = get_filtered_vars(frame)
                
                '''
                print(f"{indent}│  LOCALS   : {locals_dict}")
                print(f"{indent}│  GLOBALS  : {globals_dict}")
                '''
                
                #print(f"\n{indent}┌─ CALL depth={call_depth}")
                #print(f"{indent}│  Function : {func_name}({args_str})")
                if func_name == "<module>":
                    print(f"{indent}│  Function CALL: <module>()")
                elif func_name == "<class>":
                    print(f"{indent}│  Function CALL: <class>()")
                elif func_name == "<object>":
                    print(f"{indent}│  Function CALL: <object>()")
                else:
                    print(f"{indent}│  Function CALL: {func_name}({args_str})")
                #print(f"{indent}│  Line     : {frame.f_lineno}")
                print_stack(frame, active_only=False,switch=0)
                '''
                print(f"{indent}└────────────────────────────────")
                '''
                call_depth += 1
                return tracer

            # ==========================================================
            # FUNCTION RETURN
            # ==========================================================
            elif event == 'return':

                indent = "│   " * (call_depth - 1)
                '''
                print(f"\n{indent}┌─ RETURN depth={call_depth - 1}")
                print(f"{indent}│  Function : {func_name}()")
                '''
                globals_dict, locals_dict = get_filtered_vars(frame)
                
                print(f"{indent}│   <---program state immediately before RETurning--->")
                print(f"{indent}│   LOCALS   : {locals_dict}")
                print(f"{indent}│   GLOBALS  : {globals_dict}")
                '''
                print(f"\n{COLOR}Press Enter key to continue to next statement{RESET}")
                getch()
                '''
                args_str = call_signatures.get(id(frame), "")
                try:
                    print(f"{CURR}{indent}│   {func_name}({args_str if '<module>' not in func_name else ''}) RETurned : {repr(arg)}{RESET}")
                except Exception:
                    print(f"{CURR}{indent}│   {func_name}({args_str if '<module>' not in func_name else ''}) RETurned : <unrepr-able>{RESET}")
                
                if frame.f_back:
                    #print_stack(frame.f_back, active_only=True)
                    print_stack(frame.f_back, active_only=False)
                '''
                print(f"{indent}└────────────────────────────────")
                '''
                call_depth -= 1
                
                if sys.stdin.isatty():
                    print(f"\n{COLOR}Press Enter key to continue to next statement{RESET}")
                    getch()
                
                return tracer

            # ==========================================================
            # LINE EXECUTION
            # ==========================================================
            elif event == 'line':
 
                line_no = frame.f_lineno
                line_source = self.get_line_source(
                    filename,
                    line_no
                )

                stripped = line_source.strip()

                if (
                    not stripped or
                    stripped.startswith('#') or
                    stripped == 'pass'
                ):
                    return tracer

                indent = "│   " * call_depth

                globals_dict, locals_dict = get_filtered_vars(frame)
                
                self.print_code_file(filename, line_no)
                
                '''
                print(f"\n{indent}├─ LINE {line_no}")
                print(f"{indent}│  CODE    : {COLOR}{line_source.strip()}{RESET}")
                #self.print_code_file(filename, line_no)
                print(f"{indent}│  LOCALS  : {locals_dict}")
                print(f"{indent}│  GLOBALS : {globals_dict}")
                #self.print_code_file(filename, line_no)
                print(f"\n{COLOR}Press Enter key to continue to next statement{RESET}")
                getch()
                '''
                
                print(f"\n{indent}├─ LINE {line_no}")
                print(f"{indent}│  CODE    : {COLOR}{line_source.strip()}{RESET}")
                print(f"{indent}│  <---program state immediately before EXEcuting above CODE line--->")
                print(f"{indent}│  LOCALS  : {locals_dict}")
                print(f"{indent}│  GLOBALS : {globals_dict}")
                print_stack(frame, active_only=False,switch=1)
                if sys.stdin.isatty():
                    print(f"\n{COLOR}Press Enter key to continue to next statement{RESET}")
                    getch()
                
                return tracer
            return tracer
        return tracer
    
    def _safe_repr_dict(self, dct):
        """Safely convert dictionary values to repr strings."""
        result = {}
        for k, v in dct.items():
            try:
                #result[k] = repr(v)
                if isinstance(v, types.FunctionType):
                    result[k] = f"<function {v.__name__}>" #reduce-noise
                else:
                    result[k] = repr(v)
            except Exception:
                result[k] = f"<{type(v).__name__}: unrepresentable>"
        return result

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 P.py <script.py>")
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
        
        clear_screen()
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

