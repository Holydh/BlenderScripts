import bpy

for eachMat in bpy.data.materials:
    if eachMat.use_nodes:  # Check if the material uses nodes
        nodes = eachMat.node_tree.nodes
        links = eachMat.node_tree.links
        principled_bsdf = None
        material_output = None
        
        # Find Principled BSDF and Material Output nodes
        for node in nodes:
            if node.type == 'BSDF_PRINCIPLED':
                principled_bsdf = node
            elif node.type == 'OUTPUT_MATERIAL':
                material_output = node

        # Ensure both nodes are found
        if principled_bsdf and material_output:
            # Connect the Principled BSDF node to the Material Output node
            links.new(principled_bsdf.outputs[0], material_output.inputs[0])
