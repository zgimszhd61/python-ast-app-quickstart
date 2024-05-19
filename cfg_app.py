import ast
import networkx as nx
import matplotlib.pyplot as plt

class CFGNode:
    def __init__(self, name):
        self.name = name

class CFGBuilder(ast.NodeVisitor):
    def __init__(self):
        self.cfg = nx.DiGraph()
        self.current_node = None

    def add_node(self, name):
        node = CFGNode(name)
        self.cfg.add_node(node)
        if self.current_node:
            self.cfg.add_edge(self.current_node, node)
        self.current_node = node
        return node

    def visit_FunctionDef(self, node):
        self.add_node(f"Function: {node.name}")
        self.generic_visit(node)

    def visit_If(self, node):
        if_node = self.add_node("If")
        self.visit(node.test)
        self.current_node = if_node
        self.visit(node.body)
        if node.orelse:
            self.current_node = if_node
            self.visit(node.orelse)

    def visit_While(self, node):
        while_node = self.add_node("While")
        self.visit(node.test)
        self.current_node = while_node
        self.visit(node.body)
        if node.orelse:
            self.current_node = while_node
            self.visit(node.orelse)

    def visit_For(self, node):
        for_node = self.add_node("For")
        self.visit(node.target)
        self.visit(node.iter)
        self.current_node = for_node
        self.visit(node.body)
        if node.orelse:
            self.current_node = for_node
            self.visit(node.orelse)

    def visit_Return(self, node):
        self.add_node("Return")

    def visit_Expr(self, node):
        self.add_node("Expr")
        self.generic_visit(node)

    def generic_visit(self, node):
        try:
            super().generic_visit(node)
        except AttributeError as e:
            if "'list' object has no attribute '_fields'" in str(e):
                print(f"Skipping node due to error: {e}")
            else:
                raise

def build_cfg(source_code):
    tree = ast.parse(source_code)
    cfg_builder = CFGBuilder()
    cfg_builder.visit(tree)
    return cfg_builder.cfg

def draw_cfg(cfg):
    pos = nx.spring_layout(cfg)
    labels = {node: node.name for node in cfg.nodes()}
    nx.draw(cfg, pos, labels=labels, with_labels=True, node_size=3000, node_color="lightblue", font_size=10, font_weight="bold")
    plt.show()

# 示例Python代码
source_code = """
def complex_function(x, y):
    result = 0
    for i in range(x):
        if i % 2 == 0:
            result += i
        else:
            result -= i
    while result < y:
        result += 1
    return result

print(complex_function(10, 5))
"""

cfg = build_cfg(source_code)
draw_cfg(cfg)