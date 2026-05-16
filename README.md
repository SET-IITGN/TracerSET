# TracerSET

**TracerSET — Execution-Centric Program Comprehension Environment for Python**
TracerSET is a [program comprehension](https://en.wikipedia.org/wiki/Program_comprehension) tool that provides multiple coordinated views of Python program behavior by combining lexical structure, syntactic structure, control-flow representation, bytecode analysis, and runtime execution tracing. It enables step-by-step exploration of program execution while presenting static program representations as whole-program views, allowing users to understand how source code structure relates to execution behavior over time.

---

## Key Idea
Program understanding typically relies on separate tools and views:
- Source-level debugging (runtime execution)
- Static structure analysis (AST / CST)
- Control-flow reasoning (CFG)
- Bytecode inspection
- Execution tracing tools

TracerSET integrates these perspectives in a single environment where:
- runtime execution is step-by-step,
- static representations are computed as a single pass over the program,
- and both are presented together to support program comprehension.
---

## Features
- Step-by-step execution tracing of Python programs
- Runtime stack visualization
- Local and global variable inspection
- Source code highlighting during execution
- Token-level analysis (advanced mode)
- Concrete Syntax Tree (CST) visualization
- Abstract Syntax Tree (AST) visualization
- Control Flow Graph (CFG) generation
- Python bytecode disassembly
- Execution tracing via Python `trace` module
- Progressive learning modes:
  - Beginner
  - Intermediate
  - Advanced
---

## Usage
```
python3 tracerset.py <file.py> #defaults to beginner
python3 tracerset.py beginner <file.py>
python3 tracerset.py intermediate <file.py>
python3 tracerset.py advanced <file.py>
```

### ```beginner```
Focuses on:
- Source code execution
- Runtime stack visualization
- Variable state inspection
- Step-by-step execution flow

### ```intermediate```
Adds:
- AST visualization (static whole-program view)
- Execution trace analysis
- Combined static + dynamic execution understanding

### ```advanced```
Provides full internal program representation:
- Tokens (static analysis)
- Concrete Syntax Tree (CST)
- Abstract Syntax Tree (AST)
- Control Flow Graph (CFG)
- Bytecode disassembly
- Execution trace
- Step-by-step runtime execution state inspection
---

## Screenshots
**Version 1.0.2**
<img width="1920" height="867" alt="TracerSET Screenshot" src="https://github.com/user-attachments/assets/5f844c58-260c-43d5-b75c-43dd4f446dc3" />

---

## Video Demonstrations
**Version 1.0.2**
- [Recursive program execution](https://drive.google.com/file/d/1MAl578WOT7DtDi_TZLdOyqpdHjXAL0Q5/view?usp=sharing)
- [Programs using imports](https://drive.google.com/file/d/1UqJ2msjRhtzBqg6Dex_61MBzc8nuI8yQ/view?usp=sharing)
- More demonstrations coming soon

---
## System Requirements
- Python >=3.10
- Linux / Windows

## Dependencies
### Core dependencies
```
graphviz
libcst
python_ta
xdot
pytest
```
---
## Design Philosophy
TracerSET is built on the principle of execution-centric program comprehension, where:
- Static program structure (AST, CFG, bytecode) is computed as whole-program representations
- Dynamic runtime behavior (stack, variables, execution trace) is observed step-by-step

These two perspectives are presented together to help users connect program structure with program behavior during execution. This enables users to observe not only what a program executes, but how its execution unfolds over time.

---

## Limitations
- Currently supports Python programs only.
- Execution incurs runtime overhead due to tracing and static analysis.
- Best suited for small to medium-sized programs used for education and program comprehension.
- May produce large outputs for complex or deeply recursive programs.
- Trace behavior may vary across Python interpreter versions and runtime environments.
- Bytecode disassembly is based on the CPython virtual machine and may not generalize to other Python implementations such as PyPy or Jython.
- Not intended as a replacement for production-grade debuggers or performance profilers.
- Some visualization features depend on external tools such as Graphviz and xdot.
- Certain advanced Python features (e.g., concurrency, dynamic code execution patterns) may not be fully supported.
---

## Responsible Use Notice
During the preparation of the content in this repository, the developers were assisted by Generative AI tools to some extent. The content was reviewed and edited as needed and developers take full responsibility for the content in this repository. Regardless of this, bugs may still exist!

## Contact
Shouvick Mondal  
shouvick.mondal@iitgn.ac.in
