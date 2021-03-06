import bpy
from mathutils import Vector
from math import radians


class OBJECT_OT_AlignLabels(bpy.types.Operator):
    '''Aligns labels to currently active camera '''
    bl_idname = 'object.align_labels'
    bl_label = 'Align Labels To Camera'
    bl_options = {'REGISTER', 'UNDO'}

    align_header: bpy.props.BoolProperty(
        default=True,
        name='Align header'
    )

    align_axis_labels: bpy.props.BoolProperty(
        default=True,
        name='Align axis labels'
    )

    @classmethod
    def poll(cls, context):
        return bpy.context.object and bpy.context.scene.camera

    def execute(self, context):
        axis_count = 0
        is_pie = False
        for child in bpy.context.object.children:
            if 'Axis_Container_AxisDir.X' in child.name:
                self.align_labels('x', child)
                axis_count += 1
            elif 'Axis_Container_AxisDir.Y' in child.name:
                self.align_labels('y', child)
                axis_count += 1
            elif 'Axis_Container_AxisDir.Z' in child.name:
                self.align_labels('z', child)
                axis_count += 1

            if child.name.startswith('TextPie'):
                self.align_labels('to', child)
                is_pie = True
            if child.name == 'TextHeader':
                if not self.align_header:
                    continue
                self.align_labels('to', child)

        if axis_count in [2, 3] or is_pie:
            self.report({'INFO'}, 'Labels aligned!')
            return {'FINISHED'}
        else:   
            self.report({'WARNING'}, 'Select valid chart container!')
            return {'CANCELLED'}

    def align_labels(self, obj_type, obj):
        cam_vector = self.get_camera_vector()

        if obj_type == 'to':
            obj.rotation_euler = cam_vector
            return
        
        if not self.align_axis_labels:
            return

        for child in obj.children:
            if child.name.startswith('Text'):
                if child.name.startswith('TextLabel') and not self.align_axis_labels:
                    continue
                if obj_type == 'z':
                    child.rotation_euler = (radians(180), radians(90) - cam_vector[2], radians(90))
                elif obj_type == 'y':
                    child.rotation_euler = Vector(cam_vector) - Vector(obj.rotation_euler)
                else:
                    child.rotation_euler = cam_vector
    
    def get_camera_vector(self):
        camera = bpy.context.scene.camera
        return camera.rotation_euler
