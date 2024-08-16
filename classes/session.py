from dataclasses import dataclass

@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0
