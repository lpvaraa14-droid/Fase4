# excepciones.py

class ErrorSistemaFJ(Exception):
    """Clase base para todas las excepciones personalizadas del sistema Software FJ."""
    pass


class DatoInvalidoError(ErrorSistemaFJ):
    """Se lanza cuando un dato ingresado no cumple con el formato o reglas esperadas."""
    pass


class ParametroFaltanteError(ErrorSistemaFJ):
    """Se lanza cuando un argumento u obligatorio requerido llega vacío o nulo."""
    pass


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando se intenta operar con un servicio que está inactivo u ocupado."""
    pass


class ReservaInvalidaError(ErrorSistemaFJ):
    """Se lanza cuando hay una inconsistencia en el proceso o estado de una reserva."""
    pass


class CalculoInconsistenteError(ErrorSistemaFJ):
    """Se lanza cuando ocurre un error matemático o de rangos en los cálculos de tarifas."""
    pass