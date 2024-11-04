from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
import re
import subprocess
import time

@dataclass
class Resolution:
    x: int
    y: int


@dataclass
class Size:
    x: int
    y: int


class Type(Enum):
    LAPTOP = 1
    MONITOR = 2


class Status(Enum):
    DISABLED = 1
    ENABLED = 2


class Dpi(Enum):
    NORMAL = 96
    HIGH = 192


@dataclass
class Output:
    id: str = ""
    resolution: Resolution = None
    size: Optional[Size] = None

    def type(self) -> Type:
        if self.id == "eDP-1":
            return Type.LAPTOP
        else:
            return Type.MONITOR

    def status(self) -> Status:
        if self.size == None:
            return Status.DISABLED
        else:
            return Status.ENABLED

    def dpi(self) -> Dpi:
        if self.resolution and self.size:
            size_x_in_cm = self.size.x / 10
            size_x_in_in = size_x_in_cm / 2.54
            dpi_x = self.resolution.x / size_x_in_in

            size_y_in_cm = self.size.y / 10
            size_y_in_in = size_y_in_cm / 2.54
            dpi_y = self.resolution.y / size_y_in_in

            if max(dpi_x, dpi_y) > 150:
                return Dpi.HIGH
            else:
                return Dpi.NORMAL
        else:
            return Dpi.NORMAL

    def enable(self):
        # Set the DPI with xrdb to ensure the mouse and GTK apps are displayed correctly.
        # Note: GTK apps need to be restarted for the changes to take effect.
        command = f'echo "Xft.dpi: {self.dpi().value}" | xrdb -merge'
        subprocess.run(command, shell=True)

        # Set the DPI with xrandr to ensure i3 UI elements are displayed correctly.
        command = f"xrandr --output {self.id} --dpi {self.dpi().value} --mode {self.resolution.x}x{self.resolution.y} --pos 0x0 --primary --rotate normal"
        subprocess.run(command, shell=True)

    def disable(self):
        command = f"xrandr --output {self.id} --off"
        subprocess.run(command, shell=True)


class Outputs(list):
    def __init__(self):
        super().__init__()
        self.update()

    def update(self):
        command = "xrandr | grep -A 1 --no-group-separator -w connected"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")

        self.clear()
        for i in range(0, len(lines) - 1, 2):

            output = Output()

            id_match = re.search(r"^(.+)\sconnected\s.*$", lines[i])
            output.id = id_match.group(1)

            size_match = re.search(r"^.*\s([0-9]+)mm\sx\s([0-9]+)mm$", lines[i])
            if size_match:
                output.size = Size(int(size_match.group(1)), int(size_match.group(2)))

            resolution_match = re.search(
                r"^\s+([0-9]+)x([0-9]+)\s+[0-9]+\.[0-9]+(?:\*|\s)\+$", lines[i + 1]
            )
            output.resolution = Resolution(
                int(resolution_match.group(1)), int(resolution_match.group(2))
            )

            self.append(output)
        time.sleep(1) # Give some time between calls

    def has_enabled(self) -> bool:
        self.update()
        return any(output.status() == Status.ENABLED for output in self)
