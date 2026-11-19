"""Optional JSON recording for TracerSET's existing custom tracer.
Set TRACERSET_JSON to a NEW output filename. No sys.settrace or stdout hooks.
"""
import ast
from datetime import datetime, timezone
#from itertools import islice
import json
import os
import sys
import time


def type_name(value):
    try:
        cls = type(value)
        return type.__getattribute__(cls, "__module__") + "." + type.__getattribute__(cls, "__qualname__")
    except Exception:
        return "unknown"

'''
class Snapshot:
    def __init__(self, depth=4, items=50, chars=4000, budget=5000):
        self.depth, self.items, self.chars, self.budget = depth, items, chars, budget

    def copy(self, value, depth=0, seen=frozenset()):
        if self.budget <= 0:
            return {"truncated": "event_snapshot_budget"}
        self.budget -= 1
        kind = type(value)
        if value is None or kind is bool:
            return value
        if kind is int:
            return value if value.bit_length() <= 1024 else {"type": "int", "bits": value.bit_length()}
        if kind is float:
            return {"type": "float", "value": str(value)}
        if kind is str:
            if len(value) <= self.chars:
                return value
            return {"type": "str", "value": value[:self.chars], "length": len(value), "truncated": True}
        result = {"type": type_name(value), "object_id": hex(id(value))}
        if kind is bytes:
            result.update(hex=value[:self.chars].hex(), length=len(value), truncated=len(value) > self.chars)
            return result
        if kind not in (dict, list, tuple, set, frozenset):
            result["opaque"] = True
            return result
        result["length"] = len(value)
        if id(value) in seen:
            result["cycle"] = True
            return result
        if depth >= self.depth:
            result["truncated"] = "depth"
            return result
        seen = seen | {id(value)}
        if kind is dict:
            result["entries"] = [{"key": self.copy(k, depth+1, seen), "value": self.copy(v, depth+1, seen)}
                                 for k, v in islice(value.items(), self.items)]
        else:
            result["items"] = [self.copy(v, depth+1, seen) for v in islice(value, self.items)]
        result["truncated"] = len(value) > self.items
        return result

    def bindings(self, values):
        return {k: self.copy(v) for k, v in islice(values.items(), 200) if type(k) is str}
'''
class Snapshot:
    def copy(self, value, depth=0, seen=frozenset()):
        kind = type(value)

        if value is None or kind is bool:
            return value

        if kind is int:
            return value

        if kind is float:
            return {
                "type": "float",
                "value": str(value),
            }

        if kind is str:
            return value

        result = {
            "type": type_name(value),
            "object_id": hex(id(value)),
        }

        if kind is bytes:
            result.update(
                hex=value.hex(),
                length=len(value),
                truncated=False,
            )
            return result

        if kind not in (dict, list, tuple, set, frozenset):
            result["opaque"] = True
            return result

        result["length"] = len(value)

        if id(value) in seen:
            result["cycle"] = True
            return result

        seen = seen | {id(value)}

        if kind is dict:
            result["entries"] = [
                {
                    "key": self.copy(key, depth + 1, seen),
                    "value": self.copy(item, depth + 1, seen),
                }
                for key, item in value.items()
            ]
        else:
            result["items"] = [
                self.copy(item, depth + 1, seen)
                for item in value
            ]

        result["truncated"] = False
        return result

    def bindings(self, values):
        return {
            name: self.copy(value)
            for name, value in values.items()
            if type(name) is str
        }

