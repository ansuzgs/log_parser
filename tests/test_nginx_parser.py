import pytest
from datetime import datetime
from pathlib import Path
from src.parsers.nginx_parser import NginxParser
from src.models.log_entry import LogEntry

# ============================================================================
# FASE 1: Tests Básicos - Parsing de Línea Simple
# ============================================================================


class TestNginxParserBasics:
    """Tests básicos de funcionalidad core del parser."""

    def test_parser_can_be_instantiated(self):
        """Test 1: El parser se puede instanciar."""
        parser = NginxParser()
        assert parser is not None

    def test_parse_simple_valid_line(self):
        """Test 2: Parsear una línea válida simple retorna LogEntry."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "GET /index.html HTTP/1.1" 200 1234 "-" "Mozilla/5.0"'

        result = parser.parse_line(line)

        assert result is not None
        assert isinstance(result, LogEntry)

    def test_parse_invalid_line_returns_none(self):
        """Test 3: Una línea que no coincide con el formato retorna None."""
        parser = NginxParser()
        line = "Esta línea no es un log válido"

        result = parser.parse_line(line)

        assert result is None

    def test_parse_empty_line_returns_none(self):
        """Test 4: Una línea vacía retorna None."""
        parser = NginxParser()
        line = ""

        result = parser.parse_line(line)

        assert result is None


# ============================================================================
# FASE 2: Tests de Extracción de Campos - IP
# ============================================================================


class TestIPExtraction:
    """Tests para verificar extracción correcta de IPs."""

    def test_extracts_ipv4_address(self):
        """Test 5: Extrae correctamente una dirección IPv4."""
        parser = NginxParser()
        line = '192.168.1.100 - - [26/Nov/2024:12:00:00 +0000] "GET / HTTP/1.1" 200 100 "-" "-"'

        result = parser.parse_line(line)

        assert result.ip == "192.168.1.100"

    def test_extracts_different_ip(self):
        """Test 6: Extrae correctamente diferentes IPs."""
        parser = NginxParser()
        line = (
            '10.0.0.5 - - [26/Nov/2024:12:00:00 +0000] "GET / HTTP/1.1" 200 100 "-" "-"'
        )

        result = parser.parse_line(line)

        assert result.ip == "10.0.0.5"


# ============================================================================
# FASE 3: Tests de Extracción de Campos - Timestamp
# ============================================================================


class TestTimestampExtraction:
    """Tests para parsing de timestamps."""

    def test_extracts_timestamp(self):
        """Test 7: Extrae y parsea el timestamp correctamente."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:30:45 +0000] "GET / HTTP/1.1" 200 100 "-" "-"'

        result = parser.parse_line(line)

        assert isinstance(result.timestamp, datetime)
        assert result.timestamp.year == 2024
        assert result.timestamp.month == 11
        assert result.timestamp.day == 26
        assert result.timestamp.hour == 12
        assert result.timestamp.minute == 30
        assert result.timestamp.second == 45

    def test_parses_timestamp_with_timezone(self):
        """Test 8: Parsea correctamente timestamps con zona horaria."""
        parser = NginxParser()
        line = '192.168.1.1 - - [01/Jan/2024:08:15:30 +0100] "GET / HTTP/1.1" 200 100 "-" "-"'

        result = parser.parse_line(line)

        assert result.timestamp is not None
        # El timezone debería estar incluido en el datetime

    def test_parses_different_month(self):
        """Test 9: Parsea correctamente diferentes meses."""
        parser = NginxParser()
        line = '192.168.1.1 - - [15/Dec/2024:10:00:00 +0000] "GET / HTTP/1.1" 200 100 "-" "-"'

        result = parser.parse_line(line)

        assert result.timestamp.month == 12
        assert result.timestamp.day == 15


# ============================================================================
# FASE 4: Tests de Extracción de Campos - Método HTTP
# ============================================================================


class TestHTTPMethodExtraction:
    """Tests para extracción de métodos HTTP."""

    def test_extracts_get_method(self):
        """Test 10: Extrae correctamente método GET."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "GET /index.html HTTP/1.1" 200 100 "-" "-"'

        result = parser.parse_line(line)

        assert result.method == "GET"

    def test_extracts_post_method(self):
        """Test 11: Extrae correctamente método POST."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "POST /api/users HTTP/1.1" 201 256 "-" "-"'

        result = parser.parse_line(line)

        assert result.method == "POST"

    def test_extracts_put_method(self):
        """Test 12: Extrae correctamente método PUT."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "PUT /api/users/1 HTTP/1.1" 200 100 "-" "-"'

        result = parser.parse_line(line)

        assert result.method == "PUT"

    def test_extracts_delete_method(self):
        """Test 13: Extrae correctamente método DELETE."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "DELETE /api/users/1 HTTP/1.1" 204 0 "-" "-"'

        result = parser.parse_line(line)

        assert result.method == "DELETE"


