from collections import Counter
from datetime import date
from typing import Dict, List, Optional, Tuple, Set
from ..models.log_entry import LogEntry


class LogAnalyzer:
    """Analiza logs y calcula metricas"""

    def __init__(self, logs: List[LogEntry]) -> None:
        """Inicializa con lista de LogEntry"""
        self.logs = logs

    def total_requests(self) -> int:
        """Retorna el total de requests"""
        return len(self.logs)

    def total_errors(self) -> int:
        """Retorna el total de errores (4xx + 5xx)"""
        return sum(1 for e in self.logs if e.is_error)

    def total_success(self) -> int:
        """Retorna el total de exitos (2xx)"""
        return sum(1 for e in self.logs if e.is_success)

    def get_status_counts(self) -> Dict[int, int]:
        """Retorna conteo de códigos de estado"""
        return dict(Counter(e.status_code for e in self.logs))

    def most_common_status(self) -> Optional[int]:
        """Retorna código de estado más común."""
        if not self.logs:
            return None

        counter = Counter(e.status_code for e in self.logs)
        return counter.most_common(1)[0][0]

    def top_ips(self, n: int = 10) -> List[Tuple[str, int]]:
        """Retorna top N IPs más activas."""
        counter = Counter(e.ip for e in self.logs)
        return counter.most_common(n)

    def top_paths(self, n: int = 10) -> List[Tuple[str, int]]:
        """Retorna top N paths más activas."""
        counter = Counter(e.path for e in self.logs)
        return counter.most_common(n)

    def get_method_counts(self) -> Dict[str, int]:
        """Retorna conteno de metodos HTTP"""
        return dict(Counter(e.method for e in self.logs))

    def most_common_method(self) -> Optional[str]:
        """Retorna metodo HTTP más común."""
        if not self.logs:
            return None

        counter = Counter(e.method for e in self.logs)
        return counter.most_common(1)[0][0]

    def error_rate(self) -> float:
        """Retorna el ratio de errores"""
        if not self.logs:
            return 0.0
        return float(self.total_errors() / len(self.logs))

    def get_errors(self) -> List[LogEntry]:
        """Retorna las entradas con errores"""
        return [e for e in self.logs if e.is_error]

    def client_error_count(self) -> int:
        """Retorna el numero de errores de cliente (4xx)"""
        return sum(1 for e in self.logs if e.is_client_error)

    def server_error_count(self) -> int:
        """Retorna el numero de errores de server (5xx)"""
        return sum(1 for e in self.logs if e.is_server_error)

    def requests_by_hour(self) -> Dict[int, int]:
        """Agrupa requests por hora del dia"""
        counter = Counter(e.timestamp.hour for e in self.logs)
        return dict(counter)

    def busiest_hour(self) -> Optional[int]:
        """Retorna la hora con mas trafico"""
        by_hour = self.requests_by_hour()
        if not by_hour:
            return None
        return max(by_hour.items(), key=lambda x: x[1])[0]

    def requests_by_date(self) -> Dict[date, int]:
        """Agrupa requests por fecha"""
        counter = Counter(e.timestamp.date() for e in self.logs)
        return dict(counter)

    def total_bytes_transferred(self) -> int:
        """Retorna el numero total de bytes transferidos"""
        return sum(e.response_size for e in self.logs)

    def average_response_size(self) -> float:
        """Retorna el tamaño medio de respuesta"""
        return self.total_bytes_transferred() / len(self.logs)

    def largest_response(self) -> Optional[LogEntry]:
        """Retorna la entrada con la respuesta mas grande"""
        if not self.logs:
            return None

        return max(self.logs, key=lambda e: e.response_size)

    def unique_ips_count(self) -> int:
        """Retorna el numero de IPs unicas"""
        return len(set(e.ip for e in self.logs))

    def get_unique_ips(self) -> Set[str]:
        """Retorna un set con todas las IPs unicas"""
        return set(e.ip for e in self.logs)

    def filter_by_status(self, status: int) -> Optional[List[LogEntry]]:
        """Retorna la lista de requests filtrada por status_code"""
        return [e for e in self.logs if e.status_code == status]

    def filter_by_ip(self, ip: str) -> Optional[List[LogEntry]]:
        """Retorna la lista de requests filtrada por ip"""
        return [e for e in self.logs if e.ip == ip]

    def filter_by_method(self, method: str) -> Optional[List[LogEntry]]:
        """Retorna la lista de requests filtrada por method"""
        return [e for e in self.logs if e.method == method]

    def filter_by_path(self, path: str) -> Optional[List[LogEntry]]:
        """Retorna la lista de requests filtrada por path"""
        return [e for e in self.logs if e.path == path]

    def get_summary(self) -> Dict[str, int | float]:
        """Retorna el resumen"""
        return {
            "total_requests": self.total_requests(),
            "total_errors": self.total_errors(),
            "error_rate": self.error_rate(),
            "unique_ips": self.unique_ips_count(),
            "total_bytes": self.total_bytes_transferred()
        }












