import ast

# 示例Python代码
source_code = """
def greet(name):
    print(f"Hello, {name}!")
"""

# 将代码解析为AST
tree = ast.parse(source_code)

# 打印AST
print(ast.dump(tree, indent=4))