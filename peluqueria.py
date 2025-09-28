import uuid
from datetime import datetime, timedelta

class Cliente:
    def __init__(self, nombre, telefono, email=""):
        self.id = uuid.uuid4() 
        self.nombre = nombre
        self.telefono = telefono
        self.email = email

    def __str__(self):
        return f"Cliente: {self.nombre} (Tel: {self.telefono})"

class Servicio:
    def __init__(self, nombre, duracion_minutos: int, precio: float):
        self.id = uuid.uuid4() 
        if duracion_minutos <= 0:
            raise ValueError("La duración del servicio debe ser positiva.")
        self.nombre = nombre
        self.duracion_minutos = duracion_minutos
        self.precio = precio

    def __str__(self):
        return f"Servicio: {self.nombre} ({self.duracion_minutos} min, ${self.precio})"

class Barbero:
    def __init__(self, nombre: str, especialidad: str):
        self.id = uuid.uuid4() 
        self.nombre = nombre
        self.especialidad = especialidad
        
    def __str__(self):
        return f"Barbero: {self.nombre} ({self.especialidad})"

class Turno:
    def __init__(self, dt_inicio: datetime, cliente: Cliente, servicio: Servicio, barbero: Barbero):
        self.id = uuid.uuid4() 
        self.dt_inicio = dt_inicio
        self.cliente = cliente
        self.servicio = servicio
        self.barbero = barbero 
        
        
        self.dt_fin = self.dt_inicio + timedelta(minutes=servicio.duracion_minutos) 

    def __str__(self):
        fecha_str = self.dt_inicio.strftime("%Y-%m-%d")
        hora_inicio_str = self.dt_inicio.strftime("%H:%M")
        hora_fin_str = self.dt_fin.strftime("%H:%M")
        
        return (f"Turno ID: {self.id.hex[:6]} | {fecha_str} de {hora_inicio_str} a {hora_fin_str} | "
                f"{self.cliente.nombre} | Serv: {self.servicio.nombre} | Barb: {self.barbero.nombre}")

class Peluqueria:
    def __init__(self, nombre, direccion, telefono, horario_apertura: str = "09:00", horario_cierre: str = "18:00"):
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.turnos = []
        
        
        self.horario_apertura = datetime.strptime(horario_apertura, "%H:%M").time()
        self.horario_cierre = datetime.strptime(horario_cierre, "%H:%M").time()

    def _verificar_horario_operacion(self, nuevo_turno: Turno) -> bool:
        """Verifica si el turno está dentro del horario de apertura/cierre."""
   
        if nuevo_turno.dt_inicio.time() < self.horario_apertura:
            print(f"El turno inicia antes de la hora de apertura ({self.horario_apertura.strftime('%H:%M')}).")
            return False
        
        # Comprobar fin
        if nuevo_turno.dt_fin.time() > self.horario_cierre:
            print(f"El turno termina después de la hora de cierre ({self.horario_cierre.strftime('%H:%M')}).")
            return False
            
        return True

    def _verificar_disponibilidad_general(self, nuevo_turno: Turno) -> bool:
        """Verifica la superposición de tiempo y barbero."""
        
        for turno_existente in self.turnos:
            if nuevo_turno.barbero.id == turno_existente.barbero.id:
                if (nuevo_turno.dt_inicio < turno_existente.dt_fin and 
                    nuevo_turno.dt_fin > turno_existente.dt_inicio):
                    
                    print(f"El barbero {nuevo_turno.barbero.nombre} ya está ocupado en ese horario.")
                    return False  
        return True 

    def agregar_turno(self, turno: Turno):
        
        if not self._verificar_horario_operacion(turno):
            return 
            
        if self._verificar_disponibilidad_general(turno):
            self.turnos.append(turno)
            self.turnos.sort(key=lambda t: t.dt_inicio)
            print(f"Turno agregado exitosamente para {turno.cliente.nombre} con {turno.barbero.nombre} a las {turno.dt_inicio.strftime('%H:%M')}.")
        else:
            print("No se pudo agregar el turno por conflicto de horario/barbero.")

    def buscar_turno(self, id_o_datetime):
        """Busca por UUID (preferido) o por datetime de inicio."""
        if isinstance(id_o_datetime, uuid.UUID):
            for turno in self.turnos:
                if turno.id == id_o_datetime:
                    return turno
        elif isinstance(id_o_datetime, datetime):
            for turno in self.turnos:
                if turno.dt_inicio == id_o_datetime:
                    return turno
        
        return "No se encontró el turno"

    def eliminar_turno(self, turno):
        """Elimina un turno usando el objeto Turno o su UUID."""
        try:
            if isinstance(turno, Turno):
                self.turnos.remove(turno)
            elif isinstance(turno, uuid.UUID):
                t = self.buscar_turno(turno)
                if isinstance(t, Turno):
                    self.turnos.remove(t)
                else:
                    print(f"No se pudo eliminar: {t}")
                    return
            print(f"Turno eliminado exitosamente: {turno}")
        except ValueError:
            print("Error: El turno no se encontró en la lista.")


    def listar_turnos(self):
        if not self.turnos:
            print("(No hay turnos agendados.)")
            return
        for turno in self.turnos:
            print(turno)


