import pytest
from datetime import datetime
from collections import Counter
from src.analyzers.log_analyzer import LogAnalyzer
from src.models.log_entry import LogEntry


# ============================================================================
# FIXTURES - Datos de Prueba
# ============================================================================


@pytest.fixture
def sample_entries():
    """Fixture con 10 LogEntry de ejemplo para testing."""
    return [
        LogEntry(
            ip="192.168.1.1",
            timestamp=datetime(2024, 11, 26, 8, 0, 0),
            method="GET",
            path="/index.html",
            status_code=200,
            response_size=1024,
        ),
        LogEntry(
            ip="192.168.1.1",
            timestamp=datetime(2024, 11, 26, 8, 5, 0),
            method="GET",
            path="/about.html",
            status_code=200,
            response_size=2048,
        ),
        LogEntry(
            ip="192.168.1.2",
            timestamp=datetime(2024, 11, 26, 8, 10, 0),
            method="POST",
            path="/api/login",
            status_code=200,
            response_size=512,
        ),
        LogEntry(
            ip="192.168.1.3",
            timestamp=datetime(2024, 11, 26, 8, 15, 0),
            method="GET",
            path="/notfound",
            status_code=404,
            response_size=162,
        ),
        LogEntry(
            ip="192.168.1.1",
            timestamp=datetime(2024, 11, 26, 8, 20, 0),
            method="GET",
            path="/contact.html",
            status_code=200,
            response_size=3072,
        ),
        LogEntry(
            ip="192.168.1.4",
            timestamp=datetime(2024, 11, 26, 9, 0, 0),
            method="POST",
            path="/api/data",
            status_code=500,
            response_size=1024,
        ),
        LogEntry(
            ip="192.168.1.2",
            timestamp=datetime(2024, 11, 26, 9, 5, 0),
            method="GET",
            path="/index.html",
            status_code=200,
            response_size=1024,
        ),
        LogEntry(
            ip="192.168.1.5",
            timestamp=datetime(2024, 11, 26, 9, 10, 0),
            method="GET",
            path="/products",
            status_code=200,
            response_size=4096,
        ),
        LogEntry(
            ip="192.168.1.1",
            timestamp=datetime(2024, 11, 26, 9, 15, 0),
            method="GET",
            path="/index.html",
            status_code=200,
            response_size=1024,
        ),
        LogEntry(
            ip="192.168.1.6",
            timestamp=datetime(2024, 11, 26, 9, 20, 0),
            method="GET",
            path="/admin",
            status_code=403,
            response_size=256,
        ),
    ]


@pytest.fixture
def empty_analyzer():
    """Fixture con analyzer vacío."""
    return LogAnalyzer([])


@pytest.fixture
def analyzer(sample_entries):
    """Fixture con analyzer poblado con datos de ejemplo."""
    return LogAnalyzer(sample_entries)


# ============================================================================
# FASE 1: Tests Básicos - Inicialización
# ============================================================================


class TestLogAnalyzerCreation:
    """Tests para creación e inicialización del analyzer."""

    def test_analyzer_can_be_created(self):
        """Test 1: LogAnalyzer se puede crear."""
        analyzer = LogAnalyzer([])
        assert analyzer is not None

    def test_analyzer_accepts_list_of_entries(self, sample_entries):
        """Test 2: LogAnalyzer acepta lista de LogEntry."""
        analyzer = LogAnalyzer(sample_entries)
        assert analyzer is not None

    def test_analyzer_stores_entries(self, sample_entries):
        """Test 3: LogAnalyzer almacena las entradas."""
        analyzer = LogAnalyzer(sample_entries)
        # Debería tener acceso a las entradas de alguna forma
        assert len(sample_entries) == 10

    def test_analyzer_with_empty_list(self):
        """Test 4: LogAnalyzer funciona con lista vacía."""
        analyzer = LogAnalyzer([])
        assert analyzer is not None


