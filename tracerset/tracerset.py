import ast
import sys
import tokenize
import os
import platform

# ===============================================================
# TracerSET
# Execution-Centric Program Comprehension Environment for Python
# ===============================================================

VER='TracerSET 1.1.9'
TAG='Execution-Centric Program Comprehension Environment for Python'

COLOR = "\033[93m"
ERROR = "\033[91m"
SUCCESS = "\033[92m"
RESET = "\033[0m"

MODE_BEGINNER = "beginner"
MODE_INTERMEDIATE = "intermediate"
MODE_ADVANCED = "advanced"

MODES = {
    MODE_BEGINNER: {
        "tokens": False,
        "cst": False,
        "ast": False,
        "disassembly": False,
        "execution_trace": False,
        "step_trace": True,
    },

    MODE_INTERMEDIATE: {
        "tokens": False,
        "cst": False,
        "ast": True,
        "disassembly": False,
        "execution_trace": True,
        "step_trace": True,
    },

    MODE_ADVANCED: {
        "tokens": True,
        "cst": True,
        "ast": True,
        "disassembly": True,
        "execution_trace": True,
        "step_trace": True,
    }
}

# ============================================================
# Utility Functions
# ============================================================

def pause(section_name):
    if sys.stdin.isatty():
        print(f"\n{COLOR}Press Enter key to continue to {section_name}{RESET}")
        sys.stdin.read(1)
        rows = os.get_terminal_size().lines
        # Natural scroll
        for _ in range(rows):
            print()
        # Reposition cursor
        print("\033[H", end="", flush=True)
        
def get_python_cmd():
    return f"python{'.'.join(platform.python_version().split('.')[:2])}"

def read_source_code(filename):
    with open(filename, "r") as fp:
        return fp.read()

# ============================================================
# Display Functions
# ============================================================

def show_source_code(buff):
    print("[Source Code]:")
    print("==============")
    print(buff)

def show_tokens(filename):
    pause("[Tokens]")
    print("=========")

    with tokenize.open(filename) as f:
        tokens = tokenize.generate_tokens(f.readline)
        for token in tokens:
            print(token)

def resolve_import_file(module_name, current_file):
    base_dir = os.path.dirname(os.path.abspath(current_file))

    candidate = os.path.join(
        base_dir,
        module_name.replace(".", os.sep) + ".py"
    )

    if os.path.exists(candidate):
        return os.path.abspath(candidate)
    return None

def collect_all_python_files(entry_file):
    base_file = os.path.abspath(entry_file)

    pending = [base_file]
    visited = set()

    while pending:
        current = pending.pop(0)
        if current in visited:
            continue

        visited.add(current)

        with open(current, "r", encoding="utf-8") as f:
            source = f.read()

        tree = ast.parse(source)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported = resolve_import_file(alias.name, current)
                    if imported and imported not in visited:
                        pending.append(imported)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imported = resolve_import_file(node.module, current)
                    if imported and imported not in visited:
                        pending.append(imported)

    return list(visited)

def show_cognitive_complexity(filename):
    pause("[Cognitive Complexity]")
    print("======================")
    files = collect_all_python_files(filename)
    print("Analyzing files:")
    for f in files:
        print(" -", f)
    cmd = "complexipy -cs -C no --suggest-refactors " + " ".join(files)
    os.system(cmd)
    
def show_control_flow_graph(filename):
    try:
        import python_ta.cfg as cfg
        cfg.generate_cfg(filename)
        print(filename)
    except:
        pycmd = get_python_cmd() #if import fails!
        os.system(f"{pycmd} -m python_ta.cfg {filename}")
        print(f"{pycmd} -m python_ta.cfg {filename}")
    
    if platform.system() == 'Windows':
        if '\\' in filename:
            fname=filename.split('\\')[::-1][0]
        else:
            fname=filename.split('/')[::-1][0]
        src=fname.replace(".py",".gv")
        dest=filename.replace(".py",".cfg.png")
        print(src,fname,dest)
        os.system(f"dot -Tpng {src} > {dest}")
        print(f"DOT file written to: {dest}")
        os.system(f"start {dest}")
    elif platform.system() == 'Linux':
        fname=filename.split('/')[::-1][0]
        src=fname.replace(".py",".gv")
        dest=filename.replace(".py",".cfg.dot")
        os.system(f"rm -f *.svg; mv {src} {dest}")
        print(f"DOT file written to: {dest}")
        os.system(f"xdot {dest} 2> /dev/null")
    else:
        print("Platform not supported yet!")
        exit(-1)

def cfg_iterator(filename):
    pause("[Control Flow Graph (CFG)]")
    print("==========================")
    files = collect_all_python_files(filename)
    print("Analyzing files:")
    for f in files:
        print(" -", f)
        show_control_flow_graph(f)
    
def show_concrete_syntax_tree(filename):
    pause("[Concrete Syntax Tree (CST)]")
    print("===============================")
    pycmd = get_python_cmd()
    xpath = os.path.join(os.path.dirname(__file__), "utilities", "cst2dot.py")
    os.system(
        f"{pycmd} {xpath} {filename}"
    )

