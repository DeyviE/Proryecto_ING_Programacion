class Prestamo:
    def __init__(self, id, libro_id, usuario_id, fecha_prestamo, fecha_devolucion=None):
        self.id = id
        self.libro_id = libro_id
        self.usuario_id = usuario_id
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion
