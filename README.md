# TracerSET v1.1.5

**Execution-Centric Program Comprehension Environment for Python**

TracerSET is a [program comprehension](https://en.wikipedia.org/wiki/Program_comprehension) tool that aggregates multiple complementary views of Python program behavior, including lexical structure, syntactic structure, cognitive complexity, control-flow representation, bytecode analysis, and runtime execution tracing. It enables step-by-step exploration of program execution while presenting static program representations as whole-program views, allowing users to understand how source code structure relates to execution behavior over time.

---
## System Requirements
- Python >=3.10
- Linux / Windows
- Download from [here](https://github.com/SET-IITGN/TracerSET/releases/download/v1.1.5/tracerset-1.1.5-py3-none-any.whl), and Install from the same directory using ```pip3 install tracerset-1.1.5-py3-none-any.whl```
- Uninstall using ```pip3 uninstall tracerset-1.1.5-py3-none-any.whl```

### Other dependencies
(non-exhaustive)
```
graphviz
libcst
python_ta
xdot
pytest
complexipy
```
---
## Table of Contents
- [Key Idea](#key-idea)
- [Features](#features)
- [Usage](#usage)
  - [Beginner](#beginner)
  - [Intermediate](#intermediate)
  - [Advanced](#advanced)
- [Screenshots](#screenshots)
- [Video Demonstrations](#video-demonstrations)
- [System Requirements](#system-requirements)
- [Design Philosophy](#design-philosophy)
- [Notes on Python Bytecode and Runtime Behavior](#notes-on-python-bytecode-and-runtime-behavior)
- [Limitations](#limitations)
- [Responsible Use Notice](#responsible-use-notice)
- [Contact](#contact)

---

## Key Idea
Program understanding typically relies on separate tools and views:
- Source-level debugging (runtime execution)
- Static structure analysis (AST, CST)
- Control-flow reasoning (CFG)
- Cognitive complexity analysis
- Bytecode inspection
- Execution tracing tools

TracerSET presents these perspectives in a single environment where:
- runtime execution is step-by-step,
- static representations are computed as a single pass over the program,
- and static and dynamic views are presented sequentially, with execution occurring after structural analysis.
---

## Features
- Step-by-step execution tracing of Python programs
- Runtime stack visualization
- Local and global variable inspection
- Variable states shown before each statement executes
- Scope and alias views reflect runtime state at each execution step, based on frame reachability rather than object storage structure
- Source code highlighting during execution
- Token stream analysis (whole-program and execution-aligned views)
- Concrete Syntax Tree (CST) visualization
- Abstract Syntax Tree (AST) analysis (whole-program and execution-aligned views)
- Control Flow Graph (CFG) generation
- Python bytecode analysis (whole-program and execution-aligned views)
- Execution tracing via Python `trace` module
- Alias sets (advanced mode)
- Cognitive complexity score
- Progressive learning modes:
  - Beginner
  - Intermediate
  - Advanced
---

## Usage
```
tracerset <file.py> #defaults to beginner
tracerset beginner <file.py>
tracerset intermediate <file.py>
tracerset advanced <file.py>
```

### ```beginner```
Focuses on **basic runtime understanding of program execution**.

This mode is designed for first-time programmers to understand how a Python program runs step by step.

Includes:
- Source code display
- Control Flow Graph (CFG)
- Step-by-step program execution trace (custom detailed tracer)
- Cognitive complexity analysis (function-level complexity metrics via external analyzers)

At this stage, the learner primarily observes execution flow and control structure. No internal program representations are shown.

### ```intermediate```
Focuses on **connecting program structure with runtime execution**.

This mode builds on beginner by introducing structural understanding of the program while still emphasizing execution.

Includes:
- Source code display
- Control Flow Graph (CFG)
- Abstract Syntax Tree (AST) visualization
- Program execution trace (Python trace module output)
- Step-by-step program execution trace (custom detailed tracer)
- Cognitive complexity analysis (function-level complexity metrics via external analyzers)

This stage helps the learner connect:
- how the program is structured (AST)
- how the program executes (trace + step-by-step execution)

Tokens, CST, and bytecode are not introduced yet.

### ```advanced```
Focuses on **full internal representation of programs and execution behavior**.

This mode exposes both compiler-level structure and detailed runtime behavior for deep analysis.

Includes:
- Source code display
- Control Flow Graph (CFG)
- Whole-program token stream analysis
- Execution-aligned token stream visualization
- Concrete Syntax Tree (CST)
- Whole-program Abstract Syntax Tree (AST)
- Execution-aligned AST visualization
- Whole-program Python bytecode disassembly
- Execution-aligned VM instruction visualization
- Program execution trace (Python trace module output)
- Step-by-step program execution trace (custom detailed tracer)
- Execution-aligned Alias sets (ALIAS)
- Cognitive complexity analysis (function-level complexity metrics via external analyzers)

This final stage provides complete visibility into:
- lexical structure (whole-program and execution-aligned token views)
- syntactic structure (CST and AST)
- control-flow structure (CFG)
- bytecode-level representation (whole-program and execution-aligned views)
- runtime execution behavior

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
## Design Philosophy
TracerSET is built on the principle of execution-centric program comprehension, where:
- Static program structure (tokens, CST, AST, CFG, cognitive complexity, bytecode) is computed as whole-program representations
- Dynamic runtime behavior (stack, variables, aliases, execution trace, execution-aligned AST nodes, execution-aligned token streams, and execution-aligned VM instructions) is observed step-by-step
    
These two perspectives are presented in sequence, enabling users to first understand program structure and then observe its runtime behavior during execution. This enables users to observe not only what a program executes, but how its execution unfolds over time.

---

## Notes on Python Bytecode and Runtime Behavior

TracerSET computes whole-program CPython bytecode disassembly and exposes execution-aligned VM instructions associated with each executed source line during tracing.

The displayed VM instructions are not simplified, hidden, or normalized.
This is intentional because:

- A single source statement may compile into multiple bytecode instructions.
- Function calls may compile into multiple CPython VM instructions, including `PUSH_NULL`, `PRECALL`, `CALL`, `POP_TOP`, and implicit `RETURN_VALUE`.
- Different Python versions may generate different instruction sequences.
- The bytecode format and execution semantics are implementation-dependent.

Therefore, execution traces shown by TracerSET should be interpreted as
the actual runtime/compiler behavior of the underlying Python interpreter
(primarily CPython), rather than as a language-level abstraction.

## Limitations
- Currently supports Python programs only.
- Execution incurs runtime overhead due to tracing and analysis.
- Best suited for small to medium-sized programs used for education and program comprehension.
- Large or deeply recursive programs may produce verbose traces.
- Trace behavior, bytecode, and VM instruction sequences may vary across Python versions and runtime environments.
- Bytecode disassembly and VM-level execution views are CPython-specific and may not generalize to implementations such as PyPy or Jython.
- A single source line may map to multiple VM instructions, and mappings are interpreter-dependent.
- Execution-aligned views are driven by Python tracing events and source-line mappings. Multi-line expressions, comprehensions, generator expressions, lambdas, and other compiler-generated constructs may produce execution events that do not correspond to complete source-level statements, reflecting the behavior of the underlying Python interpreter.
- Dynamic features such as `exec`, `eval`, metaprogramming, and runtime code generation may reduce trace precision.
- Advanced concurrency features (threads, multiprocessing, async execution) are not fully supported; tracing is limited to the currently executing Python thread and frame context, without coverage of inter-process execution or event-loop-level scheduling.
- Not intended as a replacement for production-grade debuggers or profilers.
- Some visualization features depend on external tools such as Graphviz and xdot.
- Cognitive complexity analysis relies on external tooling and may vary across tool versions and environments.
---

## Responsible Use Notice
During the preparation of the content in this repository, the developers were assisted by Generative AI tools to some extent. The content was reviewed and edited as needed and developers take full responsibility for the content in this repository. Regardless of this, bugs may still exist!

## Contact
Shouvick Mondal  
shouvick.mondal@iitgn.ac.in