print("--- Inicialización ---")
peluqueria = Peluqueria("The Clipper's Den", "Av. Siempre Viva 123", "123456789", 
                    horario_apertura="09:00", horario_cierre="17:00") 

# Clientes
juan = Cliente("Juan Perez", "555-1234")
ana = Cliente("Ana Gomez", "555-5678")

# Barberos
pepe = Barbero("Pepe Cortes", "Estilista")
maria = Barbero("Maria Tijeras", "Barbería Clásica")

# Servicios
corte_45 = Servicio("Corte de Pelo", 45, 25.00) 
barba_30 = Servicio("Arreglo de Barba", 30, 15.00) 
tinte_120 = Servicio("Tinte y Corte", 120, 80.00) 

print("\n--- Agendando Turnos Base (2025-10-20) ---")

dt1_pepe = datetime(2025, 10, 20, 10, 0) 
turno1 = Turno(dt1_pepe, juan, corte_45, pepe) 
peluqueria.agregar_turno(turno1)

dt2_maria = datetime(2025, 10, 20, 10, 30) 
turno2 = Turno(dt2_maria, ana, barba_30, maria) 
peluqueria.agregar_turno(turno2)

print("\n--- Pruebas de Validación ---")

# 1. 💡 Prueba de superposición de Barbero (Pepe)
dt_superpuesto_pepe = datetime(2025, 10, 20, 10, 15) 
turno_conflicto_pepe = Turno(dt_superpuesto_pepe, ana, corte_45, pepe) 
print("Intento 1 (Conflicto de Pepe):")
peluqueria.agregar_turno(turno_conflicto_pepe) 

# 2. 💡 Prueba de horario de cierre
dt_tarde = datetime(2025, 10, 20, 16, 0) 
turno_tarde = Turno(dt_tarde, juan, tinte_120, maria)
print("\nIntento 2 (Fuera de horario):")
peluqueria.agregar_turno(turno_tarde) 

dt_valido = datetime(2025, 10, 20, 13, 0)
turno_valido = Turno(dt_valido, ana, corte_45, pepe) 
print("\nIntento 3 (Turno Válido):")
peluqueria.agregar_turno(turno_valido)

print("\n--- Listado Final de Turnos ---")
peluqueria.listar_turnos()

print("\n--- Búsqueda y Eliminación por ID ---")
turno_a_eliminar = peluqueria.buscar_turno(dt1_pepe) 
if isinstance(turno_a_eliminar, Turno):
    peluqueria.eliminar_turno(turno_a_eliminar.id) 
else:
    print(turno_a_eliminar)

print("\n--- Listado después de eliminación ---")
peluqueria.listar_turnos()