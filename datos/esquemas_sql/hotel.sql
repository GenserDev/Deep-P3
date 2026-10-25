CREATE TABLE `htl_hab` (
  `hab_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador de la habitacion',
  `hab_num` varchar(10) NOT NULL COMMENT 'numero de habitacion',
  `hab_tipo` varchar(20) NOT NULL COMMENT 'tipo de habitacion',
  `hab_tarifa` decimal(10,2) NOT NULL COMMENT 'tarifa por noche',
  `hab_piso` int NOT NULL COMMENT 'piso donde esta',
  PRIMARY KEY (`hab_id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='habitaciones del hotel';

CREATE TABLE `htl_hues` (
  `hues_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del huesped',
  `hues_nom` varchar(80) NOT NULL COMMENT 'nombre del huesped',
  `hues_pais` varchar(40) NOT NULL COMMENT 'pais del huesped',
  PRIMARY KEY (`hues_id`)
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='huespedes registrados';

CREATE TABLE `htl_res` (
  `res_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador de la reserva',
  `hues_id` int NOT NULL COMMENT 'huesped que reserva',
  `hab_id` int NOT NULL COMMENT 'habitacion reservada',
  `res_fec_ini` date NOT NULL COMMENT 'fecha de llegada',
  `res_noches` int NOT NULL COMMENT 'numero de noches',
  `res_canal` varchar(20) NOT NULL COMMENT 'canal de la reserva',
  PRIMARY KEY (`res_id`),
  KEY `hues_id` (`hues_id`),
  KEY `hab_id` (`hab_id`),
  CONSTRAINT `htl_res_ibfk_1` FOREIGN KEY (`hues_id`) REFERENCES `htl_hues` (`hues_id`),
  CONSTRAINT `htl_res_ibfk_2` FOREIGN KEY (`hab_id`) REFERENCES `htl_hab` (`hab_id`)
) ENGINE=InnoDB AUTO_INCREMENT=351 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='reservas de habitaciones';

CREATE TABLE `htl_serv` (
  `serv_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del servicio',
  `res_id` int NOT NULL COMMENT 'reserva a la que se cobra',
  `serv_tipo` varchar(20) NOT NULL COMMENT 'tipo de servicio',
  `serv_monto` decimal(10,2) NOT NULL COMMENT 'monto cobrado',
  PRIMARY KEY (`serv_id`),
  KEY `res_id` (`res_id`),
  CONSTRAINT `htl_serv_ibfk_1` FOREIGN KEY (`res_id`) REFERENCES `htl_res` (`res_id`)
) ENGINE=InnoDB AUTO_INCREMENT=301 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='servicios extra cobrados';