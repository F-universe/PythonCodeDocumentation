import ast
import os

class CodeDocumentationGenerator:
    def __init__(self, filepath):
        self.filepath = filepath
        self.documentation = []

    def generate(self):
        with open(self.filepath, "r") as file:
            file_contents = file.read()
            tree = ast.parse(file_contents)
            self.documentation.append(f"# Documentation for `{os.path.basename(self.filepath)}`\n")
            self._parse_tree(tree)
        return "\n".join(self.documentation)

    def _parse_tree(self, tree):
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                self._document_class(node)
            elif isinstance(node, ast.FunctionDef):
                self._document_function(node)

    def _document_class(self, node):
        self.documentation.append(f"## Class: `{node.name}`\n")
        docstring = ast.get_docstring(node)
        if docstring:
            self.documentation.append(f"**Description**: {docstring}\n")
        
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                self._document_function(item)

    def _document_function(self, node):
        self.documentation.append(f"### Method: `{node.name}()`\n")
        docstring = ast.get_docstring(node)
        if docstring:
            self.documentation.append(f"**Description**: {docstring}\n")
        
        # Document parameters, skipping 'self'
        if node.args.args:
            self.documentation.append("**Parameters**:")
            for arg in node.args.args:
                if arg.arg != "self":  # Skip 'self'
                    arg_name = arg.arg
                    if arg.annotation:
                        arg_type = self._get_annotation(arg.annotation)
                        self.documentation.append(f"- `{arg_name}` ({arg_type}): Description not available.")
                    else:
                        self.documentation.append(f"- `{arg_name}`: Description not available.")
        
        # Document return type
        if node.returns:
            return_type = self._get_annotation(node.returns)
            self.documentation.append(f"**Returns**: `{return_type}`\n")
        self.documentation.append("")

    def _get_annotation(self, annotation):
        if isinstance(annotation, ast.Name):
            return annotation.id
        elif isinstance(annotation, ast.Subscript):
            return f"{annotation.value.id}[{self._get_annotation(annotation.slice.value)}]"
        elif isinstance(annotation, ast.Attribute):
            return f"{annotation.value.id}.{annotation.attr}"
        return "Unknown"

    def save_to_file(self, output_filepath):
        with open(output_filepath, "w") as file:
            file.write("\n".join(self.documentation))

# Example Usage
if __name__ == "__main__":
    generator = CodeDocumentationGenerator("C:\\Users\\Fabio\\Desktop\\code parsing\\example.py")

    documentation = generator.generate()
    generator.save_to_file("DOCUMENTATION.md")
    print("Documentation generated and saved to DOCUMENTATION.md")
