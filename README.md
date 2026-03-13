# LinkLogic
Ecosistema Personalizado en Obsidian

***

# 🕸️ Obsidian Zettelkasten Linker & Orphan Detector

Un script de Python diseñado para auditar bóvedas locales de Obsidian. Modela el sistema de notas como un grafo dirigido para detectar nodos aislados (notas huérfanas) y realiza un análisis de texto inverso para sugerir conexiones basadas en menciones no enlazadas.

## ✨ Características Principales

* **Escaneo Local Optimizado:** Utiliza `pathlib` para recorrer recursivamente la bóveda sin importar la estructura de carpetas.
* **Detección de Huérfanas (O(n)):** Aplica teoría de conjuntos para identificar notas con grado de entrada cero de manera eficiente.
* **Motor de Sugerencias:** Escanea el contenido de toda la bóveda buscando coincidencias de texto plano (*case-insensitive*) para encontrar conceptos mencionados pero no enlazados formalmente con `[[ ]]`.
* **Integración Nativa:** Genera un archivo `00_Reporte_Huerfanas.md` directo en la bóveda usando la sintaxis de *checkbox* de Obsidian para una gestión rápida.
* **Ejecución "One-Click":** Incluye un script `.bat` para automatizar la ejecución del reporte desde el sistema operativo.

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3
* **Librerías Estándar:** `pathlib`, `re` (Expresiones Regulares), `os`.
* **Entorno:** Local (Diseñado y testeado en Windows).

## 🚀 Uso Rápido

1. Clonar el repositorio.
2. Editar la variable `MI_BOVEDA_REAL` dentro de `escaner.py` con la ruta absoluta a tu bóveda.
3. Ejecutar el script por consola o mediante el acceso directo `.bat`:

```bash
python escaner.py

```
