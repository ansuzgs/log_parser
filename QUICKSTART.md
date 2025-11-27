# Guía de Inicio Rápido - Log Parser

## Configuración Inicial

### 1. Crear entorno virtual
```bash
cd log-parser
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Instalar el proyecto en modo desarrollo
```bash
pip install -e .
```

## Verificar la Instalación

### Probar el parser directamente

Crea un archivo `test_parser.py` en la raíz del proyecto:

```python
from pathlib import Path
from src.parsers.nginx_parser import NginxParser

# Crear instancia del parser
parser = NginxParser()

# Parsear el archivo de ejemplo
log_file = Path("fixtures/nginx_sample.log")
entries = list(parser.parse_file(log_file))

print(f"Total de líneas parseadas: {len(entries)}")
print("\nPrimeras 3 entradas:")
for entry in entries[:3]:
    print(f"  {entry.ip} - {entry.method} {entry.path} - {entry.status_code}")

# Contar códigos de estado
from collections import Counter
status_codes = Counter(entry.status_code for entry in entries)
print("\nDistribución de códigos de estado:")
for code, count in sorted(status_codes.items()):
    print(f"  {code}: {count}")

# Errores
errors = [e for e in entries if e.is_error]
print(f"\nTotal de errores (4xx y 5xx): {len(errors)}")
```

Ejecutar:
```bash
python test_parser.py
```

## Desarrollo con TDD

### Ejemplo de test básico

Crea `tests/test_models.py`:

```python
import pytest
from datetime import datetime
from src.models.log_entry import LogEntry


def test_log_entry_creation():
    """Test que LogEntry se crea correctamente."""
    entry = LogEntry(
        ip="192.168.1.1",
        timestamp=datetime.now(),
        method="GET",
        path="/index.html",
        status_code=200,
        response_size=1024
    )
    assert entry.ip == "192.168.1.1"
    assert entry.status_code == 200


def test_log_entry_is_success():
    """Test que is_success identifica códigos 2xx."""
    entry = LogEntry(
        ip="192.168.1.1",
        timestamp=datetime.now(),
        method="GET",
        path="/",
        status_code=200,
        response_size=1024
    )
    assert entry.is_success is True
    assert entry.is_error is False


def test_log_entry_is_client_error():
    """Test que is_client_error identifica códigos 4xx."""
    entry = LogEntry(
        ip="192.168.1.1",
        timestamp=datetime.now(),
        method="GET",
        path="/notfound",
        status_code=404,
        response_size=162
    )
    assert entry.is_client_error is True
    assert entry.is_error is True


def test_log_entry_is_server_error():
    """Test que is_server_error identifica códigos 5xx."""
    entry = LogEntry(
        ip="192.168.1.1",
        timestamp=datetime.now(),
        method="POST",
        path="/api",
        status_code=500,
        response_size=1024
    )
    assert entry.is_server_error is True
    assert entry.is_error is True


def test_log_entry_validation_empty_ip():
    """Test que valida IP no puede estar vacía."""
    with pytest.raises(ValueError, match="IP no puede estar vacía"):
        LogEntry(
            ip="",
            timestamp=datetime.now(),
            method="GET",
            path="/",
            status_code=200,
            response_size=1024
        )


def test_log_entry_validation_invalid_status():
    """Test que valida código de estado debe estar en rango válido."""
    with pytest.raises(ValueError, match="Código de estado inválido"):
        LogEntry(
            ip="192.168.1.1",
            timestamp=datetime.now(),
            method="GET",
            path="/",
            status_code=999,
            response_size=1024
        )
```

Ejecutar tests:
```bash
pytest tests/test_models.py -v
```

## Siguiente Paso: Implementar el Analyzer

El siguiente archivo a implementar debería ser `src/analyzers/log_analyzer.py`.

Empieza escribiendo el test primero:

```python
# tests/test_analyzers.py
from src.analyzers.log_analyzer import LogAnalyzer
from src.parsers.nginx_parser import NginxParser
from pathlib import Path


def test_analyzer_counts_status_codes():
    """Test que el analyzer cuenta códigos de estado correctamente."""
    parser = NginxParser()
    entries = list(parser.parse_file(Path("fixtures/nginx_sample.log")))
    
    analyzer = LogAnalyzer(entries)
    status_counts = analyzer.get_status_counts()
    
    assert isinstance(status_counts, dict)
    assert 200 in status_counts
    assert status_counts[200] > 0
```

Luego implementa la clase para que el test pase.

## Estructura de Trabajo Recomendada

1. **Escribe el test primero** (TDD)
2. **Ejecuta el test** (debe fallar)
3. **Implementa el código mínimo** para que pase
4. **Refactoriza** si es necesario
5. **Repite** para la siguiente funcionalidad

## Comandos Útiles

```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests con coverage
pytest --cov=src tests/

# Ejecutar tests de un archivo específico
pytest tests/test_models.py

# Ejecutar un test específico
pytest tests/test_models.py::test_log_entry_creation

# Ver prints en tests
pytest -s

# Modo verbose
pytest -v

# Formatear código con Black
black src/ tests/

# Linter con flake8
flake8 src/ tests/

# Type checking con mypy
mypy src/
```

## Recursos Adicionales

- [Documentación de pytest](https://docs.pytest.org/)
- [Click documentation](https://click.palletsprojects.com/)
- [Rich documentation](https://rich.readthedocs.io/)
- [Python regex documentation](https://docs.python.org/3/library/re.html)
- [Regex tester online](https://regex101.com/)

## Problemas Comunes

### ImportError al ejecutar tests
Asegúrate de instalar el proyecto en modo desarrollo:
```bash
pip install -e .
```

### ModuleNotFoundError
Verifica que todos los `__init__.py` existan en las carpetas.

### Tests no se descubren
Asegúrate que los archivos de test empiecen con `test_` y las funciones también.

## Próximos Pasos Sugeridos

1. ⬜ Parser de nginx
2. ⬜ Implementar LogAnalyzer básico
3. ⬜ Implementar TableFormatter con Rich
4. ⬜ Crear comando CLI básico
5. ⬜ Agregar progress bar
6. ⬜ Parser de apache
7. ⬜ Exportación JSON/CSV
8. ⬜ Modo watch en tiempo real

¡Buena suerte con el proyecto! 🚀
