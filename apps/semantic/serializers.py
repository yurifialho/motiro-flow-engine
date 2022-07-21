from __future__ import annotations
import logging
from apps.semantic.models import NewSemanticModel

logger = logging.getLogger(__name__)

class SerializerUtil():

    @classmethod
    def getParam(cls, map: map, key: str) -> str:
        try:
            return map[key]
        except:
            return ""
    
    @classmethod
    def populateFromRequest(cls, obj: NewSemanticModel, map: map, update_id: bool = False) -> None:
        if obj is None or map is None:
            raise Exception("Invalid request params")
        
        for key, value in map.items():
            if key == 'storid' and update_id:
                obj.storid = int(value)
            elif key == 'id' and update_id:
                obj.id = value
            elif key not in ['storid','id']:
                if type(value) != list and not key.startswith("l_"):
                    key = f"l_{key}"
                obj.setProperties(key, value)
