# modelos.py

# Importamos ABC y abstractmethod para construir clases y métodos abstractos
from abc import ABC, abstractmethod
# Importamos el módulo re para validar expresiones regulares en correos electrónicos
import re
# Importamos nuestras excepciones personalizadas desde excepciones.py
from excepciones import (
    DatoInvalidoError,
    ParametroFaltanteError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    CalculoInconsistenteError,
)



# 1. Clase Aabstracta Base del Sistema

class EntidadBase(ABC):
    """Clase abstracta que representa cualquier entidad general dentro de Software FJ."""

    def __init__(self, codigo_unico: str):
        # Asignamos el código mediante el setter para validarlo desde el momento de creación
        self.codigo_unico = codigo_unico

    @property
    def codigo_unico(self) -> str:
        # Retorna el atributo privado __codigo_unico aplicando encapsulación
        return self.__codigo_unico

    @codigo_unico.setter
    def codigo_unico(self, dato_entrada: str) -> None:
        # Comprobamos que el código no sea nulo, sea texto y no contenga solo espacios
        if not dato_entrada or not isinstance(dato_entrada, str) or not dato_entrada.strip():
            # Si no cumple, lanzamos nuestra excepción de parámetro faltante
            raise ParametroFaltanteError("El código identificador de la entidad es obligatorio.")
        # Guardamos el código limpio y en mayúsculas
        self.__codigo_unico = dato_entrada.strip().upper()

    @abstractmethod
    def mostrar_ficha(self) -> str:
        # Método abstracto que obliga a las clases hijas a devolver su resumen en texto
        pass



# 2. Clase Cliente 

class Cliente(EntidadBase):
    """Representa a un cliente de Software FJ con validación estricta de datos personales."""

    def __init__(self, codigo_cliente: str, nombre_completo: str, email: str, celular: str):
        # Invocamos el constructor de EntidadBase para validar el código del cliente
        super().__init__(codigo_cliente)
        # Asignamos los datos personales pasando por cada setter encapsulado
        self.nombre_completo = nombre_completo
        self.email = email
        self.celular = celular

    @property
    def nombre_completo(self) -> str:
        # Devuelve el nombre privado del cliente
        return self.__nombre_completo

    @nombre_completo.setter
    def nombre_completo(self, texto_nombre: str) -> None:
        # Validamos que el nombre no llegue vacío
        if not texto_nombre or not texto_nombre.strip():
            raise ParametroFaltanteError("El nombre del cliente no puede quedar vacío.")
        # Verificamos que tenga al menos 3 letras para evitar nombres incompletos
        if len(texto_nombre.strip()) < 3:
            raise DatoInvalidoError(f"El nombre '{texto_nombre}' es muy corto (mínimo 3 caracteres).")
        # Guardamos el nombre sin espacios adicionales
        self.__nombre_completo = texto_nombre.strip()

    @property
    def email(self) -> str:
        # Devuelve el correo electrónico privado
        return self.__email

    @email.setter
    def email(self, texto_email: str) -> None:
        # Validamos que el correo haya sido ingresado
        if not texto_email or not texto_email.strip():
            raise ParametroFaltanteError("El correo electrónico del cliente es obligatorio.")
        # Expresión regular para comprobar estructura válida usuario@dominio.com
        expresion_email = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        # Si el texto no cumple con la expresión regular, lanzamos DatoInvalidoError
        if not re.match(expresion_email, texto_email.strip()):
            raise DatoInvalidoError(f"El formato del correo '{texto_email}' no es válido.")
        # Guardamos el correo en minúsculas
        self.__email = texto_email.strip().lower()

    @property
    def celular(self) -> str:
        # Devuelve el número celular privado
        return self.__celular

    @celular.setter
    def celular(self, numero_contacto: str) -> None:
        # Validamos que el teléfono no sea vacío
        if not numero_contacto or not numero_contacto.strip():
            raise ParametroFaltanteError("El número telefónico es obligatorio.")
        # Verificamos que sean solo números y tengan mínimo 7 dígitos
        if not numero_contacto.strip().isdigit() or len(numero_contacto.strip()) < 7:
            raise DatoInvalidoError(f"El teléfono '{numero_contacto}' debe tener al menos 7 dígitos numéricos.")
        # Guardamos el número limpio
        self.__celular = numero_contacto.strip()

    def mostrar_ficha(self) -> str:
        # Implementamos el método abstracto heredado de EntidadBase
        return f"Cliente [{self.codigo_unico}]: {self.nombre_completo} | Correo: {self.email} | Cel: {self.celular}"



