#!/usr/bin/env python

import time
from enum import Enum
import subprocess

class LidStatus(Enum):
    CLOSED = 1
    OPEN = 2

def get_lid_status() -> LidStatus:
    command = "cat /proc/acpi/button/lid/LID0/state | awk '{print $2}'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout.strip().split("\n")[0]

    if output == "closed":
        print("closed")
        return LidStatus.CLOSED

    else:
        print("open")
        return LidStatus.OPEN


def main():
    while True:

        get_lid_status()

        time.sleep(1)

if __name__ == "__main__":
    main()
