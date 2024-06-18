#Blender 4.1
import bpy

# Iterate over all selected objects
for obj in bpy.context.selected_objects:
    # Ensure the object has material slots
    if obj.material_slots:
        for mat_slot in obj.material_slots:
            # Ensure the material slot has a material
            if mat_slot.material:
                mat = mat_slot.material
                # Ensure the material uses nodes
                if mat.use_nodes:
                    nodes = mat.node_tree.nodes
                    for node in nodes:
                        # Check if the node is an image texture node
                        if node.type == "TEX_IMAGE":
                            # Set the interpolation to "Closest"
                            node.interpolation = "Closest"
else:
    print("No selected objects with material slots found.")
