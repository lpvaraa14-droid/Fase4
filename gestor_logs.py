# gestor_logs.py
import os
from datetime import datetime

class GestorLogs:
    """Gestiona el registro de eventos y errores del sistema Software FJ en archivos de texto."""

    def __init__(self, nombre_archivo_log: str = "auditoria_software_fj.log"):
        self.nombre_archivo_log = nombre_archivo_log

    def guardar_registro(self, tipo_evento: str, descripcion: str, info_tecnica: str = "") -> None:
        """Registra un evento operativo normal o de éxito en el archivo de log."""
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea_log = f"[{marca_tiempo}] [EVENTO: {tipo_evento.upper()}] - {descripcion}"
        if info_tecnica:
            linea_log += f" | Detalle: {info_tecnica}"
        
        try:
            with open(self.nombre_archivo_log, "a", encoding="utf-8") as archivo:
                archivo.write(linea_log + "\n")
        except Exception as e:
            print(f"Advertencia: No se pudo escribir en el archivo de log. Error: {e}")

    def guardar_fallo(self, modulo_origen: str, error_capturado: Exception) -> None:
        """Registra una excepción o fallo capturado en el sistema con su respectivo módulo de origen."""
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tipo_error = type(error_capturado).__name__
        linea_log = f"[{marca_tiempo}] [FALLO EN: {modulo_origen.upper()}] - {tipo_error}: {error_capturado}"
        
        try:
            with open(self.nombre_archivo_log, "a", encoding="utf-8") as archivo:
                archivo.write(linea_log + "\n")
        except Exception as e:
            print(f"Advertencia: No se pudo registrar el fallo en el log. Error: {e}")