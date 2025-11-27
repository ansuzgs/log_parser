# Log Parser & Analyzer

Un analizador de logs profesional para archivos nginx y apache que procesa archivos grandes de manera eficiente, extrae información mediante regex, y presenta resultados de forma clara.

## Características

- 📊 Análisis de logs nginx y apache
- 🚀 Procesamiento eficiente de archivos grandes (GB)
- 📈 Métricas estadísticas (top IPs, rutas más visitadas, códigos de estado)
- 🔍 Detección de anomalías y patrones de ataque
- 🎨 Múltiples formatos de salida (tabla, JSON, CSV, Markdown)
- ⚡ CLI intuitivo con progress bars
- 🧪 Tests completos con TDD

## Estructura del Proyecto

```
log-parser/
├── src/
│   ├── models/          # Modelos de datos (LogEntry)
│   ├── parsers/         # Parsers para diferentes formatos
│   ├── analyzers/       # Análisis y métricas
│   ├── formatters/      # Formateadores de salida
│   └── cli/             # Interfaz de línea de comandos
├── tests/               # Tests unitarios e integración
├── fixtures/            # Archivos de ejemplo para testing
└── requirements.txt     # Dependencias
```

## Instalación

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Instalar en modo desarrollo
pip install -e .
```

## Uso

### Análisis básico
```bash
logparse analyze nginx.log
```

### Con opciones avanzadas
```bash
# Top 20 IPs más activas
logparse analyze nginx.log --top-ips 20

# Solo errores
logparse analyze nginx.log --errors-only

# Filtrar por fechas
logparse analyze nginx.log --start 2024-01-01 --end 2024-01-31

# Exportar a JSON
logparse analyze nginx.log --output json --output-file report.json
```

## Desarrollo

### Ejecutar tests
```bash
pytest tests/
```

### Ejecutar tests con coverage
```bash
pytest --cov=src tests/
```

## Roadmap

- [ ] Parser de nginx
- [ ] Parser de apache
- [ ] Modo watch en tiempo real
- [ ] Detección de patrones de ataque
- [ ] Soporte para logs comprimidos (.gz)
- [ ] Análisis multi-archivo
- [ ] Sistema de alertas

## Aprendizajes Clave

Este proyecto enseña:
- Procesamiento eficiente de archivos grandes
- Regular expressions avanzadas
- Estructuración de datos con dataclasses
- Agregaciones y análisis estadístico
- Testing con TDD
- CLIs profesionales con Click
- Rich terminal UI

## Licencia

MIT
