import bpy
from bpy.props import *
from ... base_types.node import AnimationNode
from ... sockets.info import getBaseDataTypeItems, toListIdName, getListDataTypes, toBaseDataType

class CombineListsNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_CombineListsNode"
    bl_label = "Combine Lists"
    onlySearchTags = True

    @classmethod
    def getSearchTags(cls):
        return [("Combine " + dataType, {"assignedType" : repr(toBaseDataType(dataType))})
                for dataType in getListDataTypes()]

    def assignedTypeChanged(self, context):
        self.listIdName = toListIdName(self.assignedType)
        self.recreateSockets()

    selectedType = EnumProperty(name = "Type", items = getBaseDataTypeItems)
    assignedType = StringProperty(update = assignedTypeChanged)

    listIdName = StringProperty()

    def create(self):
        self.selectedType = "Float"
        self.assignedType = "Float"

    def draw(self, layout):
        self.invokeFunction(layout, "newInputSocket",
            text = "New Input",
            description = "Create a new input socket",
            icon = "PLUS")

    def drawAdvanced(self, layout):
        layout.prop(self, "selectedType")
        self.invokeFunction(layout, "assignSelectedListType",
            text = "Assign",
            description = "Remove all sockets and set the selected socket type")

    @property
    def inputVariables(self):
        return { socket.identifier : "list_" + str(i) for i, socket in enumerate(self.inputs) }

    def getExecutionCode(self):
        lines = []
        lines.append("outList = []")
        for i, socket in enumerate(self.inputs):
            if socket.name == "...": continue
            lines.append("outList.extend({})".format("list_" + str(i)))
        return lines

    def edit(self):
        emptySocket = self.inputs["..."]
        origin = emptySocket.directOrigin
        if origin is None: return
        socket = self.newInputSocket()
        socket.linkWith(origin)
        emptySocket.removeLinks()

    def assignSelectedListType(self):
        self.assignedType = self.selectedType

    def recreateSockets(self, inputAmount = 2):
        self.inputs.clear()
        self.outputs.clear()

        self.inputs.new("an_NodeControlSocket", "...")
        for _ in range(inputAmount):
            self.newInputSocket()
        self.outputs.new(self.listIdName, "List", "outList")

    def newInputSocket(self):
        socket = self.inputs.new(self.listIdName, "List")
        socket.dataIsModified = True
        socket.display.text = True
        socket.text = "List"
        socket.removeable = True
        socket.moveable = True
        socket.textProps.editable = True
        socket.defaultDrawType = "PREFER_PROPERTY"
        socket.moveUp()
        return socket
