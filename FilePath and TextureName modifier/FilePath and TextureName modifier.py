import bpy
import os
import shutil

def get_original_name(name):
    i = name.rfind('.')
    return name

### Insert your destination folder here :
destFolder = r'C:\Users\YourUserName\etc\etc'
### Insert the texture prefix that will be set here :
prefix = 'texture-'

path_dict = {}
x=1
new_path=""

for material in bpy.data.materials:
    if material.node_tree is None:
        continue
    for node in material.node_tree.nodes:
        if node.type != 'TEX_IMAGE':
            continue
        if node.image is None:
            continue
            
        original_name = get_original_name(node.image.name)
        relative_path = bpy.data.images[original_name].filepath
        old_path = bpy.path.abspath(relative_path)
        filepath_split = os.path.split(old_path)
        filename_ext = os.path.splitext(old_path)
        num = str(x)
        new_filename = prefix+num+filename_ext[1]
        new_path = destFolder+'\\'+new_filename
        temp_path = filepath_split[0]+'\\'+new_filename

        if old_path in path_dict.values():
            bpy.data.images[original_name].filepath = old_path
            bpy.data.images[original_name].name = original_name
            print("Final : "+old_path)
        else:
            if old_path in path_dict:
                new_path = path_dict[old_path]
                bpy.data.images[original_name].filepath = new_path
                bpy.data.images[original_name].name = new_filename
                print("Final : "+new_path)
            else:
                path_dict[old_path] = new_path
                if os.path.isfile(old_path):          
                    try:
                        os.rename(old_path, temp_path)
                    except os.FileExistsError:
                        print('FileExistsError')
                        print(old_path)
                        print(temp_path)
                        print(new_path)
                        print('Keeping on')
                        pass
                    try:
                        shutil.copy(temp_path,new_path)
                    except shutil.SameFileError:
                        print('SameFileError')
                        print(old_path)
                        print(temp_path)
                        print(new_path)
                        print('Keeping on')
                        pass
                        
                bpy.data.images[original_name].filepath = new_path
                bpy.data.images[original_name].name = new_filename  
                
                x += 1     
                
                print("Final : "+new_path)                
