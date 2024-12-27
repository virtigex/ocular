import bpy
import math
from mathutils import Euler

import bpy
import math
from mathutils import Euler

def lightscamera():
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(10, 0, 0), rotation=(1.5707, 0, 1.5707), scale=(1, 1, 1))
    bpy.ops.outliner.item_activate(deselect_all=True)


def delmesh():
    # Delect objects by type
    for o in bpy.context.scene.objects:
        if o.type == 'MESH':
            o.select_set(True)
        else:
            o.select_set(False)

    bpy.ops.object.delete()
    
def spacestation():

    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=2.0, location=(0, 0, 0))
    bpy.context.active_object.name = 'core'
    bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.2)
    bpy.context.active_object.name = 'habitation'

    no_spokes = 6

    angle = 2 * math.pi / no_spokes
    radius = 1

    for i in range(no_spokes):
        a = i * angle
        x = radius * math.cos(a)
        y = radius * math.sin(a)
        l = (x/2, y/2, 0)
        
        xrot = math.pi / 2
        zrot = math.atan2(x, -y)
        rot = (xrot, 0, zrot)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=1.0, location=l, rotation=rot)
        bpy.context.active_object.name = f'spoke-{i}'
        
lightscamera()
delmesh()
spacestation()

def spacestation2():
    # Delect objects by type
    for o in bpy.context.scene.objects:
        if o.type == 'MESH':
            o.select_set(True)
        else:
            o.select_set(False)

    bpy.ops.object.delete()

    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=2.0, location=(0, 0, 0))
    bpy.context.active_object.name = 'core'
    bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=0.2)
    bpy.context.active_object.name = 'habitation'

    no_spokes = 6

    angle = 2 * math.pi / no_spokes
    radius = 1

    for i in range(no_spokes):
        a = i * angle
        x = radius * math.cos(a)
        y = radius * math.sin(a)
        l = (x/2, y/2, 0)
        
        xrot = math.pi / 2
        zrot = math.atan2(x, -y)
        rot = (xrot, 0, zrot)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=1.0, location=l, rotation=rot)
        bpy.context.active_object.name = f'spoke-{i}'
        
