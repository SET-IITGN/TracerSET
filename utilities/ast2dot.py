# Generating a Graphviz DOT File from a Python AST

import ast
import sys
import os

class ASTDotGenerator:
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

    def collect_imports(self, tree, current_file):
        imported_files = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported = self.resolve_import_file(
                    alias.name,
                    current_file
                    )

                    if imported:
                        imported_files.append(imported)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imported = self.resolve_import_file(
                    node.module,
                    current_file
                    )
                    if imported:
                        imported_files.append(imported)

        return imported_files    

    def visit(self, node, parent=None):

        current_id = self.new_id()

        label = type(node).__name__

        # Add extra detail for important AST node types
        if isinstance(node, ast.Name):
            label += f"\\n{node.id}"

        elif isinstance(node, ast.Constant):
            label += f"\\n{repr(node.value)}"

        elif isinstance(node, ast.FunctionDef):
            label += f"\\n{node.name}"

        elif isinstance(node, ast.arg):
            label += f"\\n{node.arg}"

        self.lines.append(
            f'{current_id} [label="{self.escape(label)}"];'
        )

        if parent:
            self.lines.append(f"{parent} -> {current_id};")

        for child in ast.iter_child_nodes(node):
            self.visit(child, current_id)

    def generate(self, filename):
        self.lines.append("digraph AST {")
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

            tree = ast.parse(source)
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
        print("Usage: python3 ast_to_dot.py <program.py>")
        sys.exit(1)

    filename = sys.argv[1]

    with open(filename, "r", encoding="utf-8") as f:
        source = f.read()

    generator = ASTDotGenerator()
    dot_output = generator.generate(filename)
    output_file = filename.replace(".py", "ast.dot")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(dot_output)

    print(f"DOT file written to: {output_file}")
    os.system(f"xdot {output_file}")
    
    
