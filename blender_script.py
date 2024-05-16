import os

import numpy as np
import bpy


# Define camera positions (modify as needed)
# camera_positions = [(6, -12, 2), (2, -2, 0), (4, -2, 0.5), (6, -2, 0.5), (8, -2, 0.5)]

y = [-9, 3]
x = [-20, 20]
z = 1.7

x = [-30, 8]
y = [10, 16]

x = [-27, -7]
y = [-3, 10]

x = [-26.5, -6.5]
# y = [-2.5, 9.5]

# Define camera position ranges
x_range = np.arange(start=x[0], stop=x[1]+1, step=1)  # Include the upper bound with +1
y_range = np.arange(start=y[0], stop=y[1]+1, step=1)  # Include the upper bound with +1
z_pos = 1.7  # Fixed z position

# Create meshgrid for all combinations of x and y positions
X, Y = np.meshgrid(x_range, y_range)

# Combine positions into a 3D array with fixed z
camera_positions = np.dstack((X, Y, np.full(X.shape, z_pos)))

# save all camera positions to a txt file
# np.savetxt('camera_positions.txt', camera_positions.reshape(-1, 3), fmt='%f')

# Print the generated camera positions
print(camera_positions)


def set_equirectangular(camera):
    """
    Sets the camera to equirectangular projection.
    """
    camera.data.type = "PANO"
    camera.data.sensor_width = 1
    camera.data.panorama_type = "EQUIRECTANGULAR"


# Function to render and save image
def render_and_save(camera, filepath):
    """
    Renders the scene from the given camera and saves to filepath.
    """
    bpy.context.scene.camera = camera
    #bpy.context.scene.render.filepath = filepath
    bpy.ops.render.render(write_still=True)



# Get active scene and render settings
scene = bpy.context.scene
render_settings = scene.render
tree = scene.node_tree

scene.render.resolution_x = 256
scene.render.resolution_y = 256

# set z pass to true
scene.view_layers['ViewLayer'].use_pass_z = True
scene.view_layers['ViewLayer'].use_pass_mist = True

scene.use_nodes = True

# Define output directory (modify as needed)
output_dir = os.path.join(os.path.dirname(bpy.data.filepath), "DepthImages_new")

# clear default nodes
for n in bpy.context.scene.node_tree.nodes:
    bpy.context.scene.node_tree.nodes.remove(n)

# camera_positions = [[-35, 20, 1.7], [-35, 20, 1.7]]
print(camera_positions)
# Loop through predefined camera positions
for i in range(camera_positions.shape[0]):
    for j in range(camera_positions.shape[1]):
        position = camera_positions[i][j]

        # clear the tree
        for n in bpy.context.scene.node_tree.nodes:
            bpy.context.scene.node_tree.nodes.remove(n)
        # Create a new camera object
        camera = bpy.data.cameras.new(name="camera_" + str(position[0]) + "_" + str(position[1]) + "_" + str(position[2]) + " depth")

        # Create camera object and link to scene
        camera_obj = bpy.data.objects.new(name=camera.name, object_data=camera)
        camera_obj.rotation_euler = (90, 0, -90)
        camera_obj.location = position

        bpy.context.scene.collection.objects.link(camera_obj)

        set_equirectangular(camera_obj)

        # create input render layer node OD TU NAPREJ
        rl = tree.nodes.new('CompositorNodeRLayers')

        links = tree.links

        map = tree.nodes.new(type="CompositorNodeMapValue")
        # Size is chosen kind of arbitrarily, try out until you're satisfied with resulting depth map.
        map.size = [0.04]
        map.use_min = True
        map.min = [0]
        map.use_max = True
        map.max = [255]
        links.new(rl.outputs[2], map.inputs[0])


        fileOutput = tree.nodes.new(type="CompositorNodeOutputFile")
        fileOutput.base_path = os.path.join(os.path.dirname(bpy.data.filepath), 'DepthImages_new')
        fileOutput.file_slots.new("Depth")
        fileOutput.file_slots['Depth'].path = camera.name


        # create a new file output node and set the path
        fileOutput.file_slots["Image"].path = "camera_" + str(position[0]) + "_" + str(position[1]) + "_" + str(position[2]) + " image"
        links.new(rl.outputs[0], fileOutput.inputs[0])
        
        # bpy.context.scene.render.filepath = os.path.join(os.path.dirname(bpy.data.filepath), 'rendered.png')

        # The viewer can come in handy for inspecting the results in the GUI
        depthViewer = tree.nodes.new(type="CompositorNodeViewer")
        links.new(map.outputs[0], depthViewer.inputs[0])

        # connect the viewer to the composite output
        composite = tree.nodes.new(type="CompositorNodeComposite")
        links.new(map.outputs[0], composite.inputs[0])

        # save to file
        links.new(map.outputs[0], fileOutput.inputs[1]) # DO TLE

        # Render scene
        render_and_save(camera_obj, render_settings.filepath)


# cleanup the cameras
# for camera in bpy.data.cameras:
#     bpy.data.cameras.remove(camera)

# for camera_obj in bpy.data.objects:
#     if camera_obj.name.startswith("camera_"):
#         bpy.data.objects.remove(camera_obj)
 

print("Rendered equirectangular depth images from predefined positions!")
