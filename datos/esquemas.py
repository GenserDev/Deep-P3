# Esquemas propios del proyecto.
# Cada columna es una tupla: (nombre, tipo, clase, descripcion, extra)
# clase puede ser: pk, txt, cat, int, dec, fecha, fk
# extra depende de la clase: lista de valores, rango de numeros, rango de anios o tabla referenciada

NOMBRES = ["Ana", "Luis", "Carlos", "Maria", "Jose", "Lucia", "Pedro", "Sofia", "Diego", "Elena",
           "Jorge", "Paula", "Mario", "Andrea", "Raul", "Carmen", "Hugo", "Laura", "Pablo", "Rosa"]
APELLIDOS = ["Lopez", "Garcia", "Perez", "Martinez", "Ramirez", "Castillo", "Morales", "Herrera",
             "Mendez", "Rodas", "Ortiz", "Vasquez", "Cruz", "Reyes", "Flores"]
PERSONAS = [n + " " + a for a in APELLIDOS for n in NOMBRES]
CIUDADES = ["Guatemala", "Mixco", "Antigua", "Quetzaltenango", "Escuintla", "Coban", "Peten", "Zacapa"]
CITIES = ["Madrid", "Lima", "Bogota", "Quito", "Miami", "Toronto", "Mexico", "Santiago"]


def t(nombre, desc, n, cols, comentario=None):
    return {"nombre": nombre, "desc": desc, "n": n, "cols": cols, "comentario": comentario}


ESQUEMAS = {}

ESQUEMAS["tienda"] = [
    t("clientes", "clientes", 80, [
        ("id_cliente", "INT", "pk", "identificador del cliente", None),
        ("nombre", "VARCHAR(80)", "txt", "nombre del cliente", PERSONAS),
        ("ciudad", "VARCHAR(40)", "cat", "ciudad del cliente", CIUDADES),
        ("fecha_registro", "DATE", "fecha", "fecha de registro", (2021, 2025)),
    ]),
    t("productos", "productos", 40, [
        ("id_producto", "INT", "pk", "identificador del producto", None),
        ("nombre", "VARCHAR(80)", "txt", "nombre del producto",
         ["Laptop", "Mouse", "Teclado", "Monitor", "Audifonos", "Impresora", "Tablet", "Camara",
          "Bocina", "Router", "Disco duro", "Memoria USB", "Cargador", "Silla", "Escritorio",
          "Lampara", "Microfono", "Webcam", "Telefono", "Reloj"]),
        ("categoria", "VARCHAR(30)", "cat", "categoria del producto", ["Computo", "Audio", "Oficina", "Accesorios", "Video"]),
        ("precio", "DECIMAL(10,2)", "dec", "precio unitario en quetzales", (20, 9000)),
        ("existencia", "INT", "int", "unidades en bodega", (0, 300)),
    ]),
    t("pedidos", "pedidos", 200, [
        ("id_pedido", "INT", "pk", "identificador del pedido", None),
        ("id_cliente", "INT", "fk", "cliente que hizo el pedido", "clientes"),
        ("fecha", "DATE", "fecha", "fecha del pedido", (2023, 2025)),
        ("estado", "VARCHAR(20)", "cat", "estado del pedido", ["pendiente", "enviado", "entregado", "cancelado"]),
    ]),
    t("detalle_pedido", "lineas de pedido", 500, [
        ("id_detalle", "INT", "pk", "identificador de la linea", None),
        ("id_pedido", "INT", "fk", "pedido al que pertenece", "pedidos"),
        ("id_producto", "INT", "fk", "producto vendido", "productos"),
        ("cantidad", "INT", "int", "cantidad de unidades", (1, 10)),
    ]),
]

