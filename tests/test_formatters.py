import pytest
import json
import csv
from io import StringIO
from datetime import datetime
# from src.formatters.table_formatter import TableFormatter
from src.formatters.json_formatter import JSONFormatter
from src.formatters.csv_formatter import CSVFormatter
from src.formatters.markdown_formatter import MarkdownFormatter
from src.models.log_entry import LogEntry
from src.analyzers.log_analyzer import LogAnalyzer


# ============================================================================
# FIXTURES - Datos de Prueba
# ============================================================================

@pytest.fixture
def sample_analyzer():
    """Fixture con analyzer poblado para testing."""
    entries = [
        LogEntry("192.168.1.1", datetime(2024, 11, 26, 8, 0, 0), "GET", "/index.html", 200, 1024),
        LogEntry("192.168.1.1", datetime(2024, 11, 26, 8, 5, 0), "GET", "/about.html", 200, 2048),
        LogEntry("192.168.1.2", datetime(2024, 11, 26, 8, 10, 0), "POST", "/api/login", 200, 512),
        LogEntry("192.168.1.3", datetime(2024, 11, 26, 8, 15, 0), "GET", "/notfound", 404, 162),
        LogEntry("192.168.1.4", datetime(2024, 11, 26, 9, 0, 0), "POST", "/api/data", 500, 1024),
    ]
    return LogAnalyzer(entries)


@pytest.fixture
def empty_analyzer():
    """Fixture con analyzer vacío."""
    return LogAnalyzer([])


# ============================================================================
# FASE 1: Tests de JSONFormatter
# ============================================================================

class TestJSONFormatter:
    """Tests para el formatter JSON."""
    
    def test_json_formatter_can_be_created(self):
        """Test 1: JSONFormatter se puede crear."""
        formatter = JSONFormatter()
        assert formatter is not None
    
    def test_format_summary_returns_json_string(self, sample_analyzer):
        """Test 2: format_summary retorna un string JSON válido."""
        formatter = JSONFormatter()
        summary = sample_analyzer.get_summary()
        
        result = formatter.format_summary(summary)
        
        assert isinstance(result, str)
        # Verificar que es JSON válido
        parsed = json.loads(result)
        assert isinstance(parsed, dict)
    
    def test_format_summary_contains_all_keys(self, sample_analyzer):
        """Test 3: El JSON contiene todas las claves del summary."""
        formatter = JSONFormatter()
        summary = sample_analyzer.get_summary()
        
        result = formatter.format_summary(summary)
        parsed = json.loads(result)
        
        assert "total_requests" in parsed
        assert "total_errors" in parsed
        assert "error_rate" in parsed
        assert parsed["total_requests"] == 5
        assert parsed["total_errors"] == 2
    
    def test_format_summary_with_indent(self, sample_analyzer):
        """Test 4: format_summary acepta parámetro indent para pretty-print."""
        formatter = JSONFormatter()
        summary = sample_analyzer.get_summary()
        
        # Sin indent
        compact = formatter.format_summary(summary, indent=None)
        # Con indent
        pretty = formatter.format_summary(summary, indent=2)
        
        # El pretty debe tener saltos de línea
        assert "\n" in pretty
        # El compact no debería tener muchos
        assert len(pretty) > len(compact)
    
    def test_format_top_ips_returns_json(self, sample_analyzer):
        """Test 5: format_top_ips retorna JSON válido."""
        formatter = JSONFormatter()
        top_ips = sample_analyzer.top_ips(n=5)
        
        result = formatter.format_top_ips(top_ips)
        parsed = json.loads(result)
        
        assert isinstance(parsed, list)
        assert len(parsed) > 0
        # Cada elemento debe tener 'ip' y 'count'
        assert "ip" in parsed[0]
        assert "count" in parsed[0]
    
    def test_format_top_paths_returns_json(self, sample_analyzer):
        """Test 6: format_top_paths retorna JSON válido."""
        formatter = JSONFormatter()
        top_paths = sample_analyzer.top_paths(n=5)
        
        result = formatter.format_top_paths(top_paths)
        parsed = json.loads(result)
        
        assert isinstance(parsed, list)
        assert "path" in parsed[0]
        assert "count" in parsed[0]
    
    def test_format_status_counts_returns_json(self, sample_analyzer):
        """Test 7: format_status_counts retorna JSON válido."""
        formatter = JSONFormatter()
        status_counts = sample_analyzer.get_status_counts()
        
        result = formatter.format_status_counts(status_counts)
        parsed = json.loads(result)
        
        assert isinstance(parsed, dict)
        # Las claves deben ser strings (JSON no soporta int keys directamente)
        assert "200" in parsed or 200 in parsed


# ============================================================================
# FASE 2: Tests de CSVFormatter
# ============================================================================

