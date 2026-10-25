CREATE TABLE `gim_asistencias` (
  `asis_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador de la asistencia',
  `miem_id` int NOT NULL COMMENT 'miembro que asistio',
  `clase_id` int NOT NULL COMMENT 'clase a la que asistio',
  `asis_fecha` date NOT NULL COMMENT 'fecha de asistencia',
  `minutos` int NOT NULL COMMENT 'minutos de entrenamiento',
  PRIMARY KEY (`asis_id`),
  KEY `miem_id` (`miem_id`),
  KEY `clase_id` (`clase_id`),
  CONSTRAINT `gim_asistencias_ibfk_1` FOREIGN KEY (`miem_id`) REFERENCES `gim_miembros` (`miem_id`),
  CONSTRAINT `gim_asistencias_ibfk_2` FOREIGN KEY (`clase_id`) REFERENCES `gim_clases` (`clase_id`)
) ENGINE=InnoDB AUTO_INCREMENT=801 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='asistencias';

CREATE TABLE `gim_clases` (
  `clase_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador de la clase',
  `clase_nombre` varchar(40) NOT NULL COMMENT 'nombre de la clase',
  `sede_id` int NOT NULL COMMENT 'sede donde se da la clase',
  `cupo` int NOT NULL COMMENT 'cupo maximo',
  PRIMARY KEY (`clase_id`),
  KEY `sede_id` (`sede_id`),
  CONSTRAINT `gim_clases_ibfk_1` FOREIGN KEY (`sede_id`) REFERENCES `gim_sedes` (`sede_id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='clases';

CREATE TABLE `gim_miembros` (
  `miem_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del miembro',
  `miem_nombre` varchar(80) NOT NULL COMMENT 'nombre del miembro',
  `sede_id` int NOT NULL COMMENT 'sede donde entrena',
  `plan` varchar(20) NOT NULL COMMENT 'plan contratado',
  `cuota` decimal(8,2) NOT NULL COMMENT 'cuota mensual',
  `fecha_ingreso` date NOT NULL COMMENT 'fecha de ingreso',
  PRIMARY KEY (`miem_id`),
  KEY `sede_id` (`sede_id`),
  CONSTRAINT `gim_miembros_ibfk_1` FOREIGN KEY (`sede_id`) REFERENCES `gim_sedes` (`sede_id`)
) ENGINE=InnoDB AUTO_INCREMENT=151 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='miembros';

CREATE TABLE `gim_sedes` (
  `sede_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador de la sede',
  `sede_nombre` varchar(40) NOT NULL COMMENT 'nombre de la sede',
  `sede_ciudad` varchar(40) NOT NULL COMMENT 'ciudad de la sede',
  PRIMARY KEY (`sede_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='sedes';