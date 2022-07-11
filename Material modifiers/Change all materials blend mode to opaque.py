import bpy
mats = bpy.data.materials

for mat in mats:
    mat.blend_method = 'OPAQUE'
