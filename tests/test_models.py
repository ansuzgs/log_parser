import pytest
from datetime import date, datetime
from src.models.log_entry import LogEntry


class TestLogEntryCreation:
    """Tests para verificar que LogEntry se puede crear correctamente."""

    def test_log_entry_can_be_created_with_required_fields(self):
        """Test 1: LogEntry se puede crear con campos requeridos."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime(2024, 11, 26, 12, 0, 0),
            method="GET",
            path="/index.html",
            status_code=200,
            response_size=1024,
        )

        assert entry is not None
        assert isinstance(entry, LogEntry)

    def test_log_entry_stores_ip_correctly(self):
        """Test 2: LogEntry almacena la IP correctamente."""
        entry = LogEntry(
            ip="192.168.1.100",
            timestamp=datetime.now(),
            method="GET",
            path="/",
            status_code=200,
            response_size=100,
        )

        assert entry.ip == "192.168.1.100"

    def test_log_entry_stores_timestamp_correctly(self):
        """Test 3: LogEntry almacena el timestamp correctamente."""
        test_time = datetime(2024, 11, 26, 15, 30, 45)
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=test_time,
            method="GET",
            path="/",
            status_code=200,
            response_size=100,
        )

        assert entry.timestamp == test_time
        assert isinstance(entry.timestamp, datetime)

    def test_log_entry_stores_method_correctly(self):
        """Test 4: LogEntry almacena el método HTTP correctamente."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="POST",
            path="/api/login",
            status_code=200,
            response_size=100,
        )

        assert entry.method == "POST"

    def test_log_entry_stores_path_correctly(self):
        """Test 5: LogEntry almacena la ruta correctamente."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/api/users/123",
            status_code=200,
            response_size=100,
        )

        assert entry.path == "/api/users/123"

    def test_log_entry_stores_status_code_correctly(self):
        """Test 6: LogEntry almacena el código de estado correctamente."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/",
            status_code=404,
            response_size=100,
        )

        assert entry.status_code == 404
        assert isinstance(entry.status_code, int)

    def test_log_entry_stores_response_size_correctly(self):
        """Test 7: LogEntry almacena el tamaño de respuesta correctamente."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/",
            status_code=200,
            response_size=2048,
        )

        assert entry.response_size == 2048
        assert isinstance(entry.response_size, int)


# ============================================================================
# FASE 2: Tests de Campos Opcionales
# ============================================================================


class TestLogEntryOptionalFields:
    """Tests para campos opcionales (user_agent, referrer)."""

    def test_log_entry_without_optional_fields(self):
        """Test 8: LogEntry se puede crear sin campos opcionales."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/",
            status_code=200,
            response_size=100,
        )

        # Los campos opcionales deben ser None por defecto
        assert entry.user_agent is None
        assert entry.referrer is None

    def test_log_entry_with_user_agent(self):
        """Test 9: LogEntry almacena user_agent cuando se proporciona."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/",
            status_code=200,
            response_size=100,
            user_agent="Mozilla/5.0",
        )

        assert entry.user_agent == "Mozilla/5.0"

    def test_log_entry_with_referrer(self):
        """Test 10: LogEntry almacena referrer cuando se proporciona."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/",
            status_code=200,
            response_size=100,
            referrer="https://example.com",
        )

        assert entry.referrer == "https://example.com"

    def test_log_entry_with_all_fields(self):
        """Test 11: LogEntry con todos los campos (requeridos y opcionales)."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/",
            status_code=200,
            response_size=100,
            user_agent="Mozilla/5.0",
            referrer="https://example.com",
        )

        assert entry.user_agent == "Mozilla/5.0"
        assert entry.referrer == "https://example.com"


# ============================================================================
# FASE 3: Tests de Properties - is_success
# ============================================================================


class TestIsSuccess:
    """Tests para la property is_success."""

    def test_status_200_is_success(self):
        """Test 12: Código 200 es éxito."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/",
            status_code=200,
            response_size=100,
        )

        assert entry.is_success is True

    def test_status_201_is_success(self):
        """Test 13: Código 201 es éxito."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="POST",
            path="/api",
            status_code=201,
            response_size=100,
        )

        assert entry.is_success is True

    def test_status_299_is_success(self):
        """Test 14: Código 299 (último 2xx) es éxito."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/",
            status_code=299,
            response_size=100,
        )

        assert entry.is_success is True

    def test_status_300_is_not_success(self):
        """Test 15: Código 300 no es éxito."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/",
            status_code=300,
            response_size=100,
        )

        assert entry.is_success is False

    def test_status_404_is_not_success(self):
        """Test 16: Código 404 no es éxito."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/notfound",
            status_code=404,
            response_size=100,
        )

        assert entry.is_success is False


