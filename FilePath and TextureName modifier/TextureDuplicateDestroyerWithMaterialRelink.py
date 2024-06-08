#Blender 4.1
# Use DupeGuru to generate the duplicate report .csv file : https://github.com/arsenetar/dupeguru/
# DupeGuru scans folders for duplicate files by analysing and comparing the content of each.

# This script will then use this csv file to relink the materials using the duplicates to the original then will delete the .png files from the folder. 
# It need to be used with the textures unpacked and renamed, textures must have the same name has their materials (but still with the .png extension of course)
# So here's the steps summarized :
# 1 - BatchRenameBlenderImageNameFromMaterialName.py (run the script from the blender text editor)
# 2 - RenamePackedTextureFilePathFromBlenderImageName.py (In the blender python console)
# 3 - Unpack textures in current directory
# 4 - Run this script below

import bpy
import csv
import os

# Path to the CSV file
csv_path = "C:\\Users\\pathToYourDuplicateReport.csv"

def read_csv(csv_path):
    groups = {}
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            group_id = row['Group ID']
            file_name = row['Nom de fichier']
            folder = row['Dossier']
            if group_id not in groups:
                groups[group_id] = []
            groups[group_id].append((file_name, folder))
    return groups

def relink_duplicate_textures_and_delete_files(groups):
    for group_id, files in groups.items():
        if not files:
            continue

        # Determine the main file for this group
        main_file = files[0]
        main_texture_name = os.path.splitext(main_file[0])[0] + '.png'

        # Get the main image in Blender
        main_image = bpy.data.images.get(main_texture_name)
        if not main_image:
            print(f"Main image {main_texture_name} not found in Blender.")
            continue

        # Relink all other textures in the group to the main texture and delete them
        for file_name, folder in files[1:]:
            texture_name = os.path.splitext(file_name)[0] + '.png'
            image = bpy.data.images.get(texture_name)
            if image:
                for material in bpy.data.materials:
                    if material.use_nodes:
                        for node in material.node_tree.nodes:
                            if node.type == 'TEX_IMAGE' and node.image == image:
                                node.image = main_image
                                print(f"Relinked {texture_name} to {main_texture_name}")
                
                # Remove the image data-block from Blender
                bpy.data.images.remove(image)
            
            # Construct the full path of the image file and delete it
            file_path = os.path.join(folder, file_name)
            try:
                os.remove(file_path)
                print(f"Deleted file {file_path}")
            except OSError as e:
                print(f"Error deleting file {file_path}: {e}")

def main():
    groups = read_csv(csv_path)
    relink_duplicate_textures_and_delete_files(groups)

if __name__ == "__main__":
    main()
