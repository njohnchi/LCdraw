
import run

def compile_expr(expr):
    # run.clear_parser()
    return run.compiler(expr)


if __name__ == "__main__":

    expr = "f = a + (a * (a + (b) * (b) + (a * (a + (b)))))"
    # expr = "f = (a + b) and c"
    tree = run.compiler(expr)
    print(tree)

    # tree.print_tree()