ESQUEMAS["universidad"] = [
    t("facultades", "facultades", 6, [
        ("id_facultad", "INT", "pk", "identificador de la facultad", None),
        ("nombre", "VARCHAR(60)", "txt", "nombre de la facultad",
         ["Ingenieria", "Medicina", "Derecho", "Economia", "Arquitectura", "Humanidades"]),
        ("edificio", "VARCHAR(10)", "cat", "edificio donde esta la facultad", ["A", "B", "C", "D"]),
    ]),
    t("profesores", "profesores", 40, [
        ("id_profesor", "INT", "pk", "identificador del profesor", None),
        ("nombre", "VARCHAR(80)", "txt", "nombre del profesor", PERSONAS),
        ("id_facultad", "INT", "fk", "facultad del profesor", "facultades"),
        ("salario", "DECIMAL(10,2)", "dec", "salario mensual", (6000, 25000)),
        ("fecha_contrato", "DATE", "fecha", "fecha de contratacion", (2005, 2024)),
    ]),
    t("cursos", "cursos", 50, [
        ("id_curso", "INT", "pk", "identificador del curso", None),
        ("nombre", "VARCHAR(80)", "txt", "nombre del curso",
         ["Calculo", "Fisica", "Quimica", "Programacion", "Estadistica", "Algebra", "Historia",
          "Anatomia", "Contabilidad", "Dibujo", "Filosofia", "Redes", "Bases de datos"]),
        ("creditos", "INT", "int", "numero de creditos", (2, 6)),
        ("id_profesor", "INT", "fk", "profesor que imparte el curso", "profesores"),
    ]),
    t("estudiantes", "estudiantes", 150, [
        ("id_estudiante", "INT", "pk", "identificador del estudiante", None),
        ("nombre", "VARCHAR(80)", "txt", "nombre del estudiante", PERSONAS),
        ("id_facultad", "INT", "fk", "facultad del estudiante", "facultades"),
        ("anio_ingreso", "INT", "int", "anio de ingreso", (2018, 2025)),
        ("genero", "CHAR(1)", "cat", "genero F o M", ["F", "M"]),
    ]),
    t("inscripciones", "inscripciones", 600, [
        ("id_inscripcion", "INT", "pk", "identificador de la inscripcion", None),
        ("id_estudiante", "INT", "fk", "estudiante inscrito", "estudiantes"),
        ("id_curso", "INT", "fk", "curso inscrito", "cursos"),
        ("nota", "DECIMAL(5,2)", "dec", "nota final de 0 a 100", (30, 100)),
        ("fecha_inscripcion", "DATE", "fecha", "fecha de inscripcion", (2022, 2025)),
    ]),
]

ESQUEMAS["biblioteca"] = [
    t("autores", "autores", 30, [
        ("id_autor", "INT", "pk", "identificador del autor", None),
        ("nombre", "VARCHAR(80)", "txt", "nombre del autor", PERSONAS),
        ("pais", "VARCHAR(40)", "cat", "pais de origen", ["Guatemala", "Mexico", "Colombia", "Argentina", "Chile", "Peru", "Espana"]),
    ]),
    t("libros", "libros", 120, [
        ("id_libro", "INT", "pk", "identificador del libro", None),
        ("titulo", "VARCHAR(100)", "txt", "titulo del libro",
         ["El camino", "La casa", "Noches de lluvia", "El mar", "Cien voces", "La ciudad", "El viaje",
          "Sombras", "La montana", "El reloj", "Luz de luna", "El rio", "Memorias", "La isla"]),
        ("id_autor", "INT", "fk", "autor del libro", "autores"),
        ("genero", "VARCHAR(30)", "cat", "genero literario", ["Novela", "Poesia", "Ensayo", "Cuento", "Historia"]),
        ("anio_publicacion", "INT", "int", "anio de publicacion", (1950, 2024)),
        ("paginas", "INT", "int", "numero de paginas", (80, 900)),
    ]),
    t("socios", "socios", 90, [
        ("id_socio", "INT", "pk", "identificador del socio", None),
        ("nombre", "VARCHAR(80)", "txt", "nombre del socio", PERSONAS),
        ("municipio", "VARCHAR(40)", "cat", "municipio donde vive", CIUDADES),
        ("fecha_alta", "DATE", "fecha", "fecha de alta como socio", (2019, 2025)),
    ]),
    t("prestamos", "prestamos", 400, [
        ("id_prestamo", "INT", "pk", "identificador del prestamo", None),
        ("id_libro", "INT", "fk", "libro prestado", "libros"),
        ("id_socio", "INT", "fk", "socio que pidio el libro", "socios"),
        ("fecha_prestamo", "DATE", "fecha", "fecha del prestamo", (2023, 2025)),
        ("dias", "INT", "int", "dias que duro el prestamo", (1, 30)),
    ]),
]

