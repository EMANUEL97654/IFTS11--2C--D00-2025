class Peluqueria:
    def __init__(self, nombre, direccion, telefono):
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.turnos = []

    def agregar_turno(self, turno):
        self.turnos.append(turno)

    def buscar_turno(self, fecha, hora):
        for turno in self.turnos:
            if turno.fecha == fecha and turno.hora == hora:
                return turno
        return "No se encontro el turno"

    def eliminar_turno(self, turno):
        self.turnos.remove(turno)

    def listar_turnos(self):
        for turno in self.turnos:
            print(turno)

class Turno:
    def __init__(self, fecha, hora, cliente):
        self.fecha = fecha
        self.hora = hora
        self.cliente = cliente

    def __str__(self):
        return f"Turno para el {self.fecha} a las {self.hora} para {self.cliente}"
#Ejemplo de uso
peluqueria = Peluqueria("Peluqueria XYZ", "Av. Siempre Viva 123", "123456789")
turno1 = Turno("2022-01-01", "10:00", "Juan Perez")
turno2 = Turno("2022-01-01", "11:00", "Ana Gomez")
peluqueria.agregar_turno(turno1)
peluqueria.agregar_turno(turno2)
peluqueria.listar_turnos()
peluqueria.eliminar_turno(turno1)
peluqueria.listar_turnos()
print(peluqueria.buscar_turno("2022-01-01", "11:00"))
print(peluqueria.buscar_turno("2022-01-01", "10:00"))
