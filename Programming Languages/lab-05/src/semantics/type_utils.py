#  Copyright (c) 2021. Created by Mateusz Slazynski for the educational purposes.
#     Feel free to use/modify this code for any greater good.
#     It would be nice however if you mentioned me somewhere.
#     Still, no pressure - have a nice day!

from src.type import LambdaType, InvalidType, ArrowType, RecordType, VariantType


def type_is_invalid(t: LambdaType) -> bool:
    # TODO:
    # You should check here whether RecordType and VariantType are valid
    match t:
        case InvalidType():
            return True
        case ArrowType(left, right):
            return type_is_invalid(left) or type_is_invalid(right)
        case RecordType(types_r):
            return any(type_is_invalid(type_r) for type_r in types_r.values())
        case VariantType(types_v):
            return any(type_is_invalid(type_v) for type_v in types_v.values())
        case _:
            return False