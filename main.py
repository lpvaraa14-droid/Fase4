# main.py
# Importamos las clases del modelo desde modelos.py
from modelos import (
    Cliente,
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada,
    Reserva,
)
# Importamos la excepción base desde excepciones.py
from excepciones import ErrorSistemaFJ
# Importamos el gestor de archivos planos desde gestor_logs.py
from gestor_logs import GestorLogs


class ControladorSoftwareFJ:
    """Controlador principal que gestiona listas en memoria de clientes, servicios y reservas."""

    def __init__(self):
        # Lista en memoria para almacenar los clientes registrados
        self.lista_clientes = []
        # Lista en memoria para almacenar el catálogo de servicios
        self.catalogo_servicios = []
        # Lista en memoria para almacenar las reservas procesadas
        self.historial_reservas = []
        # Instanciamos el gestor de logs apuntando al archivo auditoria_software_fj.log
        self.bitacora = GestorLogs("auditoria_software_fj.log")

    def agregar_cliente(self, cod_cli: str, nombre_cli: str, correo_cli: str, tel_cli: str) -> None:
        # Bloque try/except/else/finally para validar y registrar un cliente de forma segura
        try:
            # Intentamos instanciar el objeto Cliente con sus respectivas validaciones
            cliente_nuevo = Cliente(cod_cli, nombre_cli, correo_cli, tel_cli)
        except ErrorSistemaFJ as fallo_validacion:
            # Capturamos errores de datos inválidos o faltantes sin detener el programa
            print(f"  [X] Error al registrar cliente ({cod_cli}): {fallo_validacion}")
            # Guardamos el incidente en el archivo plano de auditoría
            self.bitacora.guardar_fallo(f"Registro Cliente {cod_cli}", fallo_validacion)
        else:
            # El bloque else se ejecuta únicamente si no ocurrió ninguna excepción
            self.lista_clientes.append(cliente_nuevo)
            # Imprimimos la ficha del cliente creado en consola
            print(f"  [OK] {cliente_nuevo.mostrar_ficha()}")
            # Registramos el éxito en la bitácora
            self.bitacora.guardar_registro("INFO", f"Cliente creado correctamente: {cliente_nuevo.codigo_unico}")
        finally:
            # El bloque finally se ejecuta siempre al finalizar la operación
            self.bitacora.guardar_registro("DEBUG", f"Cierre de proceso de alta para cliente ID={cod_cli}")

    def agregar_servicio(self, nuevo_servicio) -> None:
        # Añadimos el servicio al catálogo en memoria
        self.catalogo_servicios.append(nuevo_servicio)
        # Mostramos el detalle técnico obtenido polimórficamente
        print(f"  [OK] Servicio habilitado: {nuevo_servicio.obtener_detalle_tecnico()}")
        # Dejamos constancia en el archivo de logs
        self.bitacora.guardar_registro("INFO", f"Servicio añadido al catálogo: {nuevo_servicio.codigo_unico}")

    def procesar_nueva_reserva(
        self,
        cod_res: str,
        cliente_sel: Cliente,
        servicio_sel,
        duracion: int,
        descuento: float = 0.0,
        recargo: float = 0.0
    ):
        # Inicializamos la variable en None antes de crear la reserva
        nueva_reserva = None
        try:
            # Creamos la reserva verificando disponibilidad y reglas
            nueva_reserva = Reserva(cod_res, cliente_sel, servicio_sel, duracion)
            # Confirmamos la reserva y calculamos su valor final
            valor_pagado = nueva_reserva.confirmar_reserva(
                descuento_aplicado=descuento,
                recargo_aplicado=recargo
            )
        except ErrorSistemaFJ as fallo_reserva:
            # Capturamos errores de negocio (servicio ocupado, descuento inválido, etc.)
            print(f"  [X] Fallo en reserva ({cod_res}): {fallo_reserva}")
            # Guardamos el error en el log
            self.bitacora.guardar_fallo(f"Procesamiento Reserva {cod_res}", fallo_reserva)
        except Exception as error_general:
            # Capturamos cualquier error inesperado para garantizar estabilidad total
            print(f"  [X] Error inesperado en reserva ({cod_res}): {error_general}")
            # Guardamos la traza del error general
            self.bitacora.guardar_fallo(f"Error Crítico Reserva {cod_res}", error_general)
        else:
            # Si la reserva fue exitosa, la agregamos al historial en memoria
            self.historial_reservas.append(nueva_reserva)
            # Mostramos la confirmación en consola
            print(f"  [OK] {nueva_reserva.mostrar_ficha()} | Cobro final: ${valor_pagado:,.2f}")
            # Registramos el éxito en la bitácora
            self.bitacora.guardar_registro("INFO", f"Reserva {cod_res} confirmada por ${valor_pagado:,.2f}")
        # Retornamos la reserva creada (o None si falló)
        return nueva_reserva


