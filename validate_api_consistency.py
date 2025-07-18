# validate_api_consistency.py
import ast
import glob
from collections import defaultdict

class APIConsistencyValidator:
    def __init__(self):
        self.class_apis = defaultdict(dict)
        self.method_signatures = defaultdict(set)
    
    def analyze_project(self):
        for pyfile in glob.glob("**/*.py", recursive=True):
            with open(pyfile, "r") as f:
                tree = ast.parse(f.read())
                self._visit_nodes(tree, pyfile)
        
        self._validate_interfaces()
    
    def _visit_nodes(self, node, filename):
        if isinstance(node, ast.ClassDef):
            class_api = {}
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    params = [a.arg for a in item.args.args]
                    class_api[item.name] = params
                    self.method_signatures[item.name].add(tuple(params))
            self.class_apis[node.name][filename] = class_api
    
    def _validate_interfaces(self):
        # 1. Check class API consistency
        for class_name, impls in self.class_apis.items():
            if len(impls) > 1:
                base_api = next(iter(impls.values()))
                for filename, api in impls.items():
                    if api != base_api:
                        print(f"CLASS INCONSISTENCY: {class_name} in {filename}")
        
        # 2. Check method signature consistency
        for method, signatures in self.method_signatures.items():
            if len(signatures) > 1:
                print(f"METHOD SIGNATURE INCONSISTENCY: {method}")
                print(f"  Found signatures: {signatures}")

if __name__ == "__main__":
    validator = APIConsistencyValidator()
    validator.analyze_project()