class OutputWatcher:
    _log_last_read_position = 0
    _EDID_KEYWORD = b"EDID"

    def __init__(self, xorg_log_path: str):
        self.xorg_log_path = xorg_log_path

    def has_changes(self) -> bool:
        with open(self.xorg_log_path, "rb") as log:
            log.seek(self._log_last_read_position)
            data = log.read()
            self._log_last_read_position = log.tell()

        return self._EDID_KEYWORD in data
