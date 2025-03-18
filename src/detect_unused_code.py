import os
import ast
import argparse
from collections import defaultdict
import json
import subprocess
from pathlib import Path

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.defined_funcs = set()
        self.defined_classes = set()
        self.used_names = set()
        self.defined_imports = set()
        self.used_imports = set()
    
    def visit_FunctionDef(self, node):
        self.defined_funcs.add(node.name)
        self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        self.defined_classes.add(node.name)
        self.generic_visit(node)
    
    def visit_Name(self, node):
        self.used_names.add(node.id)
    
    def visit_Import(self, node):
        for alias in node.names:
            self.defined_imports.add(alias.name)
    
    def visit_ImportFrom(self, node):
        for alias in node.names:
            full_import = f"{node.module}.{alias.name}" if node.module else alias.name
            self.defined_imports.add(full_import)
    
    def analyze_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=filepath)
            self.visit(tree)
        
    def get_unused(self):
        unused_funcs = self.defined_funcs - self.used_names
        unused_classes = self.defined_classes - self.used_names
        unused_imports = self.defined_imports - self.used_names
        return unused_funcs, unused_classes, unused_imports

def find_files(directory, extensions):
    files = []
    for root, _, filenames in os.walk(directory):
        for file in filenames:
            if any(file.endswith(ext) for ext in extensions):
                files.append(os.path.join(root, file))
    return files

def remove_unused_code(file_path, unused_funcs, unused_classes, unused_imports):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    skip = False
    for line in lines:
        stripped_line = line.strip()
        if any(stripped_line.startswith(f"def {func}(") for func in unused_funcs):
            skip = True
        elif any(stripped_line.startswith(f"class {cls}(") for cls in unused_classes):
            skip = True
        elif any(stripped_line.startswith("import ") and any(imp in stripped_line for imp in unused_imports)):
            skip = True
        elif any(stripped_line.startswith("from ") and any(imp in stripped_line for imp in unused_imports)):
            skip = True
        
        if not skip:
            new_lines.append(line)
        else:
            skip = False  # Reset for next lines
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def analyze_python_project(directory):
    files = find_files(directory, [".py"])
    all_defined = defaultdict(set)
    all_used = set()
    
    for file in files:
        analyzer = CodeAnalyzer()
        analyzer.analyze_file(file)
        
        all_defined['functions'].update(analyzer.defined_funcs)
        all_defined['classes'].update(analyzer.defined_classes)
        all_defined['imports'].update(analyzer.defined_imports)
        
        all_used.update(analyzer.used_names)
    
    unused_funcs = all_defined['functions'] - all_used
    unused_classes = all_defined['classes'] - all_used
    unused_imports = all_defined['imports'] - all_used
    
    return unused_funcs, unused_classes, unused_imports

def analyze_js_project(directory):
    js_files = find_files(directory, [".js", ".jsx", ".ts", ".tsx"])
    unused_funcs = set()
    unused_classes = set()
    unused_imports = set()
    
    for file in js_files:
        result = subprocess.run(["node", "analyze_js.js", file], capture_output=True, text=True)
        if result.stdout:
            try:
                data = json.loads(result.stdout)
                unused_funcs.update(data.get("functions", []))
                unused_classes.update(data.get("classes", []))
                unused_imports.update(data.get("imports", []))
            except json.JSONDecodeError:
                print(f"Error processing {file}")
    
    return unused_funcs, unused_classes, unused_imports

def remove_unused_js_code(file_path, unused_funcs, unused_classes, unused_imports):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    skip = False
    for line in lines:
        stripped_line = line.strip()
        if any(stripped_line.startswith(f"function {func}(") for func in unused_funcs):
            skip = True
        elif any(stripped_line.startswith(f"class {cls} ") for cls in unused_classes):
            skip = True
        elif any(stripped_line.startswith("import ") and any(imp in stripped_line for imp in unused_imports)):
            skip = True
        
        if not skip:
            new_lines.append(line)
        else:
            skip = False
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect and remove unused functions, classes, and imports from Python and JavaScript files.")
    parser.add_argument("directory", help="Path to the project directory")
    parser.add_argument("--remove", action="store_true", help="Remove unused code automatically")
    args = parser.parse_args()
    
    unused_funcs_py, unused_classes_py, unused_imports_py = analyze_python_project(args.directory)
    unused_funcs_js, unused_classes_js, unused_imports_js = analyze_js_project(args.directory)
    
    if args.remove:
        for file in find_files(args.directory, [".py"]):
            remove_unused_code(file, unused_funcs_py, unused_classes_py, unused_imports_py)
        for file in find_files(args.directory, [".js", ".jsx", ".ts", ".tsx"]):
            remove_unused_js_code(file, unused_funcs_js, unused_classes_js, unused_imports_js)
        print("Unused code removed!")