# 3. Clase abstracta y servicios con sus 3 clases derivadas

class Servicio(EntidadBase, ABC):
    """Clase abstracta que define el contrato base para los servicios de Software FJ."""

    def __init__(self, codigo_servicio: str, titulo_servicio: str, valor_hora: float, activo: bool = True):
        # Llamamos al constructor padre para validar el código del servicio
        super().__init__(codigo_servicio)
        # Inicializamos los atributos del servicio mediante sus setters
        self.titulo_servicio = titulo_servicio
        self.valor_hora = valor_hora
        self.activo = activo
        # Ejecutamos la validación especializada de cada clase hija
        self.verificar_reglas()

    @property
    def titulo_servicio(self) -> str:
        # Devuelve el nombre privado del servicio
        return self.__titulo_servicio

    @titulo_servicio.setter
    def titulo_servicio(self, texto_titulo: str) -> None:
        # Validamos que el título no esté vacío
        if not texto_titulo or not texto_titulo.strip():
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        # Guardamos el título limpio
        self.__titulo_servicio = texto_titulo.strip()

    @property
    def valor_hora(self) -> float:
        # Devuelve la tarifa por hora encapsulada
        return self.__valor_hora

    @valor_hora.setter
    def valor_hora(self, monto_tarifa: float) -> None:
        # Intentamos convertir el dato recibido a número decimal (float)
        try:
            precio_convertido = float(monto_tarifa)
        except (TypeError, ValueError) as fallo_conversion:
            # Encadenamiento de excepciones conservando la excepción original
            raise DatoInvalidoError(f"La tarifa '{monto_tarifa}' debe ser un número válido.") from fallo_conversion

        # Comprobamos que la tarifa sea estrictamente mayor que cero
        if precio_convertido <= 0:
            raise DatoInvalidoError(f"La tarifa por hora debe ser positiva (recibido: {precio_convertido}).")
        # Guardamos la tarifa validada
        self.__valor_hora = precio_convertido

    @property
    def activo(self) -> bool:
        # Devuelve True si el servicio está libre para reservar
        return self.__activo

    @activo.setter
    def activo(self, bandera_estado: bool) -> None:
        # Validamos que el estado sea estrictamente booleano
        if not isinstance(bandera_estado, bool):
            raise DatoInvalidoError("La disponibilidad debe ser un valor booleano (True/False).")
        # Actualizamos el estado de disponibilidad
        self.__activo = bandera_estado

    @abstractmethod
    def calcular_tarifa_base(self, cantidad_horas: int) -> float:
        # Método abstracto que cada servicio hijo implementará con su propia fórmula
        pass

    @abstractmethod
    def obtener_detalle_tecnico(self) -> str:
        # Método abstracto que cada servicio hijo sobrescribirá para describirse
        pass

    @abstractmethod
    def verificar_reglas(self) -> None:
        # Método abstracto para validar las condiciones propias de cada servicio
        pass

    # --- MÉTODO SOBRECARGADO (Variantes con impuestos, descuentos y recargos opcionales) ---
    def liquidar_costo_final(
        self,
        cantidad_horas: int,
        porcentaje_iva: float = 0.19,
        tasa_descuento: float = 0.0,
        cargo_extra: float = 0.0
    ) -> float:
        # Validamos que las horas sean un entero mayor a cero
        if not isinstance(cantidad_horas, int) or cantidad_horas <= 0:
            raise ReservaInvalidaError("La cantidad de horas debe ser un número entero positivo.")
        # Validamos que el descuento esté entre 0% y 80%
        if not (0 <= tasa_descuento <= 0.80):
            raise CalculoInconsistenteError("El porcentaje de descuento debe estar entre 0.0 y 0.80.")
        # Verificamos que ni el IVA ni los cargos extra sean negativos
        if porcentaje_iva < 0 or cargo_extra < 0:
            raise CalculoInconsistenteError("Los impuestos y cargos adicionales no pueden ser negativos.")

        # Calculamos el valor base llamando al método polimórfico calcular_tarifa_base
        valor_bruto = self.calcular_tarifa_base(cantidad_horas)
        # Calculamos cuánto dinero se descuenta
        valor_rebaja = valor_bruto * tasa_descuento
        # Calculamos el subtotal antes de impuestos
        subtotal_neto = valor_bruto - valor_rebaja + cargo_extra

        # Verificamos que el subtotal neto sea mayor a cero
        if subtotal_neto <= 0:
            raise CalculoInconsistenteError("El subtotal calculado no puede ser menor o igual a cero.")

        # Sumamos el IVA correspondiente
        monto_final = subtotal_neto * (1 + porcentaje_iva)
        # Retornamos el total redondeado a dos decimales
        return round(monto_final, 2)

    def mostrar_ficha(self) -> str:
        # Traducimos el estado booleano a una etiqueta clara
        etiqueta_disponibilidad = "Disponible" if self.activo else "Ocupado"
        # Retornamos el resumen del servicio
        return f"[{self.codigo_unico}] {self.titulo_servicio} (${self.valor_hora:,.2f}/h) - {etiqueta_disponibilidad}"


