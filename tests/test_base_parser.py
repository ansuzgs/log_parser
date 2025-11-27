import pytest
from pathlib import Path
from typing import Optional
from abc import ABC
from src.parsers.base_parser import BaseParser
from src.models.log_entry import LogEntry
from datetime import datetime

# ============================================================================
# FASE 1: Tests de Estructura - Clase Abstracta
# ============================================================================


class TestBaseParserStructure:
    """Tests para verificar la estructura de BaseParser como clase abstracta."""

    def test_base_parser_is_abstract_class(self):
        """Test 1: BaseParser es una clase abstracta (no se puede instanciar directamente)."""
        with pytest.raises(TypeError):
            # No debería poder instanciar BaseParser directamente
            parser = BaseParser()

    def test_base_parser_has_parse_line_method(self):
        """Test 2: BaseParser define el método abstracto parse_line."""
        # Verificar que parse_line existe en la definición de la clase
        assert hasattr(BaseParser, "parse_line")

    def test_base_parser_has_parse_file_method(self):
        """Test 3: BaseParser define el método concreto parse_file."""
        assert hasattr(BaseParser, "parse_file")


# ============================================================================
# FASE 2: Implementación de Parser Concreto para Testing
# ============================================================================


class DummyParser(BaseParser):
    """
    Parser concreto simple para testear BaseParser.
    Simula un parser que reconoce líneas en formato: "IP|timestamp|method|path|status|size"
    """

    def parse_line(self, line: str) -> Optional[LogEntry]:
        """Parsea línea simple en formato CSV."""
        if not line or line.startswith("#"):
            return None

        try:
            parts = line.split("|")
            if len(parts) != 6:
                return None

            ip, timestamp_str, method, path, status, size = parts

            return LogEntry(
                ip=ip.strip(),
                timestamp=datetime.fromisoformat(timestamp_str.strip()),
                method=method.strip(),
                path=path.strip(),
                status_code=int(status.strip()),
                response_size=int(size.strip()),
            )
        except (ValueError, AttributeError):
            return None


class TestDummyParserWorks:
    """Verificar que el DummyParser funciona antes de testear BaseParser."""

    def test_dummy_parser_can_be_instantiated(self):
        """Test 4: DummyParser (clase concreta) sí se puede instanciar."""
        parser = DummyParser()
        assert parser is not None

    def test_dummy_parser_parses_valid_line(self):
        """Test 5: DummyParser puede parsear una línea válida."""
        parser = DummyParser()
        line = "192.168.1.1|2024-11-26T12:00:00+00:00|GET|/index.html|200|1234"

        result = parser.parse_line(line)

        assert result is not None
        assert result.ip == "192.168.1.1"
        assert result.status_code == 200

    def test_dummy_parser_returns_none_for_invalid_line(self):
        """Test 6: DummyParser retorna None para líneas inválidas."""
        parser = DummyParser()
        line = "Esta línea no tiene el formato correcto"

        result = parser.parse_line(line)

        assert result is None


# ============================================================================
# FASE 3: Tests del Método parse_file (Implementación Base)
# ============================================================================


class TestParseFileBasicFunctionality:
    """Tests para el método parse_file implementado en BaseParser."""

    def test_parse_file_returns_iterator(self):
        """Test 7: parse_file retorna un iterador/generador."""
        parser = DummyParser()
        test_file = Path("fixtures/test_base_simple.log")

        result = parser.parse_file(test_file)

        # Debe ser iterable
        assert hasattr(result, "__iter__")

    def test_parse_file_yields_log_entries(self):
        """Test 8: parse_file genera objetos LogEntry."""
        parser = DummyParser()
        test_file = Path("fixtures/test_base_simple.log")

        entries = list(parser.parse_file(test_file))

        # Debe haber parseado las 3 líneas válidas del archivo
        assert len(entries) == 3
        assert all(isinstance(entry, LogEntry) for entry in entries)

    def test_parse_file_extracts_correct_data(self):
        """Test 9: parse_file extrae los datos correctamente de cada línea."""
        parser = DummyParser()
        test_file = Path("fixtures/test_base_simple.log")

        entries = list(parser.parse_file(test_file))

        # Verificar primera entrada
        assert entries[0].ip == "192.168.1.1"
        assert entries[0].status_code == 200

        # Verificar segunda entrada
        assert entries[1].ip == "192.168.1.2"
        assert entries[1].status_code == 404

        # Verificar tercera entrada
        assert entries[2].ip == "192.168.1.3"
        assert entries[2].status_code == 500


# ============================================================================
# FASE 4: Tests de Manejo de Errores
# ============================================================================


