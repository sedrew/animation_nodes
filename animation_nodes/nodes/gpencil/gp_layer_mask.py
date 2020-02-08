import bpy
from ... data_structures import VirtualBooleanList
from ... base_types import AnimationNode, VectorizedSocket

class GPLayerMaskLayerNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_GPLayerMaskNode"
    bl_label = "GP Layer Mask"

    useLayerList: VectorizedSocket.newProperty()
    useBooleanList: VectorizedSocket.newProperty()

    def create(self):
        self.newInput(VectorizedSocket("GPLayer", "useLayerList",
            ("Layer", "layer"), ("Layers", "layers")), dataIsModified = True)
        self.newInput(VectorizedSocket("Boolean", "useBooleanList",
            ("Mask", "maskLayer"), ("Masks", "masks")))
        self.newOutput(VectorizedSocket("GPLayer", ["useLayerList", "useBooleanList"],
            ("Layer", "layer"), ("Layers", "layers")))

    def getExecutionFunctionName(self):
        if self.useLayerList and self.useBooleanList:
            return "execute_LayerList_MaskList"
        elif self.useLayerList:
            return "execute_LayerList_Mask"
        elif self.useBooleanList:
            return "execute_Layer_MaskList"
        else:
            return "execute_Layer_Mask"

    def execute_Layer_Mask(self, layer, maskLayer):
        layer.maskLayer = maskLayer
        return layer

    def execute_Layer_MaskList(self, layer, masks):
        if len(masks) == 0: return [layer]

        layers = []
        for maskLayer in masks:
            layerNew = layer.copy()
            layer.maskLayer = maskLayer
            layers.append(layerNew)
        return layers

    def execute_LayerList_Mask(self, layers, maskLayer):
        if len(layers) == 0: return layers
        for layer in layers:
            layer.maskLayer = maskLayer
        return layers

    def execute_LayerList_MaskList(self, layers, masks):
        if len(layers) == 0 or len(masks) == 0: return layers
        masks = VirtualBooleanList.create(masks, False)
        for i, layer in enumerate(layers):
            layer.maskLayer = masks[i]
        return layers
