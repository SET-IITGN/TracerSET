# TracerSET

**TracerSET — Unified Multi-Level Program Execution Tracer for Program Comprehension**

TracerSET is a program comprehension tool that provides unified, multi-level views of program execution by integrating lexical structure, syntactic structure, control-flow, bytecode, and runtime execution state into a single interactive tracing environment.

It enables step-by-step exploration of program behavior by aligning static program representations with dynamic runtime execution, allowing users to understand how source code evolves into execution behavior.

---

## Key Idea

Program understanding typically relies on separate tools and views:
- Source-level debugging (runtime execution)
- Static structure analysis (AST / CST)
- Control-flow reasoning (CFG)
- Bytecode inspection
- Execution tracing tools

TracerSET unifies these perspectives into a single execution-driven workflow, where all views are aligned to the same execution step.

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
### Modes

#### ```beginner```

Focuses on:

- Source code execution
- Runtime stack visualization
- Variable state inspection
- Step-by-step execution flow


#### ```intermediate```

Adds:

- AST visualization
- Execution trace analysis
- Combined static + dynamic execution views


#### ```advanced```

Provides full internal program representation:

- Tokens
- Concrete Syntax Tree (CST)
- Abstract Syntax Tree (AST)
- Control Flow Graph (CFG)
- Bytecode disassembly
- Execution trace
- Step-by-step execution with full state inspection

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

- Python 3.10 – 3.12
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

- Static program structure (AST, CFG, bytecode)
- Dynamic runtime behavior (stack, variables, execution trace)

are unified along a single execution timeline.

This enables users to observe not only what a program executes, but how and why its behavior emerges during execution.

---

## Limitations

- Currently supports Python programs only.
- Execution incurs runtime overhead due to tracing, AST / CST analysis, and runtime introspection.
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
