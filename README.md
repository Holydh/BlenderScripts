# Blender python scripts

### FilePath and TextureName modifier :

Allows to rename and copy to a destination folder every unpacked texture files. It then injects all the new paths and new Blender texture names (image data block name) into blender.
Useful if you have several different textures sharing the same file name but placed inside several different folders. This allows to centralize every textures without being afraid of them being overwritten when exporting to fbx or when unpacking all to the same folder.

### Material modifiers

Various materials modifiers :
Change all materials blend mode to opaque
Change all textures filtering mod to closest
Delete all nodes in all materials when nodes name is "Invert"
Link BSDF Principled Nodes to Material Output Surface on all materials
