import bpy

for eachMat in bpy.data.materials:
    nodes = eachMat.node_tree.nodes
    links = eachMat.node_tree.links
    principled_bsdf = nodes.get("Principled BSDF")
    material_output = nodes.get("Material Output")
    for n in nodes:
        if (n.type == 'BSDF_PRINCIPLED'):
            BSDFcheck = n.outputs[0]
            if not(BSDFcheck.is_linked):
                # Connect the Principled BSDF node to the Material Output node
                links.new(material_output.inputs[0], principled_bsdf.outputs[0])
