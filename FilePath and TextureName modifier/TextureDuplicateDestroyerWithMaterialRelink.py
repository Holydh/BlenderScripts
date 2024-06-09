# Using Blender 4.1

# Use DupeGuru to generate the duplicate report .csv file : https://github.com/arsenetar/dupeguru/
# DupeGuru scans folders for duplicate files by analysing and comparing the content of each.

# This script will then use this csv file to relink the materials using the duplicates to the original then will delete the .png files from the unpacked textures folder. 
# It need to be used with the textures unpacked and renamed, textures must have the same name has their materials (but still with the .png extension of course)

# Here's the required steps (the other required scripts can be found here https://github.com/Holydh/BlenderScripts/tree/main/FilePath%20and%20TextureName%20modifier) :
# 1 - BatchRenameBlenderImageNameFromMaterialName.py (run the script from the blender text editor)
# 2 - RenamePackedTextureFilePathFromBlenderImageName.py (In the blender python console)
# 3 - Unpack textures (choose write to current directory in blender)
# 4 - Run DupeGuru in the unpacked textures directory
# 5 - Run this script below

# /!\ Depending on your OS language, you'll need to change the read_csv function with the proper csv rows. Open your csv and look up the first line.
# This is how the csv rows looks in french :
# Group ID,Nom de fichier,Dossier,Taille (KB),Dimensions,Match %

# Find these following lines (lines 38, 39, 40) in the script and replace the csv rows with yours. eg : 'Nom de fichier' should be something like 'folder name' etc.
#            group_id = row['Group ID']
#            file_name = row['Nom de fichier']
#            folder = row['Dossier']


import bpy
import csv
import os

# Path to the CSV file
csv_path = "C:\\Users\\PathToYourDuplicateReport.csv"

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

def relink_and_delete_duplicates(groups):
    for group_id, files in groups.items():
        if not files:
            continue

        # Determine the main file for this group
        main_file = files[0]
        main_texture_name = os.path.splitext(main_file[0])[0] + '.png'
        main_material_name = os.path.splitext(main_file[0])[0]

        # Get the main image and material in Blender
        main_image = bpy.data.images.get(main_texture_name)
        main_material = bpy.data.materials.get(main_material_name)
        if not main_image or not main_material:
            print(f"Main image or material {main_texture_name}/{main_material_name} not found in Blender.")
            continue

        # Relink all other materials in the group to the main material
        for file_name, folder in files[1:]:
            texture_name = os.path.splitext(file_name)[0] + '.png'
            image = bpy.data.images.get(texture_name)
            material_name = os.path.splitext(file_name)[0]
            material = bpy.data.materials.get(material_name)

            if image:
                for mat in bpy.data.materials:
                    if mat.use_nodes:
                        for node in mat.node_tree.nodes:
                            if node.type == 'TEX_IMAGE' and node.image == image:
                                node.image = main_image
                                print(f"Relinked {texture_name} to {main_texture_name}")
                
                # Remove the image data-block from Blender
                bpy.data.images.remove(image)

            if material:
                # Relink objects using the duplicate material to the main material
                for obj in bpy.data.objects:
                    if obj.type == 'MESH':
                        for slot in obj.material_slots:
                            if slot.material == material:
                                slot.material = main_material
                                print(f"Relinked material {material_name} to {main_material_name}")

                # Remove the material data-block from Blender
                bpy.data.materials.remove(material)
                print(f"Deleted material {material_name}")

            # Construct the full path of the image file and delete it
            file_path = os.path.join(folder, file_name)
            try:
                os.remove(file_path)
                print(f"Deleted file {file_path}")
            except OSError as e:
                print(f"Error deleting file {file_path}: {e}")

def main():
    groups = read_csv(csv_path)
    relink_and_delete_duplicates(groups)

if __name__ == "__main__":
    main()