def iniciar_pruebas_sistema():
    # Encabezado de presentación en consola
    print("=" * 80)
    print(" SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS - SOFTWARE FJ")
    print("=" * 80)

    # Creamos la instancia del controlador principal
    app_fj = ControladorSoftwareFJ()
    # Registramos el arranque en el archivo plano
    app_fj.bitacora.guardar_registro("INFO", "=== ARRANQUE DE SIMULACIÓN SOFTWARE FJ ===")

    

    #1: Regristro de Clientes (Validos E Invalidos)
    
    print("\n--- 1. GESTIÓN DE CLIENTES ---")
    # Operación 1: Registro exitoso de Laura Alejandra
    app_fj.agregar_cliente("CLI-01", "Laura Alejandra Quitian", "laura.quitian@unad.edu.co", "3104567890")
    # Operación 2: Registro exitoso de Lina Paola
    app_fj.agregar_cliente("CLI-02", "Lina Paola Vara Agudelo", "lina.vara@softwarefj.com", "3209876543")
    # Operación 3: Registro fallido por formato de correo incorrecto (DatoInvalidoError)
    app_fj.agregar_cliente("CLI-03", "Andrés Felipe Torres", "andres.correo.sin.arroba", "3112223344")
    # Operación 4: Registro fallido por nombre vacío (ParametroFaltanteError)
    app_fj.agregar_cliente("CLI-04", "", "cliente@dominio.com", "3001112233")

    
    #2: Creacion de servicios especializados  (Validos e Invalidos)
        print("\n--- 2. GESTIÓN DE SERVICIOS (POLIMORFISMO) ---")
    # Operación 5: Creación válida de Sala de Juntas
    try:
        sala_conferencias = ReservaSala("SRV-01", "Sala Innovación Norte", 80000.0, aforo_maximo=12, incluye_proyector=True)
        app_fj.agregar_servicio(sala_conferencias)
    except ErrorSistemaFJ as err_srv:
        app_fj.bitacora.guardar_fallo("Creación SRV-01", err_srv)

    # Operación 6: Creación válida de Alquiler de Equipos
    try:
        lote_portatiles = AlquilerEquipo("SRV-02", "Workstation Linux i9", 25000.0, categoria_hw="ALTA", num_unidades=3)
        app_fj.agregar_servicio(lote_portatiles)
    except ErrorSistemaFJ as err_srv:
        app_fj.bitacora.guardar_fallo("Creación SRV-02", err_srv)

    # Operación 7: Creación válida de Asesoría Especializada
    try:
        consultoria_seg = AsesoriaEspecializada("SRV-03", "Auditoría OWASP", 120000.0, especialidad="Ciberseguridad", es_senior=True)
        app_fj.agregar_servicio(consultoria_seg)
    except ErrorSistemaFJ as err_srv:
        app_fj.bitacora.guardar_fallo("Creación SRV-03", err_srv)

    # Operación 8: Creación inválida de Sala con tarifa negativa (DatoInvalidoError)
    try:
        sala_invalida = ReservaSala("SRV-ERR1", "Sala Fantasma", -50000.0, aforo_maximo=10)
        app_fj.agregar_servicio(sala_invalida)
    except ErrorSistemaFJ as err_srv:
        print(f"  [X] Error controlado al crear sala inválida: {err_srv}")
        app_fj.bitacora.guardar_fallo("Creación SRV-ERR1", err_srv)

    # Operación 9: Creación inválida de Equipo con categoría inexistente (DatoInvalidoError)
    try:
        equipo_invalido = AlquilerEquipo("SRV-ERR2", "Servidor Cuántico", 90000.0, categoria_hw="ULTRA_MEGA", num_unidades=1)
        app_fj.agregar_servicio(equipo_invalido)
    except ErrorSistemaFJ as err_srv:
        print(f"  [X] Error controlado al crear equipo inválido: {err_srv}")
        app_fj.bitacora.guardar_fallo("Creación SRV-ERR2", err_srv)

  
    #3: Gestión de reservas y sobrecargas de calculos
    
    print("\n--- 3. PROCESAMIENTO DE RESERVAS (EXITOSAS Y FALLIDAS) ---")
    # Obtenemos los dos clientes válidos registrados en memoria
    primer_cliente = app_fj.lista_clientes[0]
    segundo_cliente = app_fj.lista_clientes[1]

    # Operación 10: Reserva exitosa usando tarifa estándar con IVA 19%
    reserva_uno = app_fj.procesar_nueva_reserva("RES-01", primer_cliente, sala_conferencias, duracion=3)

    # Operación 11: Reserva fallida al intentar reservar la sala ya ocupada (ServicioNoDisponibleError)
    app_fj.procesar_nueva_reserva("RES-02", segundo_cliente, sala_conferencias, duracion=2)

    # Operación 12: Reserva exitosa aplicando sobrecarga con descuento (15%) y cargo extra ($20,000)
    app_fj.procesar_nueva_reserva(
        "RES-03", segundo_cliente, consultoria_seg, duracion=4, descuento=0.15, recargo=20000.0
    )

    # Operación 13: Reserva fallida por descuento inconsistente del 95% (CalculoInconsistenteError)
    app_fj.procesar_nueva_reserva(
        "RES-04", primer_cliente, lote_portatiles, duracion=2, descuento=0.95
    )


  
    # 4: Cancelación y Control de Estados

    print("\n--- 4. CANCELACIÓN Y CONTROL DE ESTADOS ---")
    # Operación 14: Cancelación válida de RES-01 y prueba de error al intentar anularla dos veces
    try:
        # Anulamos la reserva 1 y verificamos que la sala vuelve a quedar disponible
        reserva_uno.anular_reserva("Cambio de cronograma del cliente")
        print(f"  [OK] Reserva {reserva_uno.codigo_unico} cancelada. Sala disponible nuevamente: {sala_conferencias.activo}")
        app_fj.bitacora.guardar_registro("INFO", f"Reserva {reserva_uno.codigo_unico} cancelada por el usuario.")
        # Intentamos cancelar por segunda vez para comprobar que lanza ReservaInvalidaError
        reserva_uno.anular_reserva("Segundo intento de cancelación")
    except ErrorSistemaFJ as err_cancel:
        print(f"  [X] Operación no permitida detectada: {err_cancel}")
        app_fj.bitacora.guardar_fallo("Cancelación duplicada RES-01", err_cancel)


    # Resumen Final del Sistema
    
    print("\n" + "=" * 80)
    print(f" EJECUCIÓN FINALIZADA SIN INTERRUPCIONES")
    print(f" Clientes activos: {len(app_fj.lista_clientes)} | Servicios catálogo: {len(app_fj.catalogo_servicios)} | Reservas válidas: {len(app_fj.historial_reservas)}")
    print(" Todas las trazas y errores fueron almacenados en 'auditoria_software_fj.log'.")
    print("=" * 80)
    # Guardamos el cierre limpio de la simulación en el log
    app_fj.bitacora.guardar_registro("INFO", "=== FIN DE SIMULACIÓN EXITOSA ===")


# Punto de entrada principal del script
if __name__ == "__main__":
    iniciar_pruebas_sistema()
