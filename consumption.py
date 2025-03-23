from datetime import datetime
from typing import Dict


class Consumption:
    def __init__(self, source: str, buckets: Dict[datetime, int]) -> None:
        self.source = source
        self.buckets = buckets
