CREATE TABLE `lg_bod` (
  `bod_cod` int NOT NULL AUTO_INCREMENT COMMENT 'codigo de la bodega',
  `bod_nom` varchar(40) NOT NULL COMMENT 'nombre de la bodega',
  `bod_ciu` varchar(40) NOT NULL COMMENT 'ciudad de la bodega',
  `bod_cap` int NOT NULL COMMENT 'capacidad en metros cubicos',
  PRIMARY KEY (`bod_cod`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='bodegas de la empresa';

CREATE TABLE `lg_env` (
  `env_cod` int NOT NULL AUTO_INCREMENT COMMENT 'codigo del envio',
  `bod_cod` int NOT NULL COMMENT 'bodega de origen',
  `trans_cod` int NOT NULL COMMENT 'transportista asignado',
  `env_fec` date NOT NULL COMMENT 'fecha de salida del envio',
  `env_peso` decimal(10,2) NOT NULL COMMENT 'peso en kilogramos',
  `env_cost` decimal(10,2) NOT NULL COMMENT 'costo del envio',
  `env_est` varchar(20) NOT NULL COMMENT 'estado del envio',
  PRIMARY KEY (`env_cod`),
  KEY `bod_cod` (`bod_cod`),
  KEY `trans_cod` (`trans_cod`),
  CONSTRAINT `lg_env_ibfk_1` FOREIGN KEY (`bod_cod`) REFERENCES `lg_bod` (`bod_cod`),
  CONSTRAINT `lg_env_ibfk_2` FOREIGN KEY (`trans_cod`) REFERENCES `lg_trans` (`trans_cod`)
) ENGINE=InnoDB AUTO_INCREMENT=451 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='envios realizados';

CREATE TABLE `lg_inc` (
  `inc_cod` int NOT NULL AUTO_INCREMENT COMMENT 'codigo de la incidencia',
  `env_cod` int NOT NULL COMMENT 'envio afectado',
  `inc_tipo` varchar(20) NOT NULL COMMENT 'tipo de incidencia',
  `inc_fec` date NOT NULL COMMENT 'fecha de la incidencia',
  PRIMARY KEY (`inc_cod`),
  KEY `env_cod` (`env_cod`),
  CONSTRAINT `lg_inc_ibfk_1` FOREIGN KEY (`env_cod`) REFERENCES `lg_env` (`env_cod`)
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='incidencias de envios';

CREATE TABLE `lg_trans` (
  `trans_cod` int NOT NULL AUTO_INCREMENT COMMENT 'codigo del transportista',
  `trans_nom` varchar(80) NOT NULL COMMENT 'nombre del transportista',
  `trans_veh` varchar(20) NOT NULL COMMENT 'tipo de vehiculo',
  PRIMARY KEY (`trans_cod`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='transportistas';