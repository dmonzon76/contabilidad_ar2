import os

OUTPUT = "project_tree.txt"

def generate_tree(start_path):
    tree_lines = []

    for root, dirs, files in os.walk(start_path):
        level = root.replace(start_path, "").count(os.sep)
        indent = " " * 4 * level
        tree_lines.append(f"{indent}{os.path.basename(root)}/")

        subindent = " " * 4 * (level + 1)
        for f in files:
            tree_lines.append(f"{subindent}{f}")

    return "\n".join(tree_lines)


if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))
    tree_output = generate_tree(project_root)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(tree_output)

    print(f"Árbol generado en: {OUTPUT}")