# ============================================================================
# FASE 4: Tests de Properties - is_error
# ============================================================================


class TestIsError:
    """Tests para la property is_error (4xx o 5xx)."""

    def test_status_200_is_not_error(self):
        """Test 17: Código 200 no es error."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/",
            status_code=200,
            response_size=100,
        )

        assert entry.is_error is False

    def test_status_400_is_error(self):
        """Test 18: Código 400 es error."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/",
            status_code=400,
            response_size=100,
        )

        assert entry.is_error is True

    def test_status_404_is_error(self):
        """Test 19: Código 404 es error."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/notfound",
            status_code=404,
            response_size=100,
        )

        assert entry.is_error is True

    def test_status_500_is_error(self):
        """Test 20: Código 500 es error."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="POST",
            path="/api",
            status_code=500,
            response_size=100,
        )

        assert entry.is_error is True

    def test_status_503_is_error(self):
        """Test 21: Código 503 es error."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/",
            status_code=503,
            response_size=100,
        )

        assert entry.is_error is True


# ============================================================================
# FASE 5: Tests de Properties - is_client_error
# ============================================================================


class TestIsClientError:
    """Tests para la property is_client_error (4xx)."""

    def test_status_400_is_client_error(self):
        """Test 22: Código 400 es error de cliente."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/",
            status_code=400,
            response_size=100,
        )

        assert entry.is_client_error is True

    def test_status_404_is_client_error(self):
        """Test 23: Código 404 es error de cliente."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/notfound",
            status_code=404,
            response_size=100,
        )

        assert entry.is_client_error is True

    def test_status_499_is_client_error(self):
        """Test 24: Código 499 (último 4xx) es error de cliente."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/",
            status_code=499,
            response_size=100,
        )

        assert entry.is_client_error is True

    def test_status_500_is_not_client_error(self):
        """Test 25: Código 500 NO es error de cliente (es de servidor)."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/",
            status_code=500,
            response_size=100,
        )

        assert entry.is_client_error is False

    def test_status_200_is_not_client_error(self):
        """Test 26: Código 200 NO es error de cliente."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/",
            status_code=200,
            response_size=100,
        )

        assert entry.is_client_error is False


# ============================================================================
# FASE 6: Tests de Properties - is_server_error
# ============================================================================


class TestIsServerError:
    """Tests para la property is_server_error (5xx)."""

    def test_status_500_is_server_error(self):
        """Test 27: Código 500 es error de servidor."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="POST",
            path="/api",
            status_code=500,
            response_size=100,
        )

        assert entry.is_server_error is True

    def test_status_502_is_server_error(self):
        """Test 28: Código 502 es error de servidor."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/",
            status_code=502,
            response_size=100,
        )

        assert entry.is_server_error is True

    def test_status_503_is_server_error(self):
        """Test 29: Código 503 es error de servidor."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/",
            status_code=503,
            response_size=100,
        )

        assert entry.is_server_error is True

    def test_status_404_is_not_server_error(self):
        """Test 30: Código 404 NO es error de servidor (es de cliente)."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/notfound",
            status_code=404,
            response_size=100,
        )

        assert entry.is_server_error is False

    def test_status_200_is_not_server_error(self):
        """Test 31: Código 200 NO es error de servidor."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/",
            status_code=200,
            response_size=100,
        )

        assert entry.is_server_error is False


# ============================================================================
# FASE 7: Tests de Validación
# ============================================================================


class TestLogEntryValidation:
    """Tests para validación de datos en __post_init__."""

    def test_empty_ip_raises_error(self):
        """Test 32: IP vacía debe lanzar ValueError."""
        with pytest.raises(ValueError, match="IP no puede estar vacía"):
            LogEntry(
                ip="",
                timestamp=datetime.now(),
                method="GET",
                path="/",
                status_code=200,
                response_size=100,
            )

    def test_invalid_status_code_too_low(self):
        """Test 33: Código de estado < 100 debe lanzar ValueError."""
        with pytest.raises(ValueError, match="Código de estado inválido"):
            LogEntry(
                ip="192.168.1.1",
                timestamp=datetime.now(),
                method="GET",
                path="/",
                status_code=99,
                response_size=100,
            )

    def test_invalid_status_code_too_high(self):
        """Test 34: Código de estado > 599 debe lanzar ValueError."""
        with pytest.raises(ValueError, match="Código de estado inválido"):
            LogEntry(
                ip="192.168.1.1",
                timestamp=datetime.now(),
                method="GET",
                path="/",
                status_code=600,
                response_size=100,
            )

    def test_negative_response_size_raises_error(self):
        """Test 35: Tamaño de respuesta negativo debe lanzar ValueError."""
        with pytest.raises(
            ValueError, match="Tamaño de respuesta no puede ser negativo"
        ):
            LogEntry(
                ip="192.168.1.1",
                timestamp=datetime.now(),
                method="GET",
                path="/",
                status_code=200,
                response_size=-100,
            )

    def test_zero_response_size_is_valid(self):
        """Test 36: Tamaño de respuesta 0 es válido (ej: 204 No Content)."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="DELETE",
            path="/api/resource",
            status_code=204,
            response_size=0,
        )

        assert entry.response_size == 0


