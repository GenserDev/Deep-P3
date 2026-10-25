CREATE TABLE `tll_cli` (
  `cli_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del cliente',
  `cli_nom` varchar(80) NOT NULL COMMENT 'nombre del cliente',
  `cli_tel` varchar(15) NOT NULL COMMENT 'telefono',
  PRIMARY KEY (`cli_id`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='clientes del taller';

CREATE TABLE `tll_mec` (
  `mec_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del mecanico',
  `mec_nom` varchar(80) NOT NULL COMMENT 'nombre del mecanico',
  `mec_esp` varchar(20) NOT NULL COMMENT 'especialidad',
  PRIMARY KEY (`mec_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='mecanicos';

CREATE TABLE `tll_rep` (
  `rep_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador de la reparacion',
  `veh_id` int NOT NULL COMMENT 'vehiculo reparado',
  `mec_id` int NOT NULL COMMENT 'mecanico responsable',
  `rep_fec` date NOT NULL COMMENT 'fecha de ingreso al taller',
  `rep_costo` decimal(10,2) NOT NULL COMMENT 'costo de la reparacion',
  `rep_horas` int NOT NULL COMMENT 'horas de trabajo',
  PRIMARY KEY (`rep_id`),
  KEY `veh_id` (`veh_id`),
  KEY `mec_id` (`mec_id`),
  CONSTRAINT `tll_rep_ibfk_1` FOREIGN KEY (`veh_id`) REFERENCES `tll_veh` (`veh_id`),
  CONSTRAINT `tll_rep_ibfk_2` FOREIGN KEY (`mec_id`) REFERENCES `tll_mec` (`mec_id`)
) ENGINE=InnoDB AUTO_INCREMENT=381 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='reparaciones';

CREATE TABLE `tll_veh` (
  `veh_id` int NOT NULL AUTO_INCREMENT COMMENT 'identificador del vehiculo',
  `cli_id` int NOT NULL COMMENT 'duenio del vehiculo',
  `veh_marca` varchar(20) NOT NULL COMMENT 'marca del vehiculo',
  `veh_anio` int NOT NULL COMMENT 'anio del modelo',
  PRIMARY KEY (`veh_id`),
  KEY `cli_id` (`cli_id`),
  CONSTRAINT `tll_veh_ibfk_1` FOREIGN KEY (`cli_id`) REFERENCES `tll_cli` (`cli_id`)
) ENGINE=InnoDB AUTO_INCREMENT=111 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='vehiculos';