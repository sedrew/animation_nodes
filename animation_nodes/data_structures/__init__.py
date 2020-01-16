def importDataStructures():
    from . color import Color
    from . struct import ANStruct
    from . vector2d import Vector2D

    from . meshes.mesh_data import Mesh
    from . lists.clist import CList
    from . lists.polygon_indices_list import PolygonIndicesList
    from . lists.base_lists import (
        Vector3DList, Vector2DList, Matrix4x4List, EdgeIndicesList, EulerList, ColorList,
        BooleanList, FloatList, DoubleList, LongList, IntegerList, UShortList, CharList,
        QuaternionList, UIntegerList, ShortList, UShortList
    )

    from . virtual_list.virtual_list import VirtualList, VirtualPyList
    from . virtual_list.virtual_clists import (
        VirtualVector3DList, VirtualMatrix4x4List, VirtualEulerList, VirtualBooleanList,
        VirtualFloatList, VirtualDoubleList, VirtualLongList, VirtualColorList
    )

    from . splines.base_spline import Spline
    from . splines.poly_spline import PolySpline
    from . splines.bezier_spline import BezierSpline
    from . default_lists.c_default_list import CDefaultList
    from . interpolation import Interpolation
    from . falloffs.falloff_base import Falloff, BaseFalloff, CompoundFalloff

    from . sounds.sound import Sound
    from . sounds.sound_data import SoundData
    from . sounds.sound_sequence import SoundSequence

    from . action import (
        Action, ActionEvaluator, ActionChannel,
        PathActionChannel, PathIndexActionChannel,
        BoundedAction, UnboundedAction,
        BoundedActionEvaluator, UnboundedActionEvaluator,
        SimpleBoundedAction, SimpleUnboundedAction,
        DelayAction
    )

    return locals()

dataStructures = importDataStructures()
__all__ = list(dataStructures.keys())
globals().update(dataStructures)