class ReservaSala(Servicio):
    """Servicio especializado 1: Alquiler de salas de juntas, auditorios o laboratorios."""

    def __init__(self, codigo_servicio: str, titulo_servicio: str, valor_hora: float, aforo_maximo: int, incluye_proyector: bool = True, activo: bool = True):
        # Guardamos el aforo y si incluye proyector antes de llamar a super().__init__
        self.__aforo_maximo = aforo_maximo
        self.__incluye_proyector = incluye_proyector
        # Invocamos al constructor de la clase padre Servicio
        super().__init__(codigo_servicio, titulo_servicio, valor_hora, activo)

    def verificar_reglas(self) -> None:
        # Validamos que el aforo esté entre 2 y 200 personas
        if not isinstance(self.__aforo_maximo, int) or self.__aforo_maximo < 2 or self.__aforo_maximo > 200:
            raise DatoInvalidoError(f"Aforo inválido ({self.__aforo_maximo}). Debe estar entre 2 y 200 personas.")

    def calcular_tarifa_base(self, cantidad_horas: int) -> float:
        # Si incluye proyector, se cobra un cargo fijo de $15,000 COP por uso del equipo
        costo_proyector = 15000.0 if self.__incluye_proyector else 0.0
        # Retornamos tarifa por horas más el costo del proyector
        return (self.valor_hora * cantidad_horas) + costo_proyector

    def obtener_detalle_tecnico(self) -> str:
        # Definimos texto descriptivo del proyector
        texto_equipo = "con Proyector HD" if self.__incluye_proyector else "sin equipo audiovisual"
        # Retornamos la ficha técnica de la sala
        return f"Sala '{self.titulo_servicio}' | Aforo: {self.__aforo_maximo} personas ({texto_equipo})."


