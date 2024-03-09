import bpy


# Delect objects by type
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        o.select_set(True)
    else:
        o.select_set(False)

bpy.ops.object.delete()

def clearall():
    # save and reset state of selection
    selected_objects = bpy.context.selected_objects
    active_object = bpy.context.active_object
    for obj in selected_objects:
        obj.select_set(False)
        obj.delete(use_global=True)
        

    #bpy.ops.object.select_all(action='SELECT')
    #bpy.ops.object.delete(use_global=True)

#clearall()
def draw_standard_meshes():
    S = 0.2
    D = 1.0

    p = (1.00, 0.00, 0.00)
    bpy.ops.mesh.primitive_cube_add(size=S, location=p)

    p = (2.00, 0.00, 0.00)
    bpy.ops.mesh.primitive_cylinder_add(radius=S, depth=D, location=p)

    p = (3.00, 0.00, 0.00)
    bpy.ops.mesh.primitive_cone_add(radius1=S, depth=D, location=p)

    p = (4.00, 0.00, 0.00)
    bpy.ops.mesh.primitive_ico_sphere_add(radius=S, location=p)

    p = (5.00, 0.00, 0.00)
    bpy.ops.mesh.primitive_torus_add(rotation=(1.00, 0.00, 1.00), location=p)


def make_square_pyramid(name, loc):
    verts = [(0, 0, 0), (2, 0, 0), (2, 2, 0), (0, 2, 0), (1, 1, 3)]

    faces = [(0, 1, 2, 3), (0, 4, 1), (1, 4, 2), (2, 4, 3), (3, 4, 0)]

    mesh = bpy.data.meshes.new(name)

    object = bpy.data.objects.new(name, mesh)

    bpy.context.collection.objects.link(object)

    object.location = loc

    mesh.from_pydata(verts, [], faces)

    mesh.update(calc_edges=True)


#draw_standard_meshes()

#make_square_pyramid('pyramid1', (5, 3, 5))

#make_square_pyramid('pyramid2', (5, 1, 3))

for o in bpy.context.scene.objects:
    print(f'type: {o.type}, name: {o.name}')
