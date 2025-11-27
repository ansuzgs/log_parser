from datetime import datetime
import re
from typing import Optional

from ..models.log_entry import LogEntry
from .base_parser import BaseParser


class NginxParser(BaseParser):
    """
    Parser para logs en formato nginx estándar.

    Formato esperado:
    IP - - [timestamp] "METHOD path HTTP/version" status size "referrer" "user-agent"

    Ejemplo:
    192.168.1.1 - - [01/Jan/2024:12:00:00 +0000] "GET /index.html HTTP/1.1" 200 1234 "-" "Mozilla/5.0"
    """

    NGINX_PATTERN = re.compile(
        r"^(?P<ip>[\d.]+) - - "
        r"\[(?P<timestamp>[^\]]+)\] "
        r'"(?P<method>\w+) (?P<path>[^\s]+) HTTP/[^"]*" '
        r"(?P<status>\d{3}) "
        r"(?P<size>\d+) "
        r'"(?P<referrer>[^"]*)" '
        r'"(?P<user_agent>[^"]*)"'
    )

    TIMESTAMP_FORMAT = "%d/%b/%Y:%H:%M:%S %z"

    def parse_line(self, line) -> Optional[LogEntry]:
        """
        Parsea una línea de log nginx.

        Args:
            line: Línea de texto del log

        Returns:
            LogEntry si la línea coincide con el formato, None en caso contrario
        """
        match = self.NGINX_PATTERN.match(line)
        if not match:
            return None

        try:
            # Extraer datos del match
            data = match.groupdict()

            # Parsear el timestamp
            timestamp = datetime.strptime(data["timestamp"], self.TIMESTAMP_FORMAT)

            # Manejar campos opcionales
            referrer = data["referrer"] if data["referrer"] != "-" else None
            user_agent = data["user_agent"] if data["user_agent"] != "-" else None

            # Crear LogEntry
            return LogEntry(
                ip=data["ip"],
                timestamp=timestamp,
                method=data["method"],
                path=data["path"],
                status_code=int(data["status"]),
                response_size=int(data["size"]),
                referrer=referrer,
                user_agent=user_agent,
            )
        except (ValueError, KeyError) as e:
            return None