class EventRecorder:
    """Streams a single JSON document; failures disable recording, not tracing."""
    def __init__(self):
        self.stream = None
        self.count = 0
        self.errors = 0
        self.started = time.monotonic_ns()
        self.warned = False

    def warning(self, exc):
        self.errors += 1
        if not self.warned:
            self.warned = True
            try:
                sys.stderr.write("TracerSET JSON recording warning: " + type_name(exc) + "\n")
            except Exception:
                pass

    @classmethod
    def for_script(cls, script, mode):
        recorder = cls()

        # Automatically record only in advanced mode.
        if mode.lower() != "advanced":
            return recorder

        script_path = os.path.abspath(script)
        script_stem = os.path.splitext(script_path)[0]
        destination = script_stem + "-tracerset.json"

        try:
            recorder.stream = open(destination, "w", encoding="utf-8")
            header = {"schema": "tracerset.custom-trace.v1", "event_source": "custom_detailed_tracer",
                      "script": os.path.abspath(script), "mode": mode, "python": sys.version,
                      "started_utc": datetime.now(timezone.utc).isoformat(),
                      "scope": "existing custom tracer filters; current thread",
                      "semantics": {"line": "before reported source line execution", "bytecode": "static source-line association, not observed opcode execution",
                                    "return": "may also represent generator suspension or exception unwinding",
                                    "identity": "process-local; IDs may be reused after object destruction"},
                      #"snapshot_limits": {"depth": 4, "container_items": 50, "string_chars": 4000,
                      #                    "bindings_per_scope": 200, "value_nodes_per_event": 5000},
                      "snapshot_limits": {
                          "depth": None,
                          "container_items": None,
                          "string_chars": None,
                          "bindings_per_scope": None,
                          "value_nodes_per_event": None,
                      },                      
                      #"snapshot_policy": "exact builtins copied; arbitrary objects opaque; no custom repr invoked by recorder",
                      "snapshot_policy": (
                          "exact builtins copied without application-defined truncation; "
                          "circular references marked; arbitrary objects opaque; "
                          "no custom repr invoked by recorder"
                      ),                      
                      "terminal_transcript": False, "target_stdout_captured": False}
            prefix = json.dumps(header, ensure_ascii=True, allow_nan=False)
            recorder.stream.write(prefix[:-1] + ', "events": [\n')
            recorder.stream.flush()
        except Exception as exc:
            recorder.warning(exc)
            if recorder.stream is not None:
                try:
                    recorder.stream.close()
                except Exception:
                    pass
            recorder.stream = None
        return recorder
    '''
    def ast_fragment(self, node, line, remaining, depth=0):
        if node is None:
            return None
        if remaining[0] <= 0 or depth >= 40:
            return {"truncated": True}
        remaining[0] -= 1
        if hasattr(node, "lineno") and node.lineno != line:
            return None
        result = {"type": type(node).__name__}
        for key in ("lineno", "col_offset", "end_lineno", "end_col_offset", "name", "id", "arg", "attr"):
            value = getattr(node, key, None)
            if type(value) in (str, int):
                result[key] = value
        if isinstance(node, ast.Constant):
            result["constant"] = Snapshot().copy(node.value)
        children = []
        for child in ast.iter_child_nodes(node):
            if not hasattr(child, "lineno") or child.lineno == line:
                if remaining[0] <= 0:
                    children.append({"truncated": True})
                    break
                children.append(self.ast_fragment(child, line, remaining, depth+1))
        result["children"] = children
        return result
    '''
    def ast_fragment(self, node, line):
        if node is None:
            return None

        if hasattr(node, "lineno") and node.lineno != line:
            return None

        result = {
            "type": type(node).__name__,
        }

        for key in (
            "lineno",
            "col_offset",
            "end_lineno",
            "end_col_offset",
            "name",
            "id",
            "arg",
            "attr",
        ):
            value = getattr(node, key, None)

            if type(value) in (str, int):
                result[key] = value

        if isinstance(node, ast.Constant):
            result["constant"] = Snapshot().copy(node.value)

        children = []

        for child in ast.iter_child_nodes(node):
            if not hasattr(child, "lineno") or child.lineno == line:
                children.append(
                    self.ast_fragment(child, line)
                )

        result["children"] = children
        return result
            
    def record(self, event, frame, *, depth, stack, locals_view=None, globals_view=None,
               aliases=None, signature=None, arg=None, advanced=False, tokens=None,
               ast_root=None, instructions=None):
        if self.stream is None:
            return
        try:
            snap = Snapshot()
            record = {"sequence": self.count + 1, "event": event,
                      "elapsed_ns": time.monotonic_ns() - self.started,
                      "location": {"file": os.path.abspath(frame.f_code.co_filename),
                                   "line": frame.f_lineno, "function": frame.f_code.co_name,
                                   "code_first_line": frame.f_code.co_firstlineno},
                      "frame_object_id": hex(id(frame)), "call_depth": depth,
                      "stack_display_order": "outermost_first", "stack": stack,
                      "signature_display": signature,
                      "locals_and_globals_same_namespace": frame.f_locals is frame.f_globals}
            import linecache
            record["source"] = linecache.getline(frame.f_code.co_filename, frame.f_lineno).rstrip("\r\n")
            if locals_view is not None:
                record["locals_display_values"] = snap.bindings(locals_view)
                record["globals_display_values"] = snap.bindings(globals_view)
                record["binding_counts"] = {"locals": len(locals_view), "globals": len(globals_view)}
                '''
                record["binding_identity"] = {
                    "locals": {k: hex(id(frame.f_locals[k])) for k in islice(locals_view, 200) if k in frame.f_locals},
                    "globals": {k: hex(id(frame.f_globals[k])) for k in islice(globals_view, 200) if k in frame.f_globals}}
                '''
                record["binding_identity"] = {
                    "locals": {
                        k: hex(id(frame.f_locals[k]))
                        for k in locals_view
                        if k in frame.f_locals
                    },
                    "globals": {
                        k: hex(id(frame.f_globals[k]))
                        for k in globals_view
                        if k in frame.f_globals
                    },
                }                
            if advanced and aliases is not None:
                record["aliases_display"] = aliases
                record["alias_scope"] = "existing custom tracer's selected direct bindings, including singletons"
            if event == "line":
                record["timing"] = "before_reported_line_execution"
                if advanced:
                    record["context"] = {"association": "source_line_not_opcode_observation",
                        "tokens_display": tokens or [],
                        #"ast_fragment": self.ast_fragment(ast_root, frame.f_lineno, [1000]),
                        "ast_fragment": self.ast_fragment(ast_root, frame.f_lineno),                        
                        "bytecode": [{"offset": ins.offset, "opname": ins.opname, "arg": ins.arg,
                                      "argval": snap.copy(ins.argval), "starts_line": ins.starts_line}
                                     for ins in (instructions or [])]}
            elif event == "return":
                record["return_value"] = snap.copy(arg)
            elif event == "exception":
                record["exception"] = {"type": type_name(arg[1]), "value": snap.copy(arg[1]),
                                       "args": snap.copy(BaseException.args.__get__(arg[1])),
                                       "handled": "unknown_at_event"}
            payload = json.dumps(record, ensure_ascii=True, allow_nan=False)
            self.stream.write((",\n" if self.count else "") + payload)
            self.stream.flush()
            self.count += 1
        except Exception as exc:
            self.warning(exc)

    def close(self):
        if self.stream is None:
            return
        try:
            summary = {"recorded_events": self.count, "recording_errors": self.errors,
                       "finalized": True, "target_success": "not_inferred_from_existing_exception_handlers"}
            self.stream.write('\n], "summary": ' + json.dumps(summary) + '}\n')
            self.stream.flush()
        except Exception as exc:
            self.warning(exc)
        finally:
            try:
                self.stream.close()
            except Exception:
                pass
            self.stream = None