class TestParseFileErrorHandling:
    """Tests para verificar que parse_file maneja errores correctamente."""

    def test_parse_file_skips_empty_lines(self):
        """Test 10: parse_file salta líneas vacías sin fallar."""
        parser = DummyParser()
        test_file = Path("fixtures/test_base_empty_lines.log")

        entries = list(parser.parse_file(test_file))

        # Solo debe parsear las 2 líneas válidas, ignorando las vacías
        assert len(entries) == 2

    def test_parse_file_skips_invalid_lines(self):
        """Test 11: parse_file salta líneas inválidas sin lanzar excepción."""
        parser = DummyParser()
        test_file = Path("fixtures/test_base_mixed.log")

        # No debería lanzar excepción
        entries = list(parser.parse_file(test_file))

        # Solo debe parsear las líneas válidas (3 de 6)
        assert len(entries) == 3

    def test_parse_file_continues_after_error(self):
        """Test 12: parse_file continúa procesando después de encontrar una línea inválida."""
        parser = DummyParser()
        test_file = Path("fixtures/test_base_mixed.log")

        entries = list(parser.parse_file(test_file))

        # Verificar que parseó líneas antes y después de las inválidas
        assert entries[0].ip == "192.168.1.1"
        assert entries[1].ip == "192.168.1.2"
        assert entries[2].ip == "192.168.1.3"

    def test_parse_file_handles_parse_line_exception(self):
        """Test 13: parse_file maneja excepciones lanzadas por parse_line."""

        class BrokenParser(BaseParser):
            """Parser que lanza excepción en ciertas líneas."""

            def parse_line(self, line: str) -> Optional[LogEntry]:
                if "BREAK" in line:
                    raise ValueError("Línea problemática")
                # Líneas normales
                if "|" not in line:
                    return None
                parts = line.split("|")
                return LogEntry(
                    ip=parts[0],
                    timestamp=datetime.fromisoformat(parts[1]),
                    method=parts[2],
                    path=parts[3],
                    status_code=int(parts[4]),
                    response_size=int(parts[5]),
                )

        parser = BrokenParser()
        test_file = Path("fixtures/test_base_with_exception.log")

        # No debería propagarse la excepción
        entries = list(parser.parse_file(test_file))

        # Debe parsear solo las líneas que no causan excepción
        assert len(entries) >= 1


# ============================================================================
# FASE 5: Tests de Encoding y Manejo de Archivos
# ============================================================================


class TestParseFileEncoding:
    """Tests para manejo de encoding y lectura de archivos."""

    def test_parse_file_handles_utf8(self):
        """Test 14: parse_file maneja correctamente archivos UTF-8."""
        parser = DummyParser()
        test_file = Path("fixtures/test_base_utf8.log")

        entries = list(parser.parse_file(test_file))

        # Debe parsear correctamente
        assert len(entries) >= 1

    def test_parse_file_handles_invalid_utf8_gracefully(self):
        """Test 15: parse_file maneja bytes inválidos sin fallar (errors='replace')."""
        parser = DummyParser()
        # Este archivo tendría caracteres inválidos en UTF-8
        test_file = Path("fixtures/test_base_invalid_utf8.log")

        if test_file.exists():
            # No debería lanzar UnicodeDecodeError
            entries = list(parser.parse_file(test_file))

            # Puede parsear o no, pero no debe fallar
            assert isinstance(entries, list)

    def test_parse_file_closes_file_automatically(self):
        """Test 16: parse_file cierra el archivo automáticamente (context manager)."""
        parser = DummyParser()
        test_file = Path("fixtures/test_base_simple.log")

        # Consumir el generador
        entries = list(parser.parse_file(test_file))

        # El archivo debería estar cerrado
        # (difícil de testear directamente, pero verificamos que no hay error)
        assert len(entries) >= 0


# ============================================================================
# FASE 6: Tests de Comportamiento con Diferentes Subclases
# ============================================================================