class AlquilerEquipo(Servicio):
    """Servicio especializado 2: Préstamo de estaciones de trabajo, servidores o portátiles."""

    def __init__(self, codigo_servicio: str, titulo_servicio: str, valor_hora: float, categoria_hw: str, num_unidades: int, activo: bool = True):
        # Guardamos la categoría del hardware y la cantidad de unidades
        self.__categoria_hw = categoria_hw
        self.__num_unidades = num_unidades
        # Invocamos al constructor padre
        super().__init__(codigo_servicio, titulo_servicio, valor_hora, activo)

    def verificar_reglas(self) -> None:
        # Definimos las categorías de hardware permitidas en el sistema
        categorias_permitidas = ("ESTANDAR", "ALTA", "SERVIDOR")
        # Validamos que la categoría esté dentro de las permitidas
        if not self.__categoria_hw or self.__categoria_hw.upper() not in categorias_permitidas:
            raise DatoInvalidoError(f"Categoría inválida: '{self.__categoria_hw}'. Permitidas: {categorias_permitidas}.")
        # Validamos que se solicite al menos 1 equipo
        if not isinstance(self.__num_unidades, int) or self.__num_unidades <= 0:
            raise DatoInvalidoError("La cantidad de equipos debe ser mayor o igual a 1.")

    def calcular_tarifa_base(self, cantidad_horas: int) -> float:
        # Tabla de multiplicadores según la potencia del hardware
        multiplicadores_hw = {"ESTANDAR": 1.0, "ALTA": 1.35, "SERVIDOR": 1.8}
        # Obtenemos el factor correspondiente
        coeficiente = multiplicadores_hw[self.__categoria_hw.upper()]
        # Calculamos el costo multiplicando tarifa, horas, unidades y coeficiente
        return self.valor_hora * cantidad_horas * self.__num_unidades * coeficiente

    def obtener_detalle_tecnico(self) -> str:
        # Retornamos los datos técnicos del lote de hardware
        return f"Alquiler Equipos '{self.titulo_servicio}' | Categoría: {self.__categoria_hw.upper()} | Cantidad: {self.__num_unidades}."


class AsesoriaEspecializada(Servicio):
    """Servicio especializado 3: Consultoría en arquitectura de software, redes o ciberseguridad."""

    def __init__(self, codigo_servicio: str, titulo_servicio: str, valor_hora: float, especialidad: str, es_senior: bool = True, activo: bool = True):
        # Guardamos la especialidad técnica y el nivel del consultor
        self.__especialidad = especialidad
        self.__es_senior = es_senior
        # Inicializamos la clase base Servicio
        super().__init__(codigo_servicio, titulo_servicio, valor_hora, activo)

    def verificar_reglas(self) -> None:
        # Comprobamos que la especialidad tenga al menos 4 caracteres
        if not self.__especialidad or len(self.__especialidad.strip()) < 4:
            raise ParametroFaltanteError("Debe indicar una especialidad técnica válida para la asesoría.")

    def calcular_tarifa_base(self, cantidad_horas: int) -> float:
        # Si el consultor es Senior se aplica un recargo del 40% sobre la tarifa base
        factor_experiencia = 1.40 if self.__es_senior else 1.0
        # Retornamos el costo total de la consultoría
        return self.valor_hora * cantidad_horas * factor_experiencia

    def obtener_detalle_tecnico(self) -> str:
        # Etiqueta del perfil del ingeniero asignado
        perfil_consultor = "Ingeniero Senior" if self.__es_senior else "Ingeniero Semi-Senior"
        # Retornamos el detalle de la consultoría
        return f"Asesoría en {self.__especialidad} ({perfil_consultor}) - {self.titulo_servicio}."



# 4. Clase Reserva

