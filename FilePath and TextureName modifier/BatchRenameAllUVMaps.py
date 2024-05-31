import bpy

# Specify the new name for all UV maps
new_uv_map_name = "UVMap"

# Iterate over selected objects
for obj in bpy.context.selected_objects:
    # Check if the object has UV maps
    if obj.data.uv_layers:
        # Iterate over each UV map
        for uv_map in obj.data.uv_layers:
            # Rename the UV map
            uv_map.name = new_uv_map_name
