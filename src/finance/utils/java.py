from decimal import Decimal
from py4j.java_collections import JavaMap, JavaList


def map_to_dict(java_obj: JavaMap) -> dict:
    if isinstance(java_obj, JavaMap):
        return {key: map_to_dict(value) for key, value in java_obj.items()}

    if isinstance(java_obj, JavaList):
        return [map_to_dict(x) for x in java_obj]

    if isinstance(java_obj, Decimal):
        return float(java_obj)

    return java_obj