# ============================================================================
# FASE 2: Tests de Conteo Total
# ============================================================================


class TestTotalCounts:
    """Tests para conteos totales básicos."""

    def test_total_requests_with_data(self, analyzer):
        """Test 5: Retorna total de requests correctamente."""
        total = analyzer.total_requests()
        assert total == 10

    def test_total_requests_empty(self, empty_analyzer):
        """Test 6: Total de requests con analyzer vacío es 0."""
        total = empty_analyzer.total_requests()
        assert total == 0

    def test_total_errors(self, analyzer):
        """Test 7: Cuenta total de errores (4xx + 5xx)."""
        total = analyzer.total_errors()
        # En sample_entries: 1 x 404, 1 x 403, 1 x 500 = 3 errores
        assert total == 3

    def test_total_success(self, analyzer):
        """Test 8: Cuenta total de respuestas exitosas (2xx)."""
        total = analyzer.total_success()
        # En sample_entries: 7 respuestas 200
        assert total == 7


# ============================================================================
# FASE 3: Tests de Códigos de Estado
# ============================================================================


class TestStatusCodes:
    """Tests para análisis de códigos de estado."""

    def test_get_status_counts(self, analyzer):
        """Test 9: Retorna diccionario con conteo de códigos de estado."""
        counts = analyzer.get_status_counts()

        assert isinstance(counts, dict)
        assert 200 in counts
        assert counts[200] == 7  # 7 respuestas 200
        assert counts[404] == 1  # 1 respuesta 404
        assert counts[403] == 1  # 1 respuesta 403
        assert counts[500] == 1  # 1 respuesta 500

    def test_get_status_counts_empty(self, empty_analyzer):
        """Test 10: Status counts con analyzer vacío retorna dict vacío."""
        counts = empty_analyzer.get_status_counts()
        assert isinstance(counts, dict)
        assert len(counts) == 0

    def test_most_common_status(self, analyzer):
        """Test 11: Retorna el código de estado más común."""
        status = analyzer.most_common_status()
        assert status == 200  # 200 aparece 7 veces


# ============================================================================
# FASE 4: Tests de Top IPs
# ============================================================================


class TestTopIPs:
    """Tests para análisis de IPs más activas."""

    def test_top_ips_default(self, analyzer):
        """Test 12: Retorna top IPs (default top 10)."""
        top_ips = analyzer.top_ips()

        assert isinstance(top_ips, list)
        # Debería retornar lista de tuplas (ip, count)
        assert len(top_ips) > 0
        assert isinstance(top_ips[0], tuple)
        assert len(top_ips[0]) == 2

    def test_top_ips_most_active_first(self, analyzer):
        """Test 13: Las IPs están ordenadas por actividad (más activas primero)."""
        top_ips = analyzer.top_ips()

        # 192.168.1.1 aparece 4 veces (más activa)
        assert top_ips[0][0] == "192.168.1.1"
        assert top_ips[0][1] == 4

        # 192.168.1.2 aparece 2 veces (segunda más activa)
        assert top_ips[1][0] == "192.168.1.2"
        assert top_ips[1][1] == 2

    def test_top_ips_with_limit(self, analyzer):
        """Test 14: Respeta el límite N especificado."""
        top_ips = analyzer.top_ips(n=3)
        assert len(top_ips) == 3

    def test_top_ips_limit_greater_than_total(self, analyzer):
        """Test 15: Si N > total de IPs únicas, retorna todas."""
        top_ips = analyzer.top_ips(n=100)
        # Hay 6 IPs únicas en sample_entries
        assert len(top_ips) == 6

    def test_top_ips_empty(self, empty_analyzer):
        """Test 16: Top IPs con analyzer vacío retorna lista vacía."""
        top_ips = empty_analyzer.top_ips()
        assert top_ips == []


# ============================================================================
# FASE 5: Tests de Top Paths
# ============================================================================


