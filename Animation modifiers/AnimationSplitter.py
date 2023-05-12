# Credits to batFINGER's solution for the keyframes copy function : https://blender.stackexchange.com/questions/214866/copying-specific-frames-from-one-action-to-another-python

# This scripts goes through all the frames of an animation and checks all the Bones and/or object's position and/or rotation
# and compare the previous and current frame. If both frames are more different than a certain threshold, it copies all the keyframes
# since last cut in a new action. RMSE functions are used to check the level of differences between two frames.

# How to use :
# Backup your blender file
# Select the object that has the targetted animation you want to cut
# Be sure that the action you want to cut is assigned to the object (in the action editor)
# Open the script in the text editor and launch it
# Check the results in the action editor
# You can tweak thresholdBonesRotation. 0.25 has given me the best results. Decreasing it will make the scripts cut for 
# lighter differences between frames, increasing it will make it less strict
# You can also uncomment these two :
# #thresholdObjPosition = 0.5
# #thresholdObjRotation = 0.4
# And add them in the if frame_rmse > threshold statement
# This will allow to check the object position and rotation in itself instead of its bones
# Use the right frame_rmse variable for the right threshold if you do that.

import bpy
from mathutils import Vector
import math
import numpy as np


def action_slice(action, start_frame, end_frame, shift=True):
    copy = bpy.data.actions.new(name=f"{action.name}_{range_id:03}")
    copy.id_root = action.id_root
    
    for fcurve in action.fcurves:
        kfs = np.empty(len(fcurve.keyframe_points) << 1)
        fcurve.keyframe_points.foreach_get("co", kfs)
        kfs = kfs.reshape((-1, 2))
        _fc = copy.fcurves.new(
                fcurve.data_path,
                index = fcurve.array_index
                )
        _fc.keyframe_points.add(0)
        _kfs = kfs[
                np.logical_and(
                    kfs[:,0] >= start_frame, 
                    kfs[:,0] <= end_frame
                    )
                ]
        if shift:
            _kfs[:,0] -= (start_frame -1)
        _fc.keyframe_points.add(_kfs.shape[0])
        keyframe_points = _fc.keyframe_points
        for i, kf in enumerate(_kfs):
            point = keyframe_points[i]
            point.co = kf
            point.interpolation = fcurve.keyframe_points[i].interpolation
    return copy
    
    
def rmseRot(a, b):
    return math.sqrt(sum([(Vector(ai) - Vector(bi)).length_squared for ai, bi in zip(a, b)]) / len(a))

def rmseObjPos(a_pos, b_pos):
    a_pos = b_pos if a_pos is None else a_pos
    return (a_pos - b_pos).length

# set a threshold value for the RMSE. Using only the BonesRotation gives good results but you can us the other by adding them in the related if statement.
thresholdBonesRotation = 0.25
#thresholdObjPosition = 0.5
#thresholdObjRotation = 0.4

# get the selected object and its active action
obj = bpy.context.active_object
action = obj.animation_data.action

# initialize variables
keyframes = [f.co[0] for f in action.fcurves[3].keyframe_points]
start_frame = int(keyframes[0])
end_frame = int(keyframes[-1])
prev_frame_bones_rot = None
prev_frame_obj_rot = None
prev_obj_pos = obj.matrix_world.to_translation() # initialize prev_pos to the current position
prev_Bones_rmse = None
prev_obj_rot = obj.matrix_world.to_quaternion()
cur_obj_pos = None
cur_obj_rot = None
range_id = 0
range_dict = {}    

for frame in keyframes:
    # if this is the first keyframe, just set prev_frame and continue to the next keyframe
    if prev_frame_bones_rot is None:
        prev_frame_bones_rot = {}
        prev_frame_obj_rot = {}
        for pbone in obj.pose.bones:
            prev_frame_bones_rot[pbone.name] = pbone.rotation_quaternion.copy()
        prev_obj_pos = cur_obj_pos if prev_obj_pos is None else prev_obj_pos
        prev_frame_obj_rot[obj.name] = obj.matrix_world.to_quaternion()
        continue
        
    # get the current frame
    bpy.context.scene.frame_set(int(frame))
    print("current frame :")
    print(frame)# - OK
    cur_frame_Bones_Rot = {}
    cur_frame_Obj_Rot = {}
    for pbone in obj.pose.bones:
        cur_frame_Bones_Rot[pbone.name] = pbone.rotation_quaternion.copy()
    cur_obj_pos = obj.matrix_world.to_translation()
    cur_frame_Obj_Rot[obj.name] = obj.matrix_world.to_quaternion()

    print("previous Obj position :")
    print(prev_obj_pos)
    print("current Obj position :")
    print(cur_obj_pos)# - OK
    print("previous Obj rotation :")
    print(prev_frame_obj_rot[obj.name])
    print("current Obj rotation :")
    print(cur_frame_Obj_Rot[obj.name])
    

    # calculate the RMSE between the previous frame and the current frame
    frame_rmse_Bones_Rot = rmseRot(prev_frame_bones_rot.values(), cur_frame_Bones_Rot.values())
    # print("frame_rmse Bones Rotation :")
    # print(frame_rmse_Bones_Rot)
    frame_rmse_Obj_Pos = rmseObjPos(prev_obj_pos, cur_obj_pos)
    # print("frame_rmse obj position :")
    # print(frame_rmse_Obj_Pos)
    frame_rmse_Obj_Rot = rmseRot(prev_frame_obj_rot.values(), cur_frame_Obj_Rot.values())
    print("frame_rmse obj rotation :")
    print(frame_rmse_Obj_Rot)

    # if the RMSE is above the threshold, split the animation
    if prev_Bones_rmse is not None and frame_rmse_Bones_Rot > thresholdBonesRotation:
        end_frame = frame  # set the end frame to the current keyframe
        range_dict[range_id] = {"start": start_frame, "end": end_frame}  # store the start and end frames for this range of frames
        range_id += 1  # increment the ID number
        
        # reset variables for next range of frames
        start_frame = end_frame
     
        
    prev_Bones_rmse = frame_rmse_Bones_Rot
    prev_frame_bones_rot = cur_frame_Bones_Rot
    prev_frame_obj_rot = cur_frame_Obj_Rot

# add the final range to the dictionary
range_dict[range_id] = {"start": start_frame, "end": end_frame}

# create new actions for each range of frames
for range_id, frames in range_dict.items():
    start_frame = frames["start"]
    end_frame = frames["end"] -1
    action_slice(action, start_frame, end_frame, shift=True)