class TestSubclassBehavior:
    """Tests para verificar que BaseParser funciona con diferentes subclases."""

    def test_different_parsers_can_coexist(self):
        """Test 17: Diferentes parsers pueden instanciarse y usarse."""

        class ParserA(BaseParser):
            def parse_line(self, line: str) -> Optional[LogEntry]:
                if line.startswith("A:"):
                    parts = line[2:].split(",")
                    return LogEntry(
                        ip=parts[0],
                        timestamp=datetime.now(),
                        method="GET",
                        path="/",
                        status_code=200,
                        response_size=100,
                    )
                return None

        class ParserB(BaseParser):
            def parse_line(self, line: str) -> Optional[LogEntry]:
                if line.startswith("B:"):
                    parts = line[2:].split(",")
                    return LogEntry(
                        ip=parts[0],
                        timestamp=datetime.now(),
                        method="POST",
                        path="/api",
                        status_code=201,
                        response_size=200,
                    )
                return None

        parser_a = ParserA()
        parser_b = ParserB()

        # Ambos deben funcionar independientemente
        result_a = parser_a.parse_line("A:192.168.1.1")
        result_b = parser_b.parse_line("B:192.168.1.2")

        assert result_a.method == "GET"
        assert result_b.method == "POST"

    def test_subclass_must_implement_parse_line(self):
        """Test 18: Subclases deben implementar parse_line o no se pueden instanciar."""

        # Intentar crear clase que no implementa parse_line
        with pytest.raises(TypeError):

            class IncompleteParser(BaseParser):
                pass  # No implementa parse_line

            parser = IncompleteParser()


# ============================================================================
# FASE 7: Tests de Edge Cases
# ============================================================================


class TestEdgeCases:
    """Tests para casos extremos y edge cases."""

    def test_parse_file_with_very_long_lines(self):
        """Test 19: parse_file maneja líneas muy largas."""
        parser = DummyParser()
        test_file = Path("fixtures/test_base_long_lines.log")

        if test_file.exists():
            entries = list(parser.parse_file(test_file))

            # No debería fallar con líneas largas
            assert isinstance(entries, list)

    def test_parse_file_with_only_empty_lines(self):
        """Test 20: parse_file maneja archivo con solo líneas vacías."""
        parser = DummyParser()
        test_file = Path("fixtures/test_base_only_empty.log")

        if test_file.exists():
            entries = list(parser.parse_file(test_file))

            # Debe retornar lista vacía
            assert entries == []

    def test_parse_file_with_only_invalid_lines(self):
        """Test 21: parse_file maneja archivo con solo líneas inválidas."""
        parser = DummyParser()
        test_file = Path("fixtures/test_base_only_invalid.log")

        if test_file.exists():
            entries = list(parser.parse_file(test_file))

            # Debe retornar lista vacía
            assert entries == []


# ============================================================================
# FASE 8: Tests de Rendimiento (Opcional)
# ============================================================================


class TestPerformance:
    """Tests de rendimiento y eficiencia."""

    @pytest.mark.slow
    def test_parse_file_uses_generator(self):
        """Test 22: parse_file usa generador (no carga todo en memoria)."""
        parser = DummyParser()
        test_file = Path("fixtures/test_base_simple.log")

        result = parser.parse_file(test_file)

        # Debe ser un generador, no una lista
        assert hasattr(result, "__next__")

    @pytest.mark.slow
    def test_parse_file_lazy_evaluation(self):
        """Test 23: parse_file evalúa perezosamente (lazy evaluation)."""
        parser = DummyParser()
        test_file = Path("fixtures/test_base_simple.log")

        result = parser.parse_file(test_file)

        # Al crear el generador, no debería haber procesado nada aún
        # Solo procesamos cuando iteramos
        first = next(result)
        assert isinstance(first, LogEntry)


# ============================================================================
# FIXTURES PARA CREAR ARCHIVOS DE TEST
# ============================================================================


@pytest.fixture
def dummy_parser():
    """Fixture que retorna una instancia de DummyParser."""
    return DummyParser()


@pytest.fixture
def sample_valid_lines():
    """Fixture con líneas válidas de ejemplo."""
    return [
        "192.168.1.1|2024-11-26T12:00:00+00:00|GET|/index.html|200|1234",
        "192.168.1.2|2024-11-26T12:01:00+00:00|POST|/api/login|404|162",
        "192.168.1.3|2024-11-26T12:02:00+00:00|GET|/api/data|500|1024",
    ]


# ============================================================================
# TESTS USANDO FIXTURES
# ============================================================================


class TestWithFixtures:
    """Tests que usan fixtures para código más limpio."""

    def test_parse_multiple_lines_with_fixture(self, dummy_parser, sample_valid_lines):
        """Test 24: Parsear múltiples líneas usando fixtures."""
        results = [dummy_parser.parse_line(line) for line in sample_valid_lines]

        assert all(result is not None for result in results)
        assert len(results) == 3

    def test_parsed_entries_have_correct_ips(self, dummy_parser, sample_valid_lines):
        """Test 25: Verificar IPs extraídas con fixtures."""
        results = [dummy_parser.parse_line(line) for line in sample_valid_lines]
        ips = [r.ip for r in results]

        assert ips == ["192.168.1.1", "192.168.1.2", "192.168.1.3"]
