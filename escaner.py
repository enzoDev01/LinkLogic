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

def buscar_sugerencias(ruta_boveda, lista_huerfanas):
    """
    Busca el nombre de las notas huérfanas dentro del texto de todas las demás notas.
    Devuelve un diccionario: {huerfana: [nota_sugerida1, nota_sugerida2]}
    """
    # Preparamos un diccionario vacío para guardar las sugerencias
    sugerencias = {}
    for huerfana in lista_huerfanas:
        sugerencias[huerfana] = []

    directorio_base = Path(ruta_boveda)
    todas_las_notas = list(directorio_base.rglob('*.md'))

    for ruta_nota in todas_las_notas:
        nombre_actual = ruta_nota.stem

        try:
            # Abrimos la nota y pasamos todo su contenido a minúsculas
            with open(ruta_nota, 'r', encoding='utf-8') as archivo:
                contenido_limpio = archivo.read().lower()

            # Revisamos si alguna de las huérfanas es mencionada en este texto
            for huerfana in lista_huerfanas:
                # 1. No queremos que una nota se sugiera a sí misma
                if huerfana != nombre_actual:
                    # 2. Pasamos la huérfana a minúscula y buscamos si está en el texto
                    if huerfana.lower() in contenido_limpio:
                        sugerencias[huerfana].append(nombre_actual)

        except Exception as e:
            print(f"Error al leer {nombre_actual} para buscar sugerencias: {e}")

    return sugerencias

# --- NUEVA FUNCIÓN (Módulo D) ---
def generar_reporte(ruta_boveda, lista_huerfanas, mapa_sugerencias):
    """
    Crea un archivo Markdown en la bóveda con la lista de notas huérfanas
    y sus posibles conexiones sugeridas.
    """
    directorio_base = Path(ruta_boveda)
    ruta_reporte = directorio_base / "00_Reporte_Huerfanas.md" 
    
    try:
        with open(ruta_reporte, 'w', encoding='utf-8') as archivo:
            archivo.write("# 📝 Reporte de Notas Huérfanas\n\n")
            archivo.write("Las siguientes notas no reciben ningún enlace. ¡Es un buen momento para conectarlas!\n\n")
            
            if not lista_huerfanas:
                archivo.write("¡Felicidades! Todas tus notas están conectadas.\n")
            else:
                lista_huerfanas.sort()
                
                for nota in lista_huerfanas:
                    # 1. Escribimos la base del checkbox
                    linea = f"- [ ] [[{nota}]]"
                    
                    # 2. Buscamos si esta nota específica tiene sugerencias
                    sugerencias_para_esta_nota = mapa_sugerencias.get(nota, [])
                    
                    # 3. Si tiene sugerencias, las agregamos al lado con formato de enlace
                    if sugerencias_para_esta_nota:
                        # Convertimos la lista ['nota2', 'nota3'] en "[[nota2]], [[nota3]]"
                        enlaces_sugeridos = ", ".join([f"[[{s}]]" for s in sugerencias_para_esta_nota])
                        linea += f" *(Mencionada sin enlazar en: {enlaces_sugeridos})*"
                        
                    # 4. Finalmente escribimos la línea completa en el archivo
                    archivo.write(linea + "\n")
                    
        print(f"\n¡Éxito! Reporte con sugerencias generado en: {ruta_reporte}")
        
    except Exception as e:
        print(f"\nError al generar el reporte: {e}")

# --- Zona de Ejecución y Pruebas ---
if __name__ == '__main__':
    MI_BOVEDA_PRUEBA = "./boveda_prueba" 
    
    # Ejecutamos la tubería (pipeline) completa:
    archivos = obtener_notas_markdown(MI_BOVEDA_PRUEBA)
    grafo = extraer_enlaces(archivos)
    notas_solitarias = detectar_huerfanas(grafo)
    mapa_sugerencias = buscar_sugerencias(MI_BOVEDA_PRUEBA, notas_solitarias)
    
    # Generamos el reporte final inyectando las sugerencias
    generar_reporte(MI_BOVEDA_PRUEBA, notas_solitarias, mapa_sugerencias)