def show_abstract_syntax_tree(filename):
    pause("[Abstract Syntax Tree (AST)]")
    print("==============================")
    pycmd = get_python_cmd()
    xpath = os.path.join(os.path.dirname(__file__), "utilities", "ast2dot.py")
    os.system(
        f"{pycmd} {xpath} {filename}"
    )

def show_disassembly(filename):
    pause("[Python Bytecode]")
    print("==================")
    pycmd = get_python_cmd()
    os.system(
        f"{pycmd} -m dis {filename}"
    )

def show_execution_trace(filename):
    pause("[Program Execution Trace]")
    print("==========================")
    pycmd = get_python_cmd()
    os.system(
        #f"{pycmd} -m trace --count --trace --missing --coverdir tests --summary {filename}"
        f"{pycmd} -m trace --count --trace --ignore-dir={os.path.dirname(os.__file__)} --missing --coverdir tests --summary {filename}"
    )

def show_step_by_step_trace(filename):
    pause("[Step-by-step Program Execution]")
    print("=================================")
    pycmd = get_python_cmd()
    xpath = os.path.join(os.path.dirname(__file__), "utilities", "detailed.py")
    os.system(
        f"{pycmd} {xpath} {get_mode()} {filename}"
    )

def show_ast_dump(parsed_ast):
    pause("[AST Hierarchy]")
    print("================")
    print(ast.dump(parsed_ast, indent=2))

# ============================================================
# Mode Handling
# ============================================================

def get_mode():

    if len(sys.argv) != 3:
        if len(sys.argv) == 2:
            mode='beginner'
        else:
            print(f'''{COLOR}Usage:
       tracerset [beginner] <file.py> 
       tracerset intermediate <file.py>
       tracerset advanced <file.py>{RESET}''')
            sys.exit(1)
    else:
        mode = sys.argv[1].lower()
    
    if mode not in MODES:
        print(f"{ERROR}Invalid mode:{RESET} {mode}")
        print(f"\nAvailable modes:{COLOR}")
        for m in MODES:
            print(f"{m}")
        print(f"{RESET}")
        sys.exit(1)

    return mode


def show_banner(mode):
    print("=" * 63)
    print("TracerSET")
    print("Execution-Centric Program Comprehension Environment for Python")
    print("=" * 63)

    print(f"\nSelected Mode : {SUCCESS}{mode.upper()}{RESET}")

    if mode == MODE_BEGINNER:
        print("Focus         : Variables, execution flow, runtime behavior")
    elif mode == MODE_INTERMEDIATE:
        print("Focus         : Runtime behavior + AST + execution trace")
    elif mode == MODE_ADVANCED:
        print("Focus         : Full compiler/runtime internals")
    print("=" * 63)


# ============================================================
# Main Driver
# ============================================================

def main():

    mode = get_mode()
    filename = sys.argv[len(sys.argv)-1]
    
    if filename.lower() in ['-v','-version','--v','--version']:
        print(f"{VER} - {TAG}")
        return
    elif filename.lower() in ['-h','-help','--help','--h']:
        print(f'''{COLOR}Usage:
       tracerset [beginner] <file.py> 
       tracerset intermediate <file.py>
       tracerset advanced <file.py>{RESET}''')
        return
    
    config = MODES[mode]
    show_banner(mode)
    
    # --------------------------------------------------------
    # Read source code
    # --------------------------------------------------------
    buff = read_source_code(filename)
    
    # --------------------------------------------------------
    # Parse AST
    # --------------------------------------------------------
    parsed = ast.parse(buff)

    # --------------------------------------------------------
    # Always show source code
    # --------------------------------------------------------
    show_source_code(buff)
    
    # -----------------------------
    # Cognitive Complexity Layer
    # -----------------------------
    show_cognitive_complexity(filename)
    
    # --------------------------------------------------------
    # Always show control flow graph
    # --------------------------------------------------------
    cfg_iterator(filename)

    # --------------------------------------------------------
    # ADVANCED MODE
    # --------------------------------------------------------
    if config["tokens"]:
        show_tokens(filename)
    if config["cst"]:
        show_concrete_syntax_tree(filename)
    if config["ast"]:
        show_abstract_syntax_tree(filename)
    if config["disassembly"]:
        show_disassembly(filename)

    # --------------------------------------------------------
    # INTERMEDIATE + ADVANCED
    # --------------------------------------------------------
    if config["execution_trace"]:
        show_execution_trace(filename)
    
    # --------------------------------------------------------
    # ALL MODES
    # --------------------------------------------------------
    if config["step_trace"]:
        show_step_by_step_trace(filename)


if __name__ == "__main__":
    # ============================================================
    # Exception Handling
    # ============================================================

    try:
        main()

    except OSError as ex:
        print(f"{ERROR}File Error:{RESET}")
        print(f"{ex.filename}: {ex.strerror}")

    except SyntaxError as ex:
        print(f"{ERROR}Syntax Error:{RESET}")
        print(
            f'In File "{sys.argv[1]}", line {ex.lineno}'
        )
        print(ex.text)
        print(
            f"{ex.__class__.__name__}: {ex.msg}"
        )

    except KeyboardInterrupt:
        print(f"\n{ERROR}Execution interrupted by user.{RESET}")