class TestTopPaths:
    """Tests para rutas más visitadas."""

    def test_top_paths_default(self, analyzer):
        """Test 17: Retorna top paths (default top 10)."""
        top_paths = analyzer.top_paths()

        assert isinstance(top_paths, list)
        assert len(top_paths) > 0
        assert isinstance(top_paths[0], tuple)
        assert len(top_paths[0]) == 2

    def test_top_paths_most_visited_first(self, analyzer):
        """Test 18: Las rutas están ordenadas por visitas."""
        top_paths = analyzer.top_paths()

        # /index.html aparece 3 veces (más visitada)
        assert top_paths[0][0] == "/index.html"
        assert top_paths[0][1] == 3

    def test_top_paths_with_limit(self, analyzer):
        """Test 19: Respeta el límite N especificado."""
        top_paths = analyzer.top_paths(n=5)
        assert len(top_paths) == 5

    def test_top_paths_empty(self, empty_analyzer):
        """Test 20: Top paths con analyzer vacío retorna lista vacía."""
        top_paths = empty_analyzer.top_paths()
        assert top_paths == []


# ============================================================================
# FASE 6: Tests de Métodos HTTP
# ============================================================================


class TestHTTPMethods:
    """Tests para análisis de métodos HTTP."""

    def test_get_method_counts(self, analyzer):
        """Test 21: Retorna conteo de métodos HTTP."""
        methods = analyzer.get_method_counts()

        assert isinstance(methods, dict)
        assert "GET" in methods
        assert "POST" in methods
        # En sample_entries: 8 GET, 2 POST
        assert methods["GET"] == 8
        assert methods["POST"] == 2

    def test_most_common_method(self, analyzer):
        """Test 22: Retorna el método HTTP más común."""
        method = analyzer.most_common_method()
        assert method == "GET"


# ============================================================================
# FASE 7: Tests de Errores
# ============================================================================


class TestErrorAnalysis:
    """Tests para análisis de errores."""

    def test_error_rate(self, analyzer):
        """Test 23: Calcula el ratio de errores correctamente."""
        rate = analyzer.error_rate()

        # 3 errores de 10 requests = 0.3 (30%)
        assert isinstance(rate, float)
        assert rate == 0.3

    def test_error_rate_no_errors(self):
        """Test 24: Error rate con solo respuestas exitosas es 0.0."""
        entries = [
            LogEntry("192.168.1.1", datetime.now(), "GET", "/", 200, 100),
            LogEntry("192.168.1.2", datetime.now(), "GET", "/", 200, 100),
        ]
        analyzer = LogAnalyzer(entries)

        rate = analyzer.error_rate()
        assert rate == 0.0

    def test_error_rate_empty(self, empty_analyzer):
        """Test 25: Error rate con analyzer vacío es 0.0."""
        rate = empty_analyzer.error_rate()
        assert rate == 0.0

    def test_get_errors_only(self, analyzer):
        """Test 26: Retorna solo las entradas con errores."""
        errors = analyzer.get_errors()

        assert isinstance(errors, list)
        assert len(errors) == 3
        # Todos deben ser errores (4xx o 5xx)
        assert all(entry.is_error for entry in errors)

    def test_client_error_count(self, analyzer):
        """Test 27: Cuenta errores de cliente (4xx)."""
        count = analyzer.client_error_count()
        # 404 y 403 = 2 errores de cliente
        assert count == 2

    def test_server_error_count(self, analyzer):
        """Test 28: Cuenta errores de servidor (5xx)."""
        count = analyzer.server_error_count()
        # 1 error 500
        assert count == 1


# ============================================================================
# FASE 8: Tests de Análisis Temporal
# ============================================================================


