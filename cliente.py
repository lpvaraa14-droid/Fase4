import logging
from abc import ABC, abstractmethod
from datetime import datetime

# =====================================================================
# CONFIGURACIÓN DEL SISTEMA DE LOGS
# =====================================================================
# Configura el archivo 'sistema_fj.log' para registrar automáticamente 
# todos los eventos informativos (INFO) y errores (ERROR) del sistema.
logging.basicConfig(
    filename='sistema_fj.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# =====================================================================
# EXCEPCIONES PERSONALIZADAS Y ENCADENAMIENTO
# =====================================================================

class ErrorSistemaFJ(Exception):
    """
    Excepción base para todos los errores controlados del sistema Software FJ.
    Permite agrupar cualquier fallo específico del dominio de la empresa[cite: 1].
    """
    pass


class ClienteInvalidoError(ErrorSistemaFJ):
    """
    Excepción lanzada específicamente cuando los datos personales o 
    parámetros de un cliente no cumplen con las validaciones estrictas.
    """
    pass


class ServicioInvalidoError(ErrorSistemaFJ):
    """
    Excepción lanzada cuando la creación de un servicio falla o 
    contiene parámetros incorrectos (ej. costos negativos).
    """
    pass


class ReservaInvalidaError(ErrorSistemaFJ):
    """
    Excepción lanzada cuando ocurre un error durante el proceso de 
    creación, cálculo, confirmación o cancelación de una reserva[cite: 2].
    """
    pass

# =====================================================================
# CLASE ABSTRACTA BASE
# =====================================================================

class EntidadBase(ABC):
    """
    Clase abstracta que representa entidades generales del sistema Software FJ.
    Establece un contrato estructural obligatorio para las clases hijas[cite: 1, 2].
    """
    
    def __init__(self, identificador):
        # Inicializa el identificador único de la entidad
        self._identificador = identificador

    @property
    def identificador(self):
        """Propiedad de solo lectura para obtener el identificador."""
        return self._identificador

    @abstractmethod
    def obtener_detalles(self):
        """
        Método abstracto obligatorio. 
        Cada clase derivada debe implementar su propia lógica de presentación.
        """
        pass


# =====================================================================
# CLASE CLIENTE (Encapsulación y Validaciones Estrictas)
# =====================================================================

class Cliente(EntidadBase):
    """
    Clase que gestiona la información de los clientes de Software FJ,
    aplicando encapsulación y validaciones estrictas en sus atributos[cite: 1, 2].
    """
    
    def __init__(self, identificador, nombre, documento, email, telefono):
        # Hereda el identificador de EntidadBase
        super().__init__(identificador)
        # Se asignan los valores utilizando los setters para validar automáticamente
        self.nombre = nombre
        self.documento = documento
        self.email = email
        self.telefono = telefono

    # --- ENCAPSULACIÓN Y VALIDACIÓN DE NOMBRE ---
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        # Valida que el nombre no esté vacío, sea texto y tenga al menos 3 caracteres
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            logging.error(f"Intento de asignar nombre inválido: {valor}")
            raise ClienteInvalidoError("El nombre del cliente debe ser un texto válido de al menos 3 caracteres.")
        self.__nombre = valor.strip()

    # --- ENCAPSULACIÓN Y VALIDACIÓN DE DOCUMENTO ---
    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        # Valida que el documento contenga solo dígitos numéricos
        if not valor or not str(valor).isdigit() or len(str(valor)) < 6:
            logging.error(f"Intento de asignar documento inválido: {valor}")
            raise ClienteInvalidoError("El documento debe contener solo dígitos y tener al menos 6 caracteres.")
        self.__documento = str(valor)

    # --- ENCAPSULACIÓN Y VALIDACIÓN DE EMAIL ---
    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        # Valida una estructura básica de correo electrónico
        if not valor or "@" not in valor or "." not in valor:
            logging.error(f"Intento de asignar email inválido: {valor}")
            raise ClienteInvalidoError("El correo electrónico no tiene un formato válido.")
        self.__email = valor.strip()

    # --- ENCAPSULACIÓN Y VALIDACIÓN DE TELÉFONO ---
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        # Valida que el teléfono contenga al menos 7 dígitos numéricos
        if not valor or not str(valor).isdigit() or len(str(valor)) < 7:
            logging.error(f"Intento de asignar teléfono inválido: {valor}")
            raise ClienteInvalidoError("El teléfono debe contener al menos 7 dígitos numéricos.")
        self.__telefono = str(valor)

    def obtener_detalles(self):
        """Implementación del método abstracto para retornar los datos del cliente."""
        return f"Cliente: {self.__nombre} | Doc: {self.__documento} | Email: {self.__email} | Tel: {self.__telefono}"