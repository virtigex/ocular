import bpy
import math
from mathutils import Euler

# Delect objects by type
for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        o.select_set(True)
    else:
        o.select_set(False)

bpy.ops.object.delete()

class Dragon:
    def __init__(self):
        self.small_r = 1.0
        self.nodes = {}
    
    def draw_skeleton(self):
        self.add_node('left_wrist',( -2.00, 2.00, self.small_r))
        self.add_node('right_wrist', ( 2.00, 2.00, self.small_r ))
        self.add_node('left_elbow', ( -1.50, 1.0, 3.0))
        self.add_node('right_elbow', ( 1.50, 1.0, 3.0))
        self.add_node('left_shoulder',  ( -1.0, 1.5, 5.0))
        self.add_node('right_shoulder',  ( 1.0, 1.5, 5.0))
        self.add_node('left_paw',  ( -1.5, -4.0, self.small_r))
        self.add_node('right_paw',  ( 1.5, -4.0, self.small_r))
        self.add_node('left_ankle',  ( -1.5, -5.0, 1.5))
        self.add_node('right_ankle',  ( 1.5, -5.0, 1.5))
        self.add_node('left_knee',  ( -1.2, -4.0, 3.0))
        self.add_node('right_knee',  ( 1.2, -4.0, 3.0))
        self.add_node('left_hip',  ( -0.8, -5.0, 4.0))
        self.add_node('right_hip',  ( 0.8, -5.0, 4.0))

        self.join_nodes('left_wrist', 'left_elbow')
        self.join_nodes('left_elbow', 'left_shoulder')
        self.join_nodes('right_wrist', 'right_elbow')
        self.join_nodes('right_elbow', 'right_shoulder')

        self.join_nodes('left_paw', 'left_ankle')
        self.join_nodes('left_ankle', 'left_knee')
        self.join_nodes('left_knee', 'left_hip')
        self.join_nodes('right_paw', 'right_ankle')
        self.join_nodes('right_ankle', 'right_knee')
        self.join_nodes('right_knee', 'right_hip')
        
        self.add_node('mid_shoulder', self.midpoint('left_shoulder', 'right_shoulder'))
        self.add_node('mid_hip', self.midpoint('left_hip', 'right_hip'))
        
        self.join_nodes('right_shoulder', 'left_shoulder')
        self.join_nodes('right_hip', 'left_hip')
        
        lumbar = self.midpoint('mid_shoulder', 'mid_hip')
        lumbar = (lumbar[0], lumbar[1], lumbar[2]-0.3)
        self.add_node('lumbar', lumbar)
        
        self.join_nodes('mid_shoulder', 'lumbar')
        self.join_nodes('lumbar', 'mid_hip')
        
        self.add_node('neck', (0, 4, 8))
        self.add_node('head', (0, 5, 11))
        self.add_node('muzzle', (0, 7, 9))
        
        self.join_nodes('mid_shoulder', 'neck')
        self.join_nodes('neck', 'head')
        self.join_nodes('head', 'muzzle')
        
        self.add_node('tail1', (0, -8, 3))
        self.add_node('tail2', (0, -11, 5))
        self.add_node('tail3', (0, -13, 8))
        
        self.join_nodes('mid_hip', 'tail1')
        self.join_nodes('tail1', 'tail2')
        self.join_nodes('tail2', 'tail3')
        
        # wings
        self.add_node('left_wing1', (-3.5, -0.43, 8.00))
        self.add_node('left_wing2', (-5.90, 1.89, 13.25))
        self.add_node('left_wing3', (-9.6, -2.33, 16.11))
        self.add_node('left_wing4', (-13.46, -7.35, 14.25))
        self.add_node('right_wing1', (3.5, -0.43, 8.00))
        self.add_node('right_wing2', (5.90, 1.89, 13.25))
        self.add_node('right_wing3', (9.6, -2.33, 16.11))
        self.add_node('right_wing4', (13.46, -7.35, 14.25))

        self.join_nodes('left_shoulder', 'left_wing1')
        self.join_nodes('left_wing1', 'left_wing2')
        self.join_nodes('left_wing2', 'left_wing3')
        self.join_nodes('left_wing3', 'left_wing4')
        self.join_nodes('right_shoulder', 'right_wing1')
        self.join_nodes('right_wing1', 'right_wing2')
        self.join_nodes('right_wing2', 'right_wing3')
        self.join_nodes('right_wing3', 'right_wing4')
        
        self.add_node('left_wing1a', (-1.5, -4.5, 4.00))
        self.join_nodes('left_wing1', 'left_wing1a')
        self.join_nodes('left_wing1a', 'left_hip')
        self.join_nodes('left_shoulder', 'left_wing1a')
        
        self.add_node('left_wing2a', (-4.2, -4.8, 10.00))
        self.add_node('left_wing2b', (-3.5, -10.0, 8.00))
        self.join_nodes('left_wing2', 'left_wing2a')
        self.join_nodes('left_wing2a', 'left_wing2b')
        self.join_nodes('left_wing2b', 'left_wing1a')
        
        self.add_node('left_wing3a', (-10, -6.8, 13.6))
        self.add_node('left_wing3b', (-11.5, -9.5, 11))
        self.join_nodes('left_wing3', 'left_wing3a')
        self.join_nodes('left_wing3a', 'left_wing3b')
        self.join_nodes('left_wing3b', 'left_wing2b')

        self.add_node('left_wing4a', (-14.87, -10, 12.86))
        self.add_node('left_wing4b', (-16, -12.5, 11.2))
        self.join_nodes('left_wing4', 'left_wing4a')
        self.join_nodes('left_wing4a', 'left_wing4b')
        self.join_nodes('left_wing4b', 'left_wing3b')
                
        self.add_node('right_wing1a', (1.5, -4.5, 4.00))
        self.join_nodes('right_wing1', 'right_wing1a')
        self.join_nodes('right_wing1a', 'right_hip')
        self.join_nodes('right_shoulder', 'right_wing1a')
        
        self.add_node('right_wing2a', (4.2, -4.8, 10.00))
        self.add_node('right_wing2b', (3.5, -10.0, 8.00))
        self.join_nodes('right_wing2', 'right_wing2a')
        self.join_nodes('right_wing2a', 'right_wing2b')
        self.join_nodes('right_wing2b', 'right_wing1a')
        
        self.add_node('right_wing3a', (10, -6.8, 13.6))
        self.add_node('right_wing3b', (11.5, -9.5, 11))
        self.join_nodes('right_wing3', 'right_wing3a')
        self.join_nodes('right_wing3a', 'right_wing3b')
        self.join_nodes('right_wing3b', 'right_wing2b')

        self.add_node('right_wing4a', (14.87, -10, 12.86))
        self.add_node('right_wing4b', (16, -12.5, 11.2))
        self.join_nodes('right_wing4', 'right_wing4a')
        self.join_nodes('right_wing4a', 'right_wing4b')
        self.join_nodes('right_wing4b', 'right_wing3b')
        sheet = ( 'right_wing4', 'right_wing4a', 'right_wing4b', 'right_wing3b', 'right_wing3a', 'right_wing3' )
        self.add_sheet('rwing4', sheet)
                        
    def draw_wings(self):
        sheet = ( 'right_wing4', 'right_wing4a', 'right_wing4b', 'right_wing3b', 'right_wing3a', 'right_wing3' )
        self.add_sheet('rwing4', sheet)
        sheet = ( 'right_wing3', 'right_wing3a', 'right_wing3b', 'right_wing2b', 'right_wing2a', 'right_wing2' )
        self.add_sheet('rwing3', sheet)
        sheet = ( 'right_wing2', 'right_wing2a', 'right_wing2b', 'right_wing1a', 'right_wing1' )
        self.add_sheet('rwing2', sheet)
        sheet = ( 'right_wing1', 'right_wing1a', 'right_shoulder' )
        self.add_sheet('rwing1', sheet)
        
        sheet = ( 'left_wing4', 'left_wing4a', 'left_wing4b', 'left_wing3b', 'left_wing3a', 'left_wing3' )
        self.add_sheet('lwing4', sheet)
        sheet = ( 'left_wing3', 'left_wing3a', 'left_wing3b', 'left_wing2b', 'left_wing2a', 'left_wing2' )
        self.add_sheet('lwing3', sheet)
        sheet = ( 'left_wing2', 'left_wing2a', 'left_wing2b', 'left_wing1a', 'left_wing1' )
        self.add_sheet('lwing2', sheet)
        sheet = ( 'left_wing1', 'left_wing1a', 'left_shoulder' )
        self.add_sheet('lwing1', sheet)
        
        self.solidify('lwing1')
        
    def draw(self):
        self.draw_skeleton()
        self.draw_wings()

    def solidify(self, name):
        print('++++++')
        for o in bpy.context.scene.objects:
            if o.type == 'MESH':
                print(o.name)
                o.select_set(True)
            else:
                o.select_set(False)
        print('-------')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[name].select_set(True)
        o = bpy.data.objects[name]
        o.select_set(True)
        print(name)
        print(o)
        print(bpy.context.active_object)
        #mesh.solidify(1.0)
        #bpy.ops.object.modifier_add(type='SOLIDIFY')
        #bpy.context.object.modifiers[name].thickness = 1.0
        #bpy.context.object.modifiers[name].offset = -1.0
        
    def add_sheet(self, name, nodes):
        vertices = []
        for node_name in nodes:
            n = self.nodes[node_name]
            vertices.append(n)
        mesh = bpy.data.meshes.new(name)
        o = bpy.data.objects.new(name, mesh)
        bpy.context.collection.objects.link(o)
        o.location = (0, 0, 0)
        faces = [ range(len(vertices)) ]
        mesh.from_pydata(vertices, [], faces)
        mesh.update(calc_edges=True)
        
        #bpy.ops.object.select_all(action='DESELECT')
        #bpy.data.objects[name].select_set(True)
        #bpy.ops.object.select_add(action='DESELECT')
        #
        #bpy.ops.object.modifier_add(type='SOLIDIFY')
        #bpy.ops.object.delete()
        #bpy.context.object.modifiers[name].thickness = 1.0

    def add_node(self, name, center):
        self.nodes[name] = center
        bpy.ops.mesh.primitive_ico_sphere_add(radius=self.small_r, location=self.nodes[name])
        bpy.context.active_object.name = f'S({name})'
        
    def midpoint(self, node1, node2):
        p1 = self.nodes[node1]
        p2 = self.nodes[node2]
        return ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2, (p1[2]+p2[2])/2)

    def join_nodes(self, node1, node2):
        p1 = self.nodes[node1]
        p2 = self.nodes[node2]
        l = (0.5*(p1[0]+p2[0]), 0.5*(p1[1]+p2[1]), 0.5*(p1[2]+p2[2])) 
        d0 = p2[0] - p1[0]   
        d1 = p2[1] - p1[1]   
        d2 = p2[2] - p1[2]
        d = math.sqrt(d0*d0+d1*d1+d2*d2)
        u0 = d0 / d
        u1 = d1 / d
        u2 = d2 / d
        xrot = math.acos(u2)
        zrot = math.atan2(u0, -u1)
        rot = (xrot, 0, zrot)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.6*self.small_r, depth=d, location=l, rotation=rot)
        bpy.context.active_object.name = f'{node1}-{node2}'

dragon = Dragon()
dragon.draw()

for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        o.select_set(False)


 

