# excepciones.py

# Define la excepción base de la aplicación, heredando de la clase estándar 'Exception'
class ErrorSistemaFJ(Exception):
    """Clase base para todas las excepciones personalizadas del sistema Software FJ."""
    # Indica que la clase no necesita métodos ni atributos adicionales por ahora.
    pass


# Define un error específico para datos mal formateados, heredando de la excepción base 'ErrorSistemaFJ'.
class DatoInvalidoError(ErrorSistemaFJ):
    """Se lanza cuando un dato ingresado no cumple con el formato o reglas esperadas."""
    # Mantiene la implementación vacía heredando todo el comportamiento de su clase padre.
    pass


# Define un error específico para argumentos ausentes o nulos, heredando de 'ErrorSistemaFJ'.
class ParametroFaltanteError(ErrorSistemaFJ):
    """Se lanza cuando un argumento u obligatorio requerido llega vacío o nulo."""
    # Mantiene la estructura mínima requerida por la sintaxis de Python para definir la clase.
    pass


# Define un error para servicios inactivos u ocupados, heredando de 'ErrorSistemaFJ'.
class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando se intenta operar con un servicio que está inactivo u ocupado."""
    # No requiere lógica interna extra; su nombre descriptivo aporta todo el contexto necesario.
    pass


# Define un error para fallos de estado o flujo en reservas, heredando de 'ErrorSistemaFJ'.
class ReservaInvalidaError(ErrorSistemaFJ):
    """Se lanza cuando hay una inconsistencia en el proceso o estado de una reserva."""
    # Indica explícitamente que el bloque de la clase está completo sin agregar código adicional.
    pass


# Define un error para fallos matemáticos o de rangos en tarifas, heredando de 'ErrorSistemaFJ'.
class CalculoInconsistenteError(ErrorSistemaFJ):
    """Se lanza cuando ocurre un error matemático o de rangos en los cálculos de tarifas."""
    # Cierra la definición de la clase utilizando la estructura estándar de excepciones personalizadas.
    pass
