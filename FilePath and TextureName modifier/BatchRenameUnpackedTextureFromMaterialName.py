# Works for Blender 4.1

import bpy
import os

def rename_texture_files():
    # Function to construct an absolute path for a given relative path
    def abs_path(relative_path):
        return bpy.path.abspath(relative_path)

    # Iterate through all materials in the scene
    for material in bpy.data.materials:
        if material.use_nodes:
            # Access the material's node tree
            nodes = material.node_tree.nodes
            
            # Iterate through all nodes in the material
            for node in nodes:
                # Check if the node is an image node
                if node.type == 'TEX_IMAGE':
                    # Get the image associated with the node
                    image = node.image
                    if image is None:
                        continue
                    
                    # Get the path of the image file
                    image_path = image.filepath
                    
                    # Convert the path to an absolute path
                    abs_image_path = abs_path(image_path)
                    
                    # Extract the base name of the image file (without directory)
                    base_name = os.path.basename(abs_image_path)
                    
                    # Define the new file name based on the material name
                    # Replace spaces with underscores and remove unsupported characters
                    new_file_name = material.name.replace(' ', '_').replace(':', '').replace('"', '') + os.path.splitext(base_name)[1]
                    
                    # Construct the full path of the new file name
                    new_image_path = os.path.join(os.path.dirname(abs_image_path), new_file_name)
                    
                    # Rename the image file
                    try:
                        os.rename(abs_image_path, new_image_path)
                        print(f'Renamed {abs_image_path} to {new_image_path}')
                        
                        # Update the image data-block name in Blender
                        image.name = new_file_name
                        
                        # Update the image file path in Blender
                        image.filepath = new_image_path
                    except FileNotFoundError as e:
                        print(f"Error renaming {abs_image_path}: {e}")
                    except OSError as e:
                        print(f"Error renaming {abs_image_path}: {e}")

# Call the function to start renaming
rename_texture_files()
