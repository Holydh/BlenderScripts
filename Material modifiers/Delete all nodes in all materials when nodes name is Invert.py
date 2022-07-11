import bpy

for mat in bpy.data.materials:
    if mat.node_tree:
        nodes = mat.node_tree.nodes
        names = [n.name for n in nodes if n.name == 'Invert']
        for name in names:
            nodes.remove(nodes[name])
