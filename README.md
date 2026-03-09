# LinkLogic
Ecosistema Personalizado en Obsidian

***

## 📄 Documentación Fase 1: Escáner de Bóveda Zettelkasten (MVP)
Descripción del Proyecto: Script desarrollado en Python diseñado para analizar una bóveda local de Obsidian, modelar sus conexiones como un grafo dirigido e identificar "notas huérfanas" (nodos con grado de entrada cero) para generar un reporte interactivo de forma nativa.

### Arquitectura de Módulos (Fase 1):

_Módulo A (Navegación y Extracción)_: Utiliza la librería pathlib para recorrer recursivamente los directorios buscando archivos .md. Mediante expresiones regulares (re), extrae los enlaces internos (formato [[Nota]]) para construir un diccionario de adyacencia (el Grafo).

_Módulo B (Motor Lógico)_: Implementa teoría de conjuntos (sets) y normalización de strings (minúsculas, limpieza de espacios) para aislar las notas existentes de las notas mencionadas, detectando con precisión las notas huérfanas.

_Módulo D (Interfaz de Salida)_: Escribe automáticamente un archivo 00_Reporte_Huerfanas.md en la raíz de la bóveda, utilizando la sintaxis de checkbox de Obsidian (- [ ]) para facilitar la gestión del conocimiento por parte del usuario.
