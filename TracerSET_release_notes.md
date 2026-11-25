# TracerSET 1.2.6 release notes

Changes from 1.2.5. Python 3.10 or later, as before.

## Fixes

### Value display
- `LOCALS`, `GLOBALS` and `RETurned` now agree for the same value. In a 50-case probe where a function binds a global to a local and returns it, the three views agreed in 33 of 50 cases on 1.2.5 and in 50 of 50 on 1.2.6.
- Return values print through the same display path as the scope views, so they no longer show a raw `repr` with a memory address for user-defined objects. Return values containing an address text fell from 15 of 50 to 1 of 50 (the one remaining case is a built-in `memoryview`).
- User-defined objects nested inside another object's fields print as a short label, for example `<Plain object>{'x': <Plain object>}`. Built-in types such as `list` and `memoryview` print as Python prints them.
- A plain string whose text contains ` object ` or `<class` (for example `'an object label'`) is shown literally and is no longer rewritten as an object.
- Lists are snapshotted once per display, so the same list appearing in several places shows the same contents, and a list's own elements are not treated as open files.
- When a frame's locals and globals are the same namespace (module level), the globals display reuses the locals display.
- Recorded events no longer treat subclasses of `dict`, `list`, `tuple`, `set` and `frozenset` as plain containers, and the type name recorded for a value no longer depends on a user-defined `__module__` or `__qualname__`.

### Python 3.13 and later
- On Python 3.13 and later, the bytecode instructions associated with each traced line (`VM INS`) are shown. On 1.2.5 and Python 3.13 to 3.15, the 48-program suite produced 54 bytecode sections in advanced mode; on 1.2.6 it produces 546 to 548. Python 3.10 to 3.12 output is unchanged.
- Recorded instruction line numbers use the 3.13+ `line_number` field when it exists.

### Output
- Output redirected to a file or pipe now appears in reading order, and long lines are no longer cut mid-line by the output buffer. On the 48-program suite, 36 advanced-mode logs on 1.2.5 (12 each on Python 3.11, 3.12 and 3.13) had lines cut; 1.2.6 has none.
- Interactive pauses wait for a key only when both standard input and standard output are terminals.
- Standard output uses UTF-8, so redirected output on Windows no longer stops at the first box-drawing character.
- Target files, and the temporary file for piped input, are read and written as UTF-8.

### Command line and files
- The console command calls a new `cli()` entry point; `pyproject.toml` now points to `tracerset.tracerset:cli`. Running `python tracerset.py` is unchanged.
- A `SyntaxError` in the target now reports the file that contains it, including imported local modules, instead of always naming the command-line file.
- Generated file names (`.gv`, `.cfg.dot`, `.cfg.png`, `.ast.dot`, `.cst.dot`) replace only the file extension. A file name containing `.py` elsewhere no longer produces the wrong output name.

### Repository
- `make clean` removes `build/`, `dist/`, `tracerset.egg-info/`, the pytest and complexipy caches and generated `.png` files, and does not delete tracked files.
- `.gitignore` lists the build output and cache folders.
- README: usage block lists `-v` and `-h`; notes on piped input, tracing limited to the main thread, generated files, CFG limitations, and Graphviz and xdot behavior.

## Testing
- 48-program suite: 48 passed on Python 3.10, 3.11, 3.12, 3.13, 3.14 and 3.15 (Linux x86_64).
- Compared with 1.2.5 on that suite: 2,304 captured outputs, 0 with different content; the differences are line order with redirected output (1,116), cut lines in 1.2.5 (36), and the bytecode sections above.
- 50-case value matrix: 50 of 50 agree on all six Python versions on Linux, and in simulated macOS and Windows runs.
- 1,440 stress runs (plain and three modes, six Python versions) completed with no timeouts or crashes in the tool.

## Known limitations
- The output of `memoryview` and similar built-in values still includes the address Python prints.
- A user-defined object stored inside a list or tuple on another object still shows its address.
- CFG generation does not model `finally` blocks or `async def`, and has no handling for syntax that exists only in Python 3.15.
- On macOS, the control-flow graph step does not write `<stem>.cfg.dot`; on Windows, AST and CST generation opens the image viewer. These two were noted, not changed.
- Windows and macOS were tested by simulation on Linux only; native runs have not been done.
- Tracing remains limited to the main thread. Target programs that read standard input in intermediate or advanced mode see it consumed by the first execution.
