from pathlib import Path
import re

def obtener_notas_markdown(ruta_boveda):
    directorio_base = Path(ruta_boveda)
    return list(directorio_base.rglob('*.md'))

def extraer_enlaces(lista_notas):
    grafo_boveda = {}
    patron_enlace = re.compile(r'\[\[(.*?)\]\]')

    for ruta_nota in lista_notas:
        nombre_origen = ruta_nota.stem 
        try:
            with open(ruta_nota, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()
                enlaces_encontrados = patron_enlace.findall(contenido)
            grafo_boveda[nombre_origen] = enlaces_encontrados
        except Exception as e:
            print(f"Error al leer {nombre_origen}: {e}")
            
    return grafo_boveda

# --- NUEVA FUNCIÓN (Módulo B) ---
def detectar_huerfanas(grafo):
    """
    Compara las notas existentes con las notas enlazadas (normalizando el texto)
    para encontrar las verdaderas huérfanas.
    """
    # 1. Creamos un conjunto de notas mencionadas, pero "limpias"
    notas_mencionadas_limpias = set()
    for lista_de_enlaces in grafo.values():
        for enlace in lista_de_enlaces:
            # .strip() borra espacios al inicio/final y .lower() pasa todo a minúscula
            enlace_limpio = enlace.strip().lower()
            notas_mencionadas_limpias.add(enlace_limpio)
            
    # 2. Buscamos las huérfanas comprobando sus nombres limpios
    huerfanas = []
    for nota_real in grafo.keys():
        # Limpiamos también el nombre del archivo real para que la comparación sea justa
        nota_limpia = nota_real.strip().lower()
        
        # Si la nota limpia NO está en el conjunto de las mencionadas, es huérfana
        if nota_limpia not in notas_mencionadas_limpias:
            huerfanas.append(nota_real) # Guardamos el nombre original, con sus mayúsculas
            
    return huerfanas

# --- NUEVA FUNCIÓN (Módulo D) ---
def generar_reporte(ruta_boveda, lista_huerfanas):
    """
    Crea un archivo Markdown en la bóveda con la lista de notas huérfanas
    usando el formato de tareas (checkboxes) de Obsidian.
    """
    # Usamos pathlib para unir la ruta de la carpeta con el nombre del nuevo archivo
    directorio_base = Path(ruta_boveda)
    ruta_reporte = directorio_base / "00_Reporte_Huerfanas.md" 
    # (Le pongo "00_" adelante para que aparezca arriba de todo en tu lista de carpetas)
    
    try:
        # Abrimos en modo 'w' (write). Si el archivo no existe, lo crea. Si ya existe, lo sobrescribe (¡ideal para actualizar el reporte!)
        with open(ruta_reporte, 'w', encoding='utf-8') as archivo:
            # Escribimos el título y una pequeña descripción
            archivo.write("# 📝 Reporte de Notas Huérfanas\n\n")
            archivo.write("Las siguientes notas no reciben ningún enlace. ¡Es un buen momento para conectarlas!\n\n")
            
            # Si no hay huérfanas, damos buenas noticias
            if not lista_huerfanas:
                archivo.write("¡Felicidades! Todas tus notas están conectadas.\n")
            else:
                # Ordenamos la lista alfabéticamente para que sea más fácil de leer
                lista_huerfanas.sort()
                
                # Escribimos cada nota con el formato de checkbox y enlace de Obsidian
                for nota in lista_huerfanas:
                    archivo.write(f"- [ ] [[{nota}]]\n")
                    
        print(f"\n¡Éxito! Reporte generado en: {ruta_reporte}")
        
    except Exception as e:
        print(f"\nError al generar el reporte: {e}")

# --- Zona de Ejecución y Pruebas ---
if __name__ == '__main__':
    MI_BOVEDA_PRUEBA = "./boveda_prueba" 
    
    # 1. Navegación (Módulo A)
    archivos = obtener_notas_markdown(MI_BOVEDA_PRUEBA)
    # 2. Extracción (Módulo A)
    grafo = extraer_enlaces(archivos)
    # 3. Lógica (Módulo B)
    notas_solitarias = detectar_huerfanas(grafo)
    # 4. Salida (Módulo D)
    generar_reporte(MI_BOVEDA_PRUEBA, notas_solitarias)
