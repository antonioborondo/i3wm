from enum import Enum
import subprocess


class Status(Enum):
    UNKNOWN = "unknown"
    CLOSED = "closed"
    OPEN = "open"


class Lid:
    def status(self) -> Status:
        try:
            command = [
                "sh",
                "-c",
                "cat /proc/acpi/button/lid/LID0/state | awk '{print $2}'",
            ]
            command_result = subprocess.run(
                command, capture_output=True, check=True, text=True
            )
            command_output = command_result.stdout.strip()

            if command_output == Status.CLOSED.value:
                return Status.CLOSED
            elif command_output == Status.OPEN.value:
                return Status.OPEN
            else:
                return Status.UNKNOWN

        except Exception:
            return Status.UNKNOWN
