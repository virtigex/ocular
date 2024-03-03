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
        self.small_r = 0.4
        self.nodes = {}
    
    def draw(self):
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
        self.add_node('left_wing1', (-5, -1, 9))
        self.add_node('left_wing2', (-9, 1, 14))
        self.add_node('left_wing3', (-12, -4, 20))
        self.add_node('left_wing4', (-15, -12, 15))
        self.add_node('right_wing1', (5, -1, 9))
        self.add_node('right_wing2', (9, 1, 14))
        self.add_node('right_wing3', (12, -4, 20))
        self.add_node('right_wing4', (15, -12, 15))

        self.join_nodes('mid_shoulder', 'left_wing1')
        self.join_nodes('left_wing1', 'left_wing2')
        self.join_nodes('left_wing2', 'left_wing3')
        self.join_nodes('left_wing3', 'left_wing4')
        self.join_nodes('mid_shoulder', 'right_wing1')
        self.join_nodes('right_wing1', 'right_wing2')
        self.join_nodes('right_wing2', 'right_wing3')
        self.join_nodes('right_wing3', 'right_wing4')
                
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
        q = bpy.ops.mesh.primitive_cylinder_add(radius=0.6*self.small_r, depth=d, location=l, rotation=rot)
        bpy.context.active_object.name = f'{node1}-{node2}'

dragon = Dragon()
dragon.draw()

 