class TestTemporalAnalysis:
    """Tests para análisis temporal de requests."""

    def test_requests_by_hour(self, analyzer):
        """Test 29: Agrupa requests por hora."""
        by_hour = analyzer.requests_by_hour()

        assert isinstance(by_hour, dict)
        # sample_entries tiene requests en hora 8 y hora 9
        assert 8 in by_hour
        assert 9 in by_hour
        assert by_hour[8] == 5  # 5 requests en hora 8
        assert by_hour[9] == 5  # 5 requests en hora 9

    def test_busiest_hour(self, analyzer):
        """Test 30: Identifica la hora con más tráfico."""
        hour = analyzer.busiest_hour()
        # Ambas horas tienen 5 requests, debería retornar una de ellas
        assert hour in [8, 9]

    def test_requests_by_date(self, analyzer):
        """Test 31: Agrupa requests por fecha."""
        by_date = analyzer.requests_by_date()

        assert isinstance(by_date, dict)
        # Todos los sample_entries son del 2024-11-26
        from datetime import date

        test_date = date(2024, 11, 26)
        assert test_date in by_date
        assert by_date[test_date] == 10


# ============================================================================
# FASE 9: Tests de Tamaños de Respuesta
# ============================================================================


class TestResponseSizes:
    """Tests para análisis de tamaños de respuesta."""

    def test_total_bytes_transferred(self, analyzer):
        """Test 32: Calcula total de bytes transferidos."""
        total = analyzer.total_bytes_transferred()

        # Sumar todos los response_size de sample_entries
        expected = 1024 + 2048 + 512 + 162 + 3072 + 1024 + 1024 + 4096 + 1024 + 256
        assert total == expected

    def test_average_response_size(self, analyzer):
        """Test 33: Calcula tamaño promedio de respuesta."""
        avg = analyzer.average_response_size()

        total = 1024 + 2048 + 512 + 162 + 3072 + 1024 + 1024 + 4096 + 1024 + 256
        expected = total / 10
        assert avg == expected

    def test_largest_response(self, analyzer):
        """Test 34: Encuentra la respuesta más grande."""
        largest = analyzer.largest_response()

        # La respuesta más grande es 4096
        assert largest.response_size == 4096
        assert largest.path == "/products"


# ============================================================================
# FASE 10: Tests de IPs Únicas
# ============================================================================


class TestUniqueIPs:
    """Tests para análisis de IPs únicas."""

    def test_unique_ips_count(self, analyzer):
        """Test 35: Cuenta IPs únicas correctamente."""
        count = analyzer.unique_ips_count()
        # En sample_entries hay 6 IPs diferentes
        assert count == 6

    def test_get_unique_ips(self, analyzer):
        """Test 36: Retorna set de IPs únicas."""
        ips = analyzer.get_unique_ips()

        assert isinstance(ips, set)
        assert len(ips) == 6
        assert "192.168.1.1" in ips
        assert "192.168.1.2" in ips


# ============================================================================
# FASE 11: Tests de Filtrado
# ============================================================================


class TestFiltering:
    """Tests para filtrado de entradas."""

    def test_filter_by_status_code(self, analyzer):
        """Test 37: Filtra entradas por código de estado."""
        filtered = analyzer.filter_by_status(200)

        assert len(filtered) == 7
        assert all(entry.status_code == 200 for entry in filtered)

    def test_filter_by_ip(self, analyzer):
        """Test 38: Filtra entradas por IP."""
        filtered = analyzer.filter_by_ip("192.168.1.1")

        assert len(filtered) == 4
        assert all(entry.ip == "192.168.1.1" for entry in filtered)

    def test_filter_by_method(self, analyzer):
        """Test 39: Filtra entradas por método HTTP."""
        filtered = analyzer.filter_by_method("POST")

        assert len(filtered) == 2
        assert all(entry.method == "POST" for entry in filtered)

    def test_filter_by_path(self, analyzer):
        """Test 40: Filtra entradas por ruta."""
        filtered = analyzer.filter_by_path("/index.html")

        assert len(filtered) == 3
        assert all(entry.path == "/index.html" for entry in filtered)
