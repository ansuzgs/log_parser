# Estructura del Proyecto Log Parser

```
log-parser/
│
├── README.md                      # Documentación principal del proyecto
├── requirements.txt               # Dependencias Python
├── setup.py                       # Configuración de instalación
├── .gitignore                     # Archivos a ignorar en Git
│
├── src/                          # Código fuente principal
│   ├── __init__.py
│   │
│   ├── models/                   # Modelos de datos
│   │   ├── __init__.py
│   │   └── log_entry.py         # Clase LogEntry (dataclass)
│   │
│   ├── parsers/                  # Módulo de parsing
│   │   ├── __init__.py
│   │   ├── base_parser.py       # Clase abstracta BaseParser
│   │   ├── nginx_parser.py      # Parser para nginx (IMPLEMENTADO)
│   │   └── apache_parser.py     # Parser para apache (TODO)
│   │
│   ├── analyzers/                # Módulo de análisis
│   │   ├── __init__.py
│   │   └── log_analyzer.py      # Análisis y métricas (TODO)
│   │
│   ├── formatters/               # Módulo de formateo de salida
│   │   ├── __init__.py
│   │   ├── table_formatter.py   # Formato tabla con Rich (TODO)
│   │   ├── json_formatter.py    # Formato JSON (TODO)
│   │   ├── csv_formatter.py     # Formato CSV (TODO)
│   │   └── markdown_formatter.py # Formato Markdown (TODO)
│   │
│   └── cli/                      # Interfaz de línea de comandos
│       ├── __init__.py
│       └── commands.py          # Comandos CLI con Click (TODO)
│
├── tests/                        # Tests unitarios e integración
│   ├── __init__.py
│   ├── test_models.py           # Tests para LogEntry
│   ├── test_parsers.py          # Tests para parsers
│   ├── test_analyzers.py        # Tests para analyzer
│   ├── test_formatters.py       # Tests para formatters
│   └── test_cli.py              # Tests para CLI
│
└── fixtures/                     # Archivos de ejemplo
    └── nginx_sample.log         # Log de ejemplo nginx (100 líneas)

```

## Archivos Creados y Listos para Usar

### ✅ Completamente Implementados

1. **src/models/log_entry.py**
   - Dataclass inmutable para representar una entrada de log
   - Properties: is_error, is_client_error, is_server_error, is_success
   - Validación de datos en __post_init__

2. **src/parsers/base_parser.py**
   - Clase abstracta con método parse_line() y parse_file()
   - Manejo de errores graceful
   - Procesamiento línea por línea con generadores

3. **src/parsers/nginx_parser.py**
   - Regex compilado para formato nginx
   - Parsing de timestamps
   - Manejo de campos opcionales

4. **fixtures/nginx_sample.log**
   - 100 líneas de logs nginx realistas
   - Variedad de códigos de estado (200, 404, 500, 502, etc.)
   - Diferentes IPs y rutas
   - Patrones de ataque simulados (SQL injection, path traversal)
   - Timestamps distribuidos a lo largo del día

### 📝 Archivos Placeholder (Pendientes de Implementar)

- src/parsers/apache_parser.py
- src/analyzers/log_analyzer.py
- src/formatters/*.py (todos)
- src/cli/commands.py
- tests/*.py (todos)

### 📚 Documentación

- README.md con descripción completa
- requirements.txt con dependencias
- setup.py para instalación como paquete
- .gitignore configurado para Python

## Próximos Pasos

1. **Fase 1 - MVP Básico**:
   - Implementar log_analyzer.py para contar códigos de estado
   - Crear output básico con print
   - Tests para parser y analyzer

2. **Fase 2 - Análisis Avanzado**:
   - Top N IPs y rutas
   - Análisis temporal
   - Filtrado por fechas

3. **Fase 3 - Output Profesional**:
   - Implementar formatters con Rich
   - Exportación JSON/CSV

4. **Fase 4 - CLI Completo**:
   - Comandos con Click
   - Progress bars
   - Validación de argumentos

## Características del Log de Ejemplo

El archivo `fixtures/nginx_sample.log` incluye:

- ✅ 100 líneas de logs
- ✅ Códigos de estado: 200, 201, 204, 400, 401, 403, 404, 413, 500, 502, 503
- ✅ IP repetida (192.168.1.100) simulando usuario activo
- ✅ Secuencia de 5 peticiones 404 consecutivas (192.168.1.117) - posible scanner
- ✅ Intentos de SQL injection en URLs
- ✅ Intentos de path traversal
- ✅ Diferentes user agents (navegadores, bots, curl, axios)
- ✅ Timestamps a lo largo de 4 horas (08:00 - 12:00)
- ✅ Diferentes métodos HTTP (GET, POST, PUT, DELETE)
- ✅ Variedad de rutas (páginas, API endpoints, archivos estáticos)