class TestCSVFormatter:
    """Tests para el formatter CSV."""
    
    def test_csv_formatter_can_be_created(self):
        """Test 8: CSVFormatter se puede crear."""
        formatter = CSVFormatter()
        assert formatter is not None
    
    def test_format_top_ips_returns_csv_string(self, sample_analyzer):
        """Test 9: format_top_ips retorna string CSV válido."""
        formatter = CSVFormatter()
        top_ips = sample_analyzer.top_ips(n=5)
        
        result = formatter.format_top_ips(top_ips)
        
        assert isinstance(result, str)
        # Debe tener header
        assert "IP" in result or "ip" in result
        assert "Count" in result or "count" in result
    
    def test_format_top_ips_has_headers(self, sample_analyzer):
        """Test 10: CSV de top_ips tiene headers correctos."""
        formatter = CSVFormatter()
        top_ips = sample_analyzer.top_ips(n=5)
        
        result = formatter.format_top_ips(top_ips)
        lines = result.strip().split('\n')
        
        # Primera línea debe ser el header
        header = lines[0]
        assert "IP" in header or "ip" in header
        assert "Count" in header or "count" in header or "Requests" in header
    
    def test_format_top_ips_has_data_rows(self, sample_analyzer):
        """Test 11: CSV de top_ips tiene filas de datos."""
        formatter = CSVFormatter()
        top_ips = sample_analyzer.top_ips(n=5)
        
        result = formatter.format_top_ips(top_ips)
        lines = result.strip().split('\n')
        
        # Debe haber header + al menos 1 fila de datos
        assert len(lines) >= 2
        # La segunda línea debe tener una IP
        assert "192.168.1" in lines[1]
    
    def test_format_top_paths_returns_csv(self, sample_analyzer):
        """Test 12: format_top_paths retorna CSV válido."""
        formatter = CSVFormatter()
        top_paths = sample_analyzer.top_paths(n=5)
        
        result = formatter.format_top_paths(top_paths)
        
        assert isinstance(result, str)
        assert "Path" in result or "path" in result
    
    def test_format_status_counts_returns_csv(self, sample_analyzer):
        """Test 13: format_status_counts retorna CSV válido."""
        formatter = CSVFormatter()
        status_counts = sample_analyzer.get_status_counts()
        
        result = formatter.format_status_counts(status_counts)
        
        assert isinstance(result, str)
        assert "Status" in result or "status" in result
        assert "Count" in result or "count" in result
    
    def test_csv_can_be_parsed_back(self, sample_analyzer):
        """Test 14: El CSV generado se puede parsear de vuelta."""
        formatter = CSVFormatter()
        top_ips = sample_analyzer.top_ips(n=5)
        
        result = formatter.format_top_ips(top_ips)
        
        # Intentar parsear con csv.reader
        reader = csv.reader(StringIO(result))
        rows = list(reader)
        
        # Debe tener header + datos
        assert len(rows) >= 2


# ============================================================================
# FASE 3: Tests de MarkdownFormatter
# ============================================================================

class TestMarkdownFormatter:
    """Tests para el formatter Markdown."""
    
    def test_markdown_formatter_can_be_created(self):
        """Test 15: MarkdownFormatter se puede crear."""
        formatter = MarkdownFormatter()
        assert formatter is not None
    
    def test_format_summary_returns_markdown(self, sample_analyzer):
        """Test 16: format_summary retorna Markdown válido."""
        formatter = MarkdownFormatter()
        summary = sample_analyzer.get_summary()
        
        result = formatter.format_summary(summary)
        
        assert isinstance(result, str)
        # Debe tener elementos de markdown
        assert "#" in result  # Headers
    
    def test_format_summary_has_title(self, sample_analyzer):
        """Test 17: El summary en Markdown tiene título."""
        formatter = MarkdownFormatter()
        summary = sample_analyzer.get_summary()
        
        result = formatter.format_summary(summary)
        
        # Debe tener un header de nivel 1 o 2
        assert "# " in result or "## " in result
    
    def test_format_top_ips_returns_markdown_table(self, sample_analyzer):
        """Test 18: format_top_ips retorna tabla Markdown."""
        formatter = MarkdownFormatter()
        top_ips = sample_analyzer.top_ips(n=5)
        
        result = formatter.format_top_ips(top_ips)
        
        assert isinstance(result, str)
        # Tabla markdown tiene pipes |
        assert "|" in result
        # Debe tener separador de header
        assert "---" in result or "|-" in result
    
    def test_format_top_paths_returns_markdown_table(self, sample_analyzer):
        """Test 19: format_top_paths retorna tabla Markdown."""
        formatter = MarkdownFormatter()
        top_paths = sample_analyzer.top_paths(n=5)
        
        result = formatter.format_top_paths(top_paths)
        
        assert "|" in result
        assert "---" in result or "|-" in result
    
    def test_format_full_report_returns_markdown(self, sample_analyzer):
        """Test 20: format_full_report genera reporte completo."""
        formatter = MarkdownFormatter()
        
        result = formatter.format_full_report(sample_analyzer)
        
        assert isinstance(result, str)
        assert "#" in result  # Headers
        assert "|" in result  # Tablas
        # Debe contener secciones
        assert "Summary" in result or "Resumen" in result or "Total" in result