ESQUEMAS["hotel"] = [
    t("htl_hab", "habitaciones", 60, [
        ("hab_id", "INT", "pk", "identificador de la habitacion", None),
        ("hab_num", "VARCHAR(10)", "txt", "numero de habitacion", [str(i) for i in range(100, 400)]),
        ("hab_tipo", "VARCHAR(20)", "cat", "tipo de habitacion", ["sencilla", "doble", "suite", "familiar"]),
        ("hab_tarifa", "DECIMAL(10,2)", "dec", "tarifa por noche", (250, 2500)),
        ("hab_piso", "INT", "int", "piso donde esta", (1, 6)),
    ], "habitaciones del hotel"),
    t("htl_hues", "huespedes", 120, [
        ("hues_id", "INT", "pk", "identificador del huesped", None),
        ("hues_nom", "VARCHAR(80)", "txt", "nombre del huesped", PERSONAS),
        ("hues_pais", "VARCHAR(40)", "cat", "pais del huesped", ["Guatemala", "Mexico", "USA", "Canada", "Espana", "Francia"]),
    ], "huespedes registrados"),
    t("htl_res", "reservas", 350, [
        ("res_id", "INT", "pk", "identificador de la reserva", None),
        ("hues_id", "INT", "fk", "huesped que reserva", "htl_hues"),
        ("hab_id", "INT", "fk", "habitacion reservada", "htl_hab"),
        ("res_fec_ini", "DATE", "fecha", "fecha de llegada", (2023, 2025)),
        ("res_noches", "INT", "int", "numero de noches", (1, 14)),
        ("res_canal", "VARCHAR(20)", "cat", "canal de la reserva", ["web", "telefono", "agencia", "recepcion"]),
    ], "reservas de habitaciones"),
    t("htl_serv", "servicios extra", 300, [
        ("serv_id", "INT", "pk", "identificador del servicio", None),
        ("res_id", "INT", "fk", "reserva a la que se cobra", "htl_res"),
        ("serv_tipo", "VARCHAR(20)", "cat", "tipo de servicio", ["spa", "lavanderia", "restaurante", "transporte"]),
        ("serv_monto", "DECIMAL(10,2)", "dec", "monto cobrado", (50, 1200)),
    ], "servicios extra cobrados"),
]

ESQUEMAS["cine"] = [
    t("movies", "peliculas", 50, [
        ("movie_id", "INT", "pk", "identificador de la pelicula", None),
        ("title", "VARCHAR(100)", "txt", "titulo de la pelicula",
         ["Star Night", "The Return", "Blue River", "Dark City", "Lost Time", "Red Planet", "Silent Hill",
          "Golden Gate", "Last Dance", "Iron Road", "Deep Sea", "Wild Heart"]),
        ("genre", "VARCHAR(30)", "cat", "genero de la pelicula", ["Action", "Drama", "Comedy", "Horror", "Animation"]),
        ("duration_min", "INT", "int", "duracion en minutos", (80, 180)),
        ("release_year", "INT", "int", "anio de estreno", (1995, 2025)),
    ]),
    t("rooms", "salas", 8, [
        ("room_id", "INT", "pk", "identificador de la sala", None),
        ("room_name", "VARCHAR(20)", "txt", "nombre de la sala", ["Sala 1", "Sala 2", "Sala 3", "Sala 4", "Sala 5", "Sala 6", "Sala 7", "Sala 8"]),
        ("capacity", "INT", "int", "capacidad de asientos", (60, 300)),
        ("room_type", "VARCHAR(10)", "cat", "tipo de sala", ["2D", "3D", "IMAX"]),
    ]),
    t("showtimes", "funciones", 250, [
        ("showtime_id", "INT", "pk", "identificador de la funcion", None),
        ("movie_id", "INT", "fk", "pelicula proyectada", "movies"),
        ("room_id", "INT", "fk", "sala de la funcion", "rooms"),
        ("show_date", "DATE", "fecha", "fecha de la funcion", (2024, 2025)),
        ("ticket_price", "DECIMAL(8,2)", "dec", "precio del boleto", (25, 90)),
    ]),
    t("tickets", "boletos", 700, [
        ("ticket_id", "INT", "pk", "identificador del boleto", None),
        ("showtime_id", "INT", "fk", "funcion del boleto", "showtimes"),
        ("seat", "VARCHAR(5)", "txt", "asiento", [r + str(i) for r in "ABCDEFGH" for i in range(1, 15)]),
        ("payment", "VARCHAR(15)", "cat", "forma de pago", ["cash", "card", "app"]),
    ]),
]

