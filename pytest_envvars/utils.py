import ast


def get_modules_to_reload(filename):
    """Given a filename, find all modules used on this file
    and return a set with found modules
    """
    with open(filename) as test_file:
        root = ast.parse(test_file.read(), filename)

    modules = set()
    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Import):
            module = ""
        elif isinstance(node, ast.ImportFrom):
            # TO-DO: Fix problem with this sintax
            # from .. import some_module
            module = node.module
        else:
            continue

        for n in node.names:
            if not module:
                modules.add(n.name)
                continue
            modules.add(module)

    return modules
