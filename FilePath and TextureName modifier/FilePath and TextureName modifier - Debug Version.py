import bpy
import os
import shutil
import logging

logging.basicConfig(filename=r"C:\Users\YourUserName\etc\etc\log.txt", level=logging.DEBUG)

def get_original_name(name):
    i = name.rfind('.')
    return name

### Insert your destination folder here :
destFolder = r'C:\Users\YourUserName\etc\etc'
### hash table instance to keep track of old path and new path of each textures. 
### Keys are old_path
### Values are new_path
path_dict = {}
### Start number to increment
x=1

new_path=""


### Dig in each materials each texture node
for material in bpy.data.materials:
    if material.node_tree is None:
        continue
    for node in material.node_tree.nodes:
        if node.type != 'TEX_IMAGE':
            continue
        if node.image is None:
            continue
        ### Get original name of the texture from texture node
        original_name = get_original_name(node.image.name)
        relative_path = bpy.data.images[original_name].filepath
        old_path = bpy.path.abspath(relative_path)
        ### Split the original path in both
        filepath_split = os.path.split(old_path)
        ### split the filename from its extension
        filename_ext = os.path.splitext(old_path)
        ### Make the number to increment into string
        num = str(x)
        new_filename = 'mgs-'+num+filename_ext[1]
        new_path = destFolder+'\\'+new_filename
        temp_path = filepath_split[0]+'\\'+new_filename
        logging.debug("-----------------------------Main Block -----------------------------------")
        logging.debug("original_name"+" : "+original_name)
        logging.debug("old_path"+" : "+old_path)
        logging.debug("new_filename"+" : "+new_filename)
        logging.debug("new_path"+" : "+new_path)
        logging.debug("temp_path"+" : "+temp_path)
        logging.debug("--------------------------Enf of Main Block ---------------------------------------")
        logging.debug("--")
        
        ### If the processed texture is a duplicate in the hash table values, just change the blender path and blender texture name (Allows for same nodes to use the same texture file) :
        if old_path in path_dict.values():
            bpy.data.images[original_name].filepath = old_path
            bpy.data.images[original_name].name = original_name
            logging.debug("-------------1st if Block -----------------------------------")
            logging.debug("original_name"+" : "+original_name)
            logging.debug("-------------End of 1st if Block -----------------------------------")
            logging.debug("--")
            logging.debug("Final : "+old_path)
            print("Final : "+old_path)
        else:
            ### If the processed texture is a duplicate in the hash table keys, just change the blender path and blender texture name (prevents os file duplicates) :
            if old_path in path_dict:
                new_path = path_dict[old_path]
                bpy.data.images[original_name].filepath = new_path
                bpy.data.images[original_name].name = new_filename
                logging.debug("-----------------2st if Block -----------------------------------")
                logging.debug("new_filename"+" : "+new_filename)
                logging.debug("-----------------End of 2st if Block -----------------------------------")
                logging.debug("--")
                logging.debug("Final : "+new_path)
                print("Final : "+new_path)
            ### If the texture isn't in the hash table already, store the old and new path in it :
            else:
                path_dict[old_path] = new_path
                if os.path.isfile(old_path):
                    ### Rename the file              
                    try:
                        os.rename(old_path, temp_path)
                    except os.FileExistsError:
                        logging.debug('FileExistsError')
                        logging.debug(old_path)
                        logging.debug(temp_path)
                        logging.debug(new_path)
                        logging.debug('Keeping on')
                        pass
                    ### Copy the file to destination folder
                    try:
                        shutil.copy(temp_path,new_path)
                    except shutil.SameFileError:
                        logging.debug('SameFileError')
                        logging.debug(old_path)
                        logging.debug(temp_path)
                        logging.debug(new_path)
                        logging.debug('Keeping on')
                        pass
                ### Changes the blender path with the new one
                bpy.data.images[original_name].filepath = new_path
                ### Changes the blender texture name with the new one
                bpy.data.images[original_name].name = new_filename   
                logging.debug("-------------------3st if Block -----------------------------------")
                logging.debug("new_path"+" : "+new_path)
                logging.debug("new_filename"+" : "+new_filename)
                logging.debug("-------------------End of 3st if Block -----------------------------------")
                logging.debug("--")                
                x += 1
                logging.debug("Final : "+new_path)
                print("Final : "+new_path)                
    
               
        logging.debug("--")          