ESQUEMAS["gimnasio"] = [
    t("gim_sedes", "sedes", 6, [
        ("sede_id", "INT", "pk", "identificador de la sede", None),
        ("sede_nombre", "VARCHAR(40)", "txt", "nombre de la sede", ["Centro", "Norte", "Sur", "Oriente", "Occidente", "Plaza"]),
        ("sede_ciudad", "VARCHAR(40)", "cat", "ciudad de la sede", CIUDADES[:4]),
    ]),
    t("gim_miembros", "miembros", 150, [
        ("miem_id", "INT", "pk", "identificador del miembro", None),
        ("miem_nombre", "VARCHAR(80)", "txt", "nombre del miembro", PERSONAS),
        ("sede_id", "INT", "fk", "sede donde entrena", "gim_sedes"),
        ("plan", "VARCHAR(20)", "cat", "plan contratado", ["basico", "plus", "premium"]),
        ("cuota", "DECIMAL(8,2)", "dec", "cuota mensual", (150, 600)),
        ("fecha_ingreso", "DATE", "fecha", "fecha de ingreso", (2020, 2025)),
    ]),
    t("gim_clases", "clases", 30, [
        ("clase_id", "INT", "pk", "identificador de la clase", None),
        ("clase_nombre", "VARCHAR(40)", "txt", "nombre de la clase", ["Yoga", "Spinning", "Crossfit", "Zumba", "Pilates", "Boxeo", "Natacion"]),
        ("sede_id", "INT", "fk", "sede donde se da la clase", "gim_sedes"),
        ("cupo", "INT", "int", "cupo maximo", (10, 40)),
    ]),
    t("gim_asistencias", "asistencias", 800, [
        ("asis_id", "INT", "pk", "identificador de la asistencia", None),
        ("miem_id", "INT", "fk", "miembro que asistio", "gim_miembros"),
        ("clase_id", "INT", "fk", "clase a la que asistio", "gim_clases"),
        ("asis_fecha", "DATE", "fecha", "fecha de asistencia", (2024, 2025)),
        ("minutos", "INT", "int", "minutos de entrenamiento", (20, 120)),
    ]),
]

ESQUEMAS["logistica"] = [
    t("lg_bod", "bodegas", 8, [
        ("bod_cod", "INT", "pk", "codigo de la bodega", None),
        ("bod_nom", "VARCHAR(40)", "txt", "nombre de la bodega", ["Bodega Central", "Bodega Norte", "Bodega Sur", "Bodega Puerto",
                                                                  "Bodega Aeropuerto", "Bodega Este", "Bodega Oeste", "Bodega Feria"]),
        ("bod_ciu", "VARCHAR(40)", "cat", "ciudad de la bodega", CIUDADES),
        ("bod_cap", "INT", "int", "capacidad en metros cubicos", (500, 5000)),
    ], "bodegas de la empresa"),
    t("lg_trans", "transportistas", 15, [
        ("trans_cod", "INT", "pk", "codigo del transportista", None),
        ("trans_nom", "VARCHAR(80)", "txt", "nombre del transportista", PERSONAS),
        ("trans_veh", "VARCHAR(20)", "cat", "tipo de vehiculo", ["camion", "furgon", "moto", "pickup"]),
    ], "transportistas"),
    t("lg_env", "envios", 450, [
        ("env_cod", "INT", "pk", "codigo del envio", None),
        ("bod_cod", "INT", "fk", "bodega de origen", "lg_bod"),
        ("trans_cod", "INT", "fk", "transportista asignado", "lg_trans"),
        ("env_fec", "DATE", "fecha", "fecha de salida del envio", (2024, 2025)),
        ("env_peso", "DECIMAL(10,2)", "dec", "peso en kilogramos", (1, 2000)),
        ("env_cost", "DECIMAL(10,2)", "dec", "costo del envio", (30, 5000)),
        ("env_est", "VARCHAR(20)", "cat", "estado del envio", ["en ruta", "entregado", "devuelto", "retrasado"]),
    ], "envios realizados"),
    t("lg_inc", "incidencias", 120, [
        ("inc_cod", "INT", "pk", "codigo de la incidencia", None),
        ("env_cod", "INT", "fk", "envio afectado", "lg_env"),
        ("inc_tipo", "VARCHAR(20)", "cat", "tipo de incidencia", ["dano", "perdida", "demora", "direccion"]),
        ("inc_fec", "DATE", "fecha", "fecha de la incidencia", (2024, 2025)),
    ], "incidencias de envios"),
]

