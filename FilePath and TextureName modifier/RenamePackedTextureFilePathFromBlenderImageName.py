#To put in the blender python console
#Blender 4.1

for image in D.images:
    fp = f"//textures\\{image.name}"
    image.filepath = fp
    for pf in image.packed_files:
        pf.filepath = fp