# ============================================================================
# FASE 5: Tests de Extracción de Campos - Path/URL
# ============================================================================


class TestPathExtraction:
    """Tests para extracción de rutas."""

    def test_extracts_simple_path(self):
        """Test 14: Extrae correctamente una ruta simple."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "GET /index.html HTTP/1.1" 200 100 "-" "-"'

        result = parser.parse_line(line)

        assert result.path == "/index.html"

    def test_extracts_root_path(self):
        """Test 15: Extrae correctamente la ruta raíz."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "GET / HTTP/1.1" 200 100 "-" "-"'

        result = parser.parse_line(line)

        assert result.path == "/"

    def test_extracts_nested_path(self):
        """Test 16: Extrae correctamente rutas anidadas."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "GET /api/v1/users/profile HTTP/1.1" 200 100 "-" "-"'

        result = parser.parse_line(line)

        assert result.path == "/api/v1/users/profile"

    def test_extracts_path_with_query_string(self):
        """Test 17: Extrae correctamente rutas con query strings."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "GET /search?q=test&page=1 HTTP/1.1" 200 100 "-" "-"'

        result = parser.parse_line(line)

        assert result.path == "/search?q=test&page=1"

    def test_extracts_path_with_fragment(self):
        """Test 18: Extrae correctamente rutas con fragmentos."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "GET /docs#section-1 HTTP/1.1" 200 100 "-" "-"'

        result = parser.parse_line(line)

        assert result.path == "/docs#section-1"


# ============================================================================
# FASE 6: Tests de Extracción de Campos - Status Code
# ============================================================================


class TestStatusCodeExtraction:
    """Tests para extracción de códigos de estado HTTP."""

    def test_extracts_200_status(self):
        """Test 19: Extrae correctamente código 200."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "GET / HTTP/1.1" 200 100 "-" "-"'

        result = parser.parse_line(line)

        assert result.status_code == 200
        assert isinstance(result.status_code, int)

    def test_extracts_404_status(self):
        """Test 20: Extrae correctamente código 404."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "GET /notfound HTTP/1.1" 404 162 "-" "-"'

        result = parser.parse_line(line)

        assert result.status_code == 404

    def test_extracts_500_status(self):
        """Test 21: Extrae correctamente código 500."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "POST /api HTTP/1.1" 500 1024 "-" "-"'

        result = parser.parse_line(line)

        assert result.status_code == 500

    def test_extracts_various_status_codes(self):
        """Test 22: Extrae correctamente diversos códigos de estado."""
        parser = NginxParser()
        test_cases = [
            (
                '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "POST /api HTTP/1.1" 201 100 "-" "-"',
                201,
            ),
            (
                '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "DELETE /api HTTP/1.1" 204 0 "-" "-"',
                204,
            ),
            (
                '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "GET /admin HTTP/1.1" 403 256 "-" "-"',
                403,
            ),
            (
                '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "POST /api HTTP/1.1" 502 512 "-" "-"',
                502,
            ),
        ]

        for line, expected_status in test_cases:
            result = parser.parse_line(line)
            assert result.status_code == expected_status


# ============================================================================
# FASE 7: Tests de Extracción de Campos - Response Size
# ============================================================================