ESQUEMAS["banco"] = [
    t("bco_cli", "clientes del banco", 100, [
        ("cli_id", "INT", "pk", "identificador del cliente", None),
        ("cli_nom", "VARCHAR(80)", "txt", "nombre del cliente", PERSONAS),
        ("cli_ciu", "VARCHAR(40)", "cat", "ciudad del cliente", CIUDADES),
        ("cli_fnac", "DATE", "fecha", "fecha de nacimiento", (1960, 2004)),
    ]),
    t("bco_cta", "cuentas", 160, [
        ("cta_id", "INT", "pk", "identificador de la cuenta", None),
        ("cli_id", "INT", "fk", "duenio de la cuenta", "bco_cli"),
        ("cta_tipo", "VARCHAR(20)", "cat", "tipo de cuenta", ["ahorro", "monetaria", "plazo fijo"]),
        ("cta_saldo", "DECIMAL(12,2)", "dec", "saldo actual", (0, 90000)),
        ("cta_fape", "DATE", "fecha", "fecha de apertura", (2015, 2025)),
    ]),
    t("bco_mov", "movimientos", 900, [
        ("mov_id", "INT", "pk", "identificador del movimiento", None),
        ("cta_id", "INT", "fk", "cuenta del movimiento", "bco_cta"),
        ("mov_tipo", "VARCHAR(20)", "cat", "tipo de movimiento", ["deposito", "retiro", "transferencia", "pago"]),
        ("mov_monto", "DECIMAL(12,2)", "dec", "monto del movimiento", (10, 15000)),
        ("mov_fec", "DATE", "fecha", "fecha del movimiento", (2024, 2025)),
    ]),
    t("bco_prest", "prestamos", 80, [
        ("prest_id", "INT", "pk", "identificador del prestamo", None),
        ("cli_id", "INT", "fk", "cliente del prestamo", "bco_cli"),
        ("prest_monto", "DECIMAL(12,2)", "dec", "monto prestado", (5000, 300000)),
        ("prest_tasa", "DECIMAL(5,2)", "dec", "tasa de interes anual", (5, 24)),
        ("prest_plazo", "INT", "int", "plazo en meses", (6, 120)),
    ]),
]

ESQUEMAS["hr"] = [
    t("departments", "departamentos", 8, [
        ("dept_id", "INT", "pk", "identificador del departamento", None),
        ("dept_name", "VARCHAR(40)", "txt", "nombre del departamento", ["Sales", "IT", "Finance", "HR", "Marketing", "Legal", "Support", "Operations"]),
        ("location", "VARCHAR(40)", "cat", "ciudad del departamento", CITIES[:4]),
    ]),
    t("employees", "empleados", 120, [
        ("emp_id", "INT", "pk", "identificador del empleado", None),
        ("full_name", "VARCHAR(80)", "txt", "nombre del empleado", PERSONAS),
        ("dept_id", "INT", "fk", "departamento del empleado", "departments"),
        ("job_title", "VARCHAR(30)", "cat", "puesto", ["Analyst", "Manager", "Engineer", "Assistant", "Director"]),
        ("salary", "DECIMAL(10,2)", "dec", "salario mensual", (3000, 30000)),
        ("hire_date", "DATE", "fecha", "fecha de contratacion", (2010, 2025)),
    ]),
    t("projects", "proyectos", 25, [
        ("project_id", "INT", "pk", "identificador del proyecto", None),
        ("project_name", "VARCHAR(60)", "txt", "nombre del proyecto", ["Apollo", "Zeus", "Hermes", "Atlas", "Orion", "Phoenix", "Titan", "Nova"]),
        ("dept_id", "INT", "fk", "departamento responsable", "departments"),
        ("budget", "DECIMAL(12,2)", "dec", "presupuesto", (10000, 900000)),
        ("start_date", "DATE", "fecha", "fecha de inicio", (2022, 2025)),
    ]),
    t("assignments", "asignaciones", 300, [
        ("assignment_id", "INT", "pk", "identificador de la asignacion", None),
        ("emp_id", "INT", "fk", "empleado asignado", "employees"),
        ("project_id", "INT", "fk", "proyecto asignado", "projects"),
        ("hours", "INT", "int", "horas trabajadas", (5, 400)),
    ]),
]

