#Naomy Vaamondes, 7122, Sistema Avanzado de Gestión de Personal y Proyectos
class Empleado:

    contador_id = 1 #contador para los id
    
    def __init__(self, nombre, salario_base):
        self.__nombre = nombre
        self.__id_empleado = Empleado.contador_id
        Empleado.contador_id += 1
        self.__salario_base = salario_base
        self._proyectos_asignados = [] #lista para guardar los prityectos

    def get_nombre(self):
        return self.__nombre
    
    def get_id(self):
        return self.__id_empleado
    
    def get_salario_base(self):
        return self.__salario_base
    
    def get_num_proyectos(self):
        return len(self._proyectos_asignados)
    
    def calcular_salario(self):
        raise NotImplementedError("El metodo calcular_salario debe ser implementado por la subclase")
    
    def mostrar_informacion(self):
        salario = self.calcular_salario()
        print("Nombre " + self.__nombre) #concatenar con +
        print("ID " + str(self.__id_empleado))
        print("Salario " + str(salario)) #concateno con string

    def asignar_proyecto(self, proyecto):
        if not isinstance(self, Gerente):
            limite = self._get_limite_proyectos()
            if self.get_num_proyectos() >= limite:
                raise ValueError("Error El empleado " + self.__nombre + " excede su limite de " + str(limite) + " proyectos")
            if proyecto in self._proyectos_asignados:
                raise ValueError("Error El empleado " + self.__nombre + " ya esta asignado a este proyecto")
            self._proyectos_asignados.append(proyecto)
            print("Asignado " + self.__nombre + " al proyecto " + proyecto.get_nombre())
        else:
            raise ValueError("Error Los Gerentes no pueden ser asignados a proyectos como miembros")
        
    def _get_limite_proyectos(self):
        if isinstance(self, Desarrollador):
            return 3
        if isinstance(self, Diseñador):
            return 2
        return 0

class Desarrollador(Empleado):

    def __init__(self, nombre, salario_base, lenguajes, nivel):
        super().__init__(nombre, salario_base)
        self.lenguajes = lenguajes
        self.nivel = nivel

    def calcular_salario(self):
        salario = self.get_salario_base()
        bono = 0.0
        if self.nivel == "Junior":
            bono = 200.0
        elif self.nivel == "SemiSenior":
            bono = 500.0
        elif self.nivel == "Senior":
            bono = 1000.0
        return salario + bono

class Diseñador(Empleado):

    def __init__(self, nombre, salario_base, herramientas, especialidad):
        super().__init__(nombre, salario_base)
        self.herramientas = herramientas
        self.especialidad = especialidad

    def calcular_salario(self):
        salario = self.get_salario_base()
        bono = 0.0
        usa_figma = "Figma" in self.herramientas
        usa_photoshop_illustrator = any(h in self.herramientas for h in ["Photoshop", "Illustrator"])
        usa_solo_ph_il = (usa_photoshop_illustrator and not usa_figma and 
                          len(self.herramientas) <= 2 and all(h in ["Photoshop", "Illustrator"] for h in self.herramientas))
        if usa_figma:
            bono += 300.0
        elif usa_solo_ph_il:
            bono += 200.0
        if len(self.herramientas) >= 3:
            bono += 400.0
        return salario + bono

class Gerente(Empleado):

    def __init__(self, nombre, salario_base, departamento):
        super().__init__(nombre, salario_base)
        self.departamento = departamento
        self.equipo = []

    def calcular_salario(self):
        salario = self.get_salario_base()
        total_salarios_equipo = sum(emp.calcular_salario() for emp in self.equipo)
        bono = total_salarios_equipo * 0.15
        return salario + bono
    
    def mostrar_informacion(self):
        super().mostrar_informacion()
        print("Departamento " + self.departamento)
        nombres_equipo = [emp.get_nombre() for emp in self.equipo]
        print("Equipo " + str(nombres_equipo))

    def agregar_al_equipo(self, empleado):
        if isinstance(empleado, (Desarrollador, Diseñador)):
            self.equipo.append(empleado)
            print("Agregado " + empleado.get_nombre() + " al equipo de " + self.get_nombre())
        else:
            print("Error Solo Desarrolladores o Diseñadores pueden ser agregados al equipo de un Gerente")

    def asignar_proyecto(self, proyecto):
        raise ValueError("Error Los Gerentes no pueden ser asignados a proyectos como miembros")

class Proyecto:

    def __init__(self, nombre, presupuesto):
        self.__nombre = nombre
        self.__presupuesto = presupuesto
        self.empleados = []

    def get_nombre(self):
        return self.__nombre
    
    def get_presupuesto(self):
        return self.__presupuesto
    
    def agregar_empleado(self, empleado):
        try:
            empleado.asignar_proyecto(self)
            self.empleados.append(empleado)
        except ValueError as e:
            print(e)

    def costo_total(self):
        return sum(emp.calcular_salario() for emp in self.empleados)
    
    def viabilidad(self):
        costo = self.costo_total()
        viable = costo <= (self.__presupuesto * 0.7)
        print("Proyecto " + self.__nombre)
        print("Costo total " + str(costo))
        print("Presupuesto maximo viable " + str(self.__presupuesto * 0.7))
        print("Viabilidad " + str(viable))
        return viable

def procesar_empleados(lista_empleados):
    print("-Procesamiento de Empleados")
    for emp in lista_empleados:
        print("--------------------") #decoración para que se vea todo mas ordenado
        emp.mostrar_informacion()
        print("Proyectos asignados " + str(emp.get_num_proyectos()))
        if isinstance(emp, Gerente):
            print("NOTA Es Gerente No puede ser miembro de proyectos")
    print("--------------------")

#caso de purruebaaa!
print("-Inicializacion del Sistema")
gerente1 = Gerente("Aisha Herrera", 6000.0, "Desarrollo de Software")
desarrollador1 = Desarrollador("Carlos Guevara", 3000.0, ["Python", "SQL"], "SemiSenior")
desarrollador2 = Desarrollador("Alber Curvelo", 2500.0, ["Java"], "Junior")
disenador1 = Diseñador("Hanna Montana", 3200.0, ["Figma", "Photoshop", "Illustrator"], "UX")
empleados_general = [gerente1, desarrollador1, desarrollador2, disenador1]
gerente1.agregar_al_equipo(desarrollador1)
gerente1.agregar_al_equipo(desarrollador2)
gerente1.agregar_al_equipo(disenador1)
gerente1.agregar_al_equipo(gerente1) 
print("-Salarios calculados (antes de proyectos)")
procesar_empleados(empleados_general)
proyectoA = Proyecto("AppMovil", 30000.0)
proyectoB = Proyecto("SistemaWeb", 15000.0)
print("-Asignacion de Proyectos")
proyectoA.agregar_empleado(desarrollador1) 
proyectoB.agregar_empleado(desarrollador1) 
proyectoA.agregar_empleado(desarrollador2)
proyectoA.agregar_empleado(disenador1)
proyectoB.agregar_empleado(disenador1) 
proyectoA.agregar_empleado(gerente1)
print("-Viabilidad de Proyectos")
proyectoA.viabilidad()
print("--------------------") #decoración para que esté ordenadito
proyectoB.viabilidad()
print("-Prueba de Limite de Proyectos")
proyectoC = Proyecto("NuevoProducto", 50000.0)
proyectoD = Proyecto("Mantenimiento", 1000.0)
proyectoC.agregar_empleado(desarrollador1) 
proyectoD.agregar_empleado(desarrollador1) 
print("-Salarios calculados (despues de proyectos)")
procesar_empleados(empleados_general)