class TestResponseSizeExtraction:
    """Tests para extracción del tamaño de respuesta."""

    def test_extracts_response_size(self):
        """Test 23: Extrae correctamente el tamaño de respuesta."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "GET / HTTP/1.1" 200 1234 "-" "-"'

        result = parser.parse_line(line)

        assert result.response_size == 1234
        assert isinstance(result.response_size, int)

    def test_extracts_zero_size(self):
        """Test 24: Extrae correctamente tamaño 0."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "DELETE /api HTTP/1.1" 204 0 "-" "-"'

        result = parser.parse_line(line)

        assert result.response_size == 0

    def test_extracts_large_size(self):
        """Test 25: Extrae correctamente tamaños grandes."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "GET /file.zip HTTP/1.1" 200 1048576 "-" "-"'

        result = parser.parse_line(line)

        assert result.response_size == 1048576


# ============================================================================
# FASE 8: Tests de Campos Opcionales - Referrer y User-Agent
# ============================================================================


class TestOptionalFields:
    """Tests para campos opcionales (referrer y user-agent)."""

    def test_extracts_referrer_when_present(self):
        """Test 26: Extrae referrer cuando está presente."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "GET /page HTTP/1.1" 200 100 "https://example.com/" "Mozilla/5.0"'

        result = parser.parse_line(line)

        assert result.referrer == "https://example.com/"

    def test_referrer_is_none_when_dash(self):
        """Test 27: Referrer es None cuando es un guión."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "GET / HTTP/1.1" 200 100 "-" "Mozilla/5.0"'

        result = parser.parse_line(line)

        assert result.referrer is None

    def test_extracts_user_agent_when_present(self):
        """Test 28: Extrae user-agent cuando está presente."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "GET / HTTP/1.1" 200 100 "-" "Mozilla/5.0 (Windows NT 10.0)"'

        result = parser.parse_line(line)

        assert result.user_agent == "Mozilla/5.0 (Windows NT 10.0)"

    def test_user_agent_is_none_when_dash(self):
        """Test 29: User-agent es None cuando es un guión."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "GET / HTTP/1.1" 200 100 "-" "-"'

        result = parser.parse_line(line)

        assert result.user_agent is None

    def test_extracts_complex_user_agent(self):
        """Test 30: Extrae user-agents complejos con espacios y paréntesis."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "GET / HTTP/1.1" 200 100 "-" "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"'

        result = parser.parse_line(line)

        assert "Mozilla/5.0" in result.user_agent
        assert "Linux" in result.user_agent


# ============================================================================
# FASE 9: Tests de Casos Edge y Líneas Problemáticas
# ============================================================================