ESQUEMAS["music_store"] = [
    t("artists", "artistas", 30, [
        ("artist_id", "INT", "pk", "identificador del artista", None),
        ("name", "VARCHAR(80)", "txt", "nombre del artista", ["The Waves", "Luna Roja", "Los Andes", "Echo", "Neon", "Sol Mayor",
                                                            "Blue Moon", "Rock Star", "Marimba Sur", "Jazz Club"]),
        ("country", "VARCHAR(40)", "cat", "pais del artista", ["Guatemala", "USA", "Mexico", "UK", "Spain"]),
    ]),
    t("albums", "albumes", 80, [
        ("album_id", "INT", "pk", "identificador del album", None),
        ("title", "VARCHAR(100)", "txt", "titulo del album", ["First Light", "Night Road", "Volume One", "Live Tour", "Greatest Hits",
                                                            "Rain", "Summer", "Golden", "Echoes", "Home"]),
        ("artist_id", "INT", "fk", "artista del album", "artists"),
        ("year", "INT", "int", "anio de lanzamiento", (1980, 2025)),
        ("price", "DECIMAL(8,2)", "dec", "precio del album", (50, 250)),
    ]),
    t("tracks", "canciones", 400, [
        ("track_id", "INT", "pk", "identificador de la cancion", None),
        ("album_id", "INT", "fk", "album de la cancion", "albums"),
        ("track_name", "VARCHAR(100)", "txt", "nombre de la cancion", ["Intro", "Fire", "Dreams", "Alone", "Run", "Stay", "Heart", "Light",
                                                                     "Ocean", "Wind", "Smile", "Storm"]),
        ("seconds", "INT", "int", "duracion en segundos", (90, 420)),
        ("style", "VARCHAR(20)", "cat", "estilo musical", ["Rock", "Pop", "Jazz", "Latin", "Electronic"]),
    ]),
    t("sales", "ventas", 600, [
        ("sale_id", "INT", "pk", "identificador de la venta", None),
        ("album_id", "INT", "fk", "album vendido", "albums"),
        ("sale_date", "DATE", "fecha", "fecha de la venta", (2023, 2025)),
        ("units", "INT", "int", "unidades vendidas", (1, 5)),
        ("channel", "VARCHAR(20)", "cat", "canal de venta", ["store", "online", "event"]),
    ]),
]

ESQUEMAS["restaurante"] = [
    t("rst_mesas", "mesas", 20, [
        ("mesa_id", "INT", "pk", "identificador de la mesa", None),
        ("mesa_num", "INT", "int", "numero de mesa", (1, 20)),
        ("zona", "VARCHAR(20)", "cat", "zona del restaurante", ["terraza", "salon", "barra", "privado"]),
        ("sillas", "INT", "int", "cantidad de sillas", (2, 10)),
    ]),
    t("rst_meseros", "meseros", 12, [
        ("mesero_id", "INT", "pk", "identificador del mesero", None),
        ("mesero_nom", "VARCHAR(80)", "txt", "nombre del mesero", PERSONAS),
        ("turno", "VARCHAR(10)", "cat", "turno de trabajo", ["manana", "tarde", "noche"]),
    ]),
    t("rst_platos", "platos", 35, [
        ("plato_id", "INT", "pk", "identificador del plato", None),
        ("plato_nom", "VARCHAR(60)", "txt", "nombre del plato", ["Pepian", "Kakik", "Tamales", "Hilachas", "Churrasco", "Pizza", "Pasta",
                                                               "Ensalada", "Sopa", "Hamburguesa", "Tacos", "Ceviche"]),
        ("tipo", "VARCHAR(20)", "cat", "tipo de plato", ["entrada", "fuerte", "postre", "bebida"]),
        ("precio", "DECIMAL(8,2)", "dec", "precio del plato", (15, 250)),
    ]),
    t("rst_ordenes", "ordenes", 400, [
        ("orden_id", "INT", "pk", "identificador de la orden", None),
        ("mesa_id", "INT", "fk", "mesa de la orden", "rst_mesas"),
        ("mesero_id", "INT", "fk", "mesero que atendio", "rst_meseros"),
        ("plato_id", "INT", "fk", "plato pedido", "rst_platos"),
        ("orden_fecha", "DATE", "fecha", "fecha de la orden", (2024, 2025)),
        ("porciones", "INT", "int", "porciones pedidas", (1, 6)),
    ]),
]