class Reserva(EntidadBase):
    """Integra Cliente, Servicio, duración y ciclo de vida (PENDIENTE, CONFIRMADA, CANCELADA)."""

    def __init__(self, codigo_reserva: str, obj_cliente: Cliente, obj_servicio: Servicio, horas_reservadas: int):
        # Validamos el código de la reserva en EntidadBase
        super().__init__(codigo_reserva)
        # Verificamos que obj_cliente sea una instancia válida de Cliente
        if not isinstance(obj_cliente, Cliente):
            raise DatoInvalidoError("La reserva requiere un objeto Cliente válido.")
        # Verificamos que obj_servicio sea una instancia válida de Servicio
        if not isinstance(obj_servicio, Servicio):
            raise DatoInvalidoError("La reserva requiere un objeto Servicio válido.")
        # Comprobamos que el servicio esté disponible en el momento
        if not obj_servicio.activo:
            raise ServicioNoDisponibleError(
                f"El servicio '{obj_servicio.titulo_servicio}' ({obj_servicio.codigo_unico}) no está disponible."
            )
        # Validamos que la duración esté entre 1 y 24 horas
        if not isinstance(horas_reservadas, int) or horas_reservadas < 1 or horas_reservadas > 24:
            raise ReservaInvalidaError("Las horas reservadas deben estar entre 1 y 24.")

        # Encapsulamos los atributos internos de la reserva
        self.__obj_cliente = obj_cliente
        self.__obj_servicio = obj_servicio
        self.__horas_reservadas = horas_reservadas
        self.__estado_actual = "PENDIENTE"
        self.__valor_total_pagar = 0.0

    @property
    def estado_actual(self) -> str:
        # Retorna el estado en que se encuentra la reserva
        return self.__estado_actual

    @property
    def valor_total_pagar(self) -> float:
        # Retorna el total liquidado con impuestos
        return self.__valor_total_pagar

    def confirmar_reserva(self, descuento_aplicado: float = 0.0, recargo_aplicado: float = 0.0) -> float:
        # Impedimos confirmar una reserva que ya fue cancelada
        if self.__estado_actual == "CANCELADA":
            raise ReservaInvalidaError(f"La reserva {self.codigo_unico} fue cancelada y no puede confirmarse.")
        # Impedimos confirmar nuevamente una reserva ya confirmada
        if self.__estado_actual == "CONFIRMADA":
            raise ReservaInvalidaError(f"La reserva {self.codigo_unico} ya se encuentra confirmada.")

        # Calculamos el monto total usando el método sobrecargado del servicio
        self.__valor_total_pagar = self.__obj_servicio.liquidar_costo_final(
            cantidad_horas=self.__horas_reservadas,
            tasa_descuento=descuento_aplicado,
            cargo_extra=recargo_aplicado
        )
        # Actualizamos el estado a CONFIRMADA
        self.__estado_actual = "CONFIRMADA"
        # Cambiamos la disponibilidad del servicio a False para bloquear cruces
        self.__obj_servicio.activo = False
        # Retornamos el valor total a pagar
        return self.__valor_total_pagar

    def anular_reserva(self, razon_cancelacion: str) -> None:
        # Exigimos un motivo no vacío para poder anular la reserva
        if not razon_cancelacion or not razon_cancelacion.strip():
            raise ParametroFaltanteError("Debe registrar una razón válida para cancelar la reserva.")
        # Evitamos cancelar una reserva que ya estaba anulada
        if self.__estado_actual == "CANCELADA":
            raise ReservaInvalidaError(f"La reserva {self.codigo_unico} ya había sido cancelada anteriormente.")

        # Cambiamos el estado a CANCELADA
        self.__estado_actual = "CANCELADA"
        # Volvemos a habilitar el servicio para futuros clientes
        self.__obj_servicio.activo = True

    def mostrar_ficha(self) -> str:
        # Retornamos el resumen completo de la reserva
        return (
            f"Reserva [{self.codigo_unico}] | Estado: {self.__estado_actual} | "
            f"Cliente: {self.__obj_cliente.nombre_completo} | Servicio: {self.__obj_servicio.titulo_servicio} "
            f"({self.__horas_reservadas}h) | Total con IVA: ${self.__valor_total_pagar:,.2f}"
        )
