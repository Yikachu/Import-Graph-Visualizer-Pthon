import os
import ast
import networkx as nx
import matplotlib.pyplot as plt

def get_python_files(root_dir):
    python_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def extract_imports(filepath):
    imports = set()
    with open(filepath, 'r') as file:
        tree = ast.parse(file.read(), filename=filepath)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module)
    return imports

def build_import_graph(python_files):
    G = nx.DiGraph()  # Directed graph to represent imports
    
    for file in python_files:
        base_name = os.path.basename(file)
        G.add_node(base_name)
        
        imports = extract_imports(file)
        for imp in imports:
            # Check if the import is from another file in the codebase
            imp_file = imp + '.py'  # Assuming imports are in the form of 'module'=
            formatted_python_files = []
            for p in python_files:
                p = p.split("\\")
                p.pop(0)
                p = ".".join(p)
                formatted_python_files.append(p)
            G.add_edge(base_name, imp_file)

    return G


def visualize_graph(G):
    pos = nx.circular_layout(G)  # For consistent layout
    plt.figure(figsize=(12, 12))
    in_degrees = dict(G.in_degree())

    # Define a function to scale the node sizes
    def get_node_size(in_degree, min_size=100, max_size=5000):
        """Scale node size based on in-degree."""
        # Adjust these min_size and max_size to suit your visualization needs
        min_in_degree = min(in_degrees.values())
        max_in_degree = max(in_degrees.values())
        return min_size + (in_degree - min_in_degree) / (max_in_degree - min_in_degree) * (max_size - min_size)

    node_sizes = [get_node_size(in_degrees[node]) for node in G.nodes]
    nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color='lightblue', font_size=5, font_weight='bold', arrows=True)
    plt.title("Import Graph")
    plt.show()

def main(root_dir):
    python_files = get_python_files(root_dir)
    import_graph = build_import_graph(python_files)
    visualize_graph(import_graph)

if __name__ == "__main__":
    main('Loop-Labyrinth-Analysis-main')  # Replace with your codebase path