ESQUEMAS["taller"] = [
    t("tll_cli", "clientes del taller", 70, [
        ("cli_id", "INT", "pk", "identificador del cliente", None),
        ("cli_nom", "VARCHAR(80)", "txt", "nombre del cliente", PERSONAS),
        ("cli_tel", "VARCHAR(15)", "txt", "telefono", [str(50000000 + i * 137) for i in range(200)]),
    ]),
    t("tll_veh", "vehiculos", 110, [
        ("veh_id", "INT", "pk", "identificador del vehiculo", None),
        ("cli_id", "INT", "fk", "duenio del vehiculo", "tll_cli"),
        ("veh_marca", "VARCHAR(20)", "cat", "marca del vehiculo", ["Toyota", "Honda", "Nissan", "Mazda", "Kia", "Hyundai"]),
        ("veh_anio", "INT", "int", "anio del modelo", (2000, 2025)),
    ]),
    t("tll_mec", "mecanicos", 10, [
        ("mec_id", "INT", "pk", "identificador del mecanico", None),
        ("mec_nom", "VARCHAR(80)", "txt", "nombre del mecanico", PERSONAS),
        ("mec_esp", "VARCHAR(20)", "cat", "especialidad", ["motor", "frenos", "electrico", "pintura"]),
    ]),
    t("tll_rep", "reparaciones", 380, [
        ("rep_id", "INT", "pk", "identificador de la reparacion", None),
        ("veh_id", "INT", "fk", "vehiculo reparado", "tll_veh"),
        ("mec_id", "INT", "fk", "mecanico responsable", "tll_mec"),
        ("rep_fec", "DATE", "fecha", "fecha de ingreso al taller", (2023, 2025)),
        ("rep_costo", "DECIMAL(10,2)", "dec", "costo de la reparacion", (100, 12000)),
        ("rep_horas", "INT", "int", "horas de trabajo", (1, 40)),
    ]),
]

# Esquemas de validacion. No se usan para generar datos de entrenamiento.
ESQUEMAS_VALIDACION = {}

