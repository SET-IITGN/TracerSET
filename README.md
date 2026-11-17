# TracerSET v1.2.2

**Execution-Centric Program Comprehension Environment for Python**

TracerSET is a [program comprehension](https://en.wikipedia.org/wiki/Program_comprehension) environment for Python that combines complementary structural representations with runtime execution inspection.
It provides token, syntax-tree, control-flow, cognitive-complexity, and bytecode views alongside step-by-step execution tracing. Selected token, AST, and bytecode views are associated with traced source lines, helping users explore relationships between program structure and concrete execution behavior. These associations do not imply that every displayed structural element was evaluated during that execution step.

---
## System Requirements
- Python >=3.10
- - Linux, Windows, and macOS; visualization and artifact-opening behavior  varies by platform.
- Download from [here](https://github.com/SET-IITGN/TracerSET/releases/download/v1.2.2/tracerset-1.2.2-py3-none-any.whl), and Install using ```pip3 install tracerset-1.2.2-py3-none-any.whl```
- Uninstall using ```pip3 uninstall tracerset-1.2.2-py3-none-any.whl```

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
- structural analyses and representations are presented before traced execution
- runtime behavior is inspected through tracing events
- selected token, AST, and bytecode information is associated with traced source lines
---

## Features
- Step-by-step execution tracing of Python programs
- Runtime stack visualization
- Local and global variable inspection
- Local and global binding inspection at runtime tracing events
- At displayed line events, variable state is inspected before execution associated with the reported source line
- Advanced-mode alias sets grouping selected local and global bindings that refer to the same object
- Runtime scope views represent bindings visible from the inspected frame, not physical object-storage locations
- Source code highlighting during execution
- Token stream analysis (whole-program and execution-aligned views)
- Concrete Syntax Tree (CST) visualization
- Abstract Syntax Tree (AST) analysis (whole-program and execution-aligned views)
- Control Flow Graph (CFG) generation
- Python bytecode disassembly and source-line-associated instruction views
- Execution tracing via Python `trace` module
- Alias sets (advanced mode)
- Cognitive complexity score
- Progressive learning modes:
  - Beginner (default)
  - Intermediate
  - Advanced
---

## Usage
```
tracerset [file.py] #reads from terminal (stdin) if no file provided, mode defaults to beginner if no mode provided
tracerset beginner [file.py] #reads from terminal (stdin) if no file provided
tracerset intermediate [file.py] #reads from terminal (stdin) if no file provided
tracerset advanced [file.py] #reads from terminal (stdin) if no file provided
```

### Execution Behavior

Beginner mode runs the target through the custom detailed tracer. Intermediate and advanced modes run the target separately through Python's `trace` module and then through the custom detailed tracer. These are separate executions, not two views of one recorded run. Programs may request input or produce side effects more than once. Randomness, time-dependent values, files, and other external state may
differ between runs. Interactive pauses are enabled when standard input is a terminal. When source is supplied through stdin, input is read until EOF.

### ```beginner``` mode
Focuses on **basic runtime understanding of program execution**.

This mode (default) is designed for first-time programmers to understand how a Python program runs step by step.

Includes:
- Source code display and highlighting
- Step-by-step execution-event display
- Local and global variable inspection
- Runtime stack display
- Return-value and exception reporting

At this stage, the learner primarily observes execution flow. Token, syntax-tree, CFG, and bytecode views are not introduced in this mode.

### ```intermediate``` mode
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

### ```advanced``` mode
Focuses on **detailed structural representations and runtime behavior**.

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

This mode brings together complementary perspectives on:
- Token information selected by traced source line
- Selected AST fragments associated with traced source lines
- Bytecode instructions associated with traced source lines in the current code object
- Alias sets for selected direct local/global bindings

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
TracerSET organizes program comprehension around three complementary
kinds of information:

1. Structural context:
   tokens, CST, AST, CFG, cognitive complexity, and bytecode disassembly

2. Runtime observations:
   execution events, stack context, variable bindings, return values, and exceptions

3. Execution-associated representations:
   selected token, AST, and bytecode information mapped to traced source lines

Alias sets are derived from object identity among selected bindings in the inspected frame's local and global namespaces.

Structural views provide context for interpreting runtime behavior. Source-line association does not establish that every displayed token, AST element, or bytecode instruction was evaluated.

---

## Notes on Python Bytecode and Runtime Behavior

TracerSET provides CPython bytecode disassembly and, in advanced mode, displays instructions associated with traced source lines in the current code object.

The execution-associated VM view is based on source-line mappings. It is not an instruction-by-instruction record of observed opcode execution. A displayed instruction's association with a traced line does not establish that it executed during that visit.

Important considerations:
- One source line may correspond to multiple instructions
- Control flow may execute only part of the code associated with a line
- Instruction sequences and source mappings vary across Python versions
- Some instruction details are omitted or formatted for presentation
- Bytecode is interpreter-specific and should not be treated as a portable language-level representation

Interpret this view as compiler-generated instructions associated with an execution location, alongside the separately observed runtime state.

### Analysis Scope

In this documentation, whole-input views refer to analysis of the supplied source file. Some structural analyses additionally discover selected local Python modules. Coverage of imported code differs between analyses and is not comprehensive.

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
- Different views may cover different file sets. Local-import discovery is limited and does not implement complete Python package/import resolution.
- Token alignment uses token starting lines. AST alignment uses node starting lines and displays selected fragments. Multiple statements on one line, multiline constructs, and nested code objects can limit correspondence.
- Alias sets cover selected direct bindings in the current frame's local and global namespaces. They do not recursively enumerate references through containers, attributes, or all other frames.
- Object inspection and formatting may invoke user-defined representation or attribute-access behavior. Tracing and inspection are not guaranteed to be observationally neutral.
- The detailed tracer executes the target within a constructed execution environment. It does not reproduce every aspect of direct script execution, including target-specific command-line argument handling.
- Current output consists of terminal displays and generated analysis artifacts. A structured JSON/JSONL execution-event export is not provided.
---

## Responsible Use Notice
During the preparation of the content in this repository, the developers were assisted by Generative AI tools to some extent. The content was reviewed and edited as needed and developers take full responsibility for the content in this repository. Regardless of this, bugs may still exist!

## Contact
Shouvick Mondal  
shouvick.mondal@iitgn.ac.in
