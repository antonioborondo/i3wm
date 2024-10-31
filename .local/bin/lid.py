from enum import Enum
import subprocess


class Lid:
    class Status(Enum):
        UNKNOWN = "unknown"
        CLOSED = "closed"
        OPEN = "open"

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

            if command_output == self.Status.CLOSED.value:
                return self.Status.CLOSED
            elif command_output == self.Status.OPEN.value:
                return self.Status.OPEN
            else:
                return self.Status.UNKNOWN

        except Exception:
            return self.Status.UNKNOWN