# ============================================================================
# FASE 8: Tests de Inmutabilidad (Dataclass Frozen)
# ============================================================================


class TestLogEntryImmutability:
    """Tests para verificar que LogEntry es inmutable (frozen=True)."""

    def test_cannot_modify_ip(self):
        """Test 37: No se puede modificar IP después de crear."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/",
            status_code=200,
            response_size=100,
        )

        with pytest.raises(AttributeError):
            entry.ip = "192.168.1.2"

    def test_cannot_modify_status_code(self):
        """Test 38: No se puede modificar status_code después de crear."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/",
            status_code=200,
            response_size=100,
        )

        with pytest.raises(AttributeError):
            entry.status_code = 404

    def test_cannot_modify_method(self):
        """Test 39: No se puede modificar method después de crear."""
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/",
            status_code=200,
            response_size=100,
        )

        with pytest.raises(AttributeError):
            entry.method = "POST"


# ============================================================================
# FASE 9: Tests de Casos Edge y Combinaciones
# ============================================================================


class TestEdgeCases:
    """Tests para casos especiales y edge cases."""

    def test_different_http_methods(self):
        """Test 40: Diferentes métodos HTTP son soportados."""
        methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]

        for method in methods:
            entry = LogEntry(
                ip="192.168.1.1",
                timestamp=datetime.now(),
                method=method,
                path="/",
                status_code=200,
                response_size=100,
            )
            assert entry.method == method

    def test_long_path(self):
        """Test 41: Rutas largas son soportadas."""
        long_path = "/api/v1/users/123/posts/456/comments/789/replies?page=1&limit=10"
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path=long_path,
            status_code=200,
            response_size=100,
        )

        assert entry.path == long_path

    def test_large_response_size(self):
        """Test 42: Tamaños de respuesta grandes son soportados."""
        large_size = 10_000_000  # 10 MB
        entry = LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/file.zip",
            status_code=200,
            response_size=large_size,
        )

        assert entry.response_size == large_size

    def test_all_status_code_categories(self):
        """Test 43: Todos los rangos de códigos de estado funcionan correctamente."""
        test_cases = [
            (200, True, False, False, False),  # 2xx: success, not error
            (404, False, True, True, False),  # 4xx: not success, error, client error
            (500, False, True, False, True),  # 5xx: not success, error, server error
        ]

        for (
            status,
            expected_success,
            expected_error,
            expected_client,
            expected_server,
        ) in test_cases:
            entry = LogEntry(
                ip="192.168.1.1",
                timestamp=datetime.now(),
                method="GET",
                path="/",
                status_code=status,
                response_size=100,
            )

            assert entry.is_success == expected_success
            assert entry.is_error == expected_error
            assert entry.is_client_error == expected_client
            assert entry.is_server_error == expected_server


# ============================================================================
# FIXTURES PARA TESTS
# ============================================================================


@pytest.fixture
def sample_entry():
    """Fixture que retorna un LogEntry de ejemplo."""
    return LogEntry(
        ip="192.168.1.1",
        timestamp=datetime(2024, 11, 26, 12, 0, 0),
        method="GET",
        path="/index.html",
        status_code=200,
        response_size=1024,
    )


@pytest.fixture
def error_entry():
    """Fixture que retorna un LogEntry con error."""
    return LogEntry(
        ip="192.168.1.2",
        timestamp=datetime(2024, 11, 26, 12, 1, 0),
        method="GET",
        path="/notfound",
        status_code=404,
        response_size=162,
    )


# ============================================================================
# TESTS USANDO FIXTURES
# ============================================================================


class TestWithFixtures:
    """Tests que usan fixtures para código más limpio."""

    def test_sample_entry_is_success(self, sample_entry):
        """Test 44: Sample entry es exitoso."""
        assert sample_entry.is_success is True
        assert sample_entry.is_error is False

    def test_error_entry_is_client_error(self, error_entry):
        """Test 45: Error entry es error de cliente."""
        assert error_entry.is_client_error is True
        assert error_entry.is_server_error is False

    def test_entries_are_different(self, sample_entry, error_entry):
        """Test 46: Diferentes entries tienen diferentes atributos."""
        assert sample_entry.ip != error_entry.ip
        assert sample_entry.status_code != error_entry.status_code
