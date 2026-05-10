# Generating a Graphviz DOT File from a Python CST
import libcst as cst
import sys
import os


class CSTDotGenerator:
    def __init__(self):
        self.node_counter = 0
        self.lines = []

    def new_id(self):
        node_id = f"node{self.node_counter}"
        self.node_counter += 1
        return node_id

    def escape(self, text):
        return str(text).replace('"', '\\"')

    def resolve_import_file(self, module_name, current_file):
        base_dir = os.path.dirname(
            os.path.abspath(current_file)
        )

        candidate = os.path.join(
            base_dir,
            module_name.replace(".", os.sep) + ".py"
        )

        if os.path.exists(candidate):
            return os.path.abspath(candidate)

        return None

    def collect_imports(self, node, current_file):

        imported_files = []

        def walk(n):

            if isinstance(n, cst.Import):

                for alias in n.names:

                    if isinstance(alias, cst.ImportAlias):

                        module_name = alias.name.value

                        imported = self.resolve_import_file(
                            module_name,
                            current_file
                        )

                        if imported:
                            imported_files.append(imported)

            elif isinstance(n, cst.ImportFrom):

                if n.module:

                    module_name = ""

                    if isinstance(n.module, cst.Name):

                        module_name = n.module.value

                    elif isinstance(n.module, cst.Attribute):

                        parts = []

                        current = n.module

                        while isinstance(current, cst.Attribute):

                            if isinstance(current.attr, cst.Name):
                                parts.append(current.attr.value)

                            current = current.value

                        if isinstance(current, cst.Name):
                            parts.append(current.value)

                        parts.reverse()

                        module_name = ".".join(parts)

                    if module_name:

                        imported = self.resolve_import_file(
                            module_name,
                            current_file
                        )

                        if imported:
                            imported_files.append(imported)

            for child in n.children:

                if isinstance(child, cst.CSTNode):
                    walk(child)

        walk(node)

        return imported_files

    def visit(self, node, parent=None):

        current_id = self.new_id()

        label = type(node).__name__

        if isinstance(node, cst.Name):
            label += f"\\n{node.value}"

        elif isinstance(node, cst.Integer):
            label += f"\\n{node.value}"

        elif isinstance(node, cst.Float):
            label += f"\\n{node.value}"

        elif isinstance(node, cst.SimpleString):
            label += f"\\n{node.value}"

        elif isinstance(node, cst.FunctionDef):
            label += f"\\n{node.name.value}"

        elif isinstance(node, cst.Param):
            label += f"\\n{node.name.value}"

        self.lines.append(
            f'{current_id} [label="{self.escape(label)}"];'
        )

        if parent:
            self.lines.append(
                f"{parent} -> {current_id};"
            )

        for child in node.children:

            if isinstance(child, cst.CSTNode):
                self.visit(child, current_id)

    def generate(self, filename):

        self.lines.append("digraph CST {")
        self.lines.append("    rankdir=TB;")
        self.lines.append("    node [shape=box];")

        pending = [os.path.abspath(filename)]
        visited = set()

        while pending:

            current_file = pending.pop(0)

            if current_file in visited:
                continue

            visited.add(current_file)

            with open(current_file, "r", encoding="utf-8") as f:
                source = f.read()

            tree = cst.parse_module(source)

            self.visit(tree)

            imported_files = self.collect_imports(
                tree,
                current_file
            )

            for imported in imported_files:

                if imported not in visited:
                    pending.append(imported)

        self.lines.append("}")

        return "\n".join(self.lines)


if __name__ == "__main__":

    if len(sys.argv) != 2:

        print(
            "Usage: python3 cst2dot.py <program.py>"
        )

        sys.exit(1)

    filename = sys.argv[1]

    generator = CSTDotGenerator()

    dot_output = generator.generate(filename)

    output_file = filename.replace(".py", ".dot")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(dot_output)

    print(f"DOT file written to: {output_file}")
    os.system(f"xdot {output_file}")
