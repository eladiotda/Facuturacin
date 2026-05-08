class ValidationError(Exception):
    """Error de validacion de datos de entrada."""


class ConflictError(Exception):
    """Error por conflicto de datos unicos."""


class NotFoundError(Exception):
    """Error cuando un recurso requerido no existe."""