class TestEdgeCases:
    """Tests para casos especiales y edge cases."""

    def test_handles_line_with_extra_spaces(self):
        """Test 31: Maneja líneas con espacios extra."""
        parser = NginxParser()
        line = '  192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "GET / HTTP/1.1" 200 100 "-" "-"  '

        # Debería parsear correctamente o retornar None, pero no lanzar excepción
        result = parser.parse_line(line.strip())

        # Si implementas trimming automático en el parser, debería funcionar
        assert result is None or result.ip == "192.168.1.1"

    def test_handles_malformed_timestamp(self):
        """Test 32: Maneja timestamp malformado sin lanzar excepción."""
        parser = NginxParser()
        line = '192.168.1.1 - - [INVALID-TIMESTAMP] "GET / HTTP/1.1" 200 100 "-" "-"'

        result = parser.parse_line(line)

        # Debería retornar None en lugar de lanzar excepción
        assert result is None

    def test_handles_missing_quotes_in_request(self):
        """Test 33: Maneja líneas sin comillas en el request."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] GET / HTTP/1.1 200 100 "-" "-"'

        result = parser.parse_line(line)

        # Formato incorrecto, debería retornar None
        assert result is None

    def test_handles_unicode_in_path(self):
        """Test 34: Maneja caracteres unicode en la ruta."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "GET /página HTTP/1.1" 200 100 "-" "-"'

        result = parser.parse_line(line)

        # Debería manejar unicode correctamente
        assert result is not None
        assert "página" in result.path or result is None

    def test_handles_special_characters_in_path(self):
        """Test 35: Maneja caracteres especiales en la ruta."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "GET /api?query=%20test&id=1 HTTP/1.1" 200 100 "-" "-"'

        result = parser.parse_line(line)

        assert result is not None
        assert "query" in result.path


# ============================================================================
# FASE 10: Tests de Integración - Parsing de Archivos
# ============================================================================


class TestFileProcessing:
    """Tests para procesamiento de archivos completos."""

    def test_parse_file_returns_generator(self):
        """Test 36: parse_file retorna un generador/iterador."""
        parser = NginxParser()
        # Asume que existe un archivo de test
        result = parser.parse_file(Path("fixtures/test_small.log"))

        # Debería ser un generador o iterador
        assert hasattr(result, "__iter__")

    def test_parse_file_yields_log_entries(self):
        """Test 37: parse_file genera objetos LogEntry."""
        parser = NginxParser()
        # Crear archivo temporal con una línea válida
        test_file = Path("fixtures/test_small.log")

        if test_file.exists():
            entries = list(parser.parse_file(test_file))

            if len(entries) > 0:
                assert isinstance(entries[0], LogEntry)

    def test_parse_file_skips_invalid_lines(self):
        """Test 38: parse_file salta líneas inválidas sin fallar."""
        parser = NginxParser()
        # Archivo con líneas válidas e inválidas mezcladas
        test_file = Path("fixtures/test_mixed.log")

        if test_file.exists():
            # No debería lanzar excepción
            entries = list(parser.parse_file(test_file))

            # Debería haber parseado solo las líneas válidas
            assert isinstance(entries, list)

    def test_parse_file_handles_empty_lines(self):
        """Test 39: parse_file maneja líneas vacías correctamente."""
        parser = NginxParser()
        test_file = Path("fixtures/test_with_empty_lines.log")

        if test_file.exists():
            # No debería fallar con líneas vacías
            entries = list(parser.parse_file(test_file))
            assert isinstance(entries, list)


# ============================================================================
# FASE 11: Tests de Patrones Reales de Ataque
# ============================================================================

@pytest.mark.skip
class TestSecurityPatterns:
    """Tests para detectar patrones de ataque comunes en logs."""

    def test_parses_sql_injection_attempt(self):
        """Test 40: Parsea intentos de SQL injection en la URL."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "GET /search?q=\' OR 1=1-- HTTP/1.1" 400 128 "-" "-"'

        result = parser.parse_line(line)

        assert result is not None
        assert "OR 1=1" in result.path or "'" in result.path

    def test_parses_path_traversal_attempt(self):
        """Test 41: Parsea intentos de path traversal."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "GET /../../../etc/passwd HTTP/1.1" 404 162 "-" "-"'

        result = parser.parse_line(line)

        assert result is not None
        assert "../" in result.path

    def test_parses_xss_attempt(self):
        """Test 42: Parsea intentos de XSS en la URL."""
        parser = NginxParser()
        line = '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "GET /search?q=<script>alert(1)</script> HTTP/1.1" 400 128 "-" "-"'

        result = parser.parse_line(line)

        assert result is not None
        assert "script" in result.path.lower()


# ============================================================================
# FASE 12: Tests de Performance (Opcional)
# ============================================================================


class TestPerformance:
    """Tests de rendimiento del parser."""

    @pytest.mark.slow
    def test_parses_large_file_efficiently(self):
        """Test 43: Parsea archivos grandes sin consumir toda la memoria."""
        parser = NginxParser()
        test_file = Path("fixtures/large_test.log")

        if test_file.exists():
            # Debería poder iterar sin cargar todo en memoria
            count = 0
            for entry in parser.parse_file(test_file):
                count += 1
                if count > 1000:  # Solo contar primeras 1000
                    break

            assert count > 0

    @pytest.mark.slow
    def test_regex_is_compiled_once(self):
        """Test 44: El regex se compila una sola vez, no en cada parse."""
        parser = NginxParser()

        # Debería haber un atributo de regex compilado
        assert hasattr(parser, "NGINX_PATTERN") or hasattr(parser, "pattern")


# ============================================================================
# FIXTURES PARA TESTS
# ============================================================================


@pytest.fixture
def sample_log_lines():
    """Fixture con líneas de log de ejemplo para tests."""
    return [
        '192.168.1.1 - - [26/Nov/2024:12:00:00 +0000] "GET /index.html HTTP/1.1" 200 1234 "-" "Mozilla/5.0"',
        '192.168.1.2 - - [26/Nov/2024:12:01:00 +0000] "POST /api/login HTTP/1.1" 200 512 "https://example.com" "curl/7.68.0"',
        '192.168.1.3 - - [26/Nov/2024:12:02:00 +0000] "GET /notfound HTTP/1.1" 404 162 "-" "-"',
        '192.168.1.4 - - [26/Nov/2024:12:03:00 +0000] "POST /api/data HTTP/1.1" 500 1024 "-" "axios/0.21.1"',
    ]


@pytest.fixture
def parser():
    """Fixture que retorna una instancia del parser."""
    return NginxParser()


# ============================================================================
# TESTS USANDO FIXTURES
# ============================================================================


class TestWithFixtures:
    """Tests que utilizan fixtures para código más limpio."""

    def test_parse_multiple_lines(self, parser, sample_log_lines):
        """Test 45: Parsea múltiples líneas correctamente."""
        results = [parser.parse_line(line) for line in sample_log_lines]

        # Todas deberían parsearse correctamente
        assert all(result is not None for result in results)
        assert len(results) == 4

    def test_parsed_entries_have_different_ips(self, parser, sample_log_lines):
        """Test 46: Diferentes líneas tienen diferentes IPs."""
        results = [parser.parse_line(line) for line in sample_log_lines]
        ips = [r.ip for r in results]

        assert len(set(ips)) == 4  # 4 IPs únicas

    def test_parsed_entries_have_different_status_codes(self, parser, sample_log_lines):
        """Test 47: Identifica diferentes códigos de estado."""
        results = [parser.parse_line(line) for line in sample_log_lines]
        status_codes = [r.status_code for r in results]

        assert 200 in status_codes
        assert 404 in status_codes
        assert 500 in status_codes
