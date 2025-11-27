from abc import ABC, abstractmethod
from typing import Iterator, Optional

from src.models.log_entry import LogEntry


class BaseParser(ABC):

    @abstractmethod
    def parse_line(self, line) -> Optional[LogEntry]:
        pass

    def parse_file(self, file) -> Iterator[LogEntry]:
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                # if not line or line.startswith("#"):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                try:
                    tmp = self.parse_line(line)
                    if tmp is None:
                        continue
                    yield tmp
                except ValueError:
                    pass