ESQUEMAS_VALIDACION["veterinaria"] = [
    t("vet_duenos", "duenos", 60, [
        ("due_id", "INT", "pk", "identificador del dueno", None),
        ("due_nom", "VARCHAR(80)", "txt", "nombre del dueno", PERSONAS),
        ("due_ciu", "VARCHAR(40)", "cat", "ciudad del dueno", CIUDADES),
    ], "duenos de mascotas"),
    t("vet_masc", "mascotas", 110, [
        ("masc_id", "INT", "pk", "identificador de la mascota", None),
        ("masc_nom", "VARCHAR(40)", "txt", "nombre de la mascota", ["Firulais", "Luna", "Max", "Rocky", "Nina", "Toby", "Kira",
                                                                  "Simba", "Coco", "Lola", "Bruno", "Mia"]),
        ("due_id", "INT", "fk", "dueno de la mascota", "vet_duenos"),
        ("masc_esp", "VARCHAR(20)", "cat", "especie", ["perro", "gato", "ave", "conejo"]),
        ("masc_fnac", "DATE", "fecha", "fecha de nacimiento", (2012, 2024)),
        ("masc_peso", "DECIMAL(6,2)", "dec", "peso en kilogramos", (1, 45)),
    ], "mascotas atendidas"),
    t("vet_vets", "veterinarios", 8, [
        ("vet_id", "INT", "pk", "identificador del veterinario", None),
        ("vet_nom", "VARCHAR(80)", "txt", "nombre del veterinario", PERSONAS),
        ("vet_esp", "VARCHAR(30)", "cat", "especialidad", ["general", "cirugia", "dermatologia"]),
    ]),
    t("vet_cons", "consultas", 420, [
        ("cons_id", "INT", "pk", "identificador de la consulta", None),
        ("masc_id", "INT", "fk", "mascota atendida", "vet_masc"),
        ("vet_id", "INT", "fk", "veterinario que atendio", "vet_vets"),
        ("cons_fec", "DATE", "fecha", "fecha de la consulta", (2023, 2025)),
        ("cons_motivo", "VARCHAR(30)", "cat", "motivo de la consulta", ["vacuna", "control", "emergencia", "cirugia"]),
        ("cons_costo", "DECIMAL(8,2)", "dec", "costo de la consulta", (80, 3000)),
    ], "consultas realizadas"),
    t("vet_med", "medicamentos", 25, [
        ("med_id", "INT", "pk", "identificador del medicamento", None),
        ("med_nom", "VARCHAR(40)", "txt", "nombre del medicamento", ["Amoxicilina", "Ivermectina", "Meloxicam", "Prednisona",
                                                                  "Vitaminas", "Antipulgas", "Desparasitante"]),
        ("med_precio", "DECIMAL(8,2)", "dec", "precio unitario", (10, 400)),
    ]),
    t("vet_receta", "recetas", 500, [
        ("rec_id", "INT", "pk", "identificador de la receta", None),
        ("cons_id", "INT", "fk", "consulta donde se receto", "vet_cons"),
        ("med_id", "INT", "fk", "medicamento recetado", "vet_med"),
        ("rec_cant", "INT", "int", "cantidad recetada", (1, 5)),
    ], "medicamentos recetados en cada consulta"),
]

ESQUEMAS_VALIDACION["airline"] = [
    t("airports", "aeropuertos", 10, [
        ("airport_code", "INT", "pk", "codigo del aeropuerto", None),
        ("airport_name", "VARCHAR(60)", "txt", "nombre del aeropuerto", ["La Aurora", "Barajas", "Jorge Chavez", "El Dorado", "Mariscal Sucre",
                                                                       "Miami Intl", "Pearson", "Benito Juarez", "Arturo Merino", "Mundo Maya"]),
        ("city", "VARCHAR(40)", "cat", "ciudad", CITIES),
    ]),
    t("aircraft", "aviones", 15, [
        ("aircraft_id", "INT", "pk", "identificador del avion", None),
        ("model", "VARCHAR(30)", "cat", "modelo del avion", ["A320", "B737", "E190", "A330"]),
        ("seats", "INT", "int", "numero de asientos", (90, 300)),
    ]),
    t("flights", "vuelos", 300, [
        ("flight_id", "INT", "pk", "identificador del vuelo", None),
        ("origin", "INT", "fk", "aeropuerto de origen", "airports"),
        ("aircraft_id", "INT", "fk", "avion asignado", "aircraft"),
        ("dep_date", "DATE", "fecha", "fecha de salida", (2024, 2025)),
        ("base_fare", "DECIMAL(10,2)", "dec", "tarifa base en dolares", (80, 1200)),
        ("status", "VARCHAR(15)", "cat", "estado del vuelo", ["on time", "delayed", "cancelled"]),
    ]),
    t("passengers", "pasajeros", 200, [
        ("pax_id", "INT", "pk", "identificador del pasajero", None),
        ("pax_name", "VARCHAR(80)", "txt", "nombre del pasajero", PERSONAS),
        ("nationality", "VARCHAR(30)", "cat", "nacionalidad", ["Guatemala", "Mexico", "USA", "Spain", "Peru"]),
        ("birth_date", "DATE", "fecha", "fecha de nacimiento", (1950, 2015)),
    ]),
    t("bookings", "reservas", 700, [
        ("booking_id", "INT", "pk", "identificador de la reserva", None),
        ("flight_id", "INT", "fk", "vuelo reservado", "flights"),
        ("pax_id", "INT", "fk", "pasajero", "passengers"),
        ("class", "VARCHAR(15)", "cat", "clase del boleto", ["economy", "business", "first"]),
        ("paid", "DECIMAL(10,2)", "dec", "monto pagado en dolares", (80, 3000)),
        ("booking_date", "DATE", "fecha", "fecha de compra", (2023, 2025)),
    ]),
]
