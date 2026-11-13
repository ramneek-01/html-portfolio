from __future__ import annotations
import ast
from pathlib import Path

class Analyzer(ast.NodeVisitor):
    def __init__(self,source,filename="<string>"):
        self.source=source;self.filename=filename;self.lines=source.splitlines()
        self.functions=[];self.classes=0;self.findings=[]
    def add(self,rule,severity,line,message):
        self.findings.append({"rule":rule,"severity":severity,"line":line,"message":message,"file":self.filename})
    def visit_ClassDef(self,node):
        self.classes+=1;self.generic_visit(node)
    def _function(self,node):
        decisions=sum(isinstance(n,(ast.If,ast.For,ast.AsyncFor,ast.While,ast.IfExp,ast.ExceptHandler,ast.comprehension,ast.Match)) for n in ast.walk(node))
        complexity=1+decisions;end=getattr(node,"end_lineno",node.lineno);length=end-node.lineno+1
        self.functions.append({"name":node.name,"line":node.lineno,"lines":length,"complexity":complexity})
        if length>50:self.add("LONG_FUNCTION","medium",node.lineno,f"{node.name} spans {length} lines")
        if complexity>10:self.add("HIGH_COMPLEXITY","medium",node.lineno,f"{node.name} estimated complexity is {complexity}")
        def walk(n,depth):
            if isinstance(n,(ast.If,ast.For,ast.AsyncFor,ast.While,ast.Try,ast.With,ast.AsyncWith,ast.Match)):
                depth+=1
                if depth>4:self.add("DEEP_NESTING","low",getattr(n,"lineno",node.lineno),f"Nesting depth {depth} in {node.name}")
            for child in ast.iter_child_nodes(n):walk(child,depth)
        for child in node.body:walk(child,0)
    def visit_FunctionDef(self,node):self._function(node);self.generic_visit(node)
    def visit_AsyncFunctionDef(self,node):self._function(node);self.generic_visit(node)
    def visit_ExceptHandler(self,node):
        if node.type is None or (isinstance(node.type,ast.Name) and node.type.id=="Exception"):
            self.add("BROAD_EXCEPTION","low",node.lineno,"Broad exception handler can hide unexpected failures")
        self.generic_visit(node)
    @staticmethod
    def call_name(node):
        if isinstance(node,ast.Name):return node.id
        if isinstance(node,ast.Attribute):return Analyzer.call_name(node.value)+"."+node.attr
        return ""
    def visit_Call(self,node):
        name=self.call_name(node.func)
        if name in {"eval","exec"}:self.add("DYNAMIC_EXECUTION","high",node.lineno,f"{name}() executes dynamic code")
        if name=="pickle.loads":self.add("UNSAFE_DESERIALIZATION","high",node.lineno,"pickle.loads is unsafe for untrusted data")
        if name in {"subprocess.run","subprocess.call","subprocess.Popen"} and any(k.arg=="shell" and isinstance(k.value,ast.Constant) and k.value.value is True for k in node.keywords):
            self.add("SHELL_TRUE","high",node.lineno,"subprocess call uses shell=True")
        self.generic_visit(node)
    def report(self):
        try:tree=ast.parse(self.source,filename=self.filename)
        except SyntaxError as e:
            self.add("SYNTAX_ERROR","high",e.lineno or 1,e.msg);return self.result()
        self.visit(tree);return self.result()
    def result(self):
        return {"file":self.filename,"lines":len(self.lines),"classes":self.classes,"functions":self.functions,
                "function_count":len(self.functions),"findings":sorted(self.findings,key=lambda x:(x["line"],x["rule"]))}

def analyze_file(path):
    p=Path(path);return Analyzer(p.read_text(encoding="utf-8",errors="replace"),str(p)).report()
def analyze_path(path):
    p=Path(path);files=[p] if p.is_file() else sorted(p.rglob("*.py"))
    return [analyze_file(f) for f in files if f.is_file() and not any(x in {".git",".venv","venv","__pycache__"} for x in f.parts)]
