CREATE TABLE `aircraft` (
  `aircraft_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del avion',
  `model` varchar(30) NOT NULL COMMENT 'modelo del avion',
  `seats` int NOT NULL COMMENT 'numero de asientos',
  PRIMARY KEY (`aircraft_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='aviones';

CREATE TABLE `airports` (
  `airport_code` int NOT NULL AUTO_INCREMENT COMMENT 'codigo del aeropuerto',
  `airport_name` varchar(60) NOT NULL COMMENT 'nombre del aeropuerto',
  `city` varchar(40) NOT NULL COMMENT 'ciudad',
  PRIMARY KEY (`airport_code`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='aeropuertos';

CREATE TABLE `bookings` (
  `booking_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador de la reserva',
  `flight_id` int NOT NULL COMMENT 'vuelo reservado',
  `pax_id` int NOT NULL COMMENT 'pasajero',
  `class` varchar(15) NOT NULL COMMENT 'clase del boleto',
  `paid` decimal(10,2) NOT NULL COMMENT 'monto pagado en dolares',
  `booking_date` date NOT NULL COMMENT 'fecha de compra',
  PRIMARY KEY (`booking_id`),
  KEY `flight_id` (`flight_id`),
  KEY `pax_id` (`pax_id`),
  CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`flight_id`) REFERENCES `flights` (`flight_id`),
  CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`pax_id`) REFERENCES `passengers` (`pax_id`)
) ENGINE=InnoDB AUTO_INCREMENT=701 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='reservas';

CREATE TABLE `flights` (
  `flight_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del vuelo',
  `origin` int NOT NULL COMMENT 'aeropuerto de origen',
  `aircraft_id` int NOT NULL COMMENT 'avion asignado',
  `dep_date` date NOT NULL COMMENT 'fecha de salida',
  `base_fare` decimal(10,2) NOT NULL COMMENT 'tarifa base en dolares',
  `status` varchar(15) NOT NULL COMMENT 'estado del vuelo',
  PRIMARY KEY (`flight_id`),
  KEY `origin` (`origin`),
  KEY `aircraft_id` (`aircraft_id`),
  CONSTRAINT `flights_ibfk_1` FOREIGN KEY (`origin`) REFERENCES `airports` (`airport_code`),
  CONSTRAINT `flights_ibfk_2` FOREIGN KEY (`aircraft_id`) REFERENCES `aircraft` (`aircraft_id`)
) ENGINE=InnoDB AUTO_INCREMENT=301 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='vuelos';

CREATE TABLE `passengers` (
  `pax_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del pasajero',
  `pax_name` varchar(80) NOT NULL COMMENT 'nombre del pasajero',
  `nationality` varchar(30) NOT NULL COMMENT 'nacionalidad',
  `birth_date` date NOT NULL COMMENT 'fecha de nacimiento',
  PRIMARY KEY (`pax_id`)
) ENGINE=InnoDB AUTO_INCREMENT=201 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='pasajeros';