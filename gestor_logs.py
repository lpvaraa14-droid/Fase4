# gestor_logs.py

# Importa el módulo estándar 'os' para interactuar con el sistema operativo y rutas de archivos (disponible para futuras validaciones)
import os
# Importa la clase 'datetime' del módulo 'datetime' para obtener y formatear la fecha y hora actuales
from datetime import datetime


# Define la clase encargada de administrar la escritura de eventos y fallos en el archivo de registro
class GestorLogs:
    """Gestiona el registro de eventos y errores del sistema Software FJ en archivos de texto."""

    # Define el método constructor que inicializa la instancia con el nombre del archivo de log por defecto
    def __init__(self, nombre_archivo_log: str = "auditoria_software_fj.log"):
        # Almacena como atributo de instancia la ruta o nombre del archivo donde se guardarán los registros
        self.nombre_archivo_log = nombre_archivo_log

    # Define el método para guardar eventos operativos normales, recibiendo el tipo, descripción y detalles técnicos opcionales
    def guardar_registro(self, tipo_evento: str, descripcion: str, info_tecnica: str = "") -> None:
        """Registra un evento operativo normal o de éxito en el archivo de log."""
        # Obtiene la fecha y hora exacta del sistema y la convierte en una cadena con formato 'AAAA-MM-DD HH:MM:SS'
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Construye la línea base del registro combinando la marca de tiempo, el tipo de evento en mayúsculas y su descripción
        linea_log = f"[{marca_tiempo}] [EVENTO: {tipo_evento.upper()}] - {descripcion}"
        # Verifica si se proporcionó información técnica adicional (cadena no vacía)
        if info_tecnica:
            # Concatena el detalle técnico al final de la línea de registro utilizando un separador visual
            linea_log += f" | Detalle: {info_tecnica}"
        
        # Inicia un bloque de control de excepciones para proteger la ejecución ante posibles errores de entrada/salida en disco
        try:
            # Abre el archivo de log en modo añadir ('a') con codificación 'utf-8', asegurándose de cerrarlo automáticamente al salir del bloque
            with open(self.nombre_archivo_log, "a", encoding="utf-8") as archivo:
                # Escribe la línea formateada en el archivo seguida de un salto de línea ('\n')
                archivo.write(linea_log + "\n")
        # Captura cualquier excepción inesperada que ocurra al intentar abrir o escribir en el archivo
        except Exception as e:
            # Muestra un mensaje de advertencia en consola sin detener la ejecución principal del programa
            print(f"Advertencia: No se pudo escribir en el archivo de log. Error: {e}")

    # Define el método para registrar excepciones o errores críticos indicando el módulo donde se originaron
    def guardar_fallo(self, modulo_origen: str, error_capturado: Exception) -> None:
        """Registra una excepción o fallo capturado en el sistema con su respectivo módulo de origen."""
        # Captura el instante exacto en que se registra el fallo y lo formatea como texto legible
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Extrae dinámicamente el nombre de la clase de la excepción capturada (por ejemplo, 'DatoInvalidoError')
        tipo_error = type(error_capturado).__name__
        # Ensambla la línea de error con la hora, el módulo origen en mayúsculas, el tipo de excepción y su mensaje descriptivo
        linea_log = f"[{marca_tiempo}] [FALLO EN: {modulo_origen.upper()}] - {tipo_error}: {error_capturado}"
        
        # Inicia un bloque 'try' para manejar de forma segura la apertura y escritura en el archivo de auditoría
        try:
            # Abre el archivo de log en modo añadir ('a') y codificación 'utf-8' mediante un gestor de contexto ('with')
            with open(self.nombre_archivo_log, "a", encoding="utf-8") as archivo:
                # Inserta la línea del fallo al final del documento agregando un salto de línea
                archivo.write(linea_log + "\n")
        # Intercepta cualquier fallo de permisos, ruta o escritura en disco para evitar que el sistema colapse al loguear
        except Exception as e:
            # Imprime en consola una alerta detallando el motivo por el cual no se pudo guardar el fallo en el archivo
            print(f"Advertencia: No se pudo registrar el fallo en el log. Error: {e}")
