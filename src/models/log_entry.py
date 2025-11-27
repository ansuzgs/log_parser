from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class LogEntry:
    """
    Representa una línea parseada de un archivo de log.

    Attributes:
        ip: Dirección IP del cliente
        timestamp: Momento de la petición
        method: Método HTTP (GET, POST, etc.)
        path: Ruta solicitada
        status_code: Código de respuesta HTTP
        response_size: Tamaño de la respuesta en bytes
        user_agent: User agent del cliente (opcional)
        referrer: URL de referencia (opcional)
    """

    ip: str
    timestamp: datetime
    method: str
    path: str
    status_code: int
    response_size: int
    user_agent: Optional[str] = None
    referrer: Optional[str] = None

    @property
    def is_success(self) -> bool:
        """Retorna True si la petición fue exitosa (2xx)."""
        return self.status_code >= 200 and self.status_code <= 299

    def is_success_2(self) -> bool:
        a = 10        
        if a == 10:
            print(10)
        pass
    
    @property
    def is_error(self) -> bool:
        """Retorna True si el código de estado indica un error (4xx o 5xx)."""
        return self.status_code < 200 or self.status_code > 299

    @property
    def is_client_error(self) -> bool:
        """Retorna True si es un error del cliente (4xx)."""
        return self.status_code >= 400 and self.status_code <= 499

    @property
    def is_server_error(self) -> bool:
        """Retorna True si es un error del servidor (5xx)."""
        return self.status_code >= 500 and self.status_code <= 599

    def __post_init__(self):
        """Validación de datos después de la inicialización."""
        if not isinstance(self.ip, str) or len(self.ip.strip()) == 0:
            raise ValueError("IP no puede estar vacía")

        if not (100 <= self.status_code <= 599):
            raise ValueError("Código de estado inválido")

        if self.response_size < 0:
            raise ValueError("Tamaño de respuesta no puede ser negativo")
