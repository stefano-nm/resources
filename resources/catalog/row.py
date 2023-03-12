from ..utils import JSONObj


class Row(JSONObj):
    name: str
    endpoint: str
    timestamp: float
    token: str
