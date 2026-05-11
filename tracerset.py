import ast
import sys
import tokenize
import os
import platform

# ============================================================
# TracerSET
# Progressive Python Program Analysis and Execution Tracer
# ============================================================

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
    print(f"\n{COLOR}Press Enter key to continue to {section_name}{RESET}")
    input()

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

def show_control_flow_graph(filename):
    pause("[Control Flow Graph (CFG)]")
    print("==========================")
    pycmd = get_python_cmd()
    os.system(
        f"{pycmd} -m python_ta.cfg {filename}"
    )
    fname=filename.split('/')[::-1][0]
    src=fname.replace(".py",".gv")
    dest=filename.replace(".py",".cfg.dot")
    os.system(f"rm -f *.svg; mv {src} {dest}")
    print(f"DOT file written to: {dest}")
    os.system(f"xdot {dest}")
    
def show_concrete_syntax_tree(filename):
    pause("[Concrete Syntax Tree (CST)]")
    print("===============================")
    pycmd = get_python_cmd()
    os.system(
        f"{pycmd} utilities/cst2dot.py {filename}"
    )

def show_abstract_syntax_tree(filename):
    pause("[Abstract Syntax Tree (AST)]")
    print("==============================")
    pycmd = get_python_cmd()
    os.system(
        f"{pycmd} utilities/ast2dot.py {filename}"
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
        f"{pycmd} -m trace --count --trace --missing --summary {filename}"
    )

def show_step_by_step_trace(filename):
    pause("[Step-by-step Program Execution]")
    print("=================================")
    pycmd = get_python_cmd()
    os.system(
        f"{pycmd} utilities/detailed.py {filename}"
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
       python3 tracerset.py beginner <file.py> 
       python3 tracerset.py intermediate <file.py>
       python3 tracerset.py advanced <file.py>{RESET}''')
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
    print("=" * 60)
    print("TracerSET")
    print("Python Program Analysis and Execution Tracer")
    print("=" * 60)

    print(f"\nSelected Mode : {SUCCESS}{mode.upper()}{RESET}")

    if mode == MODE_BEGINNER:
        print("Focus         : Variables, execution flow, runtime behavior")
    elif mode == MODE_INTERMEDIATE:
        print("Focus         : Runtime behavior + AST + execution trace")
    elif mode == MODE_ADVANCED:
        print("Focus         : Full compiler/runtime internals")
    print("=" * 60)


# ============================================================
# Main Driver
# ============================================================

def main():

    mode = get_mode()
    filename = sys.argv[len(sys.argv)-1]
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
    
    # --------------------------------------------------------
    # Always show control flow graph
    # --------------------------------------------------------
    show_control_flow_graph(filename)

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
