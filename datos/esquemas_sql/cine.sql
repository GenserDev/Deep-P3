CREATE TABLE `movies` (
  `movie_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador de la pelicula',
  `title` varchar(100) NOT NULL COMMENT 'titulo de la pelicula',
  `genre` varchar(30) NOT NULL COMMENT 'genero de la pelicula',
  `duration_min` int NOT NULL COMMENT 'duracion en minutos',
  `release_year` int NOT NULL COMMENT 'anio de estreno',
  PRIMARY KEY (`movie_id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='peliculas';

CREATE TABLE `rooms` (
  `room_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador de la sala',
  `room_name` varchar(20) NOT NULL COMMENT 'nombre de la sala',
  `capacity` int NOT NULL COMMENT 'capacidad de asientos',
  `room_type` varchar(10) NOT NULL COMMENT 'tipo de sala',
  PRIMARY KEY (`room_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='salas';

CREATE TABLE `showtimes` (
  `showtime_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador de la funcion',
  `movie_id` int NOT NULL COMMENT 'pelicula proyectada',
  `room_id` int NOT NULL COMMENT 'sala de la funcion',
  `show_date` date NOT NULL COMMENT 'fecha de la funcion',
  `ticket_price` decimal(8,2) NOT NULL COMMENT 'precio del boleto',
  PRIMARY KEY (`showtime_id`),
  KEY `movie_id` (`movie_id`),
  KEY `room_id` (`room_id`),
  CONSTRAINT `showtimes_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movies` (`movie_id`),
  CONSTRAINT `showtimes_ibfk_2` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`room_id`)
) ENGINE=InnoDB AUTO_INCREMENT=251 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='funciones';

CREATE TABLE `tickets` (
  `ticket_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del boleto',
  `showtime_id` int NOT NULL COMMENT 'funcion del boleto',
  `seat` varchar(5) NOT NULL COMMENT 'asiento',
  `payment` varchar(15) NOT NULL COMMENT 'forma de pago',
  PRIMARY KEY (`ticket_id`),
  KEY `showtime_id` (`showtime_id`),
  CONSTRAINT `tickets_ibfk_1` FOREIGN KEY (`showtime_id`) REFERENCES `showtimes` (`showtime_id`)
) ENGINE=InnoDB AUTO_INCREMENT=701 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='boletos';