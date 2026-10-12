from enum import Enum
class Status(Enum):
    QUEUED = "queued"
    RUNNING = "running"
    DONE = "done"
    CANCELLED = "cancelled"
def is_terminal(status: Status) -> bool:
    return status in (Status.DONE, Status.CANCELLED)
