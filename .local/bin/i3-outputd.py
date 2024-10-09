#!/usr/bin/env python

from dataclasses import dataclass
from enum import Enum
from typing import List
import re
import subprocess
import time


class OutputType(Enum):
    LAPTOP = 1
    MONITOR = 2


class OutputStatus(Enum):
    DISABLED = 1
    ENABLED = 2


@dataclass
class Resolution:
    x: int
    y: int


@dataclass
class Size:
    x: int
    y: int


@dataclass
class Output:
    id: str = ""
    resolution: Resolution = None
    size: Size = None
    dpi: int = 96

    def type(self) -> OutputType:
        if self.id == "eDP-1":
            return OutputType.LAPTOP
        else:
            return OutputType.MONITOR

    def status(self) -> OutputStatus:
        if self.size == None:
            return OutputStatus.DISABLED
        else:
            return OutputStatus.ENABLED


def calculate_dpi(resolution: Resolution, size: Size) -> int:
    if resolution and size:
        size_x_in_cm = size.x / 10
        size_x_in_in = size_x_in_cm / 2.54
        dpi_x = resolution.x / size_x_in_in

        size_y_in_cm = size.y / 10
        size_y_in_in = size_y_in_cm / 2.54
        dpi_y = resolution.y / size_y_in_in

        # return int(max(dpi_x, dpi_y))
        if max(dpi_x, dpi_y) > 150:
            return 192
        else:
            return 96
    else:
        return 96


def get_outputs() -> List[Output]:
    command = "xrandr | grep -A 1 --no-group-separator -w connected"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")

    outputs: List[Output] = []
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

        output.dpi = calculate_dpi(output.resolution, output.size)

        outputs.append(output)

    return outputs

def enable_output(output: Output):
    # Set the DPI with xrdb to ensure the mouse and GTK apps are displayed correctly.
    # Note: GTK apps need to be restarted for the changes to take effect.
    command = f'echo "Xft.dpi: {output.dpi}" | xrdb -merge'
    subprocess.run(command, shell=True)

    # Set the DPI with xrandr to ensure i3 UI elements are displayed correctly.
    command = f"xrandr --output {output.id} --dpi {output.dpi} --mode {output.resolution.x}x{output.resolution.y} --pos 0x0 --primary --rotate normal"
    subprocess.run(command, shell=True)


def disable_output(output: Output):
    command = f"xrandr --output {output.id} --off"
    subprocess.run(command, shell=True)

def disable_outputs(outputs: List[Output]):
    for output in outputs:
        disable_output(output)


def enable_outputs(outputs: List[Output], output_type: OutputType):
    for output in outputs:
        if output.type() == output_type:
            enable_output(output)
            if output.status() == OutputStatus.DISABLED:
                updated_outputs = get_outputs()
                for updated_output in updated_outputs:
                    if updated_output.id == output.id:
                        enable_output(updated_output)
        else:
            disable_output(output)


class LidStatus(Enum):
    CLOSED = 1
    OPEN = 2


def get_lid_status() -> LidStatus:
    command = "cat /proc/acpi/button/lid/LID0/state | awk '{print $2}'"
    result = subprocess.run(command, capture_output=True, shell=True, text=True)
    output = result.stdout.strip()

    if output == "closed":
        return LidStatus.CLOSED
    else:
        return LidStatus.OPEN


def main():
    while True:
        lid_status = get_lid_status()
        if lid_status == LidStatus.CLOSED:
            outputs = get_outputs()
            if len(outputs) == 1:
                disable_output(outputs)
            else:
                enable_outputs(outputs, OutputType.MONITOR)
        else:
            outputs = get_outputs()
            if len(outputs) == 1:
                enable_outputs(outputs, OutputType.LAPTOP)
            else:
                enable_outputs(outputs, OutputType.MONITOR)

        time.sleep(1)


if __name__ == "__main__":
    